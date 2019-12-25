from itertools import cycle
from functools import reduce


def transform(i):
    ii = i + 1
    return ([0] * ii) + ([1] * ii) + ([0] * ii) + ([-1] * ii)


def digit(input_sequence, index):
    tx = cycle(transform(index))
    next(tx)  # skip the first

    aa = list(zip(input_sequence, tx))

    total = sum(x * y for x, y in aa)
    return abs(total) % 10


def apply(seq, count):
    for i in range(count):
        seq = [digit(seq, d) for d, _ in enumerate(seq)]

    return seq


def part1(seq):
    result = apply(seq, 100)
    print(''.join(str(x) for x in result[:8]))


def part2(seq):
    offset = reduce(lambda a, b: a * 10 + b, seq[:7])

    mult = 10000 - offset // len(seq)
    offset = offset % len(seq)
    seq = seq * mult

    for _round in range(100):
        total = 0
        for i in range(1, len(seq)+1):
            total += seq[-i]
            seq[-i] = total % 10

    message = seq[offset:offset+8]
    print(''.join(str(x) for x in message))


with open('input.txt') as f:
    data = f.read().strip()
    data = [int(ch) for ch in data]

# data = [1, 2, 3, 4, 5, 6, 7, 8]
part2(data)