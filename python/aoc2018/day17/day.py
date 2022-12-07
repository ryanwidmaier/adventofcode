import re
from collections import defaultdict, namedtuple
import itertools
from util import argmax, argmin, a_star, Coord

# x=370, y=1769..1771
parse_re = re.compile(r'(?P<c1>\w)=(?P<v1>\d+), (?P<c2>\w)=(?P<v2a>\d+)..(?P<v2b>\d+)')



class Stratum(object):
    def __init__(self, fname):
        self.grid = {}
        self.wet_count = 0
        self.fout = open('out.txt', 'w')

        f = open(fname)
        for line in f:
            line = line.rstrip()

            m = parse_re.search(line)
            if not m:
                continue

            start, stop = int(m.group('v2a')), int(m.group('v2b'))
            for i in xrange(start, stop+1):
                kwargs = {
                    m.group('c1'): int(m.group('v1')),
                    m.group('c2'): i
                }
                self.grid[Coord(**kwargs)] = '#'

        self.min_y = min(c.y for c in self.grid.keys())
        self.max_y = max(c.y for c in self.grid.keys())

    def pour(self, source, depth):
        print "Depth {:4}, Source {}, Fill Count={}".format(depth, source, self.wet_count)
        coord = source
        # self.draw()

        # Work to bottom, either wall (#) or trapped water (~)
        while not self.is_blocked(coord):
            if self.grid.get(coord) == '|':
                print "Already pouring here"
                return

            if coord.y > self.max_y:
                # self.draw()
                print "Reached the bottom"
                return

            self.wet_square(coord)
            coord = Coord(coord.x, coord.y + 1)

        # self.draw()

        contact = coord - Coord(0, 1)
        left_drop_x = self.flow_horizontal(contact, Coord(1, 0))
        right_drop_x = self.flow_horizontal(contact, Coord(-1, 0))

        # self.draw()

        # Blocked on both sides, fill another level
        while left_drop_x is None and right_drop_x is None:
            # Convert to trapped first
            self.convert_to_trapped(contact)
            # self.draw()

            # Do the next level up
            contact -= Coord(0, 1)
            self.wet_square(contact)

            left_drop_x = self.flow_horizontal(contact, Coord(1, 0))
            right_drop_x = self.flow_horizontal(contact, Coord(-1, 0))

        # Recursion FTW
        if left_drop_x:
            self.pour(Coord(left_drop_x, contact.y), depth+1)
        if right_drop_x:
            self.pour(Coord(right_drop_x, contact.y), depth+1)

    def convert_to_trapped(self, start):
        c = start.copy()
        while self.grid.get(c) != '#':
            self.grid[c.copy()] = '~'
            c -= Coord(1, 0)

        c = start.copy()
        while self.grid.get(c) != '#':
            self.grid[c.copy()] = '~'
            c += Coord(1, 0)

    def flow_horizontal(self, start, offset):
        # Case 1 (Find new drop)      Case 2 (Find wall)
        #      <---                    #   <--
        #   ||||||||*                  #||||||||*
        #   |#############             ###############

        # Scan one direction, adding wet or finding a place to drip further
        coord = start + offset
        while not self.is_blocked(coord) and self.is_blocked(coord + Coord(0, 1)):
            self.wet_square(coord)
            coord += offset

        # If we hit a wall
        if self.is_blocked(coord):
            return None
        # Else, we found an edge
        else:
            return coord.x

    def is_blocked(self, c):
        return self.grid.get(c, '.') in {'#', '~'}

    def wet_square(self, c):
        # If this is a new square.. inc and mark with wet (!)
        if not self.grid.get(c):
            self.grid[c.copy()] = '|'

            if self.min_y <= c.y <= self.max_y:
                self.wet_count += 1

    def draw(self):
        # return

        self.fout.write("Filled: {}".format(self.wet_count))

        delta = 10
        filled = [c for c, v in self.grid.iteritems() if v in {'|', '~'}]
        if len(filled):
            return

        ul, br = Coord.minmax(*filled)

        for y in xrange(ul.y-1, br.y+2):
            for x in xrange(ul.x-1-delta, br.x+1+delta):
                self.fout.write(self.grid.get(Coord(x, y), ' '))

            self.fout.write('\n')

        self.fout.write('\n')


st = Stratum('input.txt')
st.pour(Coord(500, -2), 1)
st.draw()
print st.wet_count
print sum(1 for v in st.grid.itervalues() if v == '~')