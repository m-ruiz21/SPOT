use pyo3::prelude::*;

#[pyclass]
pub struct Node { 
    #[pyo3(get)]
    pub x: usize,
    #[pyo3(get)] 
    pub y: usize,
    #[pyo3(get)]
    pub min_dist: f64,
    #[pyo3(get)]
    pub parents: Vec<(usize, usize)>,
    #[pyo3(get)]
    pub move_idx: usize,
    #[pyo3(get)]
    pub turns: usize,
}

impl std::hash::Hash for Node {
    fn hash<H: std::hash::Hasher>(&self, state: &mut H) {
        self.x.hash(state);
        self.y.hash(state);
    }
}

impl Node {
    pub fn new(x: usize, y: usize, min_dist: f64, parents: Vec<(usize, usize)>, move_idx: usize, turns: usize) -> Node {
        Node {
            x,
            y,
            min_dist,
            parents,
            move_idx,
            turns
        }
    }
}

impl Clone for Node {
    fn clone(&self) -> Self {
        Node {
            x: self.x,
            y: self.y,
            min_dist: self.min_dist,
            parents: self.parents.clone(),
            move_idx: self.move_idx,
            turns: self.turns
        }
    }
}