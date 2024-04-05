from spot_rs import scan_to_grid
import numpy as np
import matplotlib.pyplot as plt
import time

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
    xy_resolution = .1  # grid represend .1 units (LIDAR unit) in the real world  
    ang, dist = file_read("lidar01.csv")

    dist = dist * 10

    start = time.time()
    grid = \
        scan_to_grid(ang, dist, xy_resolution, 2)
    end = time.time()
    print("time:", end - start) 
    plt.imshow(grid.grid_map, cmap="hot_r", origin="lower")
    plt.colorbar()
    plt.show()

if __name__ == '__main__':
    main()    