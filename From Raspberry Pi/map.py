import numpy as np
from decimal import Decimal
import pyrealsense2 as rs 

def generate_room_map(camera_array: list) -> list:
    """
    Transposes depth camera output to create binary 2D map of room 

    Args:
        camera_array: 640x480 list of depth camera outputs
    """

    GRID_DEPTH = Decimal('2.0998')
    MAX_DISTANCE = 10000000  

    room_map = np.zeros((381, 640))

    for camera_row in camera_array:
        for camera_col in range(len(camera_row)):
            if camera_row[camera_col] < MAX_DISTANCE:
                room_row = camera_row // GRID_DEPTH
                room_map[room_row][camera_col] = 1
    

    return room_map


