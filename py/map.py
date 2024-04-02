import numpy as np
from decimal import Decimal
import pyrealsense2 as rs 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

def update(i):
    plt.clf()
    print(f"updating... {i}")
    start_time = time.time()
    global pipeline 
    array = get_pointcloud(pipeline)
    occupancy_array = create_occupancy_array(array, pov_fill=True, resolution=0.1)
    end_time = time.time()
    print(f"Time taken to update occupancy array: {end_time - start_time} seconds") 
    plt.imshow(occupancy_array, cmap='binary', origin='lower')
    plt.xlabel('X-coordinate (cells)')
    plt.ylabel('Y-coordinate (cells)')
    plt.title('Occupancy Array')
    plt.grid(True)


def visualize_2d(point_cloud):
    """
    Creates a 2D projection of a point cloud.

    Args:
        point_cloud (list of tuples): A list of tuples representing points in 3D space.
            Each tuple should contain (x, y, z) coordinates.

    Returns:
        None (displays the 2D projection plot)
    """
    # Extract x, y, and z coordinates from the point cloud
    x_coords, y_coords, z_coords = zip(*point_cloud)

    # Create a scatter plot of the point cloud in the x-y plane
    plt.figure(figsize=(8, 6))
    plt.scatter(x_coords, y_coords, c=z_coords, s=5)
    plt.colorbar(label='height-coordinate')
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.title('2D Projection of Point Cloud')
    plt.grid(True)
    plt.show()


def fill_pov(occupancy_array, camera_cell_x, pov_angle_degrees):
    for y, x in np.ndindex(occupancy_array.shape):
        dx = abs(x - camera_cell_x)
        angle_from_camera = np.degrees(np.arctan2(y, dx))
        if angle_from_camera < pov_angle_degrees / 2:
            occupancy_array[y, x] = True 


def create_occupancy_array(point_cloud, resolution=0.1, pov_angle_degrees=80, pov_fill=False):
    """
    Creates an occupancy array from a point cloud.

    Args:
        point_cloud (list of tuples): A list of tuples representing points in 3D space.
            Each tuple should contain (x, y, z) coordinates.
        resolution (float): The grid resolution (cell size) for the occupancy array.

    Returns:
        np.ndarray: A 2D occupancy array where True indicates an object is present.
    """
    # z coordinates is the depth and y is the height, so we ignore y and rename z to our 'y' 
    x_coords, y_coords, _  = zip(*point_cloud)

    # point cloud is relative to camera (has neg values)
    # so we need to define the dimensions of the occupancy array 
    # such that the min values are 0
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    num_x_cells = int(np.ceil((max_x - min_x) / resolution))
    num_y_cells = int(np.ceil((max_y - min_y) / resolution))

    camera_cell_x = int((0 - min_x) / resolution)

    occupancy_array = np.zeros((num_y_cells, num_x_cells), dtype=bool)

    if pov_fill:
        fill_pov(occupancy_array, camera_cell_x, pov_angle_degrees)

    for x, y, _ in point_cloud:
        cell_x = int((x - min_x) / resolution)
        cell_y = int((y - min_y) / resolution) 
        
        occupancy_array[cell_y, cell_x] = True

    return occupancy_array


def get_pointcloud(pipeline):
    frames = pipeline.wait_for_frames()
    depth = frames.get_depth_frame()
    if not depth: return None
    pc = rs.pointcloud()
    points = pc.calculate(depth.as_depth_frame())
    return np.asanyarray(points.get_vertices())


global pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

try:
    # Create a context object. This object owns the handles to all connected realsense devices
    pipeline = rs.pipeline()

    # Configure streams
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    # Start streaming
    pipeline.start(config)

    array = get_pointcloud(pipeline)

    visualize_2d(array)
    # fig = plt.figure(figsize=(8, 6))
    # ani = animation.FuncAnimation(fig, update, interval=100, save_count=10)  # update every 100ms
    # plt.show()

    exit(0)

except Exception as e:
    print(e)
    pass
