from inspect import signature
import itertools


class Computer:
    def __init__(self, output=(0,), debug=False):
        self.ip = 0  # program counter
        self.exit = False
        self.commands_run = 0
        self.memory = None
        self.output = output
        self.debug = debug
        self.op_params = []
        self.op_output = []

    def load_memory(self, filename):
        """ Load memory and return it """
        with open(filename) as f:
            text = f.read()

            # The program is a series of comma separated int's, not lines
            text = text.strip()
            text = text.replace('\n', '').replace('\r', '').replace(' ', '').replace('\t', '')
            memory = [int(x) for x in text.split(',')]

            return memory

    def run(self, memory):
        """ Run the program and print the outputs """
        self.memory = memory
        self.ip = 0
        self.commands_run = 0
        self.program_init()

        print()
        self.print('-', [], [])

        # Loop until program exits
        self.exit = False
        while not self.exit:
            self.commands_run += 1
            if not 0 <= self.ip < len(self.memory):
                if self.debug:
                    print("Segfault!")
                return None

            # Split into command/args
            opcode = self.memory[self.ip]

            # Use reflection to figure out how many params the op takes
            operation = getattr(self, f'op_{opcode}')
            sig = signature(operation)
            param_size = len(sig.parameters)

            # Pull out the params
            parameters = self.memory[self.ip + 1:self.ip + 1 + param_size]
            if not all(0 <= p < len(self.memory) for p in parameters):
                print("Segfault on params")
                return None

            before = None
            if self.debug:
                before = [self._fmt(p) for p in parameters]

            # Run the command
            operation(*parameters)

            # Advance after processing op code
            self.print(opcode, parameters, before)
            self.ip += 1 + param_size

        return self.memory

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

    def print(self, op, params, before):
        """ Debug print status """
        if not self.debug:
            return

        prefix = f'{self.commands_run:>4} ({self.ip:>4})'

        after = [self._fmt(p) for p in params]
        param_str = ' '.join(str(p) for p in params)
        before_str = ' '.join(str(p) for p in before)
        after_str = ' '.join(str(p) for p in after)

        print(f"{prefix}: Op={op}, Params={param_str}, Before={before_str}, After={after_str}")

    def program_init(self):
        """ Override if you need to do something before the program starts """
        pass

    def op_99(self):
        self.exit = True

    def _fmt(self, p):
        if 0 <= p < len(self.memory):
            return self.memory[p]
        return '-'