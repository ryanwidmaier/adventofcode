mod command;
mod computer;

use command::Command;
use computer::Computer;


fn parse(lines: &Vec<String>) -> Vec<Command> {
    let mut v: Vec<Command> = Vec::new();
    for line in lines {
        v.push(command::Command::parse(line));
    }
    v
}

pub fn part1(lines: &Vec<String>) {
    let prog = parse(lines);
    let c = Computer::new(prog, false);
    c.run();

    println!("Part1: ")
}

pub fn part2(lines: &Vec<String>) {
    let prog_len = parse(lines);

    // Try changing each command, one at a time
    for idx in 0..prog_len.len() {
        let mut prog = parse(lines);
        prog[idx] = match prog[idx] {
            Command::Jump(amt) => Command::Noop(amt),
            Command::Noop(amt) => Command::Jump(amt),
            Command::Acc(amt) => Command::Acc(amt)
        };

        let c = Computer::new(prog, false);
        let finished = c.run();
        if finished {
            println!("Finished after changing line {}", idx);
            return;
        }
    }

    println!("Part1: ")
}
