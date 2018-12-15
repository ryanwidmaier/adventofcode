import re
from collections import defaultdict, namedtuple
import itertools
from util import argmax, argmin, a_star, Coord, RateLogger

# initial state: #..#.#..##......###...###
state_re = re.compile(r'initial state: ([.#]+)')
# ...## => #
rule_re = re.compile(r'([.#]+) => ([.#])')


class State(object):
    def __init__(self, state):
        self.left = 0
        self.state = state
        self.rules = {}  # pattern -> output

    def add_rule(self, pattern, output):
        self.rules[pattern] = output

    def tick(self):
        buffer = ''
        # print self.state
        for idx, subset in enumerate(self._loop()):
            buffer += self.rules.get(subset, '.')
            # print "{} {:3} {}".format(subset, idx + self.left - 2, buffer[-1])

        start, end = buffer.index('#'), buffer.rindex('#')
        offset = start - 2

        self.state = buffer[start:end+1]
        self.left += offset

    def _loop(self):
        for i in xrange(1, 5):
            yield '.' * (5 - i) + self.state[:i]

        for i in xrange(len(self.state) - 4):
            yield self.state[i:i+5]

        for i in xrange(4, 0, -1):
            yield self.state[len(self.state)-i:] + '.' * (5 - i)

    def anchored_state(self, left):
        pad = max(self.left - left, 0)
        start = max(self.left, 0)
        return '.' * pad + self.state[start:]

    def value(self):
        return sum([self.left + i for i, pot in enumerate(self.state) if pot == '#'])


def parse(fname):
    state = None

    with open(fname) as f:
        for line in f:
            line = line.rstrip()

            match = state_re.search(line)
            if match:
                state = State(match.group(1))

            match = rule_re.search(line)
            if match:
                state.add_rule(match.group(1), match.group(2))

    return state

states = set()

state = parse('input.txt')
repeat = False

for t in xrange(170):
    state.tick()

    if not repeat and state.state in states:
        print "Found repeat at {}".format(t)
        print "{} {} {}".format(state.left, state.value(), state.state)

    states.add(state.state)

print ''
pot_count = len(list(s for s in state.state if s == '#'))
print pot_count

print 169, state.value() + (169 - 169) * pot_count
print 170, state.value() + (170 - 169) * pot_count
print 50000000000, state.value() + (50000000000 - 169 - 1) * pot_count


print 169 - 117