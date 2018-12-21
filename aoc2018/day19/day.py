import re
from collections import namedtuple
from util import RateLogger
from pprint import pprint

AsmCommand = namedtuple('AsmCommand', 'opcode a b c')


class Assembler(object):
    def __init__(self):
        self.ip = -1
        self.ip_register = None
        self.registers = {i: 0 for i in xrange(6)}
        self.registers[0] = 1
        self.commands = []

    def load(self, fname):
        self.commands = []

        # #ip 4
        # addi 4 16 4
        ip_re = re.compile(r'#ip (\d+)')
        command_re = re.compile(r'(?P<cmd>\w+) (?P<a>\d+) (?P<b>\d+) (?P<c>\d+)')

        f = open(fname)
        for line in f:
            line = line.rstrip()

            m = ip_re.search(line)
            if m:
                self.ip_register = int(m.group(1))

            m = command_re.search(line)
            if m:
                self.commands.append(AsmCommand(m.group('cmd'), int(m.group('a')), int(m.group('b')), int(m.group('c'))))

    def run(self):
        self.lines_hit = [0] * len(self.commands)

        rate_logger = RateLogger(log_every_n=500000)
        while 0 <= self.ip + 1 < len(self.commands):
            self.ip += 1
            rate_logger.inc()

            # if rate_logger.total >= 100000000:
            #     break

            command = self.commands[self.ip]

            self.registers[self.ip_register] = self.ip
            self.lines_hit[self.ip] += 1
            getattr(self, command.opcode)(command.a, command.b, command.c)

            print "{:3} : {:4} {:2} {:2} {:2}  --> {:3} {:3} {:3} {:3} {:3} {:3} " \
                .format(self.ip, command.opcode, command.a, command.b, command.c,
                        *self.registers.values())
            #
            if self.ip != self.registers[self.ip_register]:
                print "Jumped {} -> {}".format(self.ip, self.registers[self.ip_register])

            self.ip = self.registers[self.ip_register]

    def addr(self, a, b, c):
        self.registers[c] = self.registers[a] + self.registers[b]

    def addi(self, a, b, c):
        self.registers[c] = self.registers[a] + b

    def mulr(self, a, b, c):
        self.registers[c] = self.registers[a] * self.registers[b]

    def muli(self, a, b, c):
        self.registers[c] = self.registers[a] * b

    def banr(self, a, b, c):
        self.registers[c] = self.registers[a] & self.registers[b]

    def bani(self, a, b, c):
        self.registers[c] = self.registers[a] & b

    def borr(self, a, b, c):
        self.registers[c] = self.registers[a] | self.registers[b]

    def bori(self, a, b, c):
        self.registers[c] = self.registers[a] | b

    def setr(self, a, b, c):
        self.registers[c] = self.registers[a]

    def seti(self, a, b, c):
        self.registers[c] = a

    def gtrr(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] > self.registers[b] else 0

    def gtri(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] > b else 0

    def gtir(self, a, b, c):
        self.registers[c] = 1 if a > self.registers[b] else 0

    def eqrr(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] == self.registers[b] else 0

    def eqri(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] == b else 0

    def eqir(self, a, b, c):
        self.registers[c] = 1 if a == self.registers[b] else 0


asm = Assembler()
asm.load('input.txt')
asm.run()

pprint(asm.registers.values())

for idx, cmd in enumerate(asm.commands):
    print "{:3} : {:4} {:2} {:2} {:2}  - {}" \
        .format(idx, cmd.opcode, cmd.a, cmd.b, cmd.c, asm.lines_hit[idx])
