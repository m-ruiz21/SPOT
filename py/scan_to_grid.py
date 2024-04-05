from spot_rs import scan_to_grid
import numpy as np
import matplotlib.pyplot as plt

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
    xy_resolution = 0.02  # x-y grid resolution
    ang, dist = file_read("lidar01.csv")
    grid = \
        scan_to_grid(ang, dist, xy_resolution)
    xy_res = np.array(grid.occupancy_map).shape
    ox = np.sin(ang) * dist
    oy = np.cos(ang) * dist
    plt.figure(1, figsize=(10, 4))
    plt.subplot(122)
    plt.imshow(grid.occupancy_map, cmap="PiYG_r")
    # cmap = "binary" "PiYG_r" "PiYG_r" "bone" "bone_r" "RdYlGn_r"
    plt.clim(-0.4, 1.4)
    plt.gca().set_xticks(np.arange(-.5, xy_res[1], 1), minor=True)
    plt.gca().set_yticks(np.arange(-.5, xy_res[0], 1), minor=True)
    plt.grid(True, which="minor", color="w", linewidth=0.6, alpha=0.5)
    plt.colorbar()
    plt.subplot(121)
    plt.plot([oy, np.zeros(np.size(oy))], [ox, np.zeros(np.size(oy))], "ro-")
    plt.axis("equal")
    plt.plot(0.0, 0.0, "ob")
    plt.gca().set_aspect("equal", "box")
    bottom, top = plt.ylim()  # return the current y-lim
    plt.ylim((top, bottom))  # rescale y axis, to match the grid orientation
    plt.grid(True)
    plt.show() 


if __name__ == '__main__':
    main()