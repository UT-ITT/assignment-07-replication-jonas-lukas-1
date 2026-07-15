from DIPPID import SensorUDP 
from pynput.mouse import Controller
import time

PORT = 5700

class GyroTrackerV2:
    def __init__(self):
        self.port = PORT
        self.sensor = SensorUDP(PORT)
        self.mouse = Controller()
        
        self.grav_data = None
        self.tracking = False
        
        # Register callbacks
        self.sensor.register_callback("button_1", self.handle_button_1)
        self.sensor.register_callback("gravity", self.handle_gravity)

    def handle_gravity(self, data):
        self.grav_data = data
        
    def handle_button_1(self, data):
        # Toggle tracking on and off with the button
        if int(data) == 1: 
            self.tracking = not self.tracking
            state = "Started" if self.tracking else "Stopped"
            print(f"Tracking {state}")

    def run(self):
        print(f"Listening on port {PORT}. Press Button 1 on your phone to toggle mouse control.")
        
        # Configuration variables
        speed_multiplier = -2.0  # Increase to make the mouse move faster (negative might be needed to invert axis)
        deadzone = 1.5           # Gravity values below this are ignored to stop jitter

        while True:
            if self.tracking and self.grav_data:
                # Safely extract X and Y tilt
                # Note: You may need to swap 'x' and 'y' depending on if you hold the phone portrait or landscape
                x_tilt = self.grav_data.get('x', 0)
                y_tilt = self.grav_data.get('y', 0)

                # Apply deadzone and calculate movement (dx, dy)
                dx = x_tilt * speed_multiplier if abs(x_tilt) > deadzone else 0
                dy = y_tilt * speed_multiplier if abs(y_tilt) > deadzone else 0

                # Move the mouse relatively
                if dx != 0 or dy != 0:
                    self.mouse.move(dx, dy)
            
            # A short sleep prevents the loop from eating 100% of your CPU
            # 0.01 seconds gives a smooth 100Hz update rate
            time.sleep(0.01)
        
if __name__ == "__main__":
    try:
        tracker = GyroTracker()
        tracker.run()
    except KeyboardInterrupt:
        print("\nStopping tracker...")
        tracker.sensor.disconnect()