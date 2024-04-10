import numpy as np
import matplotlib.pyplot as plt
import time
from spot_rs import scan_to_grid 
from spot_rs import traverse_grid
import argparse
import heapq

def valid_move(x, y, grid):
    out_of_bounds = x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid)

    if out_of_bounds:
        return False
    
    return grid[y][x] > .6


def calc_score(min_dist, turns, path):
    return min_dist - .5 * turns / (len(path) + 1)


class Node:
    def __init__(self, x: int, y: int, min_dist: float, parents: list[(int, int)], move, turns, score):
        self.x = x
        self.y = y
        self.min_dist = min_dist 
        self.parents = parents
        self.move = move
        self.turns = turns
        self.score = -score

    def __lt__(self, other):
        return self.score < other.score 


def traverse_grid_py(grid: list[list[float]], start: tuple[int, int], end_y: int, moves) -> list[Node]:
    init_x, init_y = start
    init_node = Node(init_x, init_y, grid[init_y][init_x], [], 0, 0, calc_score(grid[init_y][init_x], 0, []))

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

            if not valid_move(new_x, new_y, grid):
                continue

            if new_y == end_y:
                return node.parents + [(node.x, node.y)]         
   
            turns = node.turns + (move != node.move)
            new_path = node.parents + [(node.x, node.y)]
            new_min_dist = min(grid[new_y][new_x], node.min_dist)

            score = calc_score(new_min_dist, turns, new_path)

            new_node = Node(new_x, new_y, new_min_dist, new_path, move, turns, score)
            heapq.heappush(queue, new_node)

            if new_node.score > max_node.score:
                max_node = new_node

    return max_node.parents + [(node.x, node.y)] 


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


def main(file_name, angle_step, move_step, xy_resolution, distortion_amt, compare):
    """
    Example usage
    """
    print(__file__, "start")
    ang, dist = file_read(file_name)
    dist = dist * distortion_amt
    moves = get_moves(angle_step, move_step, .25, xy_resolution)


    ### Getting times for Rust
    start = time.time()
    grid = scan_to_grid(ang, dist, xy_resolution, 2) 
    middle = time.time()
    path = traverse_grid(grid.grid_map, (40, 0), len(grid.grid_map) - 1, moves)
    end = time.time()

    print("RUST:\n\t Scan to grid: ", middle - start, "\n\t Traverse grid: ", end - middle, "\n\t Total: ", end - start) 

    plot_map_path(grid.grid_map, path)

    if compare:
        ### Getting times for Python
        start = time.time()
        grid = scan_to_grid(ang, dist, xy_resolution, 2)
        middle = time.time()
        path = traverse_grid_py(grid.grid_map, (40, 0), len(grid.grid_map) - 1, moves)
        end = time.time()   

        print("PYTHON:\n\t Scan to grid: ", middle - start, "\n\t Traverse grid: ", end - middle, "\n\t Total: ", end - start)
        plot_map_path(grid.grid_map, path)


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