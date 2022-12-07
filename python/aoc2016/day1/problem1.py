class Direction(object):
    EAST = 0
    NORTH = 1
    WEST = 2
    SOUTH = 3

    @staticmethod
    def to_str(dir):
        table = {
            Direction.EAST: "EAST",
            Direction.NORTH: "NORTH",
            Direction.WEST: "WEST",
            Direction.SOUTH: "SOUTH"
        }
        return table[dir]


class Mover:

    def __init__(self, facing):
        self.facing = facing
        self.location = (0, 0)
        self.visited = {(0, 0)}
        self.hq_location = None

    def turn(self, left):
        if left:
            self.facing = (self.facing + 1) % 4
        else:
            self.facing = (self.facing - 1) % 4

    def calc_move(self, distance):
        mult_table = {
            Direction.EAST: (1, 0),
            Direction.NORTH: (0, 1),
            Direction.WEST: (-1, 0),
            Direction.SOUTH: (0, -1)
        }

        mult = mult_table[self.facing]
        move_amount = (mult[0] * distance, mult[1] * distance)
        return self.location[0] + move_amount[0], self.location[1] + move_amount[1]

    def move(self, distance):
        # Need to walk one step at a time to figure out if we've been here before
        for d_ in xrange(1, distance+1):
            visit = self.calc_move(d_)
            if visit in self.visited and self.hq_location is None:
                self.hq_location = visit

            self.visited.add(visit)

        # Move to final location for this direction
        self.location = self.calc_move(distance)


################################################


input_data = 'R3, L5, R1, R2, L5, R2, R3, L2, L5, R5, L4, L3, R5, L1, R3, R4, R1, L3, R3, L2, L5, L2, R4, R5, R5, L4, L3, L3, R4, R4, R5, L5, L3, R2, R2, L3, L4, L5, R1, R3, L3, R2, L3, R5, L194, L2, L5, R2, R1, R1, L1, L5, L4, R4, R2, R2, L4, L1, R2, R53, R3, L5, R72, R2, L5, R3, L4, R187, L4, L5, L2, R1, R3, R5, L4, L4, R2, R5, L5, L4, L3, R5, L2, R1, R1, R4, L1, R2, L3, R5, L4, R2, L3, R1, L4, R4, L1, L2, R3, L1, L1, R4, R3, L4, R2, R5, L2, L3, L3, L1, R3, R5, R2, R3, R1, R2, L1, L4, L5, L2, R4, R5, L2, R4, R4, L3, R2, R1, L4, R3, L3, L4, L3, L1, R3, L2, R2, L4, L4, L5, R3, R5, R3, L2, R5, L2, L1, L5, L1, R2, R4, L5, R2, L4, L5, L4, L5, L2, L5, L4, R5, R3, R2, R2, L3, R3, L2, L5'
# input_data = 'R8, R4, R4, R8'

directions = [d.strip() for d in input_data.split(',')]

mover = Mover(Direction.NORTH)

for dir in directions:
    turn = dir[0]
    amount = int(dir[1:])

    mover.turn(turn == 'L')
    mover.move(amount)

    facing_str = Direction.to_str(mover.facing)

    print "{}: Turn {}, Move {}, Now facing {} at {}".format(dir, turn, amount, facing_str, mover.location)


print "Finish at: {}".format(mover.location)

print ""
print "HQ: {}".format(mover.hq_location)