import re
import sys
from pathlib import Path
from typing import Any

from util.io import read_input


parse_re = re.compile(r'')


def main(filename: str):
    p = Path(__file__).parent
    lines = read_input(p / filename, parse_line)
    lines = transform_input(lines)

    part1(lines)
    part2(lines)


def parse_line(line: str) -> str:
    return line


def transform_input(lines: list) -> Any:
    return lines


def part1(lines: list):
    answer = 0

    print(f"Part 2: {answer}")


def part2(lines: list):
    answer = 0

    print(f"Part 2: {answer}")


if __name__ == '__main__':
    print('********** Example ************')
    main('example.txt')
    print()
    print('********** Input ************')
    main('input.txt')
