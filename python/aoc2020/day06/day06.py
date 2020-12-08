from pathlib import Path
import string

def part1(groups):
    total = 0
    for group in groups:
        s = set()
        for line in group:
            s.update(line)
        total += len(s)

    print(f"Part 1: {total}")


def part2(groups):
    total = 0
    for group in groups:
        s = set(string.ascii_lowercase)
        for line in group:
            s2 = {ch for ch in line}
            s = s.intersection(s2)

        total += len(s)

    print(f"Part 2: {total}")

base = '/Users/rwidmaier/repos/misc/adventofcode/python/aoc2020/day06/'
f = 'input.txt'


groups = open(Path(base) / f).read().split('\n\n')
groups = [x.split('\n') for x in groups]
part1(groups)
part2(groups)