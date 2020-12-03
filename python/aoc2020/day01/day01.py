import sys
import itertools
import functools


def solve(lines, n):
    for x in itertools.combinations(lines, n):
        if sum(x) == 2020:
            return functools.reduce(lambda a, b: a*b, x)


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        lines = [int(l.strip()) for l in f.readlines()]

    print("Part1: ", solve(lines, 2))
    print("Part2: ", solve(lines, 3))