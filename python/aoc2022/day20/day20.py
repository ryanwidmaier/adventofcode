from pathlib import Path
from util import read_input


def parse(line: str):
    return line


def part1(lines):
    return None


def part2(lines):
    return None


# Run
p = Path.cwd() / 'input.txt'
# p = Path.cwd() / 'sample.txt'

lines_ = read_input(p, parse)

answer1 = part1(lines_)
print(f'Part 1: {answer1}')

answer2 = part2(lines_)
print(f'Part 2: {answer2}')
