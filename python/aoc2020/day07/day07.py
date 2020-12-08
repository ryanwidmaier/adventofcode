from pathlib import Path
import re
from typing import NamedTuple, List


class Child(NamedTuple):
    amount: int
    type: str


def parse(lines):
    line_re = re.compile(r'(\w+ \w+) bags contain (.*)')
    amount_re = re.compile(r'(\d+) (\w+ \w+) bags?')

    tree = {}  # type -> [Child]

    for line in lines:
        m = line_re.match(line)
        parent, children_text = m.groups()

        m2 = amount_re.findall(children_text)
        children = [Child(int(x[0]), x[1]) for x in m2]

        tree[parent] = children

    return tree


def part1(tree_, pos, unique_):
    has_gold = False
    for child in tree_[pos]:
        has_gold |= part1(tree, child.type, unique_)

    if has_gold:
        unique.add(pos)

    return has_gold or pos == 'shiny gold'


def part2(tree_, pos):
    count = 1
    for child in tree_[pos]:
        count += child.amount * part2(tree, child.type)

    return count



base = '/Users/rwidmaier/repos/misc/adventofcode/python/aoc2020/day07/'
f = 'input.txt'

lines = open(Path(base) / f).readlines()
tree = parse(lines)


unique = set()
for k in tree:
    part1(tree, k, unique)

print(len(unique))
print(part2(tree, 'shiny gold'))