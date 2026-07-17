from DIPPID import SensorUDP 
from pynput.mouse import Controller as MouseController
from pynput.mouse import Button
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key
import time

PORT = 5700

class GyroTrackerV2:
    def __init__(self):
        self.port = PORT
        self.sensor = SensorUDP(PORT)
        self.mouse = MouseController()
        self.keyboard = KeyboardController()

        self.gyro_data = None
        self.tracking = False
        
        # Register callbacks for gyro and button
        self.sensor.register_callback("button_1", self.handle_button_1)
        self.sensor.register_callback("button_2", self.handle_button_2)
        self.sensor.register_callback("button_3", self.handle_button_3)
        self.sensor.register_callback("button_4", self.handle_button_4)
        self.sensor.register_callback("gyroscope", self.handle_gyroscope)

    def handle_gyroscope(self, data):
        self.gyro_data = data
        
    def handle_button_1(self, data):
        # If button 1 is pressed, start tracking
        if int(data) == 1: 
            self.tracking = True
            print("Tracking Started")
        # If button 1 is released, stop tracking
        else:
            self.tracking = False
            print("Tracking Stopped")
            
    # Tracks while button 2 is held down, stop when released
    def handle_button_2(self, data):
        if int(data) == 1:
            if not self.tracking:
                print("Starting tracking...")
                self.tracking = True
            else:
                print("Stopping tracking...")
                self.tracking = False

    # Trigger left arrow key press when button 3 is pressed     
    def handle_button_3(self, data):
        if int(data) == 1:
            self.keyboard.press(Key.left)
            
    # Trigger left mouse click, when button 4 is pressed 
    def handle_button_4(self, data):
        if int(data) == 1:
            self.keyboard.press(Key.right)
            
    def run(self):
        print(f"Listening on port {PORT}. Hold Button 1 to control the mouse. Release to stop.")
        
        # Adjust the cursor speed
        sensitivity = -18
        
        # Filters out minor gyroscope noise
        gyro_noise = 0.1

        while True:
            if self.tracking and self.gyro_data:

                # Get the gyroscope data
                gyro_x = self.gyro_data.get('x', 0)
                gyro_z = self.gyro_data.get('z', 0)

                # If the gyroscope values are below the noise threshold, set them to zero
                if abs(gyro_x) < gyro_noise: gyro_x = 0
                if abs(gyro_z) < gyro_noise: gyro_z = 0

                # Calculate the mouse movement based on gyroscope data
                dx = gyro_z * sensitivity
                dy = gyro_x * sensitivity

                # Move the mouse if there is any movement
                if dx != 0 or dy != 0:
                    self.mouse.move(dx, dy)
            
            # Smooth 100hz polling
            time.sleep(0.01)
        
if __name__ == "__main__":
    try:
        tracker = GyroTrackerV2()
        tracker.run()
    except KeyboardInterrupt:
        print("\nStopping tracker...")
        tracker.sensor.disconnect()