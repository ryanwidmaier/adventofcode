from pprint import pprint
from datetime import datetime, timedelta

registers = {
    'a': 0,
    'b': 0,
    'c': 1,
    'd': 0
}

def get_value(key):
    if key in registers:
        return registers[key]
    return int(key)

instructions = list([l.rstrip() for l in open('input.txt')])

pc = 0
last = datetime.now()

while pc < len(instructions):
    tokens = instructions[pc].split()
    cmd, arg1 = tokens[0], tokens[1]

    if cmd == 'cpy':
        registers[tokens[2]] = get_value(arg1)
    elif cmd == 'inc':
        registers[arg1] += 1
    elif cmd == 'dec':
        registers[arg1] -= 1

    move = True
    if cmd == 'jnz' and get_value(arg1) != 0:
        pc += int(tokens[2])
    else:
        pc += 1

    if datetime.now() - last > timedelta(seconds=5):
        last = datetime.now()
        print "PC: {}  INS: '{}'  A: {}  B: {}  C: {}  D: {}"\
            .format(pc+1, instructions[pc], registers['a'], registers['b'], registers['c'], registers['d'])


pprint(registers)
