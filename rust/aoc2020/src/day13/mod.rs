use itertools::Itertools;

enum Route {
    Bus(u32),
    X
}


fn parse(lines: &Vec<String>)  -> (u32, Vec<Route>) {
    let first = &lines[0];
    let second = &lines[1];

    let departure = first.parse().unwrap();
    let schedule = second.split(",")
        .into_iter()
        .map(|b| match b {
            "x" => Route::X,
            i => Route::Bus(i.parse().unwrap())
        });

    (departure, schedule.collect())
}

pub fn part1(lines: &Vec<String>) {
    let (departure, schedule) = parse(lines);

    let mut bus = 0;
    let mut min = u32::max_value();

    for route in schedule {
        match route {
            Route::Bus(id) => {
                let arrive = ((departure / id) + 1) * id - departure;

                if arrive < min {
                    min = arrive;
                    bus = id;
                }
            },
            Route::X => ()
        }
    }

    println!("Part 1: Bus={}, Arrive={}, Answer={}", bus, min, min * bus);
}

pub fn part2(lines: &Vec<String>) {
    let (departure, schedule) = parse(lines);
    let mut remainders = vec![];
    let mut modulii = vec![];

    for (idx, route) in schedule.into_iter().enumerate() {
        match route {
            Route::Bus(id) => {
                let bus = id as i64;
                let pos = idx as i64;
                remainders.push((bus - pos) % bus);
                modulii.push(id as i64);
            },
            Route::X => ()
        }
    }

    println!("{}", remainders.iter().join(", "));
    println!("{}", modulii.iter().join(", "));

    let answer = chinese_remainder(&remainders, &modulii);
    println!("part 2: {}", answer.unwrap());
}

fn egcd(a: i64, b: i64) -> (i64, i64, i64) {
    if a == 0 {
        (b, 0, 1)
    } else {
        let (g, x, y) = egcd(b % a, a);
        (g, y - (b / a) * x, x)
    }
}

fn mod_inv(x: i64, n: i64) -> Option<i64> {
    let (g, x, _) = egcd(x, n);
    if g == 1 {
        Some((x % n + n) % n)
    } else {
        None
    }
}

fn chinese_remainder(residues: &[i64], modulii: &[i64]) -> Option<i64> {
    let prod = modulii.iter().product::<i64>();

    let mut sum = 0;

    for (&residue, &modulus) in residues.iter().zip(modulii) {
        let p = prod / modulus;
        sum += residue * mod_inv(p, modulus)? * p
    }

    Some(sum % prod)
}