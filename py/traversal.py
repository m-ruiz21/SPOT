import numpy as np
import matplotlib.pyplot as plt
import time
from spot_rs import scan_to_grid 
from spot_rs import traverse_grid
import argparse
from servo_send import servo_send, beep_send

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


def move_angle(prev_node, curr_node):
    x1, x2 = prev_node[0], curr_node[0]
    y1, y2 = prev_node[1], curr_node[1]
    print('x1', x1, 'y1', y2, 'x2', x2, 'y2', y2)
    angle = - ((np.arctan2(y2 - y1, x2 - x1) * 180/np.pi) - 90)
    return angle


PORT_NAME = '/dev/ttyUSB0' # for linux
MINIMUM_SAMPLE_SIZE = 180 # 180 readings
MAX_PATH_LOOKAHEAD_FOR_ANGLE = 7 # look max 12 steps ahead to calculate angle


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
            lidar.disconnect()
            lidar = RPLidar(None, PORT_NAME, timeout=3)


def main(angle_step, max_angle, move_step, xy_resolution):
    """
    Example usage
    """
    print(__file__, "start")
    
    moves = get_moves(angle_step, max_angle, move_step, xy_resolution)
    prev_angle = -10000
    while True:
        # ang, dist = file_read('lidar01.csv')
        ang, dist = lidar_read()
        # print("angles:", ang)
        # print("distances:", dist)
        dist = dist * 10
        
        ### Getting times for Rust
        start = time.time()
        grid = scan_to_grid(ang, dist, xy_resolution, 2) 
        middle = time.time()
        path = traverse_grid(grid.grid_map, grid.scanner_pos, grid.width - 1, moves, .1)
        end = time.time()
        
        if len(path) > MAX_PATH_LOOKAHEAD_FOR_ANGLE:
            # Testing Code for angle and distance
            print('path[0]', path[0])
            print(f'path[{MAX_PATH_LOOKAHEAD_FOR_ANGLE}]', path[MAX_PATH_LOOKAHEAD_FOR_ANGLE])
            
            angle = move_angle(path[0], path[MAX_PATH_LOOKAHEAD_FOR_ANGLE])
            print('angle = ', angle)
            
            if prev_angle != angle:
                beep_send()
            prev_angle = angle
            
            servo_send(angle)
        else:
            beep_send()
        
        
        print("RUST:\n\t Scan to grid: ", middle - start, "\n\t Traverse grid: ", end - middle, "\n\t Total: ", end - start) 

        #plot_map_path(grid.grid_map, path)
        
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process Parameters for SPOT.')
    
    # number of degrees in between valid moves
    parser.add_argument('--angle_step', type=int, default=10)
    
    # max angle either direction
    parser.add_argument('--max_angle', type=int, default=60)
    
    # number of meters robot moves in between valid moves
    parser.add_argument('--move_step', type=float, default=.25)
    
    # % of dm^2 each grid represents
    parser.add_argument('--xy_resolution', type=float, default=.1)

    args = parser.parse_args()

    main(args.angle_step, args.max_angle, args.move_step, args.xy_resolution)