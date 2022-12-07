from collections import namedtuple

Coord = namedtuple('Coord', 'x y')


class Child(object):
    def __init__(self):
        self.pos = Coord(0, 0)
        self.step = 0

    def move(self, direction):
        self.step += 1
        self.pos = next_pos(direction, self.pos)

        print "{}: Dir={}, NewPos=({}, {})".format(self.step, direction, self.pos.x, self.pos.y)

def next_pos(direction, pos):
    if direction == 'n':
        return Coord(pos.x, pos.y + 1)
    elif direction == 's':
        return Coord(pos.x, pos.y - 1)
    elif direction == 'ne':
        return Coord(pos.x + 1, pos.y)
    elif direction == 'se':
        return Coord(pos.x + 1, pos.y - 1)
    elif direction == 'nw':
        return Coord(pos.x - 1, pos.y + 1)
    elif direction == 'sw':
        return Coord(pos.x - 1, pos.y)


def distance(pos):
    """ Distance from origin """
    steps = 0

    # Move diagnol until we hit N/S axis or E/W axis
    while 0 < pos.x:
        pos = next_pos(m)



fin = open('input.txt')
dirs = fin.read().split(',')
child = Child()

dirs = ['ne', 'se'] * 10

for d in dirs:
    child.move(d)

