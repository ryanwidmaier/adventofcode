pub mod coord4;
pub mod sparse_grid4;

use crate::util::coord3::Coord3;
use crate::util::sparse_grid3::{SparseGrid3};
use crate::day17::coord4::Coord4;
use crate::day17::sparse_grid4::SparseGrid4;

#[derive(PartialEq, Eq)]
enum Cell {
    Active,
    Inactive
}

fn parse(lines: &Vec<String>)  -> SparseGrid3<Cell> {
    let mut grid = SparseGrid3::new();
    for (y, line) in lines.iter().enumerate() {
       for (x, ch) in line.chars().enumerate() {
           match ch {
               '#' => grid.set(x as i32, y as i32, 0, Cell::Active),
               '.' => (),
               _ => ()
           }
       }
    }
    grid
}

pub fn part1(lines: &Vec<String>) {
    let mut grid = parse(lines);

    println!("Before any cycles:");
    print(&grid);
    for i in 0..6 {
        do_updates_p1(&mut grid);
        println!("After {} cycle", i+1);
        print(&grid);
    }
    println!("Part1: {}", grid.values().len());
}

fn do_updates_p1(grid: &mut SparseGrid3<Cell>) {
    let mut updates = Vec::new();

    let x_range = grid.x_range();
    let y_range = grid.y_range();
    let z_range = grid.z_range();

    for x in (x_range.start() - 1)..=(x_range.end() + 1) {
        for y in (y_range.start() - 1)..=(y_range.end() + 1) {
            for z in (z_range.start() - 1)..=(z_range.end() + 1) {
                if x == 2 && y == 1 && z == 0 {
                    let here = 0;
                }
                let c = Coord3 { x, y, z };
                let state = grid.get_coord(&c).unwrap_or(&Cell::Inactive);
                let actives = grid.neighbors_values26(&c).into_iter()
                    .filter(|v| **v == Cell::Active)
                    .count();

                let new_state = match *state {
                    Cell::Active if actives == 2 || actives == 3 => Cell::Active,
                    Cell::Inactive if actives == 3 => Cell::Active,
                    _ => Cell::Inactive
                };

                updates.push((c, new_state));
            }
        }
    }

    for (c, state) in updates {
        match state {
            Cell::Active => grid.set_coord(c, state),
            Cell::Inactive => grid.remove(&c)
        }
    }
}

fn print(grid: &SparseGrid3<Cell>) {
    for z in grid.z_range() {
        println!();
        println!("z={}", z);
        for y in grid.y_range() {
            let mut s = String::new();
            for x in grid.x_range() {
                s += match grid.get(x, y, z) {
                    Some(Cell::Active) => "#",
                    _ => "."
                };
            }
            println!("{}", s);
        }
    }
}

fn parse2(lines: &Vec<String>)  -> SparseGrid4<Cell> {
    let mut grid = SparseGrid4::new();
    for (y, line) in lines.iter().enumerate() {
        for (x, ch) in line.chars().enumerate() {
            match ch {
                '#' => grid.set(x as i32, y as i32, 0, 0, Cell::Active),
                '.' => (),
                _ => ()
            }
        }
    }
    grid
}

pub fn part2(lines: &Vec<String>) {
    let mut grid = parse2(lines);

    for i in 0..6 {
        do_updates_p2(&mut grid);
    }
    println!("Part2: {}", grid.values().len());
}

fn do_updates_p2(grid: &mut SparseGrid4<Cell>) {
    let mut updates = Vec::new();

    let x_range = grid.x_range();
    let y_range = grid.y_range();
    let z_range = grid.z_range();
    let w_range = grid.w_range();

    for x in (x_range.start() - 1)..=(x_range.end() + 1) {
        for y in (y_range.start() - 1)..=(y_range.end() + 1) {
            for z in (z_range.start() - 1)..=(z_range.end() + 1) {
                for w in (w_range.start() - 1)..=(w_range.end() + 1) {
                    let c = Coord4 { x, y, z, w };
                    let state = grid.get_coord(&c).unwrap_or(&Cell::Inactive);
                    let actives = grid.neighbors_values80(&c).into_iter()
                        .filter(|v| **v == Cell::Active)
                        .count();

                    let new_state = match *state {
                        Cell::Active if actives == 2 || actives == 3 => Cell::Active,
                        Cell::Inactive if actives == 3 => Cell::Active,
                        _ => Cell::Inactive
                    };

                    updates.push((c, new_state));
                }
            }
        }
    }

    for (c, state) in updates {
        match state {
            Cell::Active => grid.set_coord(c, state),
            Cell::Inactive => grid.remove(&c)
        }
    }
}
