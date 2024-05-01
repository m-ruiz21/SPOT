from adafruit_rplidar import RPLidar, RPLidarException
import numpy as np

# PORT_NAME = '/dev/ttyUSB0'  # for linux
PORT_NAME = '/dev/cu.usbserial-0001' # for mac
MINIMUM_SAMPLE_SIZE=80  # decreasing this will increase the reaction speed of the robot but decrease the accuracy of the map
BAUDRATE = 115200
TIMEOUT = 2

def read_lidar(pipe):
    lidar = RPLidar(None, PORT_NAME, baudrate=BAUDRATE, timeout=TIMEOUT)
    while True:
        try:
            angles = []
            distances = []
            for scan in lidar.iter_scans(MINIMUM_SAMPLE_SIZE*2, MINIMUM_SAMPLE_SIZE):
                print("got reading")
                for (_, angle, distance) in scan:
                    if angle < 180:
                        continue
                    
                    angle = 180 - (angle - 180)
                    
                    angles += [np.radians(angle)]
                    distances += [distance / 1000]

                if len(angles) >= MINIMUM_SAMPLE_SIZE:
                    lidar.stop()
                    pipe.send((angles, np.array(distances)))
                    return

        except RPLidarException as e:
            print(f'RPLidar Exception: {e}')
            print("Restarting Lidar...")
            lidar.stop()
            lidar.stop_motor()
            lidar.disconnect()
            lidar = RPLidar(None, PORT_NAME, baudrate=BAUDRATE, timeout=TIMEOUT)
        
        except KeyboardInterrupt:
            lidar.stop()
            lidar.stop_motor()
            lidar.disconnect()
            break
