from DIPPID import SensorUDP 
from pynput.mouse import Controller
import time

PORT = 5700
x = 0
y = 0

class GyroTrackerV3:
    def __init__(self):
        self.port = PORT
        self.sensor = SensorUDP(PORT)
        self.mouse = Controller()
        self.tracking = True
        
        # Register callbacks for gyro instead of gravity
        self.sensor.register_callback("button_1", self.handle_button_1)
        self.sensor.register_callback("button_2", self.handle_button_2)
        self.sensor.register_callback("button_3", self.handle_button_3)
        self.sensor.register_callback("button_4", self.handle_button_4)

    def handle_gyroscope(self, data):
        self.gyro_data = data
        
    def handle_button_1(self, data):
        global x
        # If button 1 is pressed, start tracking
        if int(data) == 1:
            x = 1
            print("Tracking Started")
        # If button 1 is released, stop tracking
        else:
            x = 0
            print("Tracking Stopped")

    def handle_button_2(self, data):
        global x
        if int(data) == 1:
            x = -1
            print("Button 2 Pressed")
        else:
            x = 0
            print("Button 2 Released")

    def handle_button_3(self, data):
        global y
        if int(data) == 1:
            y = 1
            print("Button 3 Pressed")
        else:
            y = 0
            print("Button 3 Released")

    def handle_button_4(self, data):
        global y
        if int(data) == 1:
            y = -1
            print("Button 4 Pressed")
        else:
            y = 0
            print("Button 4 Released")

    def run(self):
        print(f"Listening on port {PORT}. Hold Button 1 to control the mouse. Release to stop.")
        
        # Adjust the cursor speed
        sensitivity = -18
        

        while True:
            if self.tracking:

                dx = x * sensitivity
                dy = y * sensitivity
                # Move the mouse if there is any movement
                if dx != 0 or dy != 0:
                    self.mouse.move(dx, dy)
            
            # Smooth 100hz polling
            time.sleep(0.01)
        
if __name__ == "__main__":
    try:
        tracker = GyroTrackerV3()
        tracker.run()
    except KeyboardInterrupt:
        print("\nStopping tracker...")
        tracker.sensor.disconnect()