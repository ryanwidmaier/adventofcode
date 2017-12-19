import string
from collections import deque


class SoundAssembler(object):
    def __init__(self, commands, send_q, recv_q):
        self.registers = {}
        self.commands = commands
        self.last_sent = None
        self.send_q = send_q
        self.recv_q = recv_q

    def read_register(self, value):
        if value in string.ascii_letters:
            if value not in self.registers:
                self.registers[value] = 0

            return self.registers[value]

        return int(value)

    def run(self):
        idx = 0
        while 0 <= idx < len(self.commands):
            tokens = self.commands[idx]
            cmd, reg = tokens[0], tokens[1]

            # Get/parse the arg
            arg = None
            if len(tokens) >= 3:
                arg = self.read_register(tokens[2])

            # Ensure registers init'ed to 0
            self.registers[reg] = self.registers.get(reg, 0)

            # Handle the commands
            if cmd == 'set':
                self.registers[reg] = arg
            elif cmd == 'snd':
                self.last_sent = self.read_register(reg)
            elif cmd == 'add':
                self.registers[reg] += arg
            elif cmd == 'mul':
                self.registers[reg] *= arg
            elif cmd == 'mod':
                self.registers[reg] %= arg
            elif cmd == 'rcv':
                if self.read_register(reg) != 0:
                    return self.last_sent
            elif cmd == 'jgz':
                if self.read_register(reg) > 0:
                    idx += (arg - 1)

            idx += 1


commands = []
fin = open('input.txt')
for line in fin:
    line = line.rstrip()
    commands.append(line.split())

target = SoundAssembler(commands)
recovered = target.run()

print target.registers
print recovered