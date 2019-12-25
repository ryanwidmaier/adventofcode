from aoc2019.int_code import Computer


class Day05Computer(Computer):
    def __init__(self, debug=False):
        super().__init__(debug=debug)
        self.input = []
        self.output = None
        self.mode = []

    def add_input(self, v):
        self.input.append(v)

    def op_1(self, a, b, c):
        a, b = self.adjust_params(a, b)
        self.memory[c] = a + b

    def op_2(self, a, b, c):
        a, b = self.adjust_params(a, b)
        self.memory[c] = a * b

    def op_3(self, a):
        self.memory[a] = self.input[0]
        self.input = self.input[1:]

    def op_4(self, a):
        a = self.adjust_params(a)[0]
        self.output = a
        print(self.output)

    def op_5(self, a, b):
        a, b = self.adjust_params(a, b)
        if a != 0:
            self.ip = b

    def op_6(self, a, b):
        a, b = self.adjust_params(a, b)
        if a == 0:
            self.ip = b

    def op_7(self, a, b, c):
        a, b = self.adjust_params(a, b)
        self.memory[c] = 1 if a < b else 0

    def op_8(self, a, b, c):
        a, b = self.adjust_params(a, b)
        self.memory[c] = 1 if a == b else 0

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


if __name__ == '__main__':
    co = Day05Computer()
    co.add_input(5)
    mem = co.load_memory('input.txt')
    co.run(mem)