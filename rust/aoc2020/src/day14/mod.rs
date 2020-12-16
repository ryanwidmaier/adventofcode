use regex::Regex;
use std::collections::HashMap;

enum Line {
    Mask(String),
    Set(u64, u64)
}

impl Line {
    fn parse(line: &str) -> Line {
        let re1 = Regex::new(r"^mask = ([X01]+)$").unwrap();
        let re2 = Regex::new(r"^mem\[(\d+)\] = (\d+)$").unwrap();

        // Handle mask lines
        if let Some(groups) = re1.captures(line) {
            let mask = groups.get(1).unwrap().as_str();
            // u64::from_str_radix(mask, 2).unwrap()
            return Line::Mask(String::from(mask));
        }

        // Handle set lines
        if let Some(groups) = re2.captures(line) {
            return Line::Set(
                groups.get(1).unwrap().as_str().parse().unwrap(),
                groups.get(2).unwrap().as_str().parse().unwrap(),
            );
        }

        panic!("Unexpected line");
    }
}

fn parse(lines: &Vec<String>) -> Vec<Line> {
    let mut result = Vec::new();
    for line in lines {
        result.push(Line::parse(line));
    }
    result
}

pub fn part1(lines: &Vec<String>) {
    let instructions = parse(lines);
    let mut memory: HashMap<u64, u64> = HashMap::new();

    // Need two masks so we can handle 3 states
    let mut mask1 = 0_u64;
    let mut mask2 = 0_u64;

    for line in instructions {
        match line {
            Line::Mask(mask) => {
                let mask1_str = mask.replace("1", "0").replace("X", "1");
                let mask2_str = mask.replace("X", "0");

                mask1 = u64::from_str_radix(&mask1_str, 2)
                    .expect("Failed parsing mask1");
                mask2 = u64::from_str_radix(&mask2_str, 2)
                    .expect("Failed parsing mask2");
            },
            Line::Set(addr, value) => {
                let update = memory.entry(addr).or_insert(0);
                *update = (value & mask1) | mask2;
            }
        }
    }

    let answer: u64 = memory.values().sum();
    println!("Part1: {}", answer);

    // println!("{:?}", memory);
}

pub fn part2(lines: &Vec<String>) {
    let instructions = parse(lines);
    let mut memory: HashMap<u64, u64> = HashMap::new();

    // Need two masks so we can handle 3 states
    let mut mask1 = 0_u64;
    let mut mask2: Vec<u64> = Vec::new();

    for line in instructions {
        match line {
            Line::Mask(mask) => {
                // First mask will 0 out positions where X is in the mask
                // Second mask will OR in combinations of X's (and have 1's set)
                let mask1_str = mask.replace("0", "1")
                    .replace("X", "0");
                mask1 = u64::from_str_radix(&mask1_str, 2)
                    .expect("Failed parsing mask1");

                mask2 = create_mask2s(&mask);
            },
            Line::Set(addr, value) => {
                for m2 in &mask2 {
                    let update_addr = (addr & mask1) | *m2;
                    memory.insert(update_addr, value);
                }
            }
        }
    }

    let answer: u64 = memory.values().sum();
    println!("Part1: {}", answer);

    // println!("{:?}", memory);
}

// Create masks of:
//   0 -> 0
//   1 -> 1
//   X -> [0,1]
// which will or against he result of mask 1.
fn create_mask2s(mask: &str) -> Vec<u64> {
    let mut ret = vec![];

    // Second masks will OR in the 1's for all combinations of X spots
    let xs: Vec<_> = mask.match_indices("X").collect();

    // Loop through all the level 2 m1sk values (for X substitutions)
    for bin_val in 0..2_u64.pow(xs.len() as u32) {
        let mut bin_str = format!("{:0width$b}", bin_val, width = xs.len());
        let mut mask2_str = String::from(mask);

        // Loop through each X, replacing with a bit
        while bin_str.len() > 0 {
            let x = bin_str.pop().unwrap();
            let bit = String::from(x);
            mask2_str = mask2_str.replacen('X', &bit, 1);
        }

        // Store mask as a numeric
        let mask2_num = u64::from_str_radix(&mask2_str, 2).unwrap();
        ret.push(mask2_num);
    }

    ret
}