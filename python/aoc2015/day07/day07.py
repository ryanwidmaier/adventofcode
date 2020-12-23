from functools import cache


ops = {}

@cache
def part1(target):
    if target.isdigit():
        return int(target)

    tokens, line = ops[target]

    result = 0
    if len(tokens) == 1:
        result = part1(tokens[0])
    elif tokens[0] == 'NOT':
        result = ~part1(tokens[1]) & 0xffff
    elif tokens[1] == 'AND':
        result = part1(tokens[0]) & part1(tokens[2])
    elif tokens[1] == 'OR':
        result = part1(tokens[0]) | part1(tokens[2])
    elif tokens[1] == 'LSHIFT':
        result = (part1(tokens[0]) << int(tokens[2])) & 0xffff
    elif tokens[1] == 'RSHIFT':
        result = (part1(tokens[0]) >> int(tokens[2])) & 0xffff

    return result


with open('input.txt') as f:
    lines = f.readlines()

for line in lines:
    line = line.strip()
    left, target = line.split(' -> ')
    ops[target] = (left.split(), line)

# print("d -> ", part1('d'))
# print("e -> ", part1('e'))
# print("f -> ", part1('f'))
# print("g -> ", part1('g'))
# print("h -> ", part1('h'))
# print("i -> ", part1('i'))
answer = part1('a')
print(f"Part 1: {answer}")
