# spot_rs Functional Package Documentation

## Classes

### EuclideanGrid
This class represents a Euclidean grid map and its metadata.

#### Attributes
- `grid_map`: A 2D vector representing the grid map.
- `scanner_pos`: A tuple representing the position of the scanner in the grid map.
- `width`: Width of the grid map.
- `length`: Length of the grid map.

### Node
This class represents a node in the grid.

#### Attributes
- `min_dist`
- `move_idx`
- `parents`
- `turns`
- `x`
- `y`

## Functions

### point_cloud_to_scan(points)
Converts 3D point cloud to 2D scan.

#### Arguments
- `points`: A vector of 3D points.

#### Returns
- `Tuple`: A tuple of two vectors containing angles and distances of the scan.

### scan_to_grid(angles, distances, resolution, danger_rad)
Converts LIDAR scan to gaussian grid.

#### Arguments
- `angles`: A vector of angles in radians.
- `distances`: A vector of distances in meters. 
- `resolution`: Desired resolution of the grid map.
- `danger_rad`: Maximum distance to consider as danger. 

#### Returns
- `GuassianGrid`: Contains grid and its metadata

### traverse_grid()
This function is used to traverse the grid.
