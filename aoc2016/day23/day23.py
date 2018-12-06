from pprint import pprint
from datetime import datetime, timedelta

registers = {
    'a': 12,
    'b': 0,
    'c': 0,
    'd': 0
}


def get_value(key):
    if key in registers:
        return registers[key]
    return int(key)


def toggle(pc_, line):
    tokens_ = line.split()
    cmd = tokens_[0]

    after = ''
    if cmd == 'inc':
        after = ' '.join(['dec'] + tokens_[1:])
    elif cmd in ('dec', 'tgl'):
        after = ' '.join(['inc'] + tokens_[1:])
    elif cmd == 'jnz':
        after = ' '.join(['cpy'] + tokens_[1:])
    elif cmd in ('cpy',):
        after = ' '.join(['jnz'] + tokens_[1:])

    print "Toggle {}: '{}' -> '{}'".format(pc_+1, line, after)
    return after


instructions = list([l.rstrip() for l in open('input.txt')])

pc = 0
last = datetime.now()

while pc < len(instructions):
    line = instructions[pc]
    line_pc = pc

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
            instructions[pos] = toggle(pos, instructions[pos])

    if cmd == 'jnz' and get_value(arg1) != 0:
        # TODO should we allow reading from registers for param 2?
        pc += get_value(tokens[2])
    else:
        pc += 1

    if datetime.now() - last > timedelta(seconds=5):
        last = datetime.now()
        print "PC: {:3d}  INS: '{:20s}'  A: {:10d}  B: {:10d}  C: {:10d}  D: {:10d}"\
          .format(line_pc+1, line, registers['a'], registers['b'], registers['c'], registers['d'])


pprint(registers)
