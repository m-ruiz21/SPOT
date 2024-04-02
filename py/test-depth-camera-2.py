# First import the library
import pyrealsense2 as rs

try:
    # Create a context object. This object owns the handles to all connected realsense devices
    pipeline = rs.pipeline()

    # Configure streams
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    # Start streaming
    pipeline.start(config)

    while True:
        # This call waits until a new coherent set of frames is available on a device
        # Calls to get_frame_data(...) and get_frame_timestamp(...) on a device will return stable values until wait_for_frames(...) is called
        frames = pipeline.wait_for_frames()
        depth = frames.get_depth_frame()
        if not depth: continue

        # Define depth thresholds for object detection (in meters)
        min_distance = 2  # Minimum distance to consider as an object
        max_distance = 10000000  # Maximum distance to consider as an object

        # Detect objects based on depth thresholds
        for y in range(480):
            for x in range(640):
                dist = depth.get_distance(x, y)
                if min_distance < dist < max_distance:
                    # Object detected at this pixel
                    # You can perform further processing or marking here
                    # print(f"Object detected at pixel ({x}, {y})")
                    print("distance:", dist)
                    

    exit(0)
except Exception as e:
    print(e)
    pass
