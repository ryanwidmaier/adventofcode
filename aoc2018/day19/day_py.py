registers = [0, 0, 0, 0, 0, 0]

# 0: addi 4 16 4  **JUMP**
ip = 16

# 1: seti 1 5 1
# 2: seti 1 7 3
registers[1] = 1
registers[3] = 1

# 3: mulr 1 3 5
registers[5] = registers[1] * registers[3]

# 4: eqrr 5 2 5
registers[5] = 1 if registers[5] == registers[2] else 0

# 5: addr 5 4 4  **JUMP**
ip += registers[5]

# 6: addi 4 1 4  **JUMP**
ip += 1

# 7: addr 1 0 0
registers[0] += registers[1]

# 8: addi 3 1 3
registers[3] += 1

# 9: gtrr 3 2 5
registers[5] = 1 if registers[3] > registers[2] else 0

# 10: addr 4 5 4  **JUMP**
ip += registers[5]

# 11: seti 2 4 4  **JUMP**
ip = 2

# 12: addi 1 1 1
registers[1] += 1

# 13: gtrr 1 2 5
registers[5] = 1 if registers[1] > registers[2] else 0

# 14: addr 5 4 4  **JUMP**
ip += registers[5]

# 15: seti 1 5 4  **JUMP**
ip = 1

# 16: mulr 4 4 4  **JUMP**
ip *= 16 ** 2

# 17: addi 2 2 2
registers[2] += 2

# 18: mulr 2 2 2
registers[2] *= registers[2]

# 19: mulr 4 2 2
registers[2] *= 19

# 20: addi 5 2 5
registers[5] += 2

# 21: mulr 5 4 5
registers[5] *= 21

# 22: addi 5 18 5
registers[5] += 18

# 23: addr 2 5 2
registers[2] += registers[5]

# 24: addr 4 0 4  **JUMP**
ip += registers[0]

# 25: seti 0 6 4  **JUMP**
ip = 0

# 26: setr 4 3 5
registers[5] = 26

# 27: mulr 5 4 5
registers[5] *= 27

# 28: addr 4 5 5
registers[5] += 28

# 29: mulr 4 5 5
registers[5] *= 29

# 30: muli 5 14 5
registers[5] *= 14

# 31: mulr 5 4 5
registers[5] *= 31

# 32: addr 2 5 2
registers[2] += registers[5]

# 33: seti 0 2 0
registers[0] = 0

# 34: seti 0 6 4  **JUMP**
ip = 0
