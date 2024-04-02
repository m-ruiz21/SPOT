import pyrealsense2 as rs
import numpy as np

# create intel realsense pipeline and config and start streaming and get the depth sensor's depth scale
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
pipeline.start(config)
depth_sensor = pipeline.get_active_profile().get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

# Create pointcloud object
pc = rs.pointcloud()

# Wait for a coherent pair of frames 
frames = pipeline.wait_for_frames()
depth_frame = frames.get_depth_frame()
if not depth_frame:
    print("No frames")
    exit()

# Generate the pointcloud and texture mappings
points = pc.calculate(depth_frame)
pointcloud = np.asanyarray(points.get_vertices())
pointcloud = pointcloud.view(np.float32).reshape(-1, 3)

# Get the depth image
depth_image = np.asanyarray(depth_frame.get_data())

import matplotlib.pyplot as plt
# plot depth image
plt.imshow(depth_image)
plt.show()

pipeline.stop()
