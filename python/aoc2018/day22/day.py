import re
from collections import defaultdict, namedtuple
import itertools
from util import argmax, argmin, a_star, Coord, Memoize

parse_re = re.compile(r'')

# Example
# target = Coord(10, 10)
# depth = 510
# expected = 114
#
# Input
target = Coord(6, 770)
depth = 4845

@Memoize
def geologic_index(c):
    # The region at 0,0 (the mouth of the cave) has a geologic index of 0.
    # The region at the coordinates of the target has a geologic index of 0.
    # If the region's Y coordinate is 0, the geologic index is its X coordinate times 16807.
    # If the region's X coordinate is 0, the geologic index is its Y coordinate times 48271.
    # Otherwise, the region's geologic index is the result of multiplying the erosion levels of the regions at X-1,Y and X,Y-1.

    if c == Coord(0, 0):
        return 0

    if c == target:
        return 0

    if c.y == 0:
        return c.x * 16807

    if c.x == 0:
        return c.y * 48271

    left = erosion(Coord(c.x-1, c.y))
    right = erosion(Coord(c.x, c.y-1))
    return left * right


def erosion(c):
    # A region's erosion level is its geologic index plus the cave system's depth, all modulo 20183. Then:
    #
    # If the erosion level modulo 3 is 0, the region's type is rocky.
    # If the erosion level modulo 3 is 1, the region's type is wet.
    # If the erosion level modulo 3 is 2, the region's type is narrow.
    return (geologic_index(c) + depth) % 20183


def get_type(c):
    return erosion(c) % 3


ROCKY = 0
WET = 1
NARROW = 2

def part1():
    total = 0
    for y in xrange(target.y+1):
        for x in xrange(target.x+1):
            total += get_type(Coord(x, y))

    print "Part 1: {}".format(total)

# In rocky regions, you can use the climbing gear or the torch. You cannot use neither (you'll likely slip and fall).
# In wet regions, you can use the climbing gear or neither tool. You cannot use the torch (if it gets wet, you won't have a light source).
# In narrow regions, you can use the torch or neither tool. You cannot use the climbing gear (it's too bulky to fit).

NEITHER = 0
TORCH = 1
CLIMBING = 2

def part2():
    grid = [[get_type(Coord(x, y)) for x in xrange(800)] for y in xrange(800)]
    print "Grid populated"

    def is_valid(pos, tool):
        c_type = grid[pos.y][pos.x]
        if c_type == ROCKY and tool == NEITHER:
            return False
        if c_type == WET and tool == TORCH:
            return False
        if c_type == NARROW and tool == CLIMBING:
            return False

        return True

    def possible_moves(current):
        curr_pos, curr_tool = current
        result = []

        # First try different tools
        for tool in xrange(3):
            if tool != curr_tool and is_valid(curr_pos, tool):
                result.append( ((curr_pos, tool), 7) )

        # Then try moving w/ the current tool
        if curr_pos.x > 0:
            dest = curr_pos + Coord(-1, 0)
            if is_valid(dest, curr_tool):
                result.append(((dest, curr_tool), 1))

        dest = curr_pos + Coord(1, 0)
        if is_valid(dest, curr_tool):
            result.append(((dest, curr_tool), 1))

        if curr_pos.y > 0:
            dest = curr_pos + Coord(0, -1)
            if is_valid(dest, curr_tool):
                result.append(((dest, curr_tool), 1))

        dest = curr_pos + Coord(0, 1)
        if is_valid(dest, curr_tool):
            result.append(((dest, curr_tool), 1))

        return result

    def remaining_dist(pos, goal):
        return pos[0].manhattan(goal[0]) + (7 if pos[1] != goal[1] else 0)

    start_state = (Coord(0, 0), TORCH)
    path = a_star(start_state, (target, TORCH), possible_moves_fn=possible_moves, distance_remaining_fn=remaining_dist)

    lookup = {
        NEITHER: 'NEITHER',
        TORCH: 'TORCH',
        CLIMBING: 'CLIMBING'
    }
    tick = 0
    last = start_state
    print "0: (0, 0) TORCH"
    for p in path:
        if last[0] != p[0]:
            tick += 1
        else:
            tick += 7
        last = p

        print "{}: {} {}".format(tick, p[0], lookup[p[1]])


part2()