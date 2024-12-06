from collections import defaultdict
import string
from typing import NamedTuple, Any


class AsmCommand(NamedTuple):
    cmd: str
    reg: str
    value: Any


class Assembler:
    """
    Framework for implementing assembly command simulation.  Override execute command to handle the different
    commands.
    """

    def __init__(self):
        self.registers = defaultdict(lambda: 0)
        self.commands = []
        self.index = 0
        self.instructions_run = 0

    def parse(self, filename):
        fin = open(filename)
        for line in fin:
            line = line.rstrip()

            tokens = line.split()

            cmd = tokens[0]
            reg = tokens[1] if len(tokens) > 1 else None
            val = tokens[2] if len(tokens) > 2 else None

            self.commands.append(AsmCommand(cmd, reg, val))

    def read_register(self, register):
        """ Return the value of a register, or the value if it is a literal """
        if register in string.ascii_letters:
            return self.registers[register]

        return int(register)

    def run(self):
        """ Run the simulation """
        while 0 <= self.index < len(self.commands):
            command = self.commands[self.index]

            self.execute(command.cmd, command.reg, command.value)
            self.index += 1
            self.instructions_run += 1

    def execute(self, command, register, value):
        pass

    def jump(self, amount):
        self.index += self.read_register(amount) - 1  # -1 b/c we always do + 1 after each instruction
