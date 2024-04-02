import numpy as np
from decimal import Decimal
import pyrealsense2 as rs 

def generate_room_map(frame)-> list[list[int]]:
    """
    Transposes depth camera output to create binary 2D map of room 

    Args:
        camera_array: 640x480 list of depth camera outputs
    """

    GRID_DEPTH = 20.998     # array value represents object in 20.998mm x 20.977mm square
    MAX_DISTANCE = 8000  

    room_map = np.zeros((381, 640))

    for y in range(480):
        for x in range(640):
            dist = frame.get_distance(x,y) 
            if dist < MAX_DISTANCE:
                room_row = int(dist / GRID_DEPTH)
                room_map[380 - room_row][x] = 1 if room_row != 0 else -1

    return room_map


def print_room_map(room_map):
    print(50*"-")
    for y, row in enumerate(room_map, start=150):
        if y % 3 != 0:
            continue
        for x, val in enumerate(row):
            if x % 3 != 0:
                continue
            
            if val == 0:
                print(" ", end="")
            elif val == 1:
                print("#", end="")        
            else:
                print("X", end="") 
    
    print(50*"-")


pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

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

        room_map = generate_room_map(depth.as_depth_frame())
        print_room_map(room_map)

    exit(0)

except Exception as e:
    print(e)
    pass
