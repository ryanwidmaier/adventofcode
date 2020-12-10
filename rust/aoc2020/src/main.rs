#[macro_use] extern crate lazy_static;
use std::fs::File;
use std::io::{self, BufRead};

mod day07;
mod day08;

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
        _ => {}
    }
}
