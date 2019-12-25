from inspect import signature
from collections import defaultdict
from util import GridCar, Coord


class IntComputer11:
    def __init__(self, id_='A', debug=False):
        self.id = id_
        self.ip = 0  # program counter
        self.relative_base = 0
        self.exit = False
        self.commands_run = 0
        self.memory = None
        self.debug = debug
        self.input = []
        self.output = None
        self.mode = []
        self.print_addresses = []
        self.before_memory = []

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
        self.memory = defaultdict(lambda: 0, dict(enumerate(memory_)))
        self.ip = 0
        self.relative_base = 0
        self.commands_run = 0
        self.exit = False

    def run_and_print(self):
        for output in self.run():
            print(output)

    def run(self):
        """ Run the program and print the outputs """
        self.print('-', 0, [], self.relative_base)

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
            parameters = [self.memory[i] for i in range(self.ip + 1, self.ip + 1 + param_size)]
            before_rb = self.relative_base

            # Run the command
            ip_before = self.ip
            operation(*parameters)

            # Advance after processing op code (if no jump)
            self.print(raw_opcode, ip_before, parameters, before_rb)
            if self.ip == ip_before:
                self.ip += 1 + param_size

            if self.output is not None:
                yield self.output
                self.output = None

    def print(self, op, ip, params, rb_before):
        """ Debug print status """
        if not self.debug:
            return

        prefix = f'{self.commands_run:>4} ({ip:>4}) ({rb_before:>4})'

        after_memory = self.translate(self.print_addresses)

        param_str = ' '.join(str(p) for p in params)
        before_str = ' '.join(str(p) for p in self.before_memory)
        after_str = ' '.join(str(p) for p in after_memory)

        print(f"{self.id} {prefix}: Op={op:>4}, Params= {param_str:<15}, Before= {before_str:<15}, After= {after_str}",
              flush=True)

    def translate(self, addrs):
        return [self.memory[x] if x is not None else '_' for x in addrs]

    def add_input(self, v):
        self.input.append(v)

    def adjust_op(self, opcode):
        prefix = f'{opcode:0>6}'
        self.mode = prefix[-3::-1]

        return opcode % 100

    def adjust_params(self, *params, write=False):
        result = []
        self.print_addresses = []

        for idx, val in enumerate(params):
            is_write = write and idx == len(params) - 1
            if is_write:
                # Position mode
                if self.mode[idx] == '0':
                    result.append(val)
                    self.print_addresses.append(val)
                # immediate mode
                elif self.mode[idx] == '1':
                    raise ValueError(f"Bad mode for output: 1")
                # relative mode
                elif self.mode[idx] == '2':
                    result.append(self.relative_base + val)
                    self.print_addresses.append(self.relative_base + val)
                else:
                    raise Exception(f"Bad mode: {self.mode}")
            else:
                # Position mode
                if self.mode[idx] == '0':
                    result.append(self.memory[val])
                    self.print_addresses.append(val)
                # immediate mode
                elif self.mode[idx] == '1':
                    result.append(val)
                    self.print_addresses.append(None)
                # relative mode
                elif self.mode[idx] == '2':
                    result.append(self.memory[self.relative_base+val])
                    self.print_addresses.append(self.relative_base + val)
                else:
                    raise Exception(f"Bad mode: {self.mode}")

        self.before_memory = self.translate(self.print_addresses)
        return tuple(result)

    def op_1(self, a, b, c):
        """ Addition """
        a, b, c = self.adjust_params(a, b, c, write=True)
        self.memory[c] = a + b

    def op_2(self, a, b, c):
        """ Multiplication """
        a, b, c = self.adjust_params(a, b, c, write=True)
        self.memory[c] = a * b

    def op_3(self, a):
        """ Accept input """
        a = self.adjust_params(a, write=True)[0]
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
        a, b, c = self.adjust_params(a, b, c, write=True)
        self.memory[c] = 1 if a < b else 0

    def op_8(self, a, b, c):
        """ Assign 1 if Equal """
        a, b, c = self.adjust_params(a, b, c, write=True)
        self.memory[c] = 1 if a == b else 0

    def op_9(self, a):
        a = self.adjust_params(a)[0]
        self.relative_base += a

    def op_99(self):
        """ Exit """
        self.exit = True
        print("Exiting")



def double(gen):
    ret = []
    for x in gen:
        ret.append(x)
        if len(ret) == 2:
            yield ret[0], ret[1]
            ret = []


def part1(comp):
    hull = {}
    comp.add_input(0)

    robot = GridCar(Coord(0, 0), 'north')
    for color, turn in double(comp.run()):
        hull[robot.position] = color

        # Turn and advance
        if turn == 0:
            robot.left()
        else:
            robot.right()
        robot.forward()

        comp.add_input(hull.get(robot.position, 0))

    print(len(hull))


def part2(comp):
    hull = {Coord(0, 0): 1}
    comp.add_input(1)

    robot = GridCar(Coord(0, 0), 'north')
    for color, turn in double(comp.run()):
        hull[robot.position] = color

        # Turn and advance
        if turn == 0:
            robot.left()
        else:
            robot.right()
        robot.forward()

        comp.add_input(hull.get(robot.position, 0))

    min_x = min(h.x for h in hull)
    min_y = min(h.y for h in hull)
    max_x = max(h.x for h in hull)
    max_y = max(h.y for h in hull)

    for y in range(max_y, min_y-1, -1):
        for x in range(min_x, max_x+1):
            c = '#' if hull.get(Coord(x, y), 0) == 1 else ' '
            print(c, end='')
        print()


comp = IntComputer11()
comp.program(comp.load_memory('input.txt'))

# part1(comp)
part2(comp)