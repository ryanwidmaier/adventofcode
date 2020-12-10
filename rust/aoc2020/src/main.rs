#[macro_use] extern crate lazy_static;
use std::fs::File;
use std::io::{self, BufRead};

mod day07;

fn main() {
    println!("Hello, world!");

    let base = "/Users/rwidmaier/repos/misc/adventofcode/rust/aoc2020/src";
    let fname = "day07/input.txt";
    let path = format!("{}/{}", base, fname);

    let f = File::open(&path)
        .expect(&*format!("Unable to open file: {}", &path));
    let lines = io::BufReader::new(f).lines();

    let mut v = Vec::new();
    for line in lines {
        if let Ok(l) = line {
            v.push(l);
        }
    }

    day07::part1(&v);
    day07::part2(&v);
}
