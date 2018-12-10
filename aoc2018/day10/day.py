import re
from collections import defaultdict, namedtuple
import itertools
from util import argmax, argmin, a_star, Coord, RateLogger


def print_grid(points_):
    # Print it out
    min_x, max_x = min([p.x for p in points_]), max([p.x for p in points_]),
    min_y, max_y = min([p.y for p in points_]), max([p.y for p in points_])

    for y in xrange(min_y, max_y + 1):
        for x in xrange(min_x, max_x + 1):
            c = Coord(x, y)
            if c in points_:
                print "#",
            else:
                print ".",

        print "\n",


# position=<-54220, -10694> velocity=< 5,  1>
parse_re = re.compile(
    r'position=<\s*(?P<x>-?\d+),\s*(?P<y>-?\d+)>\s*'
    r'velocity=<\s*(?P<vx>-?\d+),\s*(?P<vy>-?\d+)>'
)

points = []
velocites = []

f = open('input.txt')
for line in f:
    line = line.rstrip()

    match = parse_re.search(line)
    if match:
        points.append(Coord(int(match.group('x')), int(match.group('y'))))
        velocites.append(Coord(int(match.group('vx')), int(match.group('vy'))))

delta_height = 999999
min_delta_height = delta_height


def log(r):
    return "Processing {} records took {}s.  Total={}, delta={}"\
        .format(r.log_every_n, r.timer.elapsed_secs(), r.total, delta_height)


rate_logger = RateLogger(log_fn=log)
tick = 0

# Loop until the delta in height increases
while delta_height <= min_delta_height:
    tick += 1
    for i in xrange(len(points)):
        points[i] += velocites[i]

    delta_height = max([p.y for p in points]) - min([p.y for p in points])
    min_delta_height = min(delta_height, min_delta_height)

    rate_logger.inc()


# Undo the overstep
for i in xrange(len(points)):
    points[i] -= velocites[i]

print_grid(points)
print tick