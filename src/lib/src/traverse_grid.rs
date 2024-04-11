use pyo3::prelude::*;
use crate::models::node::Node;
use std::collections::HashSet;
use priq::PriorityQueue;

#[pyfunction]
#[pyo3(text_signature = "(grid: list[list[float]], start: (int, int), end_y: int, moves: list[int, int] /)")]
pub fn traverse_grid(grid: Vec<Vec<f64>>, start: (i32, i32), end_y: usize, moves: Vec<(i32, i32)>) -> Vec<(usize, usize)> {
    let (init_x, init_y) = start;
    let init_parents : Vec<(usize, usize)> = Vec::new(); 
    let init_node = Node::new(
        init_x as usize, init_y as usize, 
        grid[init_y as usize][init_x as usize], 
        init_parents, 
        0,
        0
    );

    let mut queue: PriorityQueue<f64, Node> = PriorityQueue::new(); 
    let mut visited: HashSet<(usize, usize)> = HashSet::new();
    
    let mut max_path: Vec<(usize, usize )> = Vec::new(); 
    let mut max_score: f64 = 0.0; 

    queue.put(0.0, init_node);

    while let Some((_, node)) = queue.pop() {
        if visited.contains(&(node.x, node.y)) {
            continue;
        }

        visited.insert((node.x, node.y));
        
        for (move_idx, (dx, dy)) in moves.iter().enumerate() {
            let new_x = node.x as i32 + dx;
            let new_y = node.y as i32 + dy;
        
            if !valid_move(new_x, new_y, &grid) {
                continue;
            } 
            
            let turns = node.turns + (move_idx != node.move_idx && move_idx != 0) as usize;

            let mut new_path = node.parents.clone();
            new_path.push((node.x, node.y));

            let new_min_dist = grid[new_y as usize][new_x as usize].min(node.min_dist);
        
            let new_score = calc_score(new_min_dist, turns, &new_path);
             
            let new_node = Node::new(new_x as usize, new_y as usize, new_min_dist, new_path, move_idx, turns);            

            if new_y == end_y as i32 {
                return new_node.parents;                
            }

            if new_score > max_score {
                max_path = new_node.parents.clone(); 
                max_score = new_score;
            }

            queue.put(-new_score, new_node); 
        }
    };

    max_path
}


/// Checks if a given move is valid
/// # Arguments
/// 
/// * `x` - X coordinate of the move
/// * `y` - Y coordinate of the move
/// * `grid` - 2D vector representing the grid
/// 
/// # Returns
/// 
/// * `bool` - True if the move is valid, false otherwise
fn valid_move(x: i32, y: i32, grid: &Vec<Vec<f64>>) -> bool {
    let out_of_bounds: bool = x < 0 || x >= grid[0].len() as i32 || y < 0 || y >= grid.len() as i32; 

    if out_of_bounds {
        return false;
    }
    
    return grid[y as usize][x as usize] > 0.6; 
}

/// calculates score of a given node
/// # Arguments 
/// 
/// * `min_dist` - Minimum distance to obstacle 
/// * `turns` - Number of turns made to reach the node
/// * `path` - Node path to the node
/// 
/// # Returns
/// 
/// * `f64` - Score of the node
fn calc_score(min_dist: f64, turns: usize, path: &Vec<(usize, usize)>) -> f64 {
    return min_dist - 0.5 * turns as f64 / (path.len() + 1) as f64; 
}