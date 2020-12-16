#[macro_use] extern crate lazy_static;
use std::fs::File;
use std::io::{self, BufRead};

mod util;
mod day07;
mod day08;
mod day10;
mod day11;
mod day12;
mod day13;
mod day14;
mod day15;
mod day16;
mod day17;
mod day18;
mod day19;
mod day20;
mod day21;
mod day22;
mod day23;
mod day24;
mod day25;

fn main() {
    let day_str= std::env::args().nth(1).expect("Day required.");
    let fname = std::env::args().nth(2).expect("File required.");
    let day: i32 = day_str.parse().unwrap();

    let base = "/Users/rwidmaier/repos/misc/adventofcode/rust/aoc2020/src";
    let path = format!("{}/day{:02}/{}", base, day, fname);

    let f = File::open(&path)
        .expect(&*format!("Unable to open file: {}", &path));
    let lines = io::BufReader::new(f).lines();

    let mut v = Vec::new();
    for line in lines {
        if let Ok(l) = line {
            v.push(l);
        }
    }

    match day {
        7 => {
            day07::part1(&v);
            day07::part2(&v);
        },
        8 => {
            day08::part1(&v);
            day08::part2(&v);
        },
        10 => {
            day10::part1(&v);
            day10::part2(&v);
        },
        11 => {
            day11::part1(&v);
            day11::part2(&v);
        },
        12 => {
            day12::part1(&v);
            day12::part2(&v);
        },
        13 => {
            day13::part1(&v);
            day13::part2(&v);
        },
        14 => {
            day14::part1(&v);
            day14::part2(&v);
        },
        15 => {
            day15::part1(&v);
            day15::part2(&v);
        },
        16 => {
            day16::part1(&v);
            day16::part2(&v);
        },
        17 => {
            day17::part1(&v);
            day17::part2(&v);
        },
        18 => {
            day18::part1(&v);
            day18::part2(&v);
        },
        19 => {
            day19::part1(&v);
            day19::part2(&v);
        },
        20 => {
            day20::part1(&v);
            day20::part2(&v);
        },
        21 => {
            day21::part1(&v);
            day21::part2(&v);
        },
        22 => {
            day22::part1(&v);
            day22::part2(&v);
        },
        23 => {
            day23::part1(&v);
            day23::part2(&v);
        },
        24 => {
            day24::part1(&v);
            day24::part2(&v);
        },
        25 => {
            day25::part1(&v);
            day25::part2(&v);
        },

        _ => {}
    }
}
