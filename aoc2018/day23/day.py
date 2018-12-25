import re
from collections import defaultdict, namedtuple
import itertools
from util import argmax, argmin, a_star, Coord, minmax
import numpy as np
from pprint import pprint


# pos=<-27072311,19664231,23616729>, r=91300896
parse_re = re.compile(r'pos=<(?P<x>-?\d+),(?P<y>-?\d+),(?P<z>-?\d+)>, r=(?P<r>-?\d+)')


def parse(fname):
    transmitters = []

    f = open(fname)
    for line in f:
        line = line.rstrip()

        m = parse_re.search(line)
        if m:
            transmitters.append((Coord(m.group('x'), m.group('y'), m.group('z')), int(m.group('r'))))

    return transmitters


def part1(transmitters):
    # Find largest
    largest_tx, largest_r = max(transmitters, key=lambda t: t[1])
    print "Largest: Coord({:,}, {:,}, {:,}), r={:,}".format(largest_tx.x, largest_tx.y, largest_tx.z, largest_r)

    count = sum(1 if largest_tx.manhattan(t[0]) <= largest_r else 0 for t in transmitters)
    print "Part1: {}".format(count)


def stats(transmitters):
    x = minmax(c[0].x for c in transmitters)
    y = minmax(c[0].y for c in transmitters)
    z = minmax(c[0].z for c in transmitters)
    r = minmax(c[1] for c in transmitters)

    print "X Min={:,}, Max={:,}, delta={:,}".format(x[0], x[1], x[1] - x[0])
    print "Y Min={:,}, Max={:,}, delta={:,}".format(y[0], y[1], y[1] - y[0])
    print "Z Min={:,}, Max={:,}, delta={:,}".format(z[0], z[1], z[1] - z[0])
    print "R Min={:,}, Max={:,}, delta={:,}".format(r[0], r[1], r[1] - r[0])

    # Find overlap counts
    overlaps = []
    for tx, r1 in transmitters:
        total = 0
        for tx2, r2 in transmitters:
            if tx.manhattan(tx2) < (r1 + r2):
                total += 1

        overlaps.append(total)

    pprint(sorted(zip(overlaps, transmitters), reverse=True))


def part2(transmitters):
    scale = 1
    transmitters = [(c/scale, r/scale) for c, r in transmitters]

    x_range = minmax(c[0].x for c in transmitters)
    y_range = minmax(c[0].y for c in transmitters)
    z_range = minmax(c[0].z for c in transmitters)

    biggest_delta = max(x_range[1] - x_range[0], y_range[1] - y_range[0], z_range[1] - z_range[0])
    center = sum([Coord(x_range[i], y_range[i], z_range[i]) for i in (0, 1)], Coord()) / 2

    # biggest_delta = 100
    answer = count_overlaps(center, biggest_delta, transmitters)
    print "Delta = {:,}.  Max={}, max_val={}".format(biggest_delta, center, answer)

    # Divide search area into halves (on each axis)
    best = search(center, biggest_delta, transmitters, (Coord(-999999999, -99999999, -999999999999), 0))
    print "Final best: {}, {}".format(best[0], best[1])


def search(center, delta, transmitters, best, region_size='-'):
    print "Enter: {}, delta={}, current_best={}, region_size={}".format(center, delta, best[1], region_size)

    # best = (coord, overlaps)
    region_counts = {}

    # delta zero means we need to figure out whether center, or adjacent is the best single square
    if delta == 0:
        for x_off, y_off, z_off in (
                (-1, 0, 0), (1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1), (0, 0, 0)
        ):
            test_c = center + Coord(x_off, y_off, z_off)
            region_counts[test_c] = count_overlaps(test_c, delta, transmitters)
    # Else, search an area
    else:
        # Count how many transmitters touch each region
        for x_mul, y_mul, z_mul in (
                (-1, 0, 0), (1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)
        ):
            offset = Coord(x_mul, y_mul, z_mul) * delta * 1.1
            offset = Coord(int(offset.x), int(offset.y), int(offset.z))
            test_c = center + offset
            region_counts[test_c] = count_overlaps(test_c, delta, transmitters)

    # Recurse on ones that may have a better answer
    best_pos, best_cnt = best

    # Sort by regions w/ most overlap
    ordered = sorted(region_counts.iteritems(), key=lambda r: (r[1], -r[0].manhattan(Coord())), reverse=True)

    # Give up, no reason to look further
    # if ordered[0][1] == 0:
    #     print "Branch ineliglble: {}".format(ordered[0][0])
    #     return ordered[0][0], 0

    # Reached the bottom of the tree, return best square
    if delta == 0:
        print "   Best for branch: {}, {}".format(ordered[0][0], ordered[0][1])
        return ordered[0]

    # Check each possible region
    for pos, cnt in ordered:
        print pos, cnt
        if cnt >= best_cnt:
            pass
            # new_pos, new_cnt = search(pos, delta/2, transmitters, (best_pos, best_cnt), cnt)

            # if new_cnt == best_cnt and new_pos.manhattan(Coord()) < best_pos.manhattan(Coord()):
            #     best_pos, best_cnt = new_pos, new_cnt
            # elif new_cnt > best_cnt:
            #     best_pos, best_cnt = new_pos, new_cnt

    print "   Exit: {}, delta={}, current_best={}".format(best_pos, delta, best_cnt)
    return (best_pos, best_cnt)


def count_overlaps(center, r, transmitters):
    total = 0
    for tx, tx_r in transmitters:
        dist = tx.manhattan(center)
        if dist <= tx_r + r:
            total += 1

    return total



#
#
#
#
#
#
#
#


transmitters = parse('example.txt')

# result = search(Coord(58667886, 24011797, 22403690), 0, transmitters, (Coord(0, 0, 0), 0))

# part1(transmitters)
part2(transmitters)
# stats(transmitters)

#           104501042
# Too high: 104501044 - Coord(58376721, 23683264, 22441059), 940
#           105083214 - Coord(58667807, 24011799, 22403608), 947

# c = Coord(58376721, 23683264, 22441059)

# c = Coord(13,12,12)
# print c.manhattan(Coord())
# print count_overlaps(c, 1, transmitters)