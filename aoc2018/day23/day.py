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

    answer = count_overlaps(center, biggest_delta, transmitters)
    print "Delta = {:,}.  Max={}, max_val={}".format(biggest_delta, center, answer)

    # Divide search area into halves (on each axis)
    delta = biggest_delta

    while delta >= 1:
        delta /= 2
        region_counts = {}

        # Count how many transmitters touch each region
        for x_mul, y_mul, z_mul in (
                (-1, 0, 0), (1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)
        ):
            offset = Coord(x_mul, y_mul, z_mul) * delta
            test_c = center + offset
            region_counts[test_c] = (count_overlaps(test_c, delta, transmitters), -test_c.manhattan(Coord()))

        print "Delta = {:,}.  Center={}".format(delta, center)
        center = argmax(region_counts)

        for k, v in region_counts.iteritems():
            m = "*MAX*" if k == center else ""
            print "   {} - {}      {}".format(k, v[0], m)


def count_overlaps(center, r, transmitters):
    total = 0
    for tx, tx_r in transmitters:
        dist = tx.manhattan(center)
        aa = tx_r + r
        if dist < tx_r + r:
            total += 1

    return total


transmitters = parse('input.txt')
# part1(transmitters)
part2(transmitters)
# stats(transmitters)


# Too high: 104501044 - Coord(58376721, 23683264, 22441059)

