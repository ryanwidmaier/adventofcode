import re
from collections import defaultdict, namedtuple
import itertools
from util import argmax, argmin, a_star, Coord, GridCar


LEFT, STRAIGHT, RIGHT = 0, 1, 2


class Cart(object):
    def __init__(self, start, char):
        lookup = {
            '>': 'east',
            '<': 'west',
            '^': 'north',
            'V': 'south',
            'v': 'south'
        }

        self.car = GridCar(start, lookup[char], invert_y=True)
        self.next_intersection = LEFT

    def move(self, mine):
        # Turn at intersection
        if mine.is_intersection(self.car.position):
            if self.next_intersection == LEFT:
                self.car.left()
            elif self.next_intersection == RIGHT:
                self.car.right()

            self.next_intersection = (self.next_intersection + 1) % 3

        # Turn at corner
        elif mine.is_corner(self.car.position):
            self.car.turn_to(mine.turn_direction(self.car.position, self.car.facing))

        self.car.forward()


class Mine(object):
    def __init__(self, filename):
        self.tracks = []
        self.carts = {}
        self.tick_number = 0

        # Parse track
        rawlines = []
        with open(filename) as f:
            for line in f:
                line = line.rstrip()
                rawlines.append(line)

        # Find carts
        for pos, char in self.raster_scan(rawlines):
            if char in {'^', '<', '>', 'V', 'v'}:
                self.carts[pos] = (Cart(pos, char))

        # Make track, filling in under the carts
        lookup = {
            '^': '|',
            'v': '|',
            'V': '|',
            '<': '-',
            '>': '-'
        }

        self.tracks = []
        for y in xrange(len(rawlines)):
            self.tracks.append([])
            for x in xrange(len(rawlines[y])):
                ch = rawlines[y][x]
                self.tracks[y].append(lookup.get(ch, ch))

    def raster_scan(self, track=None):
        target = track if track else self.tracks

        for y in xrange(len(target)):
            for x in xrange(len(target[y])):
                yield Coord(x, y), target[y][x]

    def tick(self):
        self.tick_number += 1

        # Sort to ensure we move them in the right order
        ordered = sorted(self.carts.values(), key=lambda c_: (c_.car.position.y, c_.car.position.x))

        for c in ordered:
            # Previously crashed!
            if not c.car.position in self.carts:
                continue

            del self.carts[c.car.position]
            c.move(self)

            if c.car.position in self.carts:
                print "CRASH: ({}) as tick {}.  {} carts remaining".format(c.car.position, self.tick_number, len(self.carts) - 1)
                del self.carts[c.car.position]
            else:
                self.carts[c.car.position] = c

        if len(self.carts) == 1:
            print "Final cart: {}".format(self.carts.values()[0].car.position)
            return True

        return False

    def is_intersection(self, pos):
        return self.tracks[pos.y][pos.x] == '+'

    def is_corner(self, pos):
        return self.tracks[pos.y][pos.x] in {'/', '\\'}

    def turn_direction(self, pos, facing):
        ch = self.tracks[pos.y][pos.x]

        if facing == 'east':
            return 'north' if ch == '/' else 'south'
        if facing == 'south':
            return 'east' if ch == '\\' else 'west'
        if facing == 'west':
            return 'north' if ch == '\\' else 'south'
        if facing == 'north':
            return 'east' if ch == '/' else 'west'

    def display(self):
        direction = {
            'east': '>',
            'west': '<',
            'south': 'v',
            'north': '^'
        }

        for y in xrange(len(self.tracks)):
            for x in xrange(len(self.tracks[y])):
                c = self.carts.get(Coord(x, y))
                if c:
                    print direction[c.car.facing],
                else:
                    print self.tracks[y][x],

            print ''

        print ''


m = Mine('input.txt')
while not m.tick():
    # m.display()
    pass

