from aoc2019.int_code import Computer


class Day02Computer(Computer):
    def op_1(self, a, b, c):
        """
        Opcode 1 adds together numbers read from two positions and stores the result in a third position. The three
        integers immediately after the opcode tell you these three positions - the first two indicate the positions
        from which you should read the input values, and the third indicates the position at which the output should
        be stored.
        """
        self.memory[c] = self.memory[a] + self.memory[b]
        self.op_params = [a, b]
        self.op_output = [c]

    def op_2(self, a, b, c):
        """
        Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of adding them. Again, the
        three integers after the opcode indicate where the inputs and outputs are, not their values.
        """
        self.memory[c] = self.memory[a] * self.memory[b]
        self.op_params = [a, b]
        self.op_output = [c]


computer = Day02Computer(debug=False)
init_memory = computer.load_memory('input.txt')

computer.find_inputs(init_memory, [1, 2], 19690720, upper=100)
