from pprint import pprint


reg = {i: 0 for i in xrange(6)}
# reg[0] = 12420065
reg[0] = 1670686
# reg[0] = 12111537

# 0: seti 123 0 4
reg[4] = 123

while True:
    # 1: bani 4 456 4
    reg[4] &= 456

    # 2: eqri 4 72 4
    # 3: addr 4 1 1    ** JUMP **
    if reg[4] == 72:
        break

    # 4: seti 0 0 1    ** JUMP **

# 5: seti 0 0 4
reg[4] = 0

repeat = set()

while True:
    # 6: bori 4 65536 5
    reg[5] = reg[4] | 0x10000

    # 7: seti 10704114 0 4
    reg[4] = 10704114

    while True:
        # 9: addr 4 2 4
        reg[4] += reg[5] & 0xff
        reg[4] &= 0xffffff
        reg[4] *= 65899
        reg[4] &= 0xffffff

        # 14: addr 2 1 1    ** JUMP **
        # 15: addi 1 1 1    ** JUMP **
        if 256 > reg[5]:
            # 16: seti 27 2 1   ** JUMP ** break loop
            break

        reg[2] = reg[5] / 256
        reg[3] = (reg[2] + 1) * 256

        # 26: setr 2 6 5
        reg[5] /= 256

    # 29: addr 2 1 1   ** JUMP **
    print '{}: {}'.format(len(repeat), reg[4])
    if not reg[4] in repeat:
        repeat.add(reg[4])
    else:
        print "First repeat"
        break

    if reg[4] == reg[0]:
        break

    # 30: seti 5 3 1   ** JUMP **

print "Done!"