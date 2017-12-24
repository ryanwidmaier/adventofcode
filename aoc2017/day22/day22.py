import numpy as np
from util import CoordMat as Coord

CLEAN = 0
WEAK = 1
INFECTED = 2
FLAGGED = 3

directions = [
    Coord(-1, 0),  # North
    Coord(0, 1),  # East
    Coord(1, 0),  # Sout
    Coord(0, -1)   # West
]


def expand_array(mat, pos, amount=1000):
    new_mat = np.zeros((mat.shape[0]+amount, mat.shape[1]+amount))

    r = amount / 2
    c = amount / 2
    rr = r + mat.shape[0]
    cc = c + mat.shape[1]

    new_mat[r:rr, c:cc] = mat

    pos_adjust = Coord(amount/2, amount/2)

    return new_mat, pos + pos_adjust


def turn(state, direction):
    if state == CLEAN:
        return (direction - 1) % 4

    if state == INFECTED:
        return (direction + 1) % 4

    if state == FLAGGED:
        return (direction + 2) % 4

    return direction


def activate_virus(grid, pos, direction):
    state = grid[pos.r, pos.c]

    # Step 1: Turn
    direction = turn(state, direction)

    # Step 2: Infect/clean
    grid[pos.r, pos.c] = (state + 1) % 4

    # Step 3: Move
    pos += directions[direction]

    # Step 4: Expand
    if not (0 <= pos.r < grid.shape[0] and 0 <= pos.c < grid.shape[1]):
        grid, pos = expand_array(grid, pos, 4)

    return grid, pos, direction, state == WEAK


def parse_input(filename):
    fin = open(filename)

    lines = []
    for line in fin:
        line = line.rstrip()
        row = [INFECTED if ch == '#' else CLEAN for ch in line]
        lines.append(row)

    return np.array(lines)


grid_ = parse_input('input.txt')
pos_ = Coord(grid_.shape[0] / 2, grid_.shape[1] / 2)
direction_ = 0
total_infected = 0

# print "({}, {}), {}".format(pos_.r, pos_.c, direction_)
# print grid_

for x in xrange(10000000):
    grid_, pos_, direction_, infected_ = activate_virus(grid_, pos_, direction_)
    if infected_:
        total_infected += 1

    if x % 10000 == 0:
        print "{} iterations".format(x)

    #print ""
    #print "({}, {}), {}".format(pos_.r, pos_.c, direction_)
    #print grid_


print total_infected
