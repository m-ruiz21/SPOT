angles = [
    0, 
    10,
    -10,
    20,
    -20,
    30,
    -30,
    40,
    -40,
    50,
    -50,
    60,
    -60
]

import numpy as np

# calculate the x and y grid values for each angle and distance
for angle in angles:
    x = np.sin(np.radians(angle))
    y = np.cos(np.radians(angle))
    print(f"angle: {angle}, x: {x}, y: {y}")