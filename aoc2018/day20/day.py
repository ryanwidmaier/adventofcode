import re
from collections import defaultdict, namedtuple
import itertools
from util import argmax, argmin, a_star, Coord


opposite = {'N': 'S', 'W': 'E', 'S': 'N', 'E': 'W'}

class Map(object):
    def __init__(self):
        self.rooms = defaultdict(lambda: {'N': False, 'S': False, 'W': False, 'E': False})


    def walk(self, pos, start, pattern):
        idx = start
        while idx < len(pattern):
            direction = pattern[idx]
            if direction in {'^', '$'}:
                continue

            if direction == '(':
                idx = self.walk(pos.copy(), idx+1, pattern[idx:])
            elif direction in {'|', ')'}:
                return idx

            if direction in {'N', 'E', 'W', 'S'}:
                self.rooms[pos][direction] = True
                self.rooms[pos]

            idx += 1



m = map()
m.walk(Coord(0, 0), pattern)
