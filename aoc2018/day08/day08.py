import re
from collections import defaultdict, namedtuple
import itertools
from util import argmax, argmin, a_star, Coord


f = open('input.txt')
line = None
for line in f:
    line = line.rstrip()
    break

tokens = [int(v) for v in line.split()]


def part1(tokens, idx):
    children, meta = tokens[idx], tokens[idx+1]
    idx += 2
    meta_total = 0

    for c in xrange(children):
        idx, c_meta_total = part1(tokens, idx)
        meta_total += c_meta_total

    meta_total += sum(tokens[idx:idx+meta])
    idx += meta

    return (idx, meta_total)


def part2(tokens, idx):
    num_children, meta = tokens[idx], tokens[idx+1]
    idx += 2

    children = {}
    for c in xrange(num_children):
        idx, c_meta_total = part2(tokens, idx)
        children[c+1] = c_meta_total

    if num_children == 0:
        meta_total = sum(tokens[idx:idx+meta])
    else:
        meta_total = sum(children.get(m, 0) for m in tokens[idx:idx+meta])

    idx += meta
    return (idx, meta_total)

_, meta_total = part1(tokens, 0)
print meta_total

_, meta_total = part2(tokens, 0)
print meta_total
