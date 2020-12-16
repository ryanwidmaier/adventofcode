use std::collections::HashMap;

pub fn parse(lines: &Vec<String>)  -> Vec<u32> {
    let line = lines.first().unwrap();
    line.split(",").map(|x|x.parse().unwrap()).collect()
}

pub fn part1(lines: &Vec<String>) {
    // let initial = parse(lines);
    let initial: Vec<u32> = vec![16, 12, 1, 0, 15, 7, 11];
    run_for(&initial, 2020);
}

pub fn part2(_lines: &Vec<String>) {
    let initial: Vec<u32> = vec![16, 12, 1, 0, 15, 7, 11];
    run_for(&initial, 30000000);
}

fn run_for(initial: &Vec<u32>, last_turn: u32) {
    let mut numbers = HashMap::new();

    // Do the initial numbers
    for (turn, elf_says) in initial.iter().enumerate() {
        numbers.insert(*elf_says, turn as u32);
    }

    // Keep going
    let start = initial.len() as u32;
    let mut last = *initial.last().unwrap();

    for turn in start..last_turn {
        let elf_says = match numbers.get(&last) {
            Some(prev_turn) => turn - prev_turn - 1,
            None => 0_u32
        };

        numbers.insert(last, turn - 1);
        last = elf_says;

        if turn % 10000 == 0 {
            println!("Turn = {}", turn);
        }
    }

    println!("Turn {}: Elf Says={}", last_turn, last);
}