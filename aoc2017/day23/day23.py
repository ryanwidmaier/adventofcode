from util import Assembler



class Day23Assembler(Assembler):
    def __init__(self):
        super(Day23Assembler, self).__init__()
        self.mults = 0

    def execute(self, command, register, value):
        inst_index = self.index
        if command == 'set':
            self.registers[register] = self.read_register(value)
        elif command == 'mul':
            self.registers[register] *= self.read_register(value)
            self.mults += 1
        elif command == 'sub':
            self.registers[register] -= self.read_register(value)
        elif command == 'jnz':
            if self.read_register(register) != 0:
                self.jump(value)

        # if self.instructions_run % 100000 == 0:
        print ""
        print "Instruction {}".format(self.instructions_run)
        print "{}: {} {} {}".format(inst_index, command, register, value)
        print self.registers

        if self.instructions_run > 100:
            raise ValueError()



asm = Day23Assembler()
asm.registers['a'] = 1
asm.parse('input.txt')
asm.run()


print "# mults: {}", asm.mults
