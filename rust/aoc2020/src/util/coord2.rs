use std::ops;
use std::fmt;

#[derive(PartialEq, Eq, Debug, Hash, Copy, Clone)]
pub struct Coord2 {
    pub x: i32,
    pub y: i32
}

impl Default for Coord2 {
    fn default() -> Self {
        Coord2 {
            x: 0,
            y: 0
        }
    }
}

#[derive(Copy, Clone)]
pub enum Direction {
    North,
    NorthEast,
    East,
    SouthEast,
    South,
    SouthWest,
    West,
    NorthWest
}

impl Direction {
    pub fn coord(&self) -> Coord2 {
        match self {
            Direction::North => Coord2{x:0, y:-1},
            Direction::NorthEast => Coord2{x:1, y:-1},
            Direction::East => Coord2{x:1, y:0},
            Direction::SouthEast => Coord2{x:1, y:1},
            Direction::South => Coord2{x:0, y:1},
            Direction::SouthWest => Coord2{x:-1, y:1},
            Direction::West => Coord2{x:-1, y:0},
            Direction::NorthWest => Coord2{x:-1, y:-1},
        }
    }

    pub fn directions8() -> Vec<Direction> {
        vec![Direction::North, Direction::NorthEast, Direction::East,
             Direction::SouthEast, Direction::South, Direction::SouthWest,
             Direction::West, Direction::NorthWest]
    }

    pub fn coords8() -> Vec<Coord2> {
        Direction::directions8().
            into_iter().
            map(|d| d.coord()).
            collect()
    }

    pub fn directions4() -> Vec<Direction> {
        vec![Direction::North,
             Direction::East,
             Direction::South,
             Direction::West]
    }

    pub fn idx4(&self) -> usize {
        match self {
            Direction::North => 0,
            Direction::East => 1,
            Direction::South => 2,
            Direction::West => 3,
            _ => panic!("Unsupported cardinal direction!")
        }
    }

    pub fn from_idx4(idx: usize) -> Direction {
        match idx {
            0 => Direction::North,
            1 => Direction::East,
            2 => Direction::South,
            3 => Direction::West,
            _ => {
                panic!("Unsupported idx for direction4: {}", idx)
            }
        }
    }

    pub fn coords4() -> Vec<Coord2> {
        Direction::directions4().
            into_iter().
            map(|d| d.coord()).
            collect()
    }
}

impl fmt::Display for Direction {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Direction::North => write!(f, "{}", "N"),
            Direction::NorthEast => write!(f, "{}", "NE"),
            Direction::East => write!(f, "{}", "E"),
            Direction::SouthEast => write!(f, "{}", "SE"),
            Direction::South => write!(f, "{}", "S"),
            Direction::SouthWest => write!(f, "{}", "SW"),
            Direction::West => write!(f, "{}", "W"),
            Direction::NorthWest => write!(f, "{}", "NW")
        }
    }
}


impl Coord2 {
    pub fn add_assign_ref(&mut self, other: &Coord2) {
        self.x += other.x;
        self.y += other.y;
    }

    // Return all adjacent Coords (including diagonal)
    pub fn neighbors4(&self) -> Vec<Coord2> {
        vec![
            Coord2{x:self.x,   y:self.y-1},
            Coord2{x:self.x-1, y:self.y},
            Coord2{x:self.x+1, y:self.y},
            Coord2{x:self.x,   y:self.y+1},
        ]
    }

    // Return all adjacent Coords (including diagonal)
    pub fn neighbors8(&self) -> Vec<Coord2> {
        vec![
            Coord2{x:self.x-1, y:self.y-1},
            Coord2{x:self.x,   y:self.y-1},
            Coord2{x:self.x+1, y:self.y-1},
            Coord2{x:self.x-1, y:self.y},
            Coord2{x:self.x+1, y:self.y},
            Coord2{x:self.x-1, y:self.y+1},
            Coord2{x:self.x,   y:self.y+1},
            Coord2{x:self.x+1, y:self.y+1},
        ]
    }

    // Compute the manhattan distance between two coords
    pub fn manhattan( &self, rhs: &Coord2) -> i32 {
        (self.x - rhs.x).abs() + (self.y - rhs.y).abs()
    }

    pub fn distance(&self, from: &Coord2) -> f32 {
        let total = (self.x - from.x).pow(2) +
            (self.y - from.y).pow(2);
        (total as f32).sqrt()
    }

    pub fn angle_radian(&self) -> f32 {
        (self.y as f32).atan2(self.x as f32)
    }

    pub fn from_polar(angle_radians: f32, dist: f32) -> Coord2 {
        Coord2 {
            x: (dist * angle_radians.cos()).round() as i32,
            y: (dist * angle_radians.sin()).round() as i32
        }
    }
}


impl ops::Add<&Coord2> for &Coord2 {
    type Output = Coord2;

    fn add(self, rhs: &Coord2) -> Coord2 {
        Coord2 {
            x: self.x + rhs.x,
            y: self.y + rhs.y
        }
    }
}

impl ops::Sub<&Coord2> for &Coord2 {
    type Output = Coord2;

    fn sub(self, rhs: &Coord2) -> Coord2 {
        Coord2 {
            x: self.x - rhs.x,
            y: self.y - rhs.y
        }
    }
}

impl ops::Mul<i32> for Coord2 {
    type Output = Coord2;

    fn mul(self, rhs: i32) -> Coord2 {
        Coord2 {
            x: self.x * rhs,
            y: self.y * rhs
        }
    }
}

impl ops::AddAssign for Coord2 {
    fn add_assign(&mut self, other: Self) {
        self.x += other.x;
        self.y += other.y
        // *self = Self {
        //     x: self.x + other.x,
        //     y: self.y + other.y
        // }
    }
}


impl fmt::Display for Coord2 {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "({}, {})", self.x, self.y)
    }
}
