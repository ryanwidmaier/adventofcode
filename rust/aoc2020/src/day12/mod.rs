use crate::util::robot::Robot;
use crate::util::coord2::{Coord2,Direction};

fn parse(lines: &Vec<String>) -> Vec<(char, i32)> {
    let mut v= vec![];
    for line in lines {
        let dir = line.chars().next().unwrap();
        let amount: i32 = line[1..].parse()
            .expect("Failed to parse");
        v.push((dir, amount));
    }
    v
}

pub fn part1(lines: &Vec<String>) {
    let moves = parse(lines);
    let mut robot = Robot::new(Direction::East);

    for mv in &moves {
        match mv {
            ('N', amt) => robot.shift(Direction::North, *amt),
            ('E', amt) => robot.shift(Direction::East, *amt),
            ('W', amt) => robot.shift(Direction::West, *amt),
            ('S', amt) => robot.shift(Direction::South, *amt),
            ('F', amt) => robot.forward(*amt),
            ('R', amt) => robot.rotate(*amt / 90),
            ('L', amt) => robot.rotate(*amt / 90 * -1),
            _ => ()
        }
        println!("{} - {} after {} {}", robot.position, robot.direction, mv.0, mv.1)
    }
    println!("Part1: {}", robot.manhattan(&Coord2{x:0, y:0}))
}

pub fn part2(lines: &Vec<String>) {
    let moves = parse(lines);
    let mut robot = Robot::new(Direction::East);
    let mut waypoint = Robot::new(Direction::East);
    waypoint.shift(Direction::East, 10);
    waypoint.shift(Direction::North, 1);
    println!("{} {:3}, Robot {}, Waypoint {}", "-", 0, robot.position, waypoint.position);

    for mv in &moves {
        match mv {
            ('N', amt) => waypoint.shift(Direction::North, *amt),
            ('E', amt) => waypoint.shift(Direction::East, *amt),
            ('W', amt) => waypoint.shift(Direction::West, *amt),
            ('S', amt) => waypoint.shift(Direction::South, *amt),
            ('R', amt) => {
                let new_pos = rotate(&waypoint.position, &robot.position, *amt);
                waypoint.move_to(&new_pos);
            },
            ('L', amt) => {
                let new_pos = rotate(&waypoint.position, &robot.position, *amt * -1);
                waypoint.move_to(&new_pos);
            },
            ('F', amt) => {
                let offset = (&waypoint.position - &robot.position) * *amt;
                robot.shift_coord(&offset);
                waypoint.shift_coord(&offset);
            },
            _ => ()
        }
        let offset = &waypoint.position - &robot.position;
        println!("{} {:3}, Robot {}, Waypoint {}                {}", mv.0, mv.1, robot.position, waypoint.position, offset);
    }
    println!("Part1: {}", robot.manhattan(&Coord2{x:0, y:0}));
}

fn rotate(target: &Coord2, origin: &Coord2, degrees: i32) -> Coord2 {
    let dist = target.distance(origin);
    let angle = (target - origin).angle_radian().to_degrees();
    let new_angle = angle + (degrees as f32);

    let new_offset = Coord2::from_polar(new_angle.to_radians(), dist);
    origin + &new_offset
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rotate_forward() {
        let origin = Coord2{x:0, y:0};
        let target = Coord2{x:3, y:-1};

        let actual = rotate(&target, &origin, 90);
        assert_eq!(actual, Coord2{x:1, y:3});

        let actual = rotate(&target, &origin, 180);
        assert_eq!(actual, Coord2{x:-3, y:1});

        let actual = rotate(&target, &origin, 270);
        assert_eq!(actual, Coord2{x:-1, y:-3});
    }

    #[test]
    fn test_rotate_full_loop() {
        let origin = Coord2{x:0, y:0};
        let target = Coord2{x:3, y:-1};

        let a = rotate(&target, &origin, 90);
        assert_eq!(a, Coord2{x:1, y:3});
        let b = rotate(&a, &origin, 90);
        assert_eq!(b, Coord2{x:-3, y:1});
        let c = rotate(&b, &origin, 90);
        assert_eq!(c, Coord2{x:-1, y:-3});
        let d = rotate(&c, &origin, 90);
        assert_eq!(d, target);
    }

    #[test]
    fn test_bad_rotate() {
        let origin = Coord2{x:0, y:0};
        let target = Coord2{x:-3, y:1};

        let actual = rotate(&target, &origin, 90);
        assert_eq!(actual, Coord2{x:-1, y:-3})
    }

    #[test]
    fn test_rotate_backward() {
        let origin = Coord2{x:0, y:0};
        let target = Coord2{x:3, y:-1};

        let actual = rotate(&target, &origin, -90);
        assert_eq!(actual, Coord2{x:-1, y:-3});

        let actual = rotate(&target, &origin, -180);
        assert_eq!(actual, Coord2{x:-3, y:1});

        let actual = rotate(&target, &origin, -270);
        assert_eq!(actual, Coord2{x:1, y:3});
    }
}