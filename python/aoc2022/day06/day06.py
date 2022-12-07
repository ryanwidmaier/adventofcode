from collections import deque
from pathlib import Path
from util import read_input


def parse(line: str):
    return line


def start(line, start_len) -> int:
    for idx in range(len(line) - start_len):
        part = set(line[idx:idx+start_len])
        if len(part) == start_len:
            return idx + start_len

    return -1


def run(lines, part, start_len):
    print(f'Part{part}:')
    for line in lines:
        s = start(line, start_len)
        print(f'{s}: {line}')
        print(f'{s}: ' + ' ' * (s - start_len) + '-' * start_len)
        print()


def part1(lines):
    run(lines, 1, 4)


def part2(lines):
    run(lines, 2, 14)


# Run
p = Path.cwd() / 'input.txt'
# p = Path.cwd() / 'sample.txt'

lines_ = read_input(p, parse)

answer1 = part1(lines_)
print(f'Part 1: {answer1}')

answer2 = part2(lines_)
print(f'Part 2: {answer2}')
