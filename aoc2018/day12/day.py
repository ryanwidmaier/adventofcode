import re
from collections import defaultdict, namedtuple
import itertools
from util import argmax, argmin, a_star, Coord

# initial state: #..#.#..##......###...###
state_re = re.compile(r'initial state: ([.#]+)')
# ...## => #
rule_re = re.compile(r'([.#]+) => ([.#])')


class State(object):
    def __init__(self, state):
        self.left = -3
        self.state = '...' + state
        self.rules = {}  # pattern -> output

    def add_rule(self, pattern, output):
        self.rules[pattern] = output

    def tick(self):
        buffer = '..'
        for i in xrange(-4, len(self.state)):
            x = i + self.left

            subset = self.get_subset(x)
            buffer += self.rules.get(subset, '.')

        if buffer[0] == '#':
            self.state = buffer[2:]
            self.left -= 2
        elif buffer[1] == '#':
            self.state = buffer[1:]
            self.left -= 1
        else:
            self.state = buffer

    def get_subset(self, x):
        i = x - self.left
        if i < 2:
            subset = '.' * (2 - i) + self.state[:i + 5]
        elif i > len(self.state) - 3:
            diff = len(self.state) - 3 - i
            subset = self.state[i:i+] + '.'
        else:
            subset = self.state[i:i + 5]

def parse(fname):
    state = None

    with open('input.txt') as f:
        for line in f:
            line = line.rstrip()

            match = state_re.search(line)
            if match:
                state = State(match.group(1))

            match = rule_re.search(line)
            if match:
                state.add_rule(match.group(1), match.group(2))

    return state


state = parse('example.txt')
for t in xrange(20):
    state.tick()
    print state.state