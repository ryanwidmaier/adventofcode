

fn parse(lines: &Vec<String>) -> Vec<i32> {
    let mut v: Vec<i32> = vec![];
    for line in lines {
        v.push(line.parse().unwrap())
    }
    v.sort();
    v
}

pub fn part1(lines: &Vec<String>) {
    let adapters = parse(lines);
    let mut ones = 0;
    let mut threes = 1;  // 1 for your device

    for (idx, adapter) in adapters.iter().enumerate() {
        let prev = if idx > 0 { adapters[idx-1] } else { 0 };
        let diff = adapter - prev;
        match diff {
            1 => ones += 1,
            3 => threes += 1,
            _ => {}
        }
    }

    println!("Part1: 1={}, 3={}, mult={}", ones, threes, ones * threes);
}

pub fn part2(lines: &Vec<String>) {
    let mut adapters = parse(lines);
    // Add start and end, and reverse
    adapters.insert(0, 0);
    let mut sums: Vec<i64> = vec![0; adapters.len()];

    adapters.push(adapters.last().unwrap()+3);
    sums.push(1);

    const MAX_DIFF: i32 = 3;

    for (idx, adapter) in adapters.iter().enumerate().rev() {
        for idx2 in idx+1..adapters.len() {
            let next_adapter = adapters[idx2];
            if next_adapter - adapter > MAX_DIFF {
                println!("  next was {}", next_adapter);
                break;
            }
            println!("idx={:3}, idx2={:3}, adp1={:3}, adp2={:3}", idx, idx2, adapter, next_adapter);

            sums[idx] += sums[idx2];
            println!("  update: v[{}] = {}", idx, sums[idx]);
        }
    }

    let adapters_it: Vec<String> = adapters.iter().map(|x| format!("{:3}", x)).collect();
    let sums_it: Vec<String> = sums.iter().map(|x| format!("{:3}", x)).collect();

    // println!("");
    // println!("{}", adapters_it.join(", "));
    // println!("{}", sums_it.join(", "));
    // println!("");

    println!("Part 2: {}", sums[0]);
}
