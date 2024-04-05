use pyo3::prelude::*;
const EXTEND_AREA: f32 = 1.0; // Define EXTEND_AREA as a constant at the top of your file

#[pyclass]
pub struct OccupancyGrid {
    #[pyo3(get)]
    pub occupancy_map: Vec<Vec<f32>>,
    #[pyo3(get)]
    pub min_x: f32,
    #[pyo3(get)]
    pub max_x: f32,
    #[pyo3(get)]
    pub min_y: f32,
    #[pyo3(get)]
    pub max_y: f32,
    #[pyo3(get)]
    pub x_width: usize,
    #[pyo3(get)]
    pub y_width: usize,
}


/// Converts LIDAR scan to occupancy grid.
/// # Arguments
/// 
/// * `angles` - A vector of angles in radians.
/// * `distances` - A vector of distances in meters. 
/// 
/// # Returns
/// 
/// * `OccupancyGrid` - Contains grid and its metadata
#[pyfunction]
#[pyo3(text_signature = "(angles: list<float>, distances: list<float>, resolution: float, /)")]
pub fn scan_to_grid(angles: Vec<f32>, distances: Vec<f32>, resolution: f32) -> OccupancyGrid {
    let occupied_x: Vec<f32> = distances.iter()
        .zip(angles.iter())
        .map(|(d, a)| d * a.sin())
        .collect();

    let occupied_y: Vec<f32> = distances.iter()
        .zip(angles.iter())
        .map(|(d, a)| d * a.cos())
        .collect();

    let (min_x, min_y, max_x, max_y, x_width, y_width) = calc_grid_map_config(occupied_x.clone(), occupied_y.clone(), resolution);

    let mut occupancy_map = vec![vec![0.5; y_width as usize]; x_width as usize];
    let center_x = (-min_x / resolution).round() as usize;
    let center_y = (-min_y / resolution).round() as usize;

    for (x, y) in occupied_x.iter().zip(occupied_y.iter()) {
        let ix = ((x - min_x) / resolution).round() as usize;
        let iy = ((y - min_y) / resolution).round() as usize;
        let laser_beams = bresenham((center_x, center_y), (ix, iy));
        for laser_beam in laser_beams {
            occupancy_map[laser_beam.0][laser_beam.1] = 0.0;
        }
        occupancy_map[ix][iy] = 1.0;
        if ix + 1 < x_width as usize {
            occupancy_map[ix + 1][iy] = 1.0;
        }
        if iy + 1 < y_width as usize {
            occupancy_map[ix][iy + 1] = 1.0;
        }
        if ix + 1 < x_width as usize && iy + 1 < y_width as usize {
            occupancy_map[ix + 1][iy + 1] = 1.0;
        }
    };

    OccupancyGrid {
        occupancy_map,
        min_x,
        max_x,
        min_y,
        max_y,
        x_width,
        y_width,
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
/// * A tuple containing the minimum x, minimum y, maximum x, maximum y, x width, and y width of the grid map.
fn calc_grid_map_config(occupied_x: Vec<f32>, occupied_y: Vec<f32>, resolution: f32) -> (f32, f32, f32, f32, usize, usize) {
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

    let x_width = ((max_x - min_x) / resolution).round() as usize;
    let y_width = ((max_y - min_y) / resolution).round() as usize;
    
    (min_x, min_y, max_x, max_y, x_width, y_width)
}


/// Rust implementation of Bresenham's line algorithm
/// 
/// # Arguments
/// 
/// * `start` - A tuple containing the x and y coordinates of the start point.
/// * `end` - A tuple containing the x and y coordinates of the end point.
/// 
/// # Returns
/// 
/// * A vector of tuples containing the x and y coordinates of the points from start to finish.
fn bresenham(start: (usize, usize), end: (usize, usize)) -> Vec<(usize, usize)> {
    let (mut x1, mut y1) = start;
    let (mut x2, mut y2) = end;
    let mut dx = x2 as i32 - x1 as i32;
    let mut dy = y2 as i32 - y1 as i32;

    let is_steep = dy.abs() > dx.abs();

    // rotate line if steep
    if is_steep {   
        std::mem::swap(&mut x1, &mut y1);
        std::mem::swap(&mut x2, &mut y2);
    }

    // swap start and end points if necessary and store swap state
    let swapped = if x1 > x2 {  
        std::mem::swap(&mut x1, &mut x2);
        std::mem::swap(&mut y1, &mut y2);
        true
    } else {
        false
    };

    // recalculating differentials
    dx = x2 as i32 - x1 as i32;
    dy = y2 as i32 - y1 as i32;

    let mut error = dx / 2;
    let y_step = if y1 < y2 { 1 } else { -1 };

    // generate points
    let mut y = y1 as i32;
    let mut points = Vec::new();
    for x in x1..=x2 {
        points.push(if is_steep { (y as usize, x) } else { (x, y as usize) });
        error -= dy.abs();
        if error < 0 {
            y += y_step;
            error += dx;
        }
    }

    if swapped {
        points.reverse();
    }

    points
}