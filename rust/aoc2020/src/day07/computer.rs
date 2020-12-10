
use std::collections::HashSet;
use super::command;
use crate::day07::command::Command;

pub struct Computer {
    program: Vec<command::Command>,
    log: bool
}

impl Computer {
    pub fn new(prog: Vec<Command>, log: bool) -> Computer {
        Computer {
            program: prog,
            log: log
        }
    }

    pub fn run(&self) -> bool {
        let mut executed = HashSet::new();
        let mut pc: usize = 0;
        let mut accum: i32 = 0;

        while pc < self.program.len() {
            if executed.contains(&pc) {
                println!("Repeated on {}, accum={}", pc, accum);
                return false;
            }

            executed.insert(pc);

            // Run the next instruction
            let cmd = &self.program[pc];
            let step = self.exec(cmd, &mut accum);
            self.log(cmd, pc, accum);

            // Adjust program counter
            pc = if step.is_negative() {
                pc - step.wrapping_abs() as u32 as usize
            } else {
                pc + step as usize
            }
        }

        println!("Finished: accum={}", accum);
        return true;
    }

    fn exec(&self, cmd: &Command, accum: &mut i32) -> i32 {
        match cmd {
            Command::Jump(amt) => *amt,
            Command::Acc(amt) => {
                *accum = *accum + amt;
                1
            }
            Command::Noop(_) => 1
        }
    }

    fn log(&self, cmd: &Command, pc: usize, accum: i32) {
        if self.log {
            println!("{:>4}: {:20} accum={}", pc, cmd, accum);
        }
    }
}

