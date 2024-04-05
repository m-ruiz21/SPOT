/// Combine multiple occupancy grids into a single occupancy grid
/// 
/// # Arguments
/// 
/// * `occupancy_grids` - A list of occupancy grids.
/// 
/// # Returns
/// 
/// * `Vec<Vec<f32>>` - A 2D vector representing the combined occupancy grid.
#[pyfunction]
#[pyo3(text_signature = "(occupancy_grids: list[OccupancyGrid], /)")]
pub fn combine_grid(occupancy_grids: Vec<OccupancyGrid>) {
    let x_width = occupancy_grids.iter().map(|grid| grid.x_width).max().unwrap();
    let y_width = occupancy_grids.iter().map(|grid| grid.y_width).max().unwrap(); 

    let mut combined_occupancy_grid = vec![vec![0.0; y_width]; x_width];

    for grid in occupancy_grids {
        let x_offset = (x_width - grid.x_width) / 2;
        for x in 0..grid.x_width {
            for y in 0..grid.y_width {
                combined_occupancy_grid[x + x_offset][y] = grid.occupancy_map[x][y];
            }
        }
    }

    combined_occupancy_grid
}