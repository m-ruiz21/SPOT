import numpy as np
import matplotlib.pyplot as plt
import time
from spot_rs import scan_to_grid 
from spot_rs import traverse_grid
import argparse
from servo_send import servo_send, beep_send
from adafruit_rplidar import RPLidar, RPLidarException

## LIDAR CONSTANTS
PORT_NAME = '/dev/ttyUSB0'  # for linux
MINIMUM_SAMPLE_SIZE=80  # decreasing this will increase the reaction speed of the robot but decrease the accuracy of the map
BAUDRATE = 115200
TIMEOUT = 2

## TRAVERSAL CONSTANTS
MAX_PATH_LOOKAHEAD_FOR_ANGLE = 6 # look max 6 steps ( 1.75 meters ) ahead to calculate angle
MIN_ALLOWABLE_DIST = .3
DANGER_RADIUS = .6
XY_RESOLUTION = .1

## MOVE CONSTANTS
ANGLE_STEP = 10 
MAX_ANGLE = 50
MOVE_STEP = .25

lidar = RPLidar(None, PORT_NAME, baudrate=BAUDRATE, timeout=TIMEOUT)

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


def plot_map_path(grid_map, path):
    """
    Plot the grid map and the path
    """
    plt.imshow(grid_map, cmap="hot_r", origin="lower")
    plt.colorbar()
    for node in path:
        plt.plot(node[0], node[1], 'ro')
    plt.show()


def calculate_angle(prev_node, curr_node):
    """
    Finds angle for move
    """
    x1, x2 = prev_node[0], curr_node[0]
    y1, y2 = prev_node[1], curr_node[1]

    angle = - ((np.arctan2(y2 - y1, x2 - x1) * 180/np.pi) - 90)

    return angle


def lidar_read():
    """
    Read LIDAR data 

    Returns:
        Tuple containing array of angles and distances 
    """
    global lidar

    while True:
        try:
            angles = []
            distances = []
            for scan in lidar.iter_scans(MINIMUM_SAMPLE_SIZE*2, MINIMUM_SAMPLE_SIZE):
                print("got reading")
                for (_, angle, distance) in scan:
                    if angle < 180:
                        continue
                    
                    angle = 180 - (angle - 180)
                    
                    angles += [np.radians(angle)]
                    distances += [distance / 1000]

                if len(angles) >= MINIMUM_SAMPLE_SIZE:
                    lidar.stop()
                    return angles, np.array(distances)

        except RPLidarException as e:
            print(f'RPLidar Exception: {e}')
            print("Restarting Lidar...")
            lidar.stop()
            lidar.stop_motor()
            lidar.disconnect()
            lidar = RPLidar(None, PORT_NAME, baudrate=BAUDRATE, timeout=TIMEOUT)


def timing_data_write(lidar_scan_time, path_find_time, turn_time, total_time):
    """
    Write timing data to file
    """
    with open("timing_data.csv", "a") as f:
        f.write(f"{lidar_scan_time}, {path_find_time}, {turn_time}, {total_time}\n")


def main(angle_step, max_angle, move_step, xy_resolution):
    print(__file__, "start")
    
    moves = get_moves(angle_step, max_angle, move_step, xy_resolution)
    prev_angle = -10000
    while True:
        start = time.time()

        ang, dist = lidar_read() 
        lidar_scan_time = time.time() - start 
        
        start_grid = time.time()
        grid = scan_to_grid(ang, dist, xy_resolution, DANGER_RADIUS) 
        path = traverse_grid(grid.grid_map, grid.scanner_pos, grid.width - 1, moves, MIN_ALLOWABLE_DIST)
        path_find_time = time.time() - start_grid 

        start_turn = time.time()
        if len(path) > MAX_PATH_LOOKAHEAD_FOR_ANGLE: 
            angle = calculate_angle(path[0], path[MAX_PATH_LOOKAHEAD_FOR_ANGLE])
            
            if prev_angle != angle:
                pass 
            
            prev_angle = angle
            
            servo_send(angle)
        else:
            print("Cant' find path")
            beep_send()
            servo_send(0)

        end = time.time()

        turn_time = end - start_turn
        total_time = end - start

        timing_data_write(lidar_scan_time, path_find_time, turn_time, total_time)

        
        
if __name__ == "__main__":
    main(ANGLE_STEP, MAX_ANGLE, MOVE_STEP, XY_RESOLUTION)
