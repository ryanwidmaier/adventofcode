import re
from collections import defaultdict, namedtuple
import itertools
from util import argmax, argmin, a_star, Coord
import operator

AsmCommand = namedtuple('AsmCommand', 'opcode a b output')
Observation = namedtuple('Observation', 'before command after')


class Assembler(object):
    def __init__(self, commands):
        self.registers = defaultdict(lambda: 0)
        self.commands = commands

    def run(self, command):
        cmd = self.commands[command.opcode]

        suffix = cmd[-2:] if cmd.startswith('gt') or cmd.startswith('eq') else cmd[-1:]

        a = command.a if (len(suffix) > 1 or cmd.startswith('set')) and suffix[0] == 'i' else self.registers[command.a]
        b = command.b if suffix[-1] == 'i' else self.registers[command.b]

        operators = {
            'add': operator.add,
            'mul': operator.mul,
            'ban': operator.and_,
            'bor': operator.or_,
            'set': lambda a, b: a,
            'gtr': lambda a, b: 1 if a > b else 0,
            'gti': lambda a, b: 1 if a > b else 0,
            'eqr': lambda a, b: 1 if a == b else 0,
            'eqi': lambda a, b: 1 if a == b else 0
        }

        self.registers[command.output] = operators[cmd[:3]](a, b)

    @staticmethod
    def try_commands(obs):
        math_operators = {
            'add': operator.add,
            'mul': operator.mul,
            'ban': operator.and_,
            'bor': operator.or_,
            'set': lambda a, b: a
        }

        comp_operators = {
            'gt': lambda a, b: 1 if a > b else 0,
            'eq': lambda a, b: 1 if a == b else 0
        }

        possibles = set()
        for op_list, suffix_list in [(math_operators, ['r', 'i']),
                                     (comp_operators, ['ir', 'ri', 'rr'])]:
            for name, op in op_list.iteritems():
                for suffix in suffix_list:
                    # Reset state
                    state = obs.before.copy()
                    name_ = name + suffix

                    # Get a and b
                    a = obs.command.a if (len(suffix) > 1 or name == 'set') and suffix[0] == 'i' else state[obs.command.a]
                    b = obs.command.b if suffix[-1] == 'i' else state[obs.command.b]

                    state[obs.command.output] = op(a, b)

                    if state == obs.after:
                        possibles.add(name_)

        return possibles


def load_part1():
    before_re = re.compile(r'Before: \[(\d+), (\d+), (\d+), (\d+)\]')
    after_re =  re.compile(r'After:  \[(\d+), (\d+), (\d+), (\d+)\]')
    command_re = re.compile(r'^(\d+) (\d+) (\d+) (\d+)')

    all_observations = []

    f = open('input_part1.txt')
    for line in f:
        line = line.rstrip()

        m = before_re.search(line)
        if m:
            before = {idx: int(g) for idx, g in enumerate(m.groups())}

        m = command_re.search(line)
        if m:
            command = AsmCommand(*[int(g) for g in m.groups()])

        m = after_re.search(line)
        if m:
            after = {idx: int(g) for idx, g in enumerate(m.groups())}
            observation = Observation(before, command, after)
            all_observations.append(observation)

    return all_observations


def load_part2():
    command_re = re.compile(r'^(\d+) (\d+) (\d+) (\d+)')

    program = []

    f = open('input_part2.txt')
    for line in f:
        line = line.rstrip()

        m = command_re.search(line)
        if m:
            program.append(AsmCommand(*[int(g) for g in m.groups()]))

    return program


def process_part1(observations):
    count = sum(len(Assembler.try_commands(obs)) >= 3 for obs in observations)
    print "Part 1: {}".format(count)


def deduce(observations):
    known = {}

    while True:
        for obs in observations:
            possible = Assembler.try_commands(obs)

            # Remove known
            for cmd in known.itervalues():
                if cmd in possible:
                    possible.remove(cmd)

            if len(possible) == 1:
                new_known = list(possible)[0]
                known[obs.command.opcode] = new_known
                print "{} is {}".format(obs.command.opcode, new_known)

                if len(known) == 16:
                    return known


def process_part2(commands, program):
    asm = Assembler(commands)
    for line in program:
        asm.run(line)

    print asm.registers


process_part1(load_part1())
process_part2(deduce(load_part1()), load_part2())
