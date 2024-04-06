import numpy as np
import matplotlib.pyplot as plt
import time
from spot_rs import scan_to_grid

# moves = [
#     (0, 10),
#     (2, 10),
#     (-2, 10),
#     (3, 9),
#     (-3, 9),
#     (5, 9),
#     (-5, 9),
#     (6, 8),
#     (-6, 8),
#     (8, 6),
#     (-8, 6),
#     (9, 5),
#     (-9, 5)
# ]

import heapq

def valid_move(x, y, grid):
    out_of_bounds = x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid)

    if out_of_bounds:
        return False
    
    return grid[y][x] > .6


def calc_score(min_dist, turns, path):
    return min_dist - .5 * turns / (len(path) + 1)


class Node:
    def __init__(self, x: int, y: int, min_dist: float, parents: list['Node'], move, turns, score):
        self.x = x
        self.y = y
        self.min_dist = min_dist 
        self.parents = parents
        self.move = move
        self.turns = turns
        self.score = -score

    def __lt__(self, other):
        return self.score < other.score 


def traverse_grid(grid: list[list[float]], start: tuple[int, int], end_y: int, moves) -> list[Node]:
    
    init_x, init_y = start
    init_node = Node(init_x, init_y, grid[init_y][init_x], [], 0, 0, calc_score(grid[init_y][init_x], 0, []))

    queue = [init_node]
    visited = set()

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
                return node.parents + [node]
   
            turns = node.turns + (move != node.move)
            new_path = node.parents + [node]
            new_min_dist = min(grid[new_y][new_x], node.min_dist)

            score = calc_score(new_min_dist, turns, new_path)

            new_node = Node(new_x, new_y, new_min_dist, new_path, move, turns, score)
            heapq.heappush(queue, new_node)


    return None


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


def main():
    """
    Example usage
    """
    print(__file__, "start")
    xy_resolution = .1  # grid represend decimeter in the real world  
    ang, dist = file_read("lidar01.csv")
    dist = dist * 10
    moves = get_moves(10, 60, .25, xy_resolution)

    start = time.time()
    grid = \
        scan_to_grid(ang, dist, xy_resolution, 2) 
    
    mid = time.time()
    
    path = traverse_grid(grid.grid_map, (40, 0), len(grid.grid_map) - 1, moves)
    
    end = time.time()
    
    print("total time:", end - start) 
    print("scan to grid time:", mid - start)
    print("traverse grid time:", end - mid)
    
    plt.imshow(grid.grid_map, cmap="hot_r", origin="lower")
    plt.colorbar()
    
    if path:
        for node in path:
            plt.plot(node.x, node.y, 'ro')

    plt.show()

    xy_resolution = .1  # grid represend decimeter in the real world  
    ang, dist = file_read("lidar02.csv")
    moves = get_moves(10, 60, .25, xy_resolution)
    print(moves)

    start = time.time()
    grid = \
        scan_to_grid(ang, dist, xy_resolution, 2) 
    
    mid = time.time()
    
    path = traverse_grid(grid.grid_map, (40, 0), len(grid.grid_map) - 1, moves)
    
    end = time.time()
    
    print("total time:", end - start) 
    print("scan to grid time:", mid - start)
    print("traverse grid time:", end - mid)

    plt.imshow(grid.grid_map, cmap="hot_r", origin="lower")
    plt.colorbar()
    
    if path:
        for node in path:
            plt.plot(node.x, node.y, 'ro')

    plt.show()



if __name__ == '__main__':
    main()    