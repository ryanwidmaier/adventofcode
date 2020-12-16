use std::collections::HashMap;
use super::coord2::Coord2;
use std::ops::RangeInclusive;
use std::fmt::Display;
use std::collections::hash_map::Values;

// A grid of characters, represented as sparsely to support very large grids
pub struct SparseGrid<T> {
    grid: HashMap<Coord2, T>
}

impl <T: Display> SparseGrid<T> {
    // Create a new instance
    pub fn new() -> SparseGrid<T> {
        SparseGrid {
            grid: HashMap::new()
        }
    }

    pub fn set_coord(&mut self, pos: Coord2, val: T) {
        self.grid.insert(pos, val);
    }

    pub fn set(&mut self, x: i32, y: i32, val: T) {
        self.grid.insert(Coord2 {x, y}, val);
    }

    pub fn get_coord(&self, pos: &Coord2) -> Option<&T> {
        self.grid.get(pos)
    }

    pub fn get(&self, x: i32, y: i32) -> Option<&T> {
        self.get_coord(&Coord2 { x, y } )
    }

    pub fn remove(&mut self, pos: &Coord2) {
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

    pub fn neighbors4(&self, center: &Coord2) -> Vec<(Coord2, &T)> {
        self.neighbors(center.neighbors4())
    }

    pub fn neighbors_values4(&self, center: &Coord2) -> Vec<&T> {
        self.neighbors_values(center.neighbors4())
    }

    pub fn neighbors8(&self, center: &Coord2) -> Vec<(Coord2, &T)> {
        self.neighbors(center.neighbors8())
    }

    pub fn neighbors_values8(&self, center: &Coord2) -> Vec<&T> {
        self.neighbors_values(center.neighbors8())
    }

    fn neighbors(&self, neighbors: Vec<Coord2>) -> Vec<(Coord2, &T)> {
        let mut out_vec = vec![];

        for n in neighbors {
            match self.get_coord(&n) {
                Some(v) => out_vec.push((n, v)),
                None => ()
            }
        }

        out_vec
    }

    fn neighbors_values(&self, neighbors: Vec<Coord2>) -> Vec<&T> {
        let mut out_vec = vec![];

        for n in neighbors {
            match self.get_coord(&n) {
                Some(v) => out_vec.push(v),
                None => ()
            }
        }

        out_vec
    }

    pub fn print(&self) {
        for y in self.y_range() {
            let mut line = String::from("");
            for x in self.x_range() {
                let val = self.get(x, y).
                    map_or(String::from(" "), |x| x.to_string());
                line.push_str(val.as_str());
            }
            println!("{}", line);
        }
    }

    pub fn print_range(&self, ul: &Coord2, br: &Coord2) {
        for y in ul.y..=br.y {
            let mut line = String::from("");
            for x in ul.x..=br.x {
                let val = self.get(x, y).
                    map_or(String::from(" "), |x| x.to_string());
                line.push_str(val.as_str());
            }
            println!("{}", line);
        }
    }

    pub fn values(&self) -> Values<Coord2, T> {
        self.grid.values()
    }
}
