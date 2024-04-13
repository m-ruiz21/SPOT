use pyo3::prelude::*;
use crate ::models::eucledian_grid::EuclideanGrid;

const EXTEND_AREA: f64 = 1.0; 

/// Converts LIDAR scan to gaussian grid.
/// # Arguments
/// 
/// * `angles` - A vector of angles in radians.
/// * `distances` - A vector of distances in meters. 
/// * `resolution` - Desired resolution of the grid map.
/// * `danger_rad` - Maximum distance to consider as danger. 
/// 
/// # Returns
/// 
/// * `GuassianGrid` - Contains grid and its metadata
#[pyfunction]
#[pyo3(text_signature = "(angles: list<float>, distances: list<float>, resolution: float, danger_rad: float, /)")]
pub fn scan_to_grid(angles: Vec<f64>, distances: Vec<f64>, resolution: f64, danger_rad: f64) -> EuclideanGrid {
    let occupied_x: Vec<f64> = distances.iter()
        .zip(angles.iter())
        .map(|(d, a)| d * a.sin())
        .collect();

    let occupied_y: Vec<f64> = distances.iter()
        .zip(angles.iter())
        .map(|(d, a)| d * a.cos())
        .collect();

    let (min_y, min_x, scanner_pos, width, length) = calc_grid_map_config(occupied_x.clone(), occupied_y.clone(), resolution);

    let mut grid_map = vec![vec![0.0; length]; width];
    for ix in 0..width {
        for iy in 0..length {
            let x = min_x + ix as f64 * resolution;
            let y = min_y + iy as f64 * resolution;
            
            let mut min_distance = f64::INFINITY;
            
            for (iox, ioy) in occupied_x.iter().zip(occupied_y.iter()) {
                let distance = ((iox - x).powi(2) + (ioy - y).powi(2)).sqrt();
                if distance < min_distance {
                    min_distance = distance;
                }
            };

            grid_map[ix][iy] = (min_distance as f64).min(danger_rad);
        }
    }

    EuclideanGrid {
        grid_map,
        scanner_pos,
        width,
        length,
    }
}


/// Calculates the configuration of the grid map.
/// 
/// # Arguments
/// 
/// * `occupied_x` - A vector of x coordinates of occupied points.
/// * `occupied_y` - A vector of y coordinates of occupied points.
/// * `resolution` - Desired resolution of the grid map.
/// 
/// # Returns
/// 
/// * A tuple containing the minimum x, minimum y, the position of the scanner on the map, x width, and y width of the grid map.
fn calc_grid_map_config(occupied_x: Vec<f64>, occupied_y: Vec<f64>, resolution: f64) -> (f64, f64, (usize, usize), usize, usize) {
    let min_x = (occupied_x
            .iter()
            .min_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal))
            .unwrap() - EXTEND_AREA / 2.0
        ).round();
    let min_y = (occupied_y
            .iter()
            .min_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal))
            .unwrap() - EXTEND_AREA / 2.0
        ).round();

    let max_x = (occupied_x
            .iter()
            .max_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal))
            .unwrap() + EXTEND_AREA / 2.0
        ).round();

    let max_y = (occupied_y
            .iter()
            .max_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal))
            .unwrap() + EXTEND_AREA / 2.0
        ).round();

    let width = ((max_x - min_x) / resolution).round() as usize;
    let length = ((max_y - min_y) / resolution).round() as usize;

    let scanner_pos = (
        ((0.0 - min_y) / resolution).round() as usize,
        ((0.0 - min_x) / resolution).round() as usize,
    );

    (min_y, min_x, scanner_pos, width, length)
}
