import math
import numpy as np

np.set_printoptions(suppress=True)
np.core.arrayprint._line_width = 160


def find_pos(square):
    # Find out which ring it the space is in
    block_width = 1

    while block_width**2 < square:
        block_width += 2

    # Determine how many spaces off one of the primary axes we are
    total = block_width ** 2
    axis1 = (block_width - 1) / 2

    axes = [
        total - axis1,
        total - axis1 - block_width,
        total - axis1 - block_width*2,
        total - axis1 - block_width*3,
    ]

    closest = min([abs(square - a) for a in axes])
    return closest + axis1


def find_pos2(square):

    max_dim = 201
    center = (max_dim - 1) / 2
    mat = np.zeros((max_dim, max_dim))
    first = True

    for pos in next_pos(201):
        row, col = pos

        if first:
            mat[row, col] = 1
            first = False
        else:
            mat[row, col] = mat[row-1:row+2, col-1:col+2].sum()

        print ""
        print "At: ({},{})".format(row, col)
        print mat[center-6:center+7, center-6:center+7]
        if mat[row, col] == square:
            return row - center, col - center


def next_pos(dim):
    offsets = [
        (-1, 0),
        (0, -1),
        (1, 0),
        (0, 1)
    ]

    center = (dim - 1) / 2

    cur_pos = (center, center)
    yield cur_pos

    for r in xrange(2, dim, 2):
        yield cur_pos
        cur_pos = (cur_pos[0], cur_pos[1] + 1)

        for idx, side_offset in enumerate(offsets):
            for pos in xrange(r if idx > 0 else r - 1):
                yield cur_pos
                cur_pos = (cur_pos[0] + side_offset[0], cur_pos[1] + side_offset[1])



"""
1
2 3
4 5
6 7
8 9
10 11 12 13
14 15 16 17
18 19 20 21
22 23 24 25
26 27 28 29 30 31
"""

"""
1
1   2
4   5
10 11
23 25
26 54 57 59
122 133 142 147
304 330 351 362
747 806
"""


print '9: ', find_pos(9), ' ', find_pos2(9)

print '312051: ', find_pos(312051), ' ', find_pos2(312051)
