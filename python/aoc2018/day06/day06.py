from collections import defaultdict
from util import Coord, argmin, point_in_triangle, argmax
import re
import itertools
from pprint import pprint

parse_re = re.compile(r'(\d+), (\d+)')

# Load data
points = []
with open('input.txt') as f:
    for line in f:
        result = parse_re.search(line)
        points.append(Coord(int(result.group(1)), int(result.group(2))))


# Find the grid bounds
max_x = max([p.x for p in points])
max_y = max([p.y for p in points])


def compute_part1(delta, fout=None):
    print "Computing closest for each grid point ({}, {}) -> ({}, {}) with +/- {}" \
        .format(0, 0, max_x, max_y, delta)

    area = defaultdict(lambda: 0)
    for y in xrange(-delta, max_y + 1 + delta):
        for x in xrange(-delta, max_x + 1 + delta):
            c = Coord(x, y)

            dists = [c.manhattan(p) for p in points]
            closest = argmin(dists)

            to_write = "  . "
            if sum([1 if d == dists[closest] else 0 for d in dists]) == 1:
                area[closest] += 1
                to_write = "{}{:>2} ".format('*' if dists[closest] == 0 else ' ', closest)

            if fout:
                fout.write(to_write)

        if fout:
            fout.write("\n")

    return dict(area)


def compute_part2(delta):
    print "Computing part2 for each grid point ({}, {}) -> ({}, {}) with +/- {}" \
        .format(0, 0, max_x, max_y, delta)

    area = 0
    for y in xrange(-delta, max_y + 1 + delta):
        for x in xrange(-delta, max_x + 1 + delta):
            c = Coord(x, y)

            dist = sum([c.manhattan(p) for p in points])
            if dist < 10000:
                area += 1

    return area


# fout = open('out.txt', 'w')
area0 = compute_part1(0)
area50 = compute_part1(50)

infinite = [k for k in area0 if area0[k] != area50[k]]
finite = {k: v for k, v in area0.iteritems() if k not in infinite}

print "Infinites"
for idx in sorted(infinite):
    print "  {} - {}".format(idx, points[idx])
    area0[idx] = -1

print ""
print "Areas:"
for idx in sorted(area0):
    print "  {} {}: {}".format(idx, points[idx], area0[idx])

max_id = argmax(area0)
print "Max: area={}, index={}, point={}".format(area0[max_id], max_id, points[max_id])


print "Part 2: {}".format(compute_part2(10))

# # Points are finite if they are contained in a triangle by any 3 other points
# infinite = set([(idx, p) for idx, p in enumerate(points)])
# for p1, p2, p3 in itertools.product(points, points, points):
#     # Triangle can't use the same point for 2 corners
#     if p1 == p2 or p2 == p3 or p1 == p3:
#         continue
#
#     triangle = [p1, p2, p3]
#     for idx, p in list(infinite):
#         if p not in triangle and point_in_triangle(p, triangle):
#             print "  {} {} bound by Triangle({}, {}, {})".format(idx, p, p1, p2, p3)
#             infinite.remove((idx, p))
#
# print ""
# print "Infinites"
# for idx, p in sorted(infinite):
#     print "  {} - {}".format(idx, p)
#     area[idx] = -1
#
# print ""
# print "Areas:"
# for idx in sorted(area):
#     print "  {} {}: {}".format(idx, points[idx], area[idx])
#
# max_id = argmax(area)
# print "Max: area={}, index={}, point={}".format(area[max_id], max_id, points[max_id])
#
# area = {k: v for k, v in area.items() if k != max_id}
# max_id = argmax(area)
# print "Max: area={}, index={}, point={}".format(area[max_id], max_id, points[max_id])
