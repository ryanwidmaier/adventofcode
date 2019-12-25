from aoc2019.int_code import IntComputerFinal


def ascii_command(comp, cmd):
    for ch in cmd:
        comp.add_input(ord(ch))
    comp.add_input(10)


def test(a=False, b=False, c=False, d=False, e=False, t=False, j=False, desired=False):
    # IF D == True AND (A == False or B == False or C == False)
    #   jump

    # t = true if hole at 1,2, or 3: not all(A, B, C)
    #          & |
    # F F F -> F F  T
    # T T F -> F T  T
    # T T T -> T T  F

    # assign t & j = false
    t = not j
    t &= j
    j &= t

    # t = True, if hole at any A, B, C
    t |= a
    t &= b
    t &= c
    t = not t

    # Combine T (hole at 1-3, not all(A, B, C))
    j |= t
    j &= d
    j &= e

    good = ' ' if j == desired else 'FAIL'
    a = 'T' if a else 'F'
    b = 'T' if b else 'F'
    c = 'T' if c else 'F'
    d = 'T' if d else 'F'
    t = 'T' if t else 'F'
    j = 'T' if j else 'F'

    print(f"{a}{b}{c}{d}, T={t}, J={j}   {good}")


# Jumps
test(a=False, b=False, c=False, d=True,  e=True,  t=False, j=False, desired=True)
test(a=True,  b=True,  c=False, d=True,  e=True,  t=False, j=False, desired=True)
test(a=True,  b=False, c=True,  d=True,  e=True,  t=False, j=False, desired=True)
test(a=True,  b=False, c=False, d=True,  e=True,  t=False, j=False, desired=True)

# Don't jumps
test(a=True,  b=True, c=True,   d=True,  e=True,  t=False, j=False, desired=False)
test(a=True,  b=True, c=True,   d=False, e=True,  t=False, j=False, desired=False)
test(a=True,  b=True, c=False,  d=True,  e=False, t=False, j=False, desired=False)


def part1(comp):
    def command(cmd):
        ascii_command(comp, cmd)

    prog = comp.run()

    # Read registers:
    #  A - 1 fwd
    #  B - 2 fwd
    #  C - 3 fwd
    #  D - 4 fwd
    # Write registers:
    #  T - temporary (start=false)
    #  J - jump if true (start=false)
    # AND X Y
    # OR X Y
    # NOT X Y

    # JUMP - LAND + 4

    # assign t & j = false
    command('NOT J T')
    command('AND J T')
    command('AND T J')

    # t = True, if hole at any A, B, C
    command('OR A T')
    command('AND B T')
    command('AND C T')
    command('NOT T T')

    # Combine T (hole at 1-3, not all(A, B, C))
    command('OR T J')
    command('AND D J')

    command('WALK')

    for output in prog:
        # print(output)
        print(chr(output), end='')


def part2(comp):
    def command(cmd):
        ascii_command(comp, cmd)

    prog = comp.run()

    # assign t & j = false
    command('NOT J T')
    command('AND J T')
    command('AND T J')

    # t = True, if hole at any A, B, C
    command('OR A T')
    command('AND B T')
    command('AND C T')
    command('NOT T T')

    # Combine T (hole at 1-3, not all(A, B, C))
    command('OR T J')
    command('AND D J')

    # T <-- E = True OR H = True
    command('NOT J T')
    command('AND J T')  # reset t to false
    command('OR E T')
    command('OR H T')
    command('AND T J')

    command('RUN')

    for output in prog:
        print(output)
        # print(chr(output), end='')


comp = IntComputerFinal()
comp.program(comp.load_memory('input.txt'))
# part1(comp)
part2(comp)