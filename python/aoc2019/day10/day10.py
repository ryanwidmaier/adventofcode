from util import Coord, grid_walk
from math import atan2, pi
from collections import defaultdict


def count(base, asteroids):
    visible = {atan2(c.y-base.y, c.x-base.x) for c in asteroids}
    return len(visible)


def part1(asteroids):
    distances = {p: count(p, asteroids) for p in asteroids}
    best = max(distances.items(), key=lambda x: x[1])

    print(best)


def part2(asteroids, base):
    # First collect by lined up
    angle_map = defaultdict(lambda: [])
    for c in asteroids:
        if c != base:
            angle_map[atan2((c.y-base.y)*-1, c.x-base.x)].append(c)

    def cvt(a):
        degrees = a * (180 / pi)
        if degrees > 90:
            degrees -= 360

        return degrees

    # Sort closest to farthers for each angle
    angle_list = [(cvt(a), sorted(l, key=lambda d: base.cartesian(d), reverse=True))
                  for a, l in angle_map.items()]

    # Sort angle map
    angles = sorted(angle_list, key=lambda x: x[0])

    # Now laser!
    # i = next(i for i in range(len(angles)) if angles[i][1][-1] == Coord(11, 12))
    i = len(angles) - 1
    for n in range(200):
        print(i, angles[i][0], angles[i][1][-1])
        angles[i][1].pop()

        if len(angles[i][1]) == 0:
            angles = angles[:i] + angles[i+1:]

        i = (i + -1) % len(angles)


with open('input.txt') as f:
    grid = [l.strip() for l in f]

asteroids_ = [c for c, d in grid_walk(grid) if d == '#']

part1(asteroids_)
part2(asteroids_, Coord(26, 29))