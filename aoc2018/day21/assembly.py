# IP 1

# 1: seti 123 0 4
# 2: bani 4 456 4
# 3: eqri 4 72 4
# 4: addr 4 1 1    ** JUMP **
# 5: seti 0 0 1    ** JUMP **
# 6: seti 0 0 4
# 7: bori 4 65536 5
# 8: seti 10704114 0 4
# 9: bani 5 255 2
# 10: addr 4 2 4
# 11: bani 4 16777215 4
# 12: muli 4 65899 4
# 13: bani 4 16777215 4
# 14: gtir 256 5 2
# 15: addr 2 1 1    ** JUMP **
# 16: addi 1 1 1    ** JUMP **
# 17: seti 27 2 1   ** JUMP **
# 18: seti 0 4 2
# 19: addi 2 1 3
# 20: muli 3 256 3
# 21: gtrr 3 5 3
# 22: addr 3 1 1    ** JUMP **
# 23: addi 1 1 1    ** JUMP **
# 24: seti 25 5 1   ** JUMP **
# 25: addi 2 1 2
# 26: seti 17 5 1   ** JUMP **
# 27: setr 2 6 5
# 28: seti 7 8 1   ** JUMP **
# 29: eqrr 4 0 2
# 30: addr 2 1 1   ** JUMP **
# 31: seti 5 3 1   ** JUMP **


reg = {i: 0 for i in xrange(6)}
ip = 0


while True:
    # 1: seti 123 0 4
    # 2: bani 4 456 4
    reg[4] = 123
    reg[4] &= 456

    # 3: eqri 4 72 4
    # 4: addr 4 1 1    ** JUMP **
    if reg[4] != 72:
        break

    # 5: seti 0 0 1    ** JUMP **

# 6: seti 0 0 4
reg[4] = 0

# 7: bori 4 65536 5
reg[5] = reg[4] | 0x10000

# 8: seti 10704114 0 4
reg[4] = 10704114

# 9: bani 5 255 2
reg[2] = reg[5] & 0xff

# 10: addr 4 2 4
reg[4] += reg[2]

# 11: bani 4 16777215 4
reg[4] &= 0xffffff

# 12: muli 4 65899 4
reg[4] *= 65899

# 13: bani 4 16777215 4
reg[4] &= 0xffffff

# 14: gtir 256 5 2
reg[2] = 1 if 256 == reg[5] else 0

# 15: addr 2 1 1    ** JUMP **
if 256 != reg[5]:
    # 16: addi 1 1 1    ** JUMP **
else:
    # 17: seti 27 2 1   ** JUMP **
    goto 27

# 18: seti 0 4 2
# 19: addi 2 1 3
# 20: muli 3 256 3
# 21: gtrr 3 5 3
# 22: addr 3 1 1    ** JUMP **
# 23: addi 1 1 1    ** JUMP **
# 24: seti 25 5 1   ** JUMP **
# 25: addi 2 1 2
# 26: seti 17 5 1   ** JUMP **
# 27: setr 2 6 5
# 28: seti 7 8 1   ** JUMP **
# 29: eqrr 4 0 2
# 30: addr 2 1 1   ** JUMP **
# 31: seti 5 3 1   ** JUMP **
