use std::collections::HashSet;
use std::cmp::Ordering;
use std::collections::BinaryHeap;
use pyo3::prelude::*;

fn valid_move(x: usize, y: usize, grid: &Vec<Vec<f64>>) -> bool {
    let out_of_bounds = x >= grid[0].len() || y >= grid.len();
    if out_of_bounds {
        return false;
    }
    grid[y][x] > 0.6
}

fn calc_score(min_dist: f64, turns: usize, path: &Vec<Node>) -> f64 {
    min_dist - 0.5 * turns as f64 / (path.len() + 1) as f64
}

#[derive(Clone)]
#[pyclass]
pub struct Node {
    x: usize,
    y: usize,
    min_dist: f64,
    parents: Vec<Node>,
    move_idx: usize,
    turns: usize,
    score: f64,
}

impl Node {
    fn new(x: usize, y: usize, min_dist: f64, parents: Vec<Node>, move_idx: usize, turns: usize, score: f64) -> Self {
        Node { x, y, min_dist, parents, move_idx, turns, score }
    }
}

impl PartialEq for Node {
    fn eq(&self, other: &Self) -> bool {
        self.score == other.score
    }
}

impl Eq for Node {}

impl PartialOrd for Node {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Node {
    fn cmp(&self, other: &Self) -> Ordering {
        other.score.partial_cmp(&self.score).unwrap()
    }
}

#[pyfunction]
pub fn traverse_grid(grid: Vec<Vec<f64>>, start: (usize, usize), end_y: usize, moves: Vec<(isize, isize)>) -> Option<Vec<Node>> {
    let (init_x, init_y) = start;
    let init_node = Node::new(init_x, init_y, grid[init_y][init_x], Vec::new(), 0, 0, calc_score(grid[init_y][init_x], 0, &Vec::new()));

    let mut queue = BinaryHeap::new();
    queue.push(init_node);
    let mut visited = HashSet::new();

    while let Some(node) = queue.pop() {
        if visited.contains(&(node.x, node.y)) {
            continue;
        }
        visited.insert((node.x, node.y));

        for (move_idx, (dx, dy)) in moves.iter().enumerate() {
            let new_x = (node.x as isize + dx) as usize;
            let new_y = (node.y as isize + dy) as usize;

            if !valid_move(new_x, new_y, &grid) {
                continue;
            }

            if new_y == end_y {
                return Some(node.parents.clone().into_iter().chain(std::iter::once(node)).collect());
            }

            let turns = node.turns + if move_idx != node.move_idx { 1 } else { 0 };
            let mut new_path = node.parents.clone();
            new_path.push(node.clone());
            let new_min_dist = grid[new_y][new_x].min(node.min_dist);

            let score = calc_score(new_min_dist, turns, &new_path);

            let new_node = Node::new(new_x, new_y, new_min_dist, new_path, move_idx, turns, score);
            queue.push(new_node);
        }
    }

    None
}
