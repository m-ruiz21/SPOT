from adafruit_rplidar import RPLidar
from adafruit_rplidar import RPLidarException
import numpy as np
from spot_rs import scan_to_grid
import matplotlib.pyplot as plt

# Setup the RPLidar
# PORT_NAME = '/dev/ttyUSB0' # for linux

GRID_RES = 100  # grid represend .1 mm (LIDAR unit) in the real world  
PORT_NAME = '/dev/cu.usbserial-0001' # for mac
lidar = RPLidar(None, PORT_NAME, timeout=3)

def stop_lidar():
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    print("Lidar stopped")


def scan_to_csv(angles, distances):
    with open("lidar.csv", "w") as f:
        for i in range(len(angles)):
            f.write(f"{angles[i]},{distances[i]}\n")


def process_data(angles, distances): 
    scan_to_csv(angles, distances)
    # can change this to our main flow later


angles = []
distances = []

try:
    while True:
        for scan in lidar.iter_scans():
            for (_, angle, distance) in scan:
                if angle > 180:
                    continue

                angle = np.radians(angle)
                angles.append(angle)
                distances.append(distance)
            
            if len(angles) > 180:
                break

        process_data(angles, distances)
        
        angles.clear()
        distances.clear()

except KeyboardInterrupt:
    print("Recieved Keyboard Interrupt")
    stop_lidar()
    exit()
except RPLidarException as e:
    print(f'RPLidar Exception: {e}')


stop_lidar()