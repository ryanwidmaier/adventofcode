use crate::util::coord2::{Coord2, Direction};

pub struct Robot {
    pub position: Coord2,
    pub direction: Direction
}

impl Robot {
    pub fn new(dir: Direction) -> Robot {
        Robot {
            position: Coord2{x:0, y:0},
            direction: dir
        }
    }

    pub fn forward(&mut self, amount: i32) {
        let offset = self.direction.coord() * amount;
        self.position = &self.position + &offset;
    }

    pub fn shift(&mut self, dir: Direction, amount: i32) {
        let offset = dir.coord() * amount;
        self.position = &self.position + &offset;
    }

    pub fn shift_coord(&mut self, offset: &Coord2) {
        self.position = &self.position + &offset;
    }

    pub fn move_to(&mut self, pos: &Coord2) {
        self.position = Coord2{x:pos.x, y:pos.y};
    }

    pub fn rotate(&mut self, turns: i32) {
        let idx = self.direction.idx4();
        let new_idx = (((idx as i32 + turns) % 4) + 4) % 4;

        self.direction = Direction::from_idx4(new_idx as usize);
    }

    pub fn manhattan(&self, from: &Coord2) -> i32 {
        self.position.manhattan(from)
    }

}
