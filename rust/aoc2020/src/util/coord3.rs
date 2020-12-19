use std::ops;
use std::fmt;

#[derive(PartialEq, Eq, Debug, Hash, Copy, Clone)]
pub struct Coord3 {
    pub x: i32,
    pub y: i32,
    pub z: i32
}

impl Default for Coord3 {
    fn default() -> Self {
        Coord3 {
            x: 0,
            y: 0,
            z: 0
        }
    }
}


impl Coord3 {
    pub fn add_assign_ref(&mut self, other: &Coord3) {
        self.x += other.x;
        self.y += other.y;
        self.z += other.z;
    }

    // Return all adjacent Coords (including diagonal)
    pub fn neighbors26(&self) -> Vec<Coord3> {
        let mut result = Vec::new();
        for x in -1..=1 {
            for y in -1..=1 {
                for z in -1..=1 {
                    if !(x == 0 && y == 0 && z == 0) {
                        result.push(Coord3 {
                            x: self.x+x,
                            y: self.y+y ,
                            z: self.z+z
                        });
                    }
                }
            }
        }

        return result;
    }

    // Compute the manhattan distance between two coords
    pub fn manhattan( &self, rhs: &Coord3) -> i32 {
        (self.x - rhs.x).abs() + (self.y - rhs.y).abs() + (self.z - rhs.z).abs()
    }

    pub fn distance(&self, from: &Coord3) -> f32 {
        let total = (self.x - from.x).pow(2) +
            (self.y - from.y).pow(2) +
            (self.z - from.z).pow(2);
        (total as f32).sqrt()
    }
}


impl ops::Add<&Coord3> for &Coord3 {
    type Output = Coord3;

    fn add(self, rhs: &Coord3) -> Coord3 {
        Coord3 {
            x: self.x + rhs.x,
            y: self.y + rhs.y,
            z: self.z + rhs.z
        }
    }
}

impl ops::Sub<&Coord3> for &Coord3 {
    type Output = Coord3;

    fn sub(self, rhs: &Coord3) -> Coord3 {
        Coord3 {
            x: self.x - rhs.x,
            y: self.y - rhs.y,
            z: self.z - rhs.z
        }
    }
}

impl ops::Mul<i32> for Coord3 {
    type Output = Coord3;

    fn mul(self, rhs: i32) -> Coord3 {
        Coord3 {
            x: self.x * rhs,
            y: self.y * rhs,
            z: self.z * rhs
        }
    }
}

impl ops::AddAssign for Coord3 {
    fn add_assign(&mut self, other: Self) {
        self.x += other.x;
        self.y += other.y;
        self.z += other.z;
    }
}


impl fmt::Display for Coord3 {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "({}, {}, {})", self.x, self.y, self.z)
    }
}
