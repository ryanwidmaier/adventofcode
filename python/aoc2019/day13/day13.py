from inspect import signature
from collections import defaultdict
from util import GridCar, Coord


class IntComputer12:
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


def output(gen, cnt=1):
    ret = []
    for x in gen:
        ret.append(x)
        if len(ret) == cnt:
            yield tuple(ret)
            ret = []


def print_screen(screen):
    min_x = min(h.x for h in screen)
    min_y = min(h.y for h in screen)
    max_x = max(h.x for h in screen)
    max_y = max(h.y for h in screen)

    translate = {
        0: ' ',
        1: 'W',
        2: '=',
        3: '-',
        4: 'o',
    }

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            c = screen.get(Coord(x, y), 0)
            sprite = translate[c]
            print(sprite, end='')

        print()


def part1(comp):
    screen = {}

    for x, y, tile in output(comp.run(), cnt=3):
        screen[Coord(x, y)] = tile
        print_screen(screen)

    print(len([t for t in screen.values() if t == 2]))


def part2(comp):
    screen = {}
    score = None
    initial = True

    # free play
    comp.memory[0] = 2
    for idx, (x, y, tile) in enumerate(output(comp.run(), cnt=3)):
        if x == -1 and y == 0:
            score = tile
            print(f'Score: {score}')
        else:
            screen[Coord(x, y)] = tile

            # if idx > 1054:
            #     print(x, y, tile)
            #     print_screen(screen)

        # When the ball moves, we need to move the paddle
        ball = [c for c, x in screen.items() if x == 4]
        paddle = [c for c, x in screen.items() if x == 3]

        if (initial or tile == 4) and score is not None:
            initial = False
            ball = ball[0].x
            paddle = paddle[0].x

            if paddle < ball:
                comp.add_input(1)
            elif paddle > ball:
                comp.add_input(-1)
            else:
                comp.add_input(0)

    print(score)


comp = IntComputer12()
comp.program(comp.load_memory('input.txt'))

# part1(comp)
part2(comp)