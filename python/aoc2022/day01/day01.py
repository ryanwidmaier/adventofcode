from pathlib import Path
from util import argmax

p = Path('input.txt')


elves = [0]

with p.open() as f:
    for line in f:
        line = line.strip()
        if not line:
            elves.append(0)
        else:
            elves[-1] += int(line)


max_idx = argmax(elves)
print(f"Part 1: {max_idx}, w/ {elves[max_idx]}")


elves = sorted(elves, reverse=True)

print(f"Part2: {sum(elves[:3])}")


part1 = max(sum([int(c) for c in elf.split('\n')]) for elf in Path('sample.txt').read_text().strip().split('\n\n'))
part2 = sum(
    sorted(
        sum([int(c) for c in elf.split('\n')])
        for elf in Path('sample.txt').read_text().strip().split('\n\n')
    )[-3:],
)

print(part1)
print(part2)
