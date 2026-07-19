import os
import cv2
import numpy as np
from DIPPID import SensorUDP 
from pynput.mouse import Controller as MouseController
from pynput.mouse import Button
from pynput.keyboard import Controller as KeyboardController, Key, Listener

# Ports and IP addresses for DROIDCAM and DIPPID
DROIDCAM_PORT = 4747
DROIDCAM_IP = "192.168.178.72"
DIPPID_PORT = 5700
DIPPID_IP = "192.168.178.141"

# Performance and configuration parameters
POLLING_RATE = 1          
SCALE_FACTOR = 0.5       
SENSITIVITY = 5        
BLACKOUT_THRESHOLD = 30   
DEADZONE = 0.2

# Interpolation parameters
SMOOTHING_FACTOR = 0.4

class MovingTracker:
    def __init__(self):
        self.droidcam_port = DROIDCAM_PORT
        self.droidcam_ip = DROIDCAM_IP
        self.dippid_port = DIPPID_PORT
        self.dippid_ip = DIPPID_IP
        self.sensor = SensorUDP(DIPPID_PORT, DIPPID_IP)
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        
        # Flag to control the main loop
        self.running = True
        self.tracking = True
        
        # Start the keyboard listener in the background
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()
        
        # Register callbacks for buttons
        self.sensor.register_callback("button_1", self.handle_button_1)
        self.sensor.register_callback("button_2", self.handle_button_2)
        self.sensor.register_callback("button_3", self.handle_button_3)
        self.sensor.register_callback("button_4", self.handle_button_4)
        
        # Coordinates for mouse movement
        self.x = 0
        self.y = 0
        self.smoothed_x = 0
        self.smoothed_y = 0
        self.frame_count = 0
        
        # Initialize video stream
        self.stream_url = f"http://{self.droidcam_ip}:{self.droidcam_port}/video/640x480"
        self.cap = cv2.VideoCapture(self.stream_url)
        
        # Verify DroidCam connection before trying to read frames
        if not self.cap.isOpened():
            print("Error: Could not connect to DroidCam.")
            print("\nPlease ensure the app is open on your phone and the IP/Port are correct.")
            self.running = False
            self.prev_gray = None
            return
        
        # Initialize the first frame
        ret, frame = self.cap.read()
        if not ret or frame is None:
            print("Error: Failed to grab the first frame from DroidCam.") 
            self.running = False
            self.prev_gray = None
            return

        self.prev_gray = self.preprocess_frame(frame)
    
    # Trigger left mouse click when button 1 is pressed
    def handle_button_1(self, data):
        if int(data) == 1:
            self.mouse.click(Button.left, 1)
            
    # Stop tracking when button 2 is pressed
    def handle_button_2(self, data):
        if int(data) == 1:
            if self.tracking:
                print("Stopping tracking...")
                self.tracking = False
            else:
                print("Starting tracking...")
                self.tracking = True

    # Trigger left arrow key press when button 3 is pressed     
    def handle_button_3(self, data):
        if int(data) == 1:
            self.keyboard.press(Key.left)
            
    # Trigger right arrow key press when button 4 is pressed 
    def handle_button_4(self, data):
        if int(data) == 1:
            self.keyboard.press(Key.right)
    
    # Rotate and resize the frame
    def preprocess_frame(self, frame):
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        small_frame = cv2.resize(frame, (0, 0), fx=SCALE_FACTOR, fy=SCALE_FACTOR)
        gray_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
        return gray_frame
    
    # Handle ESC key press to stop the program
    def on_press(self, key):
        if key == Key.esc:
            print("\nESC pressed. Exiting...")
            self.running = False
            return False
    
    # Clean up resources when stopping the program
    def cleanup(self):
        print("Stopping tracker...")
        if hasattr(self, 'listener') and self.listener.running:
            self.listener.stop()
        if hasattr(self, 'sensor'):
            self.sensor.disconnect()
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
    
    def run(self):
        while self.running:
            # Read a frame from the video stream
            ret, frame = self.cap.read()
                
            # Break the loop if the frame is not grabbed successfully
            if not ret or frame is None:
                print("Failed to grab frame. Exiting...")
                return
            
            # Process the frame only if tracking is enabled
            if self.tracking:
                # Preprocess the frame for optical flow calculations
                self.frame_count += 1
                
                # Only process the frame if it meets the polling rate
                if self.frame_count % POLLING_RATE == 0:
                    curr_gray = self.preprocess_frame(frame)
                    
                    # If average brightness is below the blackout threshold, reset previous frame and stop movement
                    if np.mean(curr_gray) < BLACKOUT_THRESHOLD:
                        self.prev_gray = curr_gray
                        self.x, self.y = 0, 0
                    else:
                        flow = cv2.calcOpticalFlowFarneback(
                            self.prev_gray, curr_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
                        
                        # Divide the total optical flow by the polling rate 
                        # to distribute the movement evenly across the skipped frames
                        self.x = np.mean(flow[..., 0]) / POLLING_RATE
                        self.y = np.mean(flow[..., 1]) / POLLING_RATE
                        
                        self.prev_gray = curr_gray
                        
                # Interpolate Movement
                self.smoothed_x = (self.smoothed_x * (1 - SMOOTHING_FACTOR)) + (self.x * SMOOTHING_FACTOR)
                self.smoothed_y = (self.smoothed_y * (1 - SMOOTHING_FACTOR)) + (self.y * SMOOTHING_FACTOR)
                
                # Move the pointer if the smoothed values exceed the deadzone
                if abs(self.smoothed_x) > DEADZONE or abs(self.smoothed_y) > DEADZONE:
                    move_x = -(self.smoothed_x * SENSITIVITY)
                    move_y = -(self.smoothed_y * SENSITIVITY)
                    
                    self.mouse.move(move_x, move_y)
                    
            else:
                # If tracking is False, keep the previous frame updated 
                # to prevent a massive cursor jump when tracking is resumed
                self.prev_gray = self.preprocess_frame(frame)
                
                # Zero out movement variables while paused
                self.x, self.y = 0, 0
                self.smoothed_x, self.smoothed_y = 0, 0
                
                
if __name__ == "__main__":
    try:
        tracker = MovingTracker()
        tracker.run()
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected.")
    finally:
        if 'tracker' in locals():
            tracker.cleanup()
        os._exit(0)