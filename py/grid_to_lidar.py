import numpy as np
from spot_rs import scan_to_grid
import matplotlib.pyplot as plt

def grid_to_lidar(grid_map, xy_resolution, max_dist):
    """
    Create a LIDAR scan from an occupancy grid 
    """
    x, y = np.where(grid_map == 1)
    x = x * xy_resolution
    y = y * xy_resolution
    angles = np.arctan2(y, x)
    distances = np.sqrt(x**2 + y**2)
    distances[distances > max_dist] = max_dist
    return angles, distances


def main():
    # get grid map 800 x 800 grid map
    grid_map = np.zeros((800, 800))

    grid_map[0][700:800] = 1

    grid_map[600][300:700] = 1
    print(grid_map)

    scan = grid_to_lidar(grid_map, 1, 9)
    print(scan)
    grid = scan_to_grid(scan[0], scan[1], .1, 20)

    plt.imshow(grid.grid_map, cmap="hot_r", origin="lower")
    plt.colorbar()
    plt.show()

    with open("lidar02.csv", "w") as f:
        for i in range(len(scan[0])):
            f.write("{},{}\n".format(scan[0][i], scan[1][i]))


if __name__ == '__main__':
    main()