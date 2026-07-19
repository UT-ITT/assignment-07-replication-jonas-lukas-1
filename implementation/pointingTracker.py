from DIPPID import SensorUDP 
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key, Listener

import time

PORT = 5700

class PointingTracker:
    def __init__(self):
        self.port = PORT
        self.sensor = SensorUDP(PORT)
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        
        # Flag to control the main loop
        self.running = True
        
        # Start the keyboard listener in the background
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

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
            
    # Trigger right arrow key press when button 4 is pressed 
    def handle_button_4(self, data):
        if int(data) == 1:
            self.mouse.click(Button.left, 1)
            
    # Handle ESC key press to stop the program
    def on_press(self, key):
        if key == Key.esc:
            print("\nESC pressed. Exiting...")
            self.running = False
            return False
    
    # Clean up resources when stopping the program
    def cleanup(self):
        print("Stopping tracker...")
        if self.listener.running:
            self.listener.stop()
        self.sensor.disconnect()
            
    def run(self):
        print(f"Listening on port {PORT}. Hold Button 1 to control the mouse. Release to stop.")
        
        # Adjust the cursor speed
        sensitivity = -18
        
        # Filters out minor gyroscope noise
        gyro_noise = 0.1

        while self.running:
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
        
        self.cleanup()
        
if __name__ == "__main__":
    try:
        tracker = PointingTracker()
        tracker.run()
    except KeyboardInterrupt:
        tracker.cleanup()