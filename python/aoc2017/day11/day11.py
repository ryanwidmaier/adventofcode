from util import Coord


def move(pos_, direction):
    offsets = {
        'nw': Coord(x=-1, y=1),
        'n':  Coord(y=1, z=-1),
        'ne': Coord(x=1, z=-1),
        'se': Coord(x=1, y=-1),
        's':  Coord(y=-1, z=1),
        'sw': Coord(x=-1, z=1)
    }

    return pos_ + offsets[direction]


def distance(pos):
    return (abs(pos.x) + abs(pos.y) + abs(pos.z)) / 2


fin = open('input.txt')
dirs = fin.read().split(',')

# dirs = ['ne', 'se'] * 10

pos = Coord(0, 0, 0)
furthest = 0

for d in dirs:
    pos = move(pos, d)
    furthest = max(furthest, distance(pos))


print distance(pos)
print furthest

