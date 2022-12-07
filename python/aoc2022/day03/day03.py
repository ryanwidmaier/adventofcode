import itertools
import string
from pathlib import Path
from util import read_input

PRIORITY = dict((t[1], t[0]) for t in enumerate(string.ascii_letters, start=1))


def parse(line: str):
    mid = len(line) // 2
    return line[:mid], line[mid:]


def part1(lines):
    priority = 0

    for line in lines:
        ruck1, ruck2 = parse(line)
        overlap = set(ruck1).intersection(ruck2).pop()
        priority += PRIORITY[overlap]

    return priority


def part2(lines):
    groups = [lines[i:i+3] for i in range(0, len(lines), 3)]
    priority = 0

    for group in groups:
        overlap = set(group[0]).intersection(group[1]).intersection(group[2]).pop()
        priority += PRIORITY[overlap]

    return priority


# Run
p = Path.cwd() / 'input.txt'
# p = Path.cwd() / 'sample.txt'

lines = read_input(p)

answer1 = part1(lines)
print(f'Part 1: {answer1}')

answer2 = part2(lines)
print(f'Part 2: {answer2}')
