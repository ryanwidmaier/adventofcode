from pathlib import Path
from util import read_input


def parse(line: str):
    tokens = [t.split('-') for t in line.split(',')]
    return [[int(x) for x in y] for y in tokens]


def contained(a, b):
    if a[0] <= b[0] and b[1] <= a[1]:
        return True
    if b[0] <= a[0] and a[1] <= b[1]:
        return True
    return False


def overlap(a, b):
    if a[0] <= b[0] <= a[1]:
        return True
    if a[0] <= b[1] <= a[1]:
        return True
    return contained(a, b)


def part1(lines):
    return sum(1 for (a, b) in lines if contained(a, b))


def part2(lines):
    return sum(1 for (a, b) in lines if overlap(a, b))


# Run
p = Path.cwd() / 'input.txt'
# p = Path.cwd() / 'sample.txt'

lines_ = read_input(p, parse)

answer1 = part1(lines_)
print(f'Part 1: {answer1}')

answer2 = part2(lines_)
print(f'Part 2: {answer2}')
