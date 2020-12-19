use std::collections::HashMap;
use crate::util::coord3::Coord3;
use std::ops::RangeInclusive;
use std::collections::hash_map::Values;

// A grid of characters, represented as sparsely to support very large grids
pub struct SparseGrid3<T> {
    grid: HashMap<Coord3, T>
}

impl <T> SparseGrid3<T> {
    // Create a new instance
    pub fn new() -> SparseGrid3<T> {
        SparseGrid3 {
            grid: HashMap::new()
        }
    }

    pub fn set_coord(&mut self, pos: Coord3, val: T) {
        self.grid.insert(pos, val);
    }

    pub fn set(&mut self, x: i32, y: i32, z: i32, val: T) {
        self.grid.insert(Coord3 {x, y, z}, val);
    }

    pub fn get_coord(&self, pos: &Coord3) -> Option<&T> {
        self.grid.get(pos)
    }

    pub fn get(&self, x: i32, y: i32, z: i32) -> Option<&T> {
        self.get_coord(&Coord3 { x, y, z} )
    }

    pub fn remove(&mut self, pos: &Coord3) {
        self.grid.remove(pos);
    }

    pub fn x_range(&self) -> RangeInclusive<i32> {
        let min_x = self.grid.keys().map(|c| c.x).min().unwrap_or(0);
        let max_x = self.grid.keys().map(|c| c.x).max().unwrap_or(0);
        min_x..=max_x
    }

    pub fn y_range(&self) -> RangeInclusive<i32> {
        let min_y = self.grid.keys().map(|c| c.y).min().unwrap_or(0);
        let max_y = self.grid.keys().map(|c| c.y).max().unwrap_or(0);
        min_y..=max_y
    }

    pub fn z_range(&self) -> RangeInclusive<i32> {
        let min_z = self.grid.keys().map(|c| c.z).min().unwrap_or(0);
        let max_z = self.grid.keys().map(|c| c.z).max().unwrap_or(0);
        min_z..=max_z
    }

    pub fn neighbors26(&self, center: &Coord3) -> Vec<(Coord3, &T)> {
        self.neighbors(center.neighbors26())
    }

    pub fn neighbors_values26(&self, center: &Coord3) -> Vec<&T> {
        self.neighbors_values(center.neighbors26())
    }

    fn neighbors(&self, neighbors: Vec<Coord3>) -> Vec<(Coord3, &T)> {
        let mut out_vec = vec![];

        for n in neighbors {
            match self.get_coord(&n) {
                Some(v) => out_vec.push((n, v)),
                None => ()
            }
        }

        out_vec
    }

    fn neighbors_values(&self, neighbors: Vec<Coord3>) -> Vec<&T> {
        let mut out_vec = vec![];

        for n in neighbors {
            match self.get_coord(&n) {
                Some(v) => out_vec.push(v),
                None => ()
            }
        }

        out_vec
    }

    pub fn values(&self) -> Values<Coord3, T> {
        self.grid.values()
    }
}
