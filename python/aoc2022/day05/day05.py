from collections import deque
from typing import NamedTuple
from pathlib import Path
import re
from util import read_input


class Step(NamedTuple):
    amount: int
    src: int
    tgt: int


def parse(p):
    text = p.read_text()
    raw_stacks, instructions = text.split('\n\n')

    # stacks
    stacks = []
    for row in reversed(raw_stacks.rstrip().split('\n')[:-1]):
        cargos = [row[i] for i in range(1, len(row), 4)]
        for idx, c in enumerate(cargos):
            if idx >= len(stacks):
                stacks.append([])
            if c != ' ':
                stacks[idx].append(c)

    # instructions
    steps = []
    for line in instructions.strip().split('\n'):
        line = line.strip()
        m = re.match(r'^move (?P<amt>\d+) from (?P<src>\d+) to (?P<tgt>\d+)$', line)
        steps.append(Step(
            amount=int(m.group('amt')),
            src=int(m.group('src'))-1,
            tgt=int(m.group('tgt'))-1,
        ))

    return stacks, steps


def part1(lines):
    stacks, steps = lines
    for step in steps:
        src, tgt = stacks[step.src], stacks[step.tgt]

        move = reversed(src[-step.amount:])

        stacks[step.src] = src[:-step.amount]
        tgt += move

    return ''.join(s[-1] for s in stacks if s)


def part2(lines):
    stacks, steps = lines
    for step in steps:
        src, tgt = stacks[step.src], stacks[step.tgt]

        move = src[-step.amount:]

        stacks[step.src] = src[:-step.amount]
        tgt += move

    return ''.join(s[-1] for s in stacks if s)


# Run
p = Path.cwd() / 'input.txt'
# p = Path.cwd() / 'sample.txt'

lines_ = parse(p)
answer1 = part1(lines_)
print(f'Part 1: {answer1}')

lines_ = parse(p)
answer2 = part2(lines_)
print(f'Part 2: {answer2}')
