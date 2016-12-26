from pprint import pprint
from datetime import datetime, timedelta

registers = {
    'a': 7,
    'b': 0,
    'c': 0,
    'd': 0
}


def get_value(key):
    if key in registers:
        return registers[key]
    return int(key)


def toggle(line):
    tokens = instructions[pc].split()
    cmd = tokens[0]

    if cmd == 'inc':
        return ' '.join(['dec'] + tokens[1:])
    elif cmd == 'dec':
        return ' '.join(['inc'] + tokens[1:])
    elif cmd == 'jnz':
        return ' '.join(['cpy'] + tokens[1:])
    elif cmd in ('cpy', 'tgl'):
        return ' '.join(['jnz'] + tokens[1:])

    raise ValueError("Couldn't toggle {}".format(cmd))


instructions = list([l.rstrip() for l in open('input.txt')])

pc = 0
last = datetime.now()

while pc < len(instructions):
    tokens = instructions[pc].split()
    cmd, arg1 = tokens[0], tokens[1]

    if cmd == 'cpy':
        if tokens[2] in 'abcd':
            registers[tokens[2]] = get_value(arg1)
    elif cmd == 'inc':
        if arg1 in 'abcd':
            registers[arg1] += 1
    elif cmd == 'dec':
        if arg1 in 'abcd':
            registers[arg1] -= 1
    elif cmd == 'tgl':
        pos = get_value(arg1) + pc
        if 0 <= pos < len(instructions):
            instructions[pos] = toggle(instructions[pos])

    if cmd == 'jnz' and get_value(arg1) != 0:
        # TODO should we allow reading from registers for param 2?
        if tokens[2] not in 'abcd':
            pc += int(tokens[2])
        else:
            pc += 1
    else:
        pc += 1

    if datetime.now() - last > timedelta(seconds=5):
        last = datetime.now()
        print "PC: {}  INS: '{}'  A: {}  B: {}  C: {}  D: {}"\
            .format(pc+1, instructions[pc], registers['a'], registers['b'], registers['c'], registers['d'])


pprint(registers)
