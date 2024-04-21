import os
from math import cos, sin, pi, floor
from adafruit_rplidar import RPLidar

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME)


for scan in lidar.iter_scans():
    for (_, angle, distance) in scan:
        print(angle, distance)
# def process_data(data):
#     global max_distance
#     for angle in range(360):
#         distance = data[angle]
#         max_distance = max([min([5000, distance]), max_distance])
#         radians = angle * pi / 180.0
#         x = distance * cos(radians)
#         y = distance * sin(radians)
            
# scan_data = [0] * 360

# try:
#     print(lidar.info)
#     for scan in lidar.iter_scans():
#         for (_, angle, distance) in scan:
#             scan_data[min([359, floor(angle)])] = distance
#         process_data(scan_data)
# except KeyboardInterrupt:
#     print('Stopping.')
    
# lidar.stop()
# lidar.disconnect()