from adafruit_rplidar import RPLidar, RPLidarException
import numpy as np
import os

## LIDAR CONSTANTS
PORT_NAME = '/dev/ttyUSB0'  # for linux
MINIMUM_SAMPLE_SIZE=80  # decreasing this will increase the reaction speed of the robot but decrease the accuracy of the map

def send_data(angles, distances):
    """
    Send LiDAR data to FIFO pipe
    """ 

    try:
        with open('/tmp/lidar_pipe', 'w') as f:
            for angle, distance in zip(angles, distances):
                f.write(f'{angle} {distance}\n')
    except Exception as e:
        print(f"Error: {e}")


def main():
    """
    Read LIDAR data 
    """
    if not os.path.exists('/tmp/lidar_pipe'):
        os.mkfifo('/tmp/lidar_pipe')

    lidar = RPLidar(None, PORT_NAME, timeout=3, baudrate=115200)

    while True:
        try:
            angles = []
            distances = []
            for scan in lidar.iter_scans(MINIMUM_SAMPLE_SIZE*2, MINIMUM_SAMPLE_SIZE):
                for (_, angle, distance) in scan:
                    if angle < 180:
                        continue
                    
                    angle = 180 - (angle - 180)
                    
                    angles += [np.radians(angle)]
                    distances += [distance / 1000]

                if len(angles) >= MINIMUM_SAMPLE_SIZE:
                    return angles, np.array(distances)

        except RPLidarException as e:
            print(f'RPLidar Exception: {e}')
            print("Restarting Lidar...")
            lidar.stop()
            lidar.disconnect()
            lidar = RPLidar(None, PORT_NAME, timeout=3)