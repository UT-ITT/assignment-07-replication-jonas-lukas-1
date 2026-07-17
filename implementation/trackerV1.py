from DIPPID import SensorUDP 
from pynput.mouse import Controller
import time

PORT = 5700

class GyroTrackerV1:
    def __init__(self):
        self.port = PORT
        self.sensor = SensorUDP(PORT)
        self.mouse = Controller()
        
        self.grav_data = None
        self.tracking = False
        
        # Register callbacks for gravity and button
        self.sensor.register_callback("button_1", self.handle_button_1)
        self.sensor.register_callback("gravity", self.handle_gravity)

    def handle_gravity(self, data):
        self.grav_data = data
        
    def handle_button_1(self, data):
        # If button 1 is pressed, start tracking
        if int(data) == 1: 
            self.tracking = not self.tracking
            state = "Started" if self.tracking else "Stopped"
            print(f"Tracking {state}")

    def run(self):
        print(f"Listening on port {PORT}. Press Button 1 on your phone to toggle mouse control.")
        
        # Adjust cursor speed
        sensitivity = -2.0
        deadzone = 1.5

        while True:
            if self.tracking and self.grav_data:
                # Get the gravity data
                x_tilt = self.grav_data.get('x', 0)
                y_tilt = self.grav_data.get('y', 0)

                # Calculate the mouse movement based on gravitiy data
                dx = x_tilt * sensitivity if abs(x_tilt) > deadzone else 0
                dy = y_tilt * sensitivity if abs(y_tilt) > deadzone else 0

                # Move the mouse if there is any movement
                if dx != 0 or dy != 0:
                    self.mouse.move(dx, dy)
            
            time.sleep(0.01)
        
if __name__ == "__main__":
    try:
        tracker = GyroTrackerV1()
        tracker.run()
    except KeyboardInterrupt:
        print("\nStopping tracker...")
        tracker.sensor.disconnect()