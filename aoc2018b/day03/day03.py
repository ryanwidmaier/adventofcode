import re
from collections import namedtuple, defaultdict

Box = namedtuple('Box', 'id left right top bottom')

#   #1 @ 286,440: 19x24
pattern = re.compile(r'#(?P<id>\d+) @ (?P<left>\d+),(?P<top>\d+): (?P<width>\d+)x(?P<height>\d+)')


# grid[left][top]
grid = defaultdict(lambda: defaultdict(lambda: 0))

boxes = []
amount_overlap = 0

f = open('input.txt')
for line in f:
    result = pattern.search(line)

    left = int(result.group('left'))
    top = int(result.group('top'))
    width = int(result.group('width'))
    height = int(result.group('height'))

    # right = left + int(result.group('width'))
    # bottom = top + int(result.group('height'))
    #
    # b = Box(result.group('id'), left, right, top, bottom)

    for ll in range(width):
        for tt in range(height):
            grid[left + ll][top + tt] += 1

            if grid[left + ll][top + tt] == 2:
                amount_overlap += 1

print(amount_overlap)


f = open('input.txt')
for line in f:
    result = pattern.search(line)

    left = int(result.group('left'))
    top = int(result.group('top'))
    width = int(result.group('width'))
    height = int(result.group('height'))

    # right = left + int(result.group('width'))
    # bottom = top + int(result.group('height'))
    #
    # b = Box(result.group('id'), left, right, top, bottom)

    overlap = True
    for ll in range(width):
        for tt in range(height):
            if grid[left + ll][top + tt] > 1:
                overlap = False
                break

    if overlap:
        print("Overlapping ID: " + result.group("id"))