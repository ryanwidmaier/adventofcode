use super::util::coord2::Coord2;
use super::util::sparse_grid::SparseGrid;
use std::fmt::{Display, Formatter, Result};
use crate::util::coord2::Direction;

#[derive(PartialEq, Eq)]
enum Cell {
    Floor,
    EmptySeat,
    OccupiedSeat
}

impl Cell {
    fn from(val: char) -> Cell {
        match val {
            '.' => Cell::Floor,
            'L' => Cell::EmptySeat,
            '#' => Cell::OccupiedSeat,
            _ => panic!("Unknown char: {}", val)
        }
    }
}

impl Display for Cell {
    fn fmt(&self, f: &mut Formatter) -> Result {
        match self {
            Cell::Floor => write!(f, "{}", '.'),
            Cell::EmptySeat => write!(f, "{}", 'L'),
            Cell::OccupiedSeat => write!(f, "{}", '#')
        }
    }
}

fn parse(lines: &Vec<String>) -> SparseGrid<Cell> {
    let mut grid: SparseGrid<Cell> = SparseGrid::new();
    for (y, line) in lines.iter().enumerate() {
        for (x, ch) in line.chars().enumerate() {
            let c = Cell::from(ch);
            grid.set(x as i32, y as i32, c);
        }
    }

    grid
}


pub fn part1(lines: &Vec<String>) {
    let mut grid = parse(lines);
    let mut updated = 1;

    while updated > 0 {
        updated = do_updates(&mut grid);
        // println!();
        // println!("  Step {}", t);
        // grid.print();

        if updated == 0 {
            let occupied = grid
                .values()
                .filter(|v| **v == Cell::OccupiedSeat)
                .count();

            println!("Part1: Done after {} steps, occupied={}", t, occupied);
            break;
        }

    }
}

fn do_updates(grid: &mut SparseGrid<Cell>) -> usize {
    let mut updates: Vec<(Coord2, Cell)> = vec![];

    for y in grid.y_range() {
        for x in grid.x_range() {
            let c = Coord2{x, y};

            // Figure out how many neighbors are occupied
            let neighbors = grid.neighbors_values8(&c);
            let occupied = neighbors.into_iter()
                .filter(|n| **n == Cell::OccupiedSeat )
                .count();


            // Determine the update, if any
            let new_v = match grid.get_coord(&c) {
                Some(Cell::EmptySeat) if occupied == 0 => Some(Cell::OccupiedSeat),
                Some(Cell::OccupiedSeat) if occupied >= 4 => Some(Cell::EmptySeat),
                _ => None
            };

            // Put updates in update list
            match new_v {
                Some(v) => updates.push((c, v)),
                None => ()
            };
        }
    }

    // Now apply all the updates
    let count = updates.len();
    println!("Count {}", count);
    for (c, v) in updates {
        grid.set_coord(c, v);
    }
    count
}

pub fn part2(lines: &Vec<String>) {
    let mut grid = parse(lines);

    for t in 0..100000 {
        let updated = do_updates2(&mut grid);
        // println!();
        // println!("  Step {}", t);
        // grid.print();

        if updated == 0 {
            let occupied = grid
                .values()
                .filter(|v| **v == Cell::OccupiedSeat)
                .count();

            println!("Part2: Done after {} steps, occupied={}", t, occupied);
            break;
        }

    }
}

fn do_updates2(grid: &mut SparseGrid<Cell>) -> usize {
    let mut updates: Vec<(Coord2, Cell)> = vec![];
    let offsets = Direction::coords8();


    for y in grid.y_range() {
        for x in grid.x_range() {
            let c = Coord2{x, y};

            // Figure out how many neighbors are occupied
            let occupied = offsets.iter()
                .map(|o| first_seat(grid, &c, &o))
                .filter(|v|*v == Cell::OccupiedSeat)
                .count();

            // Determine the update, if any
            let new_v = match grid.get_coord(&c) {
                Some(Cell::EmptySeat) if occupied == 0 => Some(Cell::OccupiedSeat),
                Some(Cell::OccupiedSeat) if occupied >= 5 => Some(Cell::EmptySeat),
                _ => None
            };

            // Put updates in update list
            match new_v {
                Some(v) => updates.push((c, v)),
                None => ()
            };
        }
    }

    // Now apply all the updates
    let count = updates.len();
    println!("Count {}", count);
    for (c, v) in updates {
        grid.set_coord(c, v);
    }
    count
}

fn first_seat(grid: &SparseGrid<Cell>, start: &Coord2, offset: &Coord2) -> Cell {
    let mut check = Coord2{x: start.x, y: start.y };
    loop {
        check.add_assign_ref(offset);

        match grid.get_coord(&check) {
            Some(Cell::OccupiedSeat) => return Cell::OccupiedSeat,
            Some(Cell::EmptySeat) => return Cell::EmptySeat,
            Some(Cell::Floor) => (),
            None => return Cell::Floor
        }
    }
}
