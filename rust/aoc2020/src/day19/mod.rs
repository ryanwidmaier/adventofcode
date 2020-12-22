
enum Entry {
    Rule(usize),
    Literal(char)
}

type CFGPattern = Vec<Entry>;


struct Node {
    patterns: Vec<Vec<Entry>>
}


fn parse(lines: &Vec<String>)  -> (Vec<Node>, Vec<String>) {
    let mut inputs = Vec::new();
    let mut tree: Vec<Node> = Vec::new();
    for i in 0..200 {
        tree.push(Node { patterns: Vec::new() })
    }

    for line in lines {
        if line.contains(":") {
            build_node(&mut tree, line);
        }
        else if line.len() > 0 {
            inputs.push(line.clone());
        }
    }

    (tree, inputs)
}

fn build_node(tree: &mut Vec<Node>, line: &String) {
    let tokens: Vec<_> = line.split_whitespace().collect();
    let cfg_idx: usize = tokens[0][..tokens[0].len()-1].parse().unwrap();

    let node: &mut Node = &mut tree[cfg_idx];
    let patterns = &mut node.patterns;
    patterns.push(Vec::new());

    for i in 1..tokens.len() {
        // Start a new pattern for this rule
        if tokens[i] == "|" {
            patterns.push(Vec::new());
        }
        // append a literal to this rule
        else if tokens[i].contains("\"") {
            let literal_val = tokens[i].chars().nth(1).unwrap();
            let literal = Entry::Literal(literal_val);
            patterns.last_mut().unwrap().push(literal);
        }
        // Append a rule ref to this rule
        else {
            let rule_num = tokens[i].parse().unwrap();
            let rule = Entry::Rule(rule_num);
            patterns.last_mut().unwrap().push(rule);
        }
    }
}

fn to_chomsky(tree: &Vec<Node>) -> Vec<Node> {
    let result = Vec::new();
    // Just need to reduce to 2 rules per group
    for node in tree {
        for group in &node.patterns {
            let last = group.last().unwrap();
            for i in
        }
    }
    result
}

pub fn part1(lines: &Vec<String>) {
    let (cfg, inputs) = parse(lines);

    for line in lines {

    }
}

// Validate whether a string matches the CFG
fn validate(tree: &Vec<Node>, line: &str) -> bool {
    let mut rules_stack = vec![0];
    validate_recursive(tree, line)
}

// // Recursive validation. Returns # chars consumed.
// // rules stack, top is left most rule to match
// fn validate_recursive(tree: &Vec<Node>, line: &str, rule: usize) -> bool {
//     if line.is_empty() && rules.is_empty() {
//         return true;
//     }
//
//     // Going to try to resolve the first rule + the rest (recursive)
//     // Resolve the first (left most) rule from stack
//     let left_rule: usize = rules_stack.pop().expected("Stack is empty!");
//
//     // 0 =
//     //    pattern 1 -> 4 1 5
//     //       return is_valid(s, 4 1 5)
//     //
//     // 4 = a
//
//
//     // For each pattern group, check for full match
//     for patterns in &tree[left_rule] {
//         rules_stack.extend(patterns.iter().rev());
//
//         // Match if all clauses match
//         let matches = patterns.iter().map(|v| {
//             validate_recursive()
//         }).all();
//
//     }
//
//     let matches = match left_rule {
//         Entry::Rule(rule) => {
//             rules_stack.push(rule);
//             validate_recursive(tree, line, rules_stack)
//         },
//         Entry::Literal(ch) => {
//             let remaining = &line[..line.len()];
//             line.starts_with(ch) && validate_recursive(tree, remaining, rules_stack)
//         }
//     };
//
//     matches
// }

fn validate3(tree: &Vec<Node>, line: &str) -> bool {
    let possibles: Vec<usize> = vec![0];

    for ch in line.chars() {

    }
    false
}

fn expand(possibles: &Vec<usize>, letter: ch) {

}


pub fn part2(lines: &Vec<String>) {

}

