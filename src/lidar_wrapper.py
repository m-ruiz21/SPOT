from adafruit_rplidar import RPLidar, RPLidarException
import numpy as np

PORT_NAME = '/dev/ttyUSB0'  # for linux
# PORT_NAME = '/dev/cu.usbserial-0001' # for mac
BAUDRATE = 115200
TIMEOUT = 2

def read_lidar(pipe):
    lidar = RPLidar(None, PORT_NAME, baudrate=BAUDRATE, timeout=TIMEOUT)
    while True:
        try:
            angles = []
            distances = []
            for scan in lidar.iter_scans():
                print("got reading")
                for (_, angle, distance) in scan:
                    if angle < 180:
                        continue
                    
                    angle = 180 - (angle - 180)
                    pipe.send((np.radians(angle), distance / 1000))                    

        except RPLidarException as e:
            print(f'RPLidar Exception: {e}')
            print("Restarting Lidar...")
            lidar.stop()
            lidar.disconnect()
            lidar = RPLidar(None, PORT_NAME, baudrate=BAUDRATE, timeout=TIMEOUT)
        
        except KeyboardInterrupt:
            lidar.stop()
            lidar.stop_motor()
            lidar.disconnect()
            break
