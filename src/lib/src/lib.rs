use pyo3::prelude::*;
mod scan_to_grid;
mod point_cloud_to_scan;

/// A Python module implemented in Rust.
#[pymodule]
fn spot_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(scan_to_grid::scan_to_grid, m)?)?;
    m.add_function(wrap_pyfunction!(point_cloud_to_scan::point_cloud_to_scan, m)?)?;
    m.add_class::<scan_to_grid::OccupancyGrid>()?; 
    Ok(())
}
