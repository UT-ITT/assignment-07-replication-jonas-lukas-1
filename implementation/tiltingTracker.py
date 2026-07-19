import time

from DIPPID import SensorUDP 
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController, Key, Listener

PORT = 5700

class TiltingTracker:
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

        # Set up data storage
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

        while self.running:
            if self.tracking and self.grav_data:
                # Get the gravity data
                x_tilt = self.grav_data.get('x', 0)
                y_tilt = self.grav_data.get('y', 0)

                # Calculate the mouse movement based on gravitiy data
                dx = (x_tilt - (deadzone if x_tilt > 0 else -deadzone)) * sensitivity if abs(x_tilt) > deadzone else 0
                dy = (y_tilt - (deadzone if y_tilt > 0 else -deadzone)) * sensitivity if abs(y_tilt) > deadzone else 0

                # Move the mouse if there is any movement
                if dx != 0 or dy != 0:
                    self.mouse.move(dx, dy)
            
            # Smooth 100hz polling
            time.sleep(0.01)
            
        self.cleanup()
            
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
        
if __name__ == "__main__":
    try:
        tracker = TiltingTracker()
        tracker.run()
    except KeyboardInterrupt:
        tracker.cleanup()