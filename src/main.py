import subprocess
import numpy as np
import matplotlib.pyplot as plt
import time
from spot_rs import scan_to_grid 
from spot_rs import traverse_grid
import argparse
from servo_send import servo_send, beep_send
import multiprocessing
from lidar_wrapper import read_lidar
from adafruit_rplidar import RPLidar 

## LIDAR CONSTANTS
# PORT_NAME = '/dev/ttyUSB0'  # for linux
MINIMUM_SAMPLE_SIZE=80  # decreasing this will increase the reaction speed of the robot but decrease the accuracy of the map

## TRAVERSAL CONSTANTS
MAX_PATH_LOOKAHEAD_FOR_ANGLE = 2 # look max 6 steps ( .5 meters ) ahead to calculate angle
MIN_ALLOWABLE_DIST = .3
DANGER_RADIUS = .6
XY_RESOLUTION = .1
GET_BENCHMARK = False
TURN_DELAY = 1      # delay in seconds between turns to control frequency spot can change directions 
BEEP_DELAY = .5      # delay in seconds between beeps to control frequency spot can beep

## MOVE CONSTANTS
ANGLE_STEP = 10 
MAX_ANGLE = 50
MOVE_STEP = .25

def get_moves(angle_step: int, max_angle: int, move_dist: float, resolution: float) -> list:
    """
    Gets all possible moves for SPOT 

    Args:
        angle_step: Angle step for moves
        max_angle: Max angle for moves
        move_dist: Move distance
        resolution: Resolution of the grid map

    Returns:
        List of all possible moves
    """
    max_dist = round(move_dist / resolution)

    moves = [(0, max_dist)]
    for angle in range(angle_step, max_angle + 1, angle_step):
        x = round(np.sin(np.radians(angle)) * max_dist)
        y = round(np.cos(np.radians(angle)) * max_dist)
        moves += [(x, y), (-x, y)]

    return moves


def calculate_angle(prev_node, curr_node):
    """
    Finds angle for move
    """
    x1, x2 = prev_node[0], curr_node[0]
    y1, y2 = prev_node[1], curr_node[1]

    angle = - ((np.arctan2(y2 - y1, x2 - x1) * 180/np.pi) - 90)

    return angle


def timing_data_write(lidar_scan_time, path_find_time, turn_time, total_time):
    """
    Write timing data to file
    """
    with open("timing_data.csv", "a") as f:
        f.write(f"{lidar_scan_time}, {path_find_time}, {turn_time}, {total_time}\n")


def get_lidar_data(pipe):
    angles = []
    distances = []
    while len(angles) < MINIMUM_SAMPLE_SIZE:
        angle, distance = pipe.recv()
        angles.append(angle)
        distances.append(distance)

    return angles, distances


def main(pipe):
    print(__file__, "start")
    
    moves = get_moves(ANGLE_STEP, MAX_ANGLE, MOVE_STEP, XY_RESOLUTION)
    prev_angle = -10000
    
    last_beep_time = time.time()
    last_turn_time = time.time()
    while True:
        start = time.time()

        ang, dist = get_lidar_data(pipe) 
        lidar_scan_time = time.time() - start 
        
        start_grid = time.time()
        grid = scan_to_grid(ang, dist, XY_RESOLUTION, DANGER_RADIUS) 
        path = traverse_grid(grid.grid_map, grid.scanner_pos, grid.width - 1, moves, MIN_ALLOWABLE_DIST)
        path_find_time = time.time() - start_grid 

        start_turn = time.time()
        if len(path) > MAX_PATH_LOOKAHEAD_FOR_ANGLE: 
            angle = calculate_angle(path[0], path[MAX_PATH_LOOKAHEAD_FOR_ANGLE])
            
            if time.time() - last_turn_time < TURN_DELAY:
                continue

            if prev_angle != angle:
                pass 
            
            prev_angle = angle
            
            servo_send(angle)

            if angle != 0:
                last_turn_time = time.time()
        else:
            print("Cant' find path")
            servo_send(0)
            if time.time() - last_beep_time < BEEP_DELAY:
                continue

            beep_send()
            last_beep_time = time.time()

        end = time.time()

        turn_time = end - start_turn
        total_time = end - start
        if (GET_BENCHMARK): 
            timing_data_write(lidar_scan_time, path_find_time, turn_time, total_time) 
        
        
if __name__ == "__main__":
    # In the main code
    parent_pipe, child_pipe = multiprocessing.Pipe()
    p = multiprocessing.Process(target=read_lidar, args=(child_pipe,))
    p.start()

    # Read from the pipe in the main code
    try: 
        main(parent_pipe)
    except KeyboardInterrupt:
        print("Exiting...")
        p.terminate()
        p.join()
        print("All processes ended")
