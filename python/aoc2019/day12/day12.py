from util import Coord, RateLogger
import re
import math
from functools import reduce


def compare(a, b):
    if a < b:
        return 1
    elif a > b:
        return -1
    return 0


class Moon:

    def __init__(self, line):
        m = re.match(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>', line)
        self.position = Coord(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        self.velocity = Coord(0, 0, 0)
        self.start_pos = self.position.copy()

    def gravity(self, moons):
        for m in moons:
            self.velocity.x += compare(self.position.x, m.position.x)
            self.velocity.y += compare(self.position.y, m.position.y)
            self.velocity.z += compare(self.position.z, m.position.z)

    def move(self):
        self.position += self.velocity

    def energy(self):
        return self.position.manhattan() * self.velocity.manhattan()

    def is_reset(self, axis):
        return self.velocity[axis] == 0 and self.position[axis] == self.start_pos[axis]

    def __str__(self):
        p = self.position
        v = self.velocity
        return f'pos=<x={p.x:>3}, y={p.y:>3}, z={p.z:>3}>, vel=<x={v.x:>3}, y={v.y:>3}, z={v.z:>3}>'


def part1(moons):
    for t in range(1000):
        for m in moons:
            m.gravity(moons)

        for m in moons:
            m.move()

    print(sum(m.energy() for m in moons))


def part2(moons):
    found = {}

    i = 0
    while len(found) < 3:
        for m in moons:
            m.gravity(moons)

        for m in moons:
            m.move()

        for axis in range(3):
            if axis not in found:
                if all(m.is_reset(axis) for m in moons):
                    found[axis] = i+1

        i += 1

    print(found[0], found[1], found[2])
    print(f"Expected: 4686774924")

    def least_common_mult(a, b):
        return a * b // math.gcd(a, b)

    print(reduce(least_common_mult, found.values()))


moons_ = []
with open('input.txt') as f:
    for line in f:
        moons_.append(Moon(line.strip()))

# part1(moons)
part2(moons_)
