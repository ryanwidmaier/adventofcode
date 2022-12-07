import string
from collections import deque


class SoundAssembler(object):
    def __init__(self, commands, send_q, recv_q, prog):
        self.registers = {'p': prog}
        self.commands = commands
        self.last_sent = None
        self.send_q = send_q
        self.recv_q = recv_q
        self.prog = prog
        self.num_sent = 0
        self.idx = 0

    def read_register(self, value):
        if value in string.ascii_letters:
            if value not in self.registers:
                self.registers[value] = 0

            return self.registers[value]

        return int(value)

    def has_work(self):
        return not self.is_locked() and not self.is_terminated()

    def is_locked(self):
        return len(self.recv_q) == 0

    def is_terminated(self):
        return not (0 <= self.idx < len(self.commands))

    def run(self):
        while 0 <= self.idx < len(self.commands):
            tokens = self.commands[self.idx]
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
                self.send_q.append(self.read_register(reg))
                self.num_sent += 1
            elif cmd == 'add':
                self.registers[reg] += arg
            elif cmd == 'mul':
                self.registers[reg] *= arg
            elif cmd == 'mod':
                self.registers[reg] %= arg
            elif cmd == 'rcv':
                if len(self.recv_q) == 0:
                    return

                self.registers[cmd] = self.recv_q.pop()
            elif cmd == 'jgz':
                if self.read_register(reg) > 0:
                    self.idx += arg - 1

            self.idx += 1

        print "Prog {} TERMINATED".format(self.prog)


commands = []
fin = open('input.txt')
for line in fin:
    line = line.rstrip()
    commands.append(line.split())


q0, q1 = deque(), deque()

prog0 = SoundAssembler(commands, q1, q0, 0)
prog1 = SoundAssembler(commands, q0, q1, 1)

prog1.run()
prog0.run()

while prog0.has_work() or prog1.has_work():
    prog1.run()
    prog0.run()

prog1.run()
prog0.run()

print "0: {}".format(prog0.num_sent)
print "1: {}".format(prog1.num_sent)
