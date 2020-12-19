use std::collections::HashMap;
use crate::day17::coord4::Coord4;
use std::ops::RangeInclusive;
use std::collections::hash_map::Values;

// A grid of characters, represented as sparsely to support very large grids
pub struct SparseGrid4<T> {
    grid: HashMap<Coord4, T>
}

impl <T> SparseGrid4<T> {
    // Create a new instance
    pub fn new() -> SparseGrid4<T> {
        SparseGrid4 {
            grid: HashMap::new()
        }
    }

    pub fn set_coord(&mut self, pos: Coord4, val: T) {
        self.grid.insert(pos, val);
    }

    pub fn set(&mut self, x: i32, y: i32, z: i32, w: i32, val: T) {
        self.grid.insert(Coord4 {x, y, z, w}, val);
    }

    pub fn get_coord(&self, pos: &Coord4) -> Option<&T> {
        self.grid.get(pos)
    }

    pub fn get(&self, x: i32, y: i32, z: i32, w: i32) -> Option<&T> {
        self.get_coord(&Coord4 { x, y, z, w} )
    }

    pub fn remove(&mut self, pos: &Coord4) {
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

    pub fn w_range(&self) -> RangeInclusive<i32> {
        let min_w = self.grid.keys().map(|c| c.w).min().unwrap_or(0);
        let max_w = self.grid.keys().map(|c| c.w).max().unwrap_or(0);
        min_w..=max_w
    }

    pub fn neighbors80(&self, center: &Coord4) -> Vec<(Coord4, &T)> {
        self.neighbors(center.neighbors80())
    }

    pub fn neighbors_values80(&self, center: &Coord4) -> Vec<&T> {
        self.neighbors_values(center.neighbors80())
    }

    fn neighbors(&self, neighbors: Vec<Coord4>) -> Vec<(Coord4, &T)> {
        let mut out_vec = vec![];

        for n in neighbors {
            match self.get_coord(&n) {
                Some(v) => out_vec.push((n, v)),
                None => ()
            }
        }

        out_vec
    }

    fn neighbors_values(&self, neighbors: Vec<Coord4>) -> Vec<&T> {
        let mut out_vec = vec![];

        for n in neighbors {
            match self.get_coord(&n) {
                Some(v) => out_vec.push(v),
                None => ()
            }
        }

        out_vec
    }

    pub fn values(&self) -> Values<Coord4, T> {
        self.grid.values()
    }
}
