use regex::Regex;
use std::fmt;

pub enum Command {
    Jump(i32),
    Acc(i32),
    Noop(i32)
}
impl Command {
    // nop +0
    // acc +1
    // jmp +4
    pub fn parse(line: &str) -> Command {
        lazy_static! {
            static ref RE: Regex = Regex::new(r"(\w+) ([+\-])(\d+)").unwrap();
        }

        let groups = RE.captures(line)
            .expect(format!("Line doesn't match regex: {}", line).as_str());
        let sign = match &groups[2] {
            "-" => -1,
            "+" => 1,
            "" => 1,
            v => panic!("Unknown sign ({}): {}", v, line)
        };

        let param1raw = &groups[3];
        let param1: i32 = param1raw.parse()
            .expect(format!("Expected integer amount for line: {}", line).as_str());
        let param1 = param1 * sign;

        match &groups[1] {
            "jmp" => Command::Jump(param1),
            "acc" => Command::Acc(param1),
            "nop" => Command::Noop(param1),
            _ => panic!("Unknown command {}", line)
        }
    }
}
impl fmt::Display for Command {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Command::Jump(amt) => write!(f, "jmp {}", amt),
            Command::Acc(amt) => write!(f, "acc {}", amt),
            Command::Noop(amt) => write!(f, "nop {}", amt),
        }
    }
}
