from pathlib import Path
from util import read_input

winner = {
    ('A', 'X'): 3,  # rock
    ('A', 'Y'): 6,
    ('A', 'Z'): 0,
    ('B', 'X'): 0,  # paper
    ('B', 'Y'): 3,
    ('B', 'Z'): 6,
    ('C', 'X'): 6,  # scissors
    ('C', 'Y'): 0,
    ('C', 'Z'): 3,
}


def score_round(elf, you):
    return winner[(elf, you)] + ord(you) - ord('X') + 1

def part2(elf, outcome):
    target = (ord(outcome) - ord('X')) * 3
    you = [k[1] for k, v in winner.items() if k[0] == elf and v == target]
    return score_round(elf, you[0])


lines = read_input(Path.cwd() / 'input.txt', lambda x: x.split())
part1 = sum(score_round(*line) for line in lines)
print(f"Part1: {part1}")

part2_ = sum(part2(*line) for line in lines)
print(f"Part2: {part2_}")
