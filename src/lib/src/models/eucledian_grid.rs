use pyo3::prelude::*;

/// Represents a Eucledian grid map and its metadata
/// 
/// # Attributes
/// 
/// * `grid_map` - A 2D vector representing the grid map.
/// * `scanner_pos` - A tuple representing the position of the scanner in the grid map.
/// * `width` - Width of the grid map.
/// * `length` - Length of the grid map.
#[pyclass]
pub struct EuclideanGrid {
    #[pyo3(get)]
    pub grid_map: Vec<Vec<f64>>,    
    #[pyo3(get)]
    pub scanner_pos: (usize, usize), 
    #[pyo3(get)]
    pub width: usize,             
    #[pyo3(get)]
    pub length: usize,             
}