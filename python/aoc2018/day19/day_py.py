# [1350, 899, 898, 899, 256, 1]
#   0 : addi  4 16  4  - 1
#   1 : seti  1  5  1  - 1
#   2 : seti  1  7  3  - 898
#   3 : mulr  1  3  5  - 806404
#   4 : eqrr  5  2  5  - 806404
#   5 : addr  5  4  4  - 806404
#   6 : addi  4  1  4  - 806400
#   7 : addr  1  0  0  - 4
#   8 : addi  3  1  3  - 806404
#   9 : gtrr  3  2  5  - 806404
#  10 : addr  4  5  4  - 806404
#  11 : seti  2  4  4  - 805506
#  12 : addi  1  1  1  - 898
#  13 : gtrr  1  2  5  - 898
#  14 : addr  5  4  4  - 898
#  15 : seti  1  5  4  - 897
#  16 : mulr  4  4  4  - 1
#  17 : addi  2  2  2  - 1
#  18 : mulr  2  2  2  - 1
#  19 : mulr  4  2  2  - 1
#  20 : muli  2 11  2  - 1
#  21 : addi  5  2  5  - 1
#  22 : mulr  5  4  5  - 1
#  23 : addi  5 18  5  - 1
#  24 : addr  2  5  2  - 1
#  25 : addr  4  0  4  - 1
#  26 : seti  0  6  4  - 1
#  27 : setr  4  3  5  - 0
#  28 : mulr  5  4  5  - 0
#  29 : addr  4  5  5  - 0
#  30 : mulr  4  5  5  - 0
#  31 : muli  5 14  5  - 0
#  32 : mulr  5  4  5  - 0
#  33 : addr  2  5  2  - 0
#  34 : seti  0  2  0  - 0
#  35 : seti  0  6  4  - 0


registers = [0, 0, 898, 0, 0, 6]

# 1: seti 1 5 1

while True:
    # 2: seti 1 7 3
    registers[1] = 1
    registers[3] = 1

    while True:
        # 3: mulr 1 3 5
        # 4: eqrr 5 2 5
        # 5: addr 5 4 4  **JUMP**
        # 6: addi 4 1 4  **JUMP**
        if registers[1] * registers[3] != registers[2]:
            # 7: addr 1 0 0
            registers[0] += registers[1]

        # 8: addi 3 1 3
        registers[3] += 1

        # 9 : gtrr  3  2  5  - 806404
        # 10 : addr  4  5  4  - 806404
        # 11 : seti  2  4  4  - 805506
        if registers[3] > registers[2]:
            break

    registers[5] = 1

    # 12: addi 1 1 1
    registers[1] += 1

    # 13: gtrr 1 2 5
    registers[5] = 1 if registers[1] > registers[2] else 0
    if registers[1] > registers[2]:
        # 14: addr 5 4 4  **JUMP**
        break

    # 15: seti 1 5 4  **JUMP**

from pprint import pprint

pprint(registers)