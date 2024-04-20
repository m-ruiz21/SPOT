import numpy as np
import matplotlib.pyplot as plt
import time
from spot_rs import scan_to_grid 
from spot_rs import traverse_grid
import argparse
import heapq

def get_moves(angle_step, max_angle, move_dist, resolution):
    max_dist = round(move_dist / resolution)

    moves = [(0, max_dist)]
    for angle in range(angle_step, max_angle + 1, angle_step):
        x = round(np.sin(np.radians(angle)) * max_dist)
        y = round(np.cos(np.radians(angle)) * max_dist)
        moves += [(x, y), (-x, y)]

    return moves


def file_read(f):
    """
    Reading LIDAR laser beams (angles and corresponding distance data)
    """
    with open(f) as data:
        measures = [line.split(",") for line in data]
    angles = []
    distances = []
    for measure in measures:
        angles.append(float(measure[0]))
        distances.append(float(measure[1]))
    angles = np.array(angles)
    distances = np.array(distances)
    return angles, distances


def plot_map_path(grid_map, path):
    """
    Plotting the grid map and the path
    """
    plt.imshow(grid_map, cmap="hot_r", origin="lower")
    plt.colorbar()
    for node in path:
        plt.plot(node[0], node[1], 'ro')
    plt.show()


def move_angle(curr_node, prev_node):
    x1, x2 = prev_node[0], curr_node[0]
    y1, y2 = prev_node[1], curr_node[1]
    angle = - ((np.arctan2(y2 - y1, x2 - x1) * 180/np.pi) - 90)
    return angle

def move_dist(curr_node, prev_node):
    x1, x2 = prev_node[0], curr_node[0]
    y1, y2 = prev_node[1], curr_node[1]
    dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist

PORT_NAME = '/dev/ttyUSB0' # for linux
MINIMUM_SAMPLE_SIZE = 180 # 180 readings
from adafruit_rplidar import RPLidar, RPLidarException
lidar = RPLidar(None, PORT_NAME, timeout=3)

def lidar_read():
    global lidar
    while True:
        try:
            angles = []
            distances = []
            for scan in lidar.iter_scans():
                for (_, angle, distance) in scan:
                    if angle > 180:
                        continue
                    angles += [np.radians(angle)]
                    distances += [distance / 1000]
            
                if len(angles) >= MINIMUM_SAMPLE_SIZE:
                    return angles, np.array(distances)

        except RPLidarException as e:
            print(f'RPLidar Exception: {e}')
            print("Restarting Lidar...")
            lidar.stop()
            lidar.disconnect()
            lidar = RPLidar(None, PORT_NAME, timeout=3)


def main(file_name, angle_step, move_step, xy_resolution, distortion_amt):
    """
    Example usage
    """
    print(__file__, "start")

    # ONLY FOR EXAMPLE
    # ang, dist = file_read(file_name)
    ang, dist = lidar_read()
    print("angles:", ang)
    print("distances:", dist)
    dist = dist * distortion_amt

    # ONLY FOR EXAMPLE
    moves = get_moves(angle_step, move_step, .25, xy_resolution)
    
    ### Getting times for Rust
    start = time.time()
    grid = scan_to_grid(ang, dist, xy_resolution, 2) 
    middle = time.time()
    path = traverse_grid(grid.grid_map, grid.scanner_pos, grid.width - 1, moves)
    end = time.time()
    
    # Testing Code for angle and distance
    angle_list = []
    last_angle = -1000
    for i in range(1, len(path)):
        curr_node, prev_node = path[i], path[i - 1]
        curr_angle =  move_angle(curr_node, prev_node)
        curr_dist = move_dist(curr_node, prev_node)
        if last_angle != curr_angle:
            angle_list.append((curr_dist, curr_angle))
        
        last_angle = curr_angle
        
    print(angle_list)
    print("RUST:\n\t Scan to grid: ", middle - start, "\n\t Traverse grid: ", end - middle, "\n\t Total: ", end - start) 

    plot_map_path(grid.grid_map, path)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--file_name', default="lidar01.csv")
    parser.add_argument('--angle_step', type=int, default=10)
    parser.add_argument('--move_step', type=int, default=60)
    parser.add_argument('--xy_resolution', type=float, default=0.1)
    parser.add_argument('--distortion_amt', type=float, default=10)

    args = parser.parse_args()

    main(args.file_name, args.angle_step, args.move_step, args.xy_resolution, args.distortion_amt)