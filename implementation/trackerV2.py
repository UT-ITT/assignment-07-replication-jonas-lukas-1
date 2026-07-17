from DIPPID import SensorUDP 
from pynput.mouse import Controller
import time

PORT = 5700

class GyroTrackerV2:
    def __init__(self):
        self.port = PORT
        self.sensor = SensorUDP(PORT)
        self.mouse = Controller()
        
        self.gyro_data = None
        self.tracking = False
        
        # Register callbacks for gyro and button
        self.sensor.register_callback("button_1", self.handle_button_1)
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