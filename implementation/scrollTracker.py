import time

from DIPPID import SensorUDP 
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController, Key, Listener

PORT = 5700
SENSITIVITY = 5
x = 0
y = 0

class ScrollTracker:
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
        
        # Register callbacks for gyro instead of gravity
        self.sensor.register_callback("button_1", self.handle_button_1)
        self.sensor.register_callback("button_2", self.handle_button_2)
        self.sensor.register_callback("button_3", self.handle_button_3)
        self.sensor.register_callback("button_4", self.handle_button_4)

    def handle_gyroscope(self, data):
        self.gyro_data = data
    
    # Move the mouse left when button 1 is pressed, stop when released
    def handle_button_1(self, data):
        global x
        if int(data) == 1:
            x = -1
        else:
            x = 0

    # Move the mouse up when button 2 is pressed, stop when released
    def handle_button_2(self, data):
        global y
        if int(data) == 1:
            y = -1
        else:
            y = 0

    # Move the mouse down when button 3 is pressed, stop when released
    def handle_button_3(self, data):
        global y
        if int(data) == 1:
            y = 1
        else:
            y = 0
            
    # Move the mouse right when button 4 is pressed, stop when released
    def handle_button_4(self, data):
        global x
        if int(data) == 1:
            x = 1
        else:
            x = 0
            
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
        
    # Main loop to run the tracker
    def run(self):
        print(f"Listening on port {PORT}. Press Button 1-4 on your phone to control the mouse. \nPress ESC to exit the program.")
          
        while self.running:
            dx = x * SENSITIVITY
            dy = y * SENSITIVITY
            
            # Move the mouse if there is any movement
            if dx != 0 or dy != 0:
                self.mouse.move(dx, dy)
            
            # Smooth 100hz polling
            time.sleep(0.01)
            
        self.cleanup()
        
if __name__ == "__main__":
    try:
        tracker = ScrollTracker()
        tracker.run()
    except KeyboardInterrupt:
        tracker.cleanup()