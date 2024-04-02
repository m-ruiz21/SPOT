# create python script to use rplidar to find objects

import sys
import time
import math
import numpy as np
import matplotlib.pyplot as plt
from rplidar import RPLidar

lidar = RPLidar('/COM6')

print("kaka")
info = lidar.get_info()
print(info)
print("poo poo kaka")

health = lidar.get_health()
print(health)

for i, scan in enumerate(lidar.iter_scans()):
    print('%d: Got %d measurments' % (i, len(scan)))
    if i > 10:
        break

lidar.stop()
lidar.stop_motor()
lidar.disconnect()
