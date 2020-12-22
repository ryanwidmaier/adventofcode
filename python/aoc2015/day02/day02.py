

def part1(lines):
    total = 0
    for line in lines:
        l, w, h = line.strip().split('x')
        l, w, h = int(l), int(w), int(h)
        parts = [l * w,  w * h, h * l]
        total += sum(parts) * 2 + min(parts)

    print("Part 1: ", total)


def part2(lines):
    total = 0
    for line in lines:
        l, w, h = line.strip().split('x')
        l, w, h = int(l), int(w), int(h)
        parts = [l + w,  w + h, h + l]
        total += min(parts) * 2 + l * w * h

    print("Part 2: ", total)


with open('input.txt') as f:
   lines = f.readlines()

part1(lines)
part2(lines)
