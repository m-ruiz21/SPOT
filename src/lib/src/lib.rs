use pyo3::prelude::*;
mod scan_to_grid;
mod traverse_grid;

mod models {
    pub mod node;
    pub mod eucledian_grid;
}

#[pymodule]
fn spot_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(scan_to_grid::scan_to_grid, m)?)?;
    m.add_function(wrap_pyfunction!(traverse_grid::traverse_grid, m)?)?;
    m.add_class::<models::eucledian_grid::EuclideanGrid>()?; 
    m.add_class::<models::node::Node>()?;
    Ok(())
}
