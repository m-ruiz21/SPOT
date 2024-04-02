import numpy as np
import cv2
import pyrealsense2 as rs
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Initialize RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# Start streaming
pipeline.start(config)

fig, ax = plt.subplots()

def update(i):
    # Wait for a new depth frame
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()

    if not depth_frame:
        return

    # Convert depth frame to numpy array
    depth_image = np.asanyarray(depth_frame.get_data())

    # scale depth image to cm instead of mm
    depth_scaled = depth_image * 0.1
    # find the maximum depth value
    max_depth = np.max(depth_scaled)

    depth_map = np.zeros((640, 640), np.uint8)

    # find width and height of the image
    for y in range(220, 300):
        for x in range(640):
            depth_index = int(depth_scaled[y, x]) - 1 
            if depth_index < 200:
                depth_map[depth_index, x] = 1


    ax.clear()
    ax.imshow(depth_map, cmap='gray_r', origin='lower')

ani = FuncAnimation(fig, update, interval=100)

try:
    plt.show()
finally:
    pipeline.stop()
    cv2.destroyAllWindows()
