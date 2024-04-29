import numpy as np
import matplotlib.pyplot as plt
import time
import heapq
import argparse
from spot_rs import scan_to_grid

def file_read(file_name):
    """
    Reading LIDAR laser beams (angles and corresponding distance data)
    """
    with open(file_name) as data:
        measures = [line.split(",") for line in data]
    angles = []
    distances = []
    for measure in measures:
        angles.append(float(measure[0]))
        distances.append(float(measure[1]))
    angles = np.array(angles)
    distances = np.array(distances)
    return angles, distances


class Node:
    def __init__(self, x, y, min_dist, parents, move, turns, score):
        self.x = x
        self.y = y
        self.min_dist = min_dist 
        self.parents = parents
        self.move = move
        self.turns = turns
        self.score = -score

    def __lt__(self, other):
        return self.score < other.score 

def valid_move(x, y, grid):
    out_of_bounds = x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid)

    if out_of_bounds:
        return False
    
    return grid[y][x] > .2

def calc_score(min_dist, turns, path, end_y):
    if not path: 
        return 0

    dist_to_goal = end_y - path[-1][1]
    return  .9 * min_dist - .5 * turns / (len(path) + 1) - .01 * dist_to_goal

def traverse_grid_py(grid, start, end_y, moves):
    init_x, init_y = start
    init_node = Node(init_x, init_y, grid[init_y][init_x], [], 0, 0, calc_score(grid[init_y][init_x], 0, [], end_y))

    queue = [init_node]
    visited = set()

    max_node = Node(0, 0, 0, [], 0, 0, 0) 

    while queue:
        node = heapq.heappop(queue)
        if (node.x, node.y) in visited:
            continue

        visited.add((node.x, node.y))

        for move, (dx, dy) in enumerate(moves): 
            new_x, new_y = node.x + dx, node.y + dy
                
            if new_y == end_y:
                print("found path")
                yield node.parents + [(node.x, node.y)]

            if not valid_move(new_x, new_y, grid):
                continue
   
            turns = node.turns + (move != node.move and move != 0)
            new_path = node.parents + [(node.x, node.y)]
            new_min_dist = min(grid[new_y][new_x], node.min_dist)

            score = calc_score(new_min_dist, turns, new_path, end_y)

            new_node = Node(new_x, new_y, new_min_dist, new_path, move, turns, score)
            heapq.heappush(queue, new_node)

            if new_node.score > max_node.score:
                max_node = new_node

        yield node.parents + [(node.x, node.y)] 

def plot_map_path(grid_map, paths):
    """ 
    Plotting the grid map and the paths
    """
    plt.imshow(grid_map, cmap="hot_r", origin="lower")
    plt.colorbar()
    plt.show(block=False)
    for path in paths:
        plt.clf()  # Clear the plot
        plt.imshow(grid_map, cmap="hot_r", origin="lower")
        x, y = zip(*path)
        plt.plot(x, y, 'ro-')
        
        if path[-1][-1] == len(grid_map) - 1:
            break
        
        plt.pause(0.0000000000000000000000000000000000001)

    plt.show()

def main(file_name, angle_step, move_step, xy_resolution, distortion_amt, compare):
    print(__file__, "start")

    # Define moves
    max_dist = round(0.25 / xy_resolution)
    moves = [(0, max_dist)]
    for angle in range(angle_step, 60, angle_step):
        x = round(np.sin(np.radians(angle)) * max_dist)
        y = round(np.cos(np.radians(angle)) * max_dist)
        moves += [(x, y), (-x, y)]

    # Load data
    angles, distances = file_read(file_name)
    distances = distances * distortion_amt
    grid = scan_to_grid(angles, distances, xy_resolution, 2)

    # Visualize paths
    paths = traverse_grid_py(grid.grid_map, grid.scanner_pos, grid.width - 1, moves)
    plot_map_path(grid.grid_map, paths)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--file_name', default="lidar01.csv")
    parser.add_argument('--angle_step', type=int, default=10)
    parser.add_argument('--move_step', type=int, default=60)
    parser.add_argument('--xy_resolution', type=float, default=0.1)
    parser.add_argument('--distortion_amt', type=int, default=10)
    parser.add_argument('--compare', type=bool, default=True)

    args = parser.parse_args()

    main(args.file_name, args.angle_step, args.move_step, args.xy_resolution, args.distortion_amt, args.compare)
