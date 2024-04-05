use pyo3::prelude::*;

/// Converts 3D point cloud to 2D scan.
/// 
/// # Arguments
/// 
/// * `points` - A vector of 3D points.
/// 
/// # Returns
/// 
/// * `Tuple` - A tuple of two vectors containing angles and distances of the scan.
#[pyfunction]
#[pyo3(text_signature = "(points: list[tuple[float, float, float]], scale: float, /)")]
pub fn point_cloud_to_scan(points: Vec<(f32, f32, f32)>, scale: f32) -> (Vec<f32>, Vec<f32>) {
    let mut angles = Vec::new();
    let mut distances = Vec::new();
    
    for point in points {
        let (x, y) = (point.0 * scale, point.2 * scale);    // convert it to m
        let distance = (x.powi(2) + y.powi(2)).sqrt();
        let angle = (y / x).atan();
        distances.push(distance);
        angles.push(angle);
    }
    
    (angles, distances)
}
