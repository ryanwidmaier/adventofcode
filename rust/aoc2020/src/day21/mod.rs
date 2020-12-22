// use std::collections::{HashMap,HashSet};
// use std::iter::FromIterator;
// use regex::Regex;
// use itertools::Itertools;
//
//
// struct Line {
//     ingredients: Vec<String>,
//     allergens: Vec<String>
// }
//
//
//
// fn parse(lines: &Vec<String>)  -> Vec<Line> {
//     let result = Vec::new();
//     for line in lines {
//         let line.split(" (")
//     }
//     result
// }
//
// pub fn part1(lines: &Vec<String>) {
//     let data = parse(lines);
//
//     let errors: i32 = data.nearby.iter()
//         .map(|t| t.error_rate(&data.rules))
//         .sum();
//
//     println!("Part 1: {}", errors);
// }
//
//
// pub fn part2(lines: &Vec<String>) {
//     let data = parse(lines);
//
//     // Create a grid of field names x columns.  True means possible match, False means not possible
//     let mut grid = Vec::new();
//     let size = data.ticket.fields.len();
//     for _ in 0..size {
//         grid.push(vec![true; size]);
//     }
//
//     // Create easy lookup of fields to idx
//     let indices_to_fields = HashMap::from_iter(
//         data.rules.keys()
//             .sorted()
//             .enumerate()
//     );
//
//     // Loop through all the tickets, clearing cells where field can't be column
//     for ticket in data.nearby.iter().chain(vec![&data.ticket].into_iter()) {
//         // Throw out invalids
//         if !ticket.is_valid(&data.rules) {
//             continue;
//         }
//
//         for (col_idx, v) in ticket.fields.iter().enumerate() {
//             let candidates = Ticket::find_candiates(*v, &data.rules);
//             println!("{} -> {:?}", v, &candidates);
//             for (field_idx, field) in &indices_to_fields {
//                 if !candidates.contains(*field) {
//                     grid[*field_idx][col_idx] = false;
//                 }
//             }
//         }
//     }
//
//     println!("Initial");
//     print_grid(&grid, &indices_to_fields);
//
//     // Now we can use our grid to repeatedly clear cells until only 1 true remains in each
//     // column and row.
//     let mut known: HashMap<String, usize> = HashMap::new();
//     let mut pass = 1;
//     while known.len() < size {
//         let before = count(&grid);
//
//         // Do row wise checking
//         for field_idx in 0..size {
//             match check_line(&grid, field_idx, field_idx+1, 0, size) {
//                 Some(found) => update_found(&mut grid, found, &mut known, &indices_to_fields),
//                 None => ()
//             }
//         }
//         // Do column wise checking
//         for col_idx in 0..size {
//             match check_line(&grid, 0, size, col_idx, col_idx+1) {
//                 Some(found) => update_found(&mut grid, found, &mut known, &indices_to_fields),
//                 None => ()
//             }
//         }
//
//         let after = count(&grid);
//         println!();
//         println!("Pass {}, {} cells remaining", pass, after);
//         print_grid(&grid, &indices_to_fields);
//         pass += 1;
//         if before == after {
//             println!("No change!");
//             break;
//         }
//     }
//
//     let answer: i64 = known.iter()
//         .filter(|(f, i)| (*f).starts_with("departure"))
//         .inspect(|(f, i)| println!("{} -> {}", *f, i))
//         .map(|(f, i)| *(&data.ticket.fields[*i]) as i64)
//         .product();
//     println!("Part2: {}", answer);
// }
//
// // Count how many posibles are left
// fn count(grid: &Vec<Vec<bool>>) -> usize {
//     grid.iter().map(|v| {
//         v.iter().filter(|vv| **vv).count()
//     }).sum()
// }
//
// /// Check 1 row or column, to see if only 1 possible answer remains. If so return it's coord
// fn check_line(grid: &Vec<Vec<bool>>, field_start: usize, field_stop: usize,
//               col_start: usize, col_stop: usize) -> Option<(usize, usize)> {
//
//     let mut count = 0;
//     let mut found = None;
//     for field_idx in field_start..field_stop {
//         for col_idx in col_start..col_stop {
//             if grid[field_idx][col_idx] {
//                 count += 1;
//                 if count > 1 {
//                     return None;
//                 }
//                 found = Some((field_idx, col_idx))
//             }
//         }
//     }
//
//     if count == 1 {
//         found
//     }
//     else {
//         None
//     }
// }
//
// /// Clears grid squares for a found position, and updates our known state.
// fn update_found(grid: &mut Vec<Vec<bool>>,
//                 found: (usize, usize),
//                 known: &mut HashMap<String, usize>,
//                 indices_to_fields: &HashMap<usize, &String>) {
//
//     // Figure out what field it was
//     let field = indices_to_fields[&found.0];
//     if known.contains_key(field) {
//         return;
//     }
//
//     known.insert(String::from(field), found.1);
//     println!("{}: Found {} ({}) -> Col {}", known.len(), field, found.0, found.1);
//
//     // clear all the cells on the grid inline w/ the found pos.
//     let size = grid.len();
//     for field_idx in 0..size {
//         if field_idx != found.0 {
//             grid[field_idx][found.1] = false;
//         }
//     }
//     for col_idx in 0..size {
//         if col_idx != found.1 {
//             grid[found.0][col_idx] = false;
//         }
//     }
//
// }
//
// fn print_grid(grid: &Vec<Vec<bool>>, indices_to_fields: &HashMap<usize, &String>) {
//     let size = grid.len();
//     let mut header = String::new();
//     for col_idx in 0..size {
//         header += format!("{:2}", col_idx).as_str();
//     }
//     println!("{:20} {}", "", header);
//
//     for field_idx in 0..size {
//         let mut line = String::new();
//         for col_idx in 0..size {
//             line += match grid[field_idx][col_idx] {
//                 true => " X",
//                 false => " ."
//             };
//         }
//
//         println!("{:20} {}", indices_to_fields[&field_idx], line);
//     }
// }
