## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

# run inside /home/pi/Desktop/pi_rplidar/CircuitPython 9.x/venv
# do ./bin/python3 ./test-depth-camera.py


#####################################################
## librealsense tutorial #1 - Accessing depth data ##
#####################################################

# First import the library
import pyrealsense2 as rs

DEPTH_WIDTH = 640
DEPTH_HEIGHT = 480

OVERLAP = 1.0/12

def getSectors(x):
	sectors = []

	if 0 < x and x < DEPTH * (1/3 + OVERLAP):
		sectors += [0]

	if DEPTH * (1/3 - OVERLAP) < x and x < DEPTH * (2/3 + OVERLAP):
		sectors += [1]

	if DEPTH * (2/3 - OVERLAP) < x and x < DEPTH * (1 + OVERLAP):
		sectors += [2]

	return sectors

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


        for x in range(DEPTH_WIDTH):
            sector = getSector(x)
            for y in range(DEPTH_HEIGHT):
                dist = depth.get_distance(x, y) # meters
    exit(0)
#except rs.error as e:
#    # Method calls agaisnt librealsense objects may throw exceptions of type pylibrs.error
#    print("pylibrs.error was thrown when calling %s(%s):\n", % (e.get_failed_function(), e.get_failed_args()))
#    print("    %s\n", e.what())
#    exit(1)
except Exception as e:
    print(e)
    pass
