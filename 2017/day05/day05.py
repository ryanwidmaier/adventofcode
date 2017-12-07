
fin = open('input.txt')
instructions = [int(l.rstrip()) for l in fin]

step = 0
pos = 0

while pos >= 0 and pos < len(instructions):
    step += 1
    jump = instructions[pos]

    if jump >= 3:
        instructions[pos] -= 1
    else:
        instructions[pos] += 1

    pos += jump


print "Steps: ", step
