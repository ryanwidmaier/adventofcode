
def part1(data):
    up = [x for x in data if x == '(']
    down = [x for x in data if x == ')']
    print("Part 1: ", len(up) - len(down))


def part2(data):
    floor = 0
    for idx, ch in enumerate(data):
        floor += 1 if ch == '(' else -1
        if floor < 0:
            print(f"Part 2: {idx+1}")
            return



with open('input.txt') as f:
    data = f.read()

part1(data)
part2(data)
