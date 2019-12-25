import re
from collections import deque
import unittest


deal_re = re.compile(r'deal into new stack')
inc_re = re.compile(r'deal with increment (\d+)')
cut_re = re.compile(r'cut (-?\d+)')


class LinearFn:
    def __init__(self, deck_size):
        self.fns = []
        self.deck_size = deck_size

    def deal(self):
        # Input:  0 1 2 3 4
        # Output: 4 3 2 1 0
        self.fns.append((-1, self.deck_size-1))

    def cut(self, n):
        """ Inverted cut is a pos=shift right, neg=shift left """
        # Input: 0 1 2 3 4
        # Cut 2: 3 4 0 1 2
        self.fns.append((1, n))

    def increment(self, n):
        pass

    def apply(self, pos):
        x = pos
        for a, b in self.fns[::-1]:
            x = a * x + b

        return x % self.deck_size

def part1(lines, n):
    deck = deque(range(n))

    for line in lines:
        m = deal_re.match(line)
        if m:
            deck.reverse()

        m = cut_re.match(line)
        if m:
            cut = int(m.group(1))
            deck.rotate(cut * -1)

        m = inc_re.match(line)
        if m:
            increment = int(m.group(1))
            new_deck = [None] * n
            i = 0
            while len(deck) > 0:
                new_deck[i] = deck.popleft()
                i = (i + increment) % n

            deck = deque(new_deck)

    return deck


def part2(lines, deck_size):
    lfn = LinearFn(deck_size)

    # Loop through the lines in reverse, building a combined linear function
    for line in lines[::-1]:
        m = deal_re.match(line)
        if m:
            lfn.deal()

        m = cut_re.match(line)
        if m:
            cut = int(m.group(1))
            lfn.cut(cut)

        m = inc_re.match(line)
        if m:
            increment = int(m.group(1))
            lfn.increment(increment)

    print(lfn.apply(5))


if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.readlines()

    deck_ = part1(lines, 10)
    print(deck_)
    # print(deck_.index(2019))

