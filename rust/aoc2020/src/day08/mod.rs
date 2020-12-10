
fn parse(lines: &Vec<String>) -> Vec<i64> {
    let mut v: Vec<i64> = Vec::new();
    for line in lines {
        v.push(line.parse().unwrap());
    }
    v
}

pub fn part1(lines: &Vec<String>) {
    let input = parse(lines);
    let (answer, idx) = find_part1(&input);
    println!("Part 1: Invalid {}, {}", answer, idx);
}

pub fn find_part1(input: &Vec<i64>) -> (i64, usize) {
    let prev = 25;
    for curr in prev..input.len() {
        if !is_valid(&input, curr, prev) {
            return (input[curr], curr);
        }
    }

    (0, 0)
}

pub fn part2(lines: &Vec<String>) {
    let input = parse(lines);
    let (answer, answer_idx) = find_part1(&input);

    // Walk backwards, starting from the idx before the part1 answer
    for curr in (1..answer_idx).rev() {
        println!("Curr: {}", curr);

        // Sum values until they exactly match answer, or overshoot
        let mut sum = answer;
        let mut idx = curr;
        while sum > 0 {
            sum -= input[idx];
            println!(" {:>10} {:>10}", input[idx], sum);
            idx -= 1;
        }

        if sum == 0 {
            let elems = &input[idx+1..=curr];
            let elems_str: Vec<String> = elems.iter()
                .map(|x| x.to_string())
                .collect();

            println!("Found:");
            println!("{}, {}", idx+1, curr);
            println!("{}", elems_str.join(", "));

            let min_value: Option<&i64> = elems.iter().min();
            let max_value: Option<&i64> = elems.iter().max();

            println!("{} {}", min_value.unwrap(), max_value.unwrap());
            println!("{}", min_value.unwrap() + max_value.unwrap());
            return;
        }
    }
    println!("Part2: ")
}


pub fn is_valid(lines: &Vec<i64>, curr: usize, size: usize) -> bool {
    let start = curr - size;
    let range = &lines[start..curr];

    for j in range {
        for k in range {
            if j != k && j + k == lines[curr] {
                return true;
            }
        }
    }
    return false;
}