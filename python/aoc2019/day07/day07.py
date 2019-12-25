from aoc2019.day05.day05 import Day05Computer
import itertools
from queue import Queue

from inspect import signature
import itertools


class IntComputer:
    def __init__(self, id_='A', debug=False):
        self.id = id_
        self.ip = 0  # program counter
        self.exit = False
        self.commands_run = 0
        self.memory = None
        self.debug = debug
        self.input = []
        self.output = None
        self.mode = []

    @staticmethod
    def load_memory(filename):
        """ Load memory and return it """
        with open(filename) as f:
            text = f.read()

            # The program is a series of comma separated int's, not lines
            text = text.strip()
            text = text.replace('\n', '').replace('\r', '').replace(' ', '').replace('\t', '')
            return [int(x) for x in text.split(',')]

    def program(self, memory_):
        self.memory = memory_.copy()
        self.ip = 0
        self.commands_run = 0
        self.exit = False

    def run(self):
        """ Run the program and print the outputs """
        self.print('-', 0, [], [])

        # Loop until program exits
        self.exit = False
        while not self.exit:
            self.commands_run += 1
            if not 0 <= self.ip < len(self.memory):
                if self.debug:
                    print("Segfault!")
                return None

            # Split into command/args
            raw_opcode = self.memory[self.ip]
            opcode = self.adjust_op(raw_opcode)

            # Use reflection to figure out how many params the op takes
            operation = getattr(self, f'op_{opcode}')
            sig = signature(operation)
            param_size = len(sig.parameters)

            # Pull out the params
            parameters = self.memory[self.ip + 1:self.ip + 1 + param_size]

            before = None
            if self.debug:
                before = [self._fmt(p, i) for i, p in enumerate(parameters)]

            # Run the command
            ip_before = self.ip
            operation(*parameters)

            # Advance after processing op code (if no jump)
            self.print(raw_opcode, ip_before, parameters, before)
            if self.ip == ip_before:
                self.ip += 1 + param_size

            if self.output is not None:
                yield self.output
                self.output = None

        # raise StopIteration()

    def print(self, op, ip, params, before):
        """ Debug print status """
        if not self.debug:
            return

        prefix = f'{self.commands_run:>4} ({ip:>4})'

        after = [self._fmt(p, i) for i, p in enumerate(params)]
        param_str = ' '.join(str(p) for p in params)
        before_str = ' '.join(str(p) for p in before)
        after_str = ' '.join(str(p) for p in after)

        print(f"{self.id} {prefix}: Op={op:>4}, Params= {param_str:<15}, Before= {before_str:<15}, After= {after_str}")

    def _fmt(self, p, i):
        if 0 <= p < len(self.memory):
            return self.memory[p]
        return '-'

    def add_input(self, v):
        self.input.append(v)

    def adjust_op(self, opcode):
        prefix = f'{opcode:0>6}'
        self.mode = prefix[-3::-1]

        return opcode % 100

    def adjust_params(self, *params):
        result = []
        for idx, val in enumerate(params):
            # Position mode
            if self.mode[idx] == '0':
                result.append(self.memory[val])

            # immediate mode
            elif self.mode[idx] == '1':
                result.append(val)

            else:
                raise Exception(f"Bad mode: {self.mode}")

        return tuple(result)

    def op_1(self, a, b, c):
        """ Addition """
        a, b = self.adjust_params(a, b)
        self.memory[c] = a + b

    def op_2(self, a, b, c):
        """ Multiplication """
        a, b = self.adjust_params(a, b)
        self.memory[c] = a * b

    def op_3(self, a):
        """ Accept input """
        self.memory[a] = self.input[0]
        self.input = self.input[1:]

    def op_4(self, a):
        """ Emit Output """
        a = self.adjust_params(a)[0]
        self.output = a

    def op_5(self, a, b):
        """ Jump if true """
        a, b = self.adjust_params(a, b)
        if a != 0:
            self.ip = b

    def op_6(self, a, b):
        """ Jump if False """
        a, b = self.adjust_params(a, b)
        if a == 0:
            self.ip = b

    def op_7(self, a, b, c):
        """ Assign 1 if Less than """
        a, b = self.adjust_params(a, b)
        self.memory[c] = 1 if a < b else 0

    def op_8(self, a, b, c):
        """ Assign 1 if Equal """
        a, b = self.adjust_params(a, b)
        self.memory[c] = 1 if a == b else 0

    def op_99(self):
        """ Exit """
        self.exit = True
        print("Exiting")


memory = IntComputer.load_memory('input.txt')


def part1():
    max_permutation = 0

    for phases in itertools.permutations([0, 1, 2, 3, 4]):
        print()
        print(f"Phases: {phases}")

        computers = []
        for ph in phases:
            computers.append(IntComputer(debug=False))
            computers[-1].program(memory)
            computers[-1].add_input(ph)

        output = 0
        try:
            for amp in computers:
                amp.add_input(output)

                output = next(amp.run())
                print(output)

        except StopIteration:
            pass

        print(f"Output: {output}")
        max_permutation = max(max_permutation, output)

    print(max_permutation)


def part2():
    max_permutation = 0

    for phases in itertools.permutations([5, 6, 7, 8, 9]):
        print()
        print(f"Phases: {phases}")

        # Create the computers
        output = 0
        computers = []
        for ph in phases:
            comp = IntComputer(debug=False)
            comp.program(memory)
            comp.add_input(ph)

            computers.append((comp, comp.run()))

        # Feedback loop
        idx = 0
        try:
            while True:
                amp, fn = computers[idx]
                amp.add_input(output)

                output = next(fn)
                idx = (idx + 1) % len(computers)
        except StopIteration:
            pass

        print(f"Output: {output}")
        max_permutation = max(max_permutation, output)

    print(max_permutation)

part2()