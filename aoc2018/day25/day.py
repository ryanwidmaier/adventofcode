import re
from collections import defaultdict, namedtuple
import itertools
from util import argmax, argmin, a_star, Coord

parse_re = re.compile(r'')


f = open('input.txt')
for line in f:
    line = line.rstrip()

    match = parse_re.search(line)
    if match:
        pass
