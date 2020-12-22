use std::fmt::{Display, Formatter, Result};


#[derive(PartialEq, Eq, Debug)]
enum Op {
    Add,
    Multiply,
    LeftParen,
    RightParen,
    Value(i64)
}

impl Op {
    fn precedence(&self) -> i32 {
        match self {
            &Op::Add => 2,
            &Op::Multiply => 1,
            &Op::LeftParen => 0,
            &Op::RightParen => 0,
            &Op::Value(_) => 0
        }
    }

    fn from(s: &str) -> Op {
        match s {
            "*" => Op::Multiply,
            "+" => Op::Add,
            "(" => Op::LeftParen,
            ")" => Op::RightParen,
            v => Op::Value(v.parse().unwrap())
        }
    }
}

impl Display for Op {
    fn fmt(&self, f: &mut Formatter) -> Result {
        match self {
            Op::Add => write!(f, "+"),
            Op::Multiply => write!(f, "*"),
            Op::LeftParen => write!(f, "("),
            Op::RightParen => write!(f, ")"),
            Op::Value(v) => write!(f, "{}", v)
        }
    }
}

fn eval(line: &String) -> i64 {
    // lazy man way to make it easier to tokenize
    println!("{}", line);
    let line_ws = line.replace('(', "( ").replace(')', " )");
    let tokens = line_ws.split_whitespace();

    let mut ops_stack = Vec::new();
    let mut val_stack: Vec<i64> = Vec::new();
    for token in tokens.rev() {
        println!("Token: {},   {:?}     {:?}", token, ops_stack, val_stack);
        match token {
            "*" => ops_stack.push(Op::Multiply),
            "+" => ops_stack.push(Op::Add),
            ")" => ops_stack.push(Op::RightParen),

            // On close, resolve back to the last open
            "(" => resolve(&mut ops_stack, &mut val_stack),

            // Anything else is a number
            rhs_str => val_stack.push(rhs_str.parse().unwrap()),
        }
    }

    resolve(&mut ops_stack, &mut val_stack);

    val_stack.pop().unwrap()
}

fn resolve(ops_stack: &mut Vec<Op>, val_stack: &mut Vec<i64>) {
    let mut op = ops_stack.pop();
    while op != Some(Op::RightParen) && op != None {
        let lhs = val_stack.pop().unwrap();
        let rhs = val_stack.pop().unwrap();

        match &op {
            &Some(Op::Add) => val_stack.push(lhs + rhs),
            &Some(Op::Multiply) => val_stack.push(lhs * rhs),
            _ => ()
        }
        op = ops_stack.pop();
    }
}

pub fn part1(lines: &Vec<String>) {
    let answer: i64 = lines.iter()
        .map(|l| eval(l))
        .sum();
    println!("Part 1: {}", answer);
}

pub fn part2(lines: &Vec<String>) {
    eval2(&String::from("2 * 3 + (4 * 5)"));
    let answer: i64 = lines.iter()
        .map(|l| {
            let v = eval2(l);
            println!("{}  =  {}", v, l);
            v
        })
        .sum();
    println!("Part 2: {}", answer);
}

fn eval2(line: &String) -> i64 {
    // lazy man way to make it easier to tokenize
    let line_ws = line.replace('(', "( ").replace(')', " )");
    let tokens = line_ws.split_whitespace();

    // 9 + (9 * 5 + 8 * 8 + 6) * 8
    let mut op_stack: Vec<Op> = Vec::new();
    let mut output = Vec::new();
    for token in tokens {
        match token {
            "*" | "+" => {
                let new_op = Op::from(token);
                let mut top = op_stack.last().map_or(0, |v| v.precedence());

                while new_op.precedence() <= top {
                    output.push(op_stack.pop().unwrap());

                    top = op_stack.last().map_or(0, |v| v.precedence());
                }
                op_stack.push(new_op);
            },
            "(" => op_stack.push(Op::LeftParen),
            ")" => {
                let mut op = op_stack.pop();
                while op != Some(Op::LeftParen) {
                    output.push(op.unwrap());
                    op = op_stack.pop();
                }
            },
            val => output.push(Op::from(val))
        }
    }

    // println!("{:?}", &op_stack);
    while !op_stack.is_empty() {
        output.push(op_stack.pop().unwrap());
    }

    // println!("{:?}", &output);

    // Now eval postfix
    let mut stack: Vec<Op> = Vec::new();
    for token in output {
        match token {
            Op::Multiply => {
                let lhs = stack.pop().unwrap();
                let rhs = stack.pop().unwrap();

                match (lhs, rhs) {
                    (Op::Value(l), Op::Value(r)) => stack.push(Op::Value(l * r)),
                    _ => ()
                }
            },
            Op::Add => {
                let lhs = stack.pop().unwrap();
                let rhs = stack.pop().unwrap();

                match (lhs, rhs) {
                    (Op::Value(l), Op::Value(r)) => stack.push(Op::Value(l + r)),
                    _ => ()
                }
            },
            Op::Value(v) => stack.push(Op::Value(v)),
            _ => ()
        }
    }
    match stack.last() {
        Some(Op::Value(v)) => *v,
        _ => panic!("aaah")
    }
}

fn prec(op: &str) -> i32 {
    match op {
        "+" => 3,
        "*" => 2,
        _ => 0
    }
}
