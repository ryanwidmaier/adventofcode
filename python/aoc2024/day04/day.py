import re
import sys
from pathlib import Path

from util.grid import Coord, print_dict_grid
from util.io import read_input


Grid = dict[Coord, str]

parse_re = re.compile(r'')


def main(filename: str):
    p = Path(__file__).parent
    lines = read_input(p / filename, parse_line)
    grid = transform_input(lines)
    part1(grid)
    part2(grid)


def parse_line(line: str) -> str:
    return line


def transform_input(lines: list) -> Grid:
    return {
        Coord(x, y): val
        for y, row in enumerate(lines)
        for x, val in enumerate(row)
    }


def part1(grid):
    found = 0
    offsets = Coord(0, 0).neighbors(True)
    for dir in offsets:
        for pos, val in grid.items():
            if val != 'X':
                continue

            word = grid.get(pos)
            word += grid.get(pos + dir, ' ')
            word += grid.get(pos + dir*2, ' ')
            word += grid.get(pos + dir*3, ' ')

            if word == 'XMAS':
                found += 1

    print(f"Part 1: {found}")


def part2(grid):
    answer = 0
    debug = {}
    for pos, val in grid.items():
        debug[pos] = '.'
        if val != 'A':
            continue

        bl = grid.get(pos + Coord(-1, -1), ' ')
        br = grid.get(pos + Coord(1, -1), ' ')
        ur = grid.get(pos + Coord(1, 1), ' ')
        ul = grid.get(pos + Coord(-1, 1), ' ')

        check = ''.join(sorted(bl + br + ul + ur))
        if check == 'MMSS' and bl != ur and br != ul:
            debug[pos] = 'A'
            answer += 1

    print(f"Part 2: {answer}")


if __name__ == '__main__':
    print('********** Example ************')
    main('example.txt')
    print()
    print('********** Input ************')
    main('input.txt')
