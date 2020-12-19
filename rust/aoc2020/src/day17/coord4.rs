use std::ops;
use std::fmt;

#[derive(PartialEq, Eq, Debug, Hash, Copy, Clone)]
pub struct Coord4 {
    pub x: i32,
    pub y: i32,
    pub z: i32,
    pub w: i32
}

impl Default for Coord4 {
    fn default() -> Self {
        Coord4 {
            x: 0,
            y: 0,
            z: 0,
            w: 0
        }
    }
}


impl Coord4 {
    pub fn add_assign_ref(&mut self, other: &Coord4) {
        self.x += other.x;
        self.y += other.y;
        self.z += other.z;
        self.w += other.w;
    }

    // Return all adjacent Coords (including diagonal)
    pub fn neighbors80(&self) -> Vec<Coord4> {
        let mut result = Vec::new();
        for x in -1..=1 {
            for y in -1..=1 {
                for z in -1..=1 {
                    for w in -1..=1 {
                        if !(x == 0 && y == 0 && z == 0 && w == 0) {
                            result.push(Coord4 {
                                x: self.x + x,
                                y: self.y + y,
                                z: self.z + z,
                                w: self.w + w
                            });
                        }
                    }
                }
            }
        }

        return result;
    }

    // Compute the manhattan distance between two coords
    pub fn manhattan( &self, rhs: &Coord4) -> i32 {
        (self.x - rhs.x).abs() + (self.y - rhs.y).abs() + (self.z - rhs.z).abs() + (self.w - rhs.w).abs()
    }
}


impl ops::Add<&Coord4> for &Coord4 {
    type Output = Coord4;

    fn add(self, rhs: &Coord4) -> Coord4 {
        Coord4 {
            x: self.x + rhs.x,
            y: self.y + rhs.y,
            z: self.z + rhs.z,
            w: self.w + rhs.w
        }
    }
}

impl ops::Sub<&Coord4> for &Coord4 {
    type Output = Coord4;

    fn sub(self, rhs: &Coord4) -> Coord4 {
        Coord4 {
            x: self.x - rhs.x,
            y: self.y - rhs.y,
            z: self.z - rhs.z,
            w: self.w - rhs.w
        }
    }
}

impl ops::Mul<i32> for Coord4 {
    type Output = Coord4;

    fn mul(self, rhs: i32) -> Coord4 {
        Coord4 {
            x: self.x * rhs,
            y: self.y * rhs,
            z: self.z * rhs,
            w: self.w * rhs
        }
    }
}

impl ops::AddAssign for Coord4 {
    fn add_assign(&mut self, other: Self) {
        self.x += other.x;
        self.y += other.y;
        self.z += other.z;
        self.w += other.w;
    }
}


impl fmt::Display for Coord4 {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "({}, {}, {}, {})", self.x, self.y, self.z, self.w)
    }
}
