from inspect import signature
import itertools
from collections import defaultdict


class Computer:
    def __init__(self, debug=False):
        self.ip = 0  # program counter
        self.exit = False
        self.commands_run = 0
        self.memory = None
        self.initial_memory = None
        self.output = None
        self.debug = debug
        self.op_params = []
        self.op_output = []

    @staticmethod
    def load_memory(filename):
        """ Load memory and return it """
        with open(filename) as f:
            text = f.read()

            # The program is a series of comma separated int's, not lines
            text = text.strip()
            text = text.replace('\n', '').replace('\r', '').replace(' ', '').replace('\t', '')
            memory = [int(x) for x in text.split(',')]

            return memory

    def program(self, memory):
        self.initial_memory = memory.copy()
        self.memory = memory.copy()
        self.ip = 0
        self.commands_run = 0
        self.program_init()

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

        return None

    def find_inputs(self, init_memory, input_positions, desired, output_position=0, upper=1000):
        """ Search for inputs that produce the desired output """
        for input_vals in itertools.product(*[range(0, upper) for _ in input_positions]):
            # Set input values
            memory = init_memory.copy()
            for pos, val in zip(input_positions, input_vals):
                memory[pos] = val

            # Run the program
            memory = self.run(memory.copy())
            if memory is None:
                continue

            print(f"{output_position} = {memory[output_position]} when:")
            for pos in input_positions:
                print(f"  {pos} <- {memory[pos]}")

            # Check for success
            if memory[output_position] == desired:
                break
        else:
            print("Not found!")

    def print(self, op, ip, params, before):
        """ Debug print status """
        if not self.debug:
            return

        prefix = f'{self.commands_run:>4} ({ip:>4})'

        after = [self._fmt(p, i) for i, p in enumerate(params)]
        param_str = ' '.join(str(p) for p in params)
        before_str = ' '.join(str(p) for p in before)
        after_str = ' '.join(str(p) for p in after)

        print(f"{prefix}: Op={op:>4}, Params= {param_str:<15}, Before= {before_str:<15}, After= {after_str}")

    def _fmt(self, p, i):
        if 0 <= p < len(self.memory):
            return self.memory[p]
        return '-'

    def program_init(self):
        """ Override if you need to do something before the program starts """
        pass

    def adjust_op(self, opcode):
        return opcode

    def adjust_params(self, params):
        return params

    def op_99(self):
        self.exit = True
        print("Exiting")



class IntComputerFinal:
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
        self.initial_memory = None

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
        self.initial_memory = memory_.copy()
        self.restart()

    def restart(self):
        self.memory = defaultdict(lambda: 0, dict(enumerate(self.initial_memory)))
        self.ip = 0
        self.relative_base = 0
        self.commands_run = 0
        self.exit = False
        self.input = []
        self.output = None

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

            while opcode == 3 and len(self.input) == 0:
                yield None

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

    def add_input(self, *v):
        self.input += v

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
