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


def main(file_name, angle_step, move_step, xy_resolution, distortion_amt):
    """
    Example usage
    """
    print(__file__, "start")

    # ONLY FOR EXAMPLE
    ang, dist = file_read(file_name)
    dist = dist * distortion_amt

    occupied_x = (np.cos(ang) * dist) / xy_resolution
    print(min(occupied_x))

    # ONLY FOR EXAMPLE
    moves = get_moves(angle_step, move_step, .25, xy_resolution)

    ### Getting times for Rust
    start = time.time()
    grid = scan_to_grid(ang, dist, xy_resolution, 2) 
    middle = time.time()
    path = traverse_grid(grid.grid_map, grid.scanner_pos, grid.width - 1, moves)
    end = time.time()

    print("RUST:\n\t Scan to grid: ", middle - start, "\n\t Traverse grid: ", end - middle, "\n\t Total: ", end - start) 

    plot_map_path(grid.grid_map, path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--file_name', default="lidar01.csv")
    parser.add_argument('--angle_step', type=int, default=10)
    parser.add_argument('--move_step', type=int, default=60)
    parser.add_argument('--xy_resolution', type=float, default=0.1)
    parser.add_argument('--distortion_amt', type=int, default=10)

    args = parser.parse_args()

    main(args.file_name, args.angle_step, args.move_step, args.xy_resolution, args.distortion_amt)
