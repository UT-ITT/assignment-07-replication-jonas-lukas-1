import argparse
import os
import matplotlib.pyplot as plt
from DIPPID import SensorUDP
import time

PORT = 5700

# Exploration class for collecting and plotting sensor data
# to get better understanding of the sensor's capabilities and behavior
# for actual implementation.
class Exploration:
    def __init__(self):
        # Initialize the sensor
        self.port = PORT
        self.sensor = SensorUDP(PORT)
        
        # Set up data storage
        self.gyro_data = []
        self.accel_data = []
        self.grav_data = []
        self.tracking = False
        
        # Set default location and file name for saving data
        self.location = "data"
        self.file_name = "sensor_data"

        # Register callbacks for buttons
        self.sensor.register_callback("button_1", self.handle_button_1)
        self.sensor.register_callback("button_2", self.handle_button_2)
    
    # Set the location for saving data  
    def set_location(self, location):
        self.location = location
        
    # Set the base file name for saving data
    def set_file_name(self, file_name):
        self.file_name = file_name

    # Handle accelerometer data
    def handle_accelerometer(self, data):
        self.accel_data.append(data)

    # Handle gyroscope data
    def handle_gyroscope(self, data):
        self.gyro_data.append(data)
  
    # Handle gravity data
    def handle_gravity(self, data):
        self.grav_data.append(data)

    # Toggles tracking if clicked once, stops if clicked again
    def handle_button_1(self, data):
        if int(data) == 1:
            if not self.tracking:
                print("Starting tracking...")
                self.start_tracking()
            else:
                print("Stopping tracking...")
                self.stop_tracking()
                
    # Tracks while button 2 is held down, stop when released
    def handle_button_2(self, data):
        if not self.tracking:
            print("Starting tracking...")
            self.start_tracking()
        else:
            print("Stopping tracking...")
            self.stop_tracking()

    # Start tracking by registering callbacks for accelerometer, gyroscope, and gravity data
    # Set tracking to True
    def start_tracking(self):
        self.sensor.register_callback("accelerometer", self.handle_accelerometer)
        self.sensor.register_callback("gyroscope", self.handle_gyroscope)
        self.sensor.register_callback("gravity", self.handle_gravity)
        self.tracking = True
   
    # Stop tracking by unregistering callbacks for accelerometer, gyroscope, and gravity data
    # Set tracking to False
    def stop_tracking(self):
        self.sensor.unregister_callback("accelerometer", self.handle_accelerometer)
        self.sensor.unregister_callback("gyroscope", self.handle_gyroscope)
        self.sensor.unregister_callback("gravity", self.handle_gravity)
        self.tracking = False
        
        # Plot, save and clear collected data
        plots = self.plot_data()
        self.save_plots(plots)
        self.clear_data()
    
    # Generate plots for accelerometer, gyroscope, and gravity data if available
    def plot_data(self):
        datasets = [
            (self.accel_data, "accelerometer"),
            (self.gyro_data, "gyro"),
            (self.grav_data, "gravity"),
        ]

        plots = []

        for data, sensor_name in datasets:
            if not data:
                continue

            fig = plt.figure(figsize=(8, 4))
            for axis in ("x", "y", "z"):
                values = [sample.get(axis, 0) for sample in data]
                plt.plot(values, label=axis)

            plt.title(sensor_name)
            plt.xlabel("Sample")
            plt.ylabel("Value")
            plt.legend()
            plt.tight_layout()
            plots.append((fig, sensor_name))

        return plots
    
    # Save the generated plots to the specified location with the specified file name
    def save_plots(self, plots):
        for fig, sensor_name in plots:
            file_path = os.path.join(self.location, f"{self.file_name}_{sensor_name}.png")
            fig.savefig(file_path)
            plt.close(fig)

    # Clear all collected data
    def clear_data(self):
        self.gyro_data.clear()
        self.accel_data.clear()
        self.grav_data.clear()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exploration Mode for DIPPID Sensor Data")
    parser.add_argument("--location", type=str, default="data", help="Directory to save the data")
    parser.add_argument("--file_name", type=str, default="sensor_data", help="Base name for the saved data files")
    args = parser.parse_args()
    
    # Ensure the directory exists
    if not os.path.exists(args.location):
        os.makedirs(args.location)
    
    # Convert the location to an absolute path
    args.location = os.path.abspath(args.location)

    exploration = Exploration()
    exploration.set_location(args.location)
    exploration.set_file_name(args.file_name)

    try:
        print("Listening for sensor data. Press Strg+C to exit.")
        # Keep the main thread alive to catch the interrupt cleanly
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping tracker...")
        # Optional: you could call a cleanup method here if needed
        os._exit(0)