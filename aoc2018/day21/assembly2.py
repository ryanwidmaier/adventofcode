
reg = {i: 0 for i in xrange(6)}

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

while True:
    # 6: bori 4 65536 5
    reg[5] = reg[4] | 0x10000

    # 7: seti 10704114 0 4
    reg[4] = 10704114

    while True:
        # 8: bani 5 255 2
        reg[2] = reg[5] & 0xff

        # 9: addr 4 2 4
        reg[4] += reg[2]

        # 10: bani 4 16777215 4
        reg[4] &= 0xffffff

        # 11: muli 4 65899 4
        reg[4] *= 65899

        # 12: bani 4 16777215 4
        reg[4] &= 0xffffff

        # 13: gtir 256 5 2
        reg[2] = 1 if 256 > reg[5] else 0

        # 14: addr 2 1 1    ** JUMP **
        if 256 <= reg[5]:
            # 15: addi 1 1 1    ** JUMP **
            pass
        else:
            # 16: seti 27 2 1   ** JUMP ** break loop
            break

        # 17: seti 0 4 2
        reg[2] = 0

        while reg[3] < reg[5]:
            # 18: addi 2 1 3
            # 19: muli 3 256 3
            # 20: gtrr 3 5 3
            # 21: addr 3 1 1    ** JUMP **
            # 22: addi 1 1 1    ** JUMP **
            # 23: seti 25 5 1   ** JUMP ** break loop
            # 24: addi 2 1 2
            # 25: seti 17 5 1   ** JUMP **
            reg[2] += 1
            reg[3] += (reg[2] + 1) * 256

        # 26: setr 2 6 5
        reg[5] = reg[2]

        # 27: seti 7 8 1   ** JUMP **

    # 28: eqrr 4 0 2
    reg[2] = 1 if reg[4] == reg[0] else 0

    # 29: addr 2 1 1   ** JUMP **
    if reg[4] == reg[0]:
        break

    # 30: seti 5 3 1   ** JUMP **