import re
from collections import defaultdict


with open('input.txt') as f:
    lines = f.readlines()

pattern = re.compile(r'(toggle|turn on|turn off) (\d+),(\d+) through (\d+),(\d+)')


# Part 1
grid = defaultdict(bool)
for line in lines:
    m = pattern.match(line)
    action, x1, y1, x2, y2 = m.groups()
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            if action.startswith('turn'):
                grid[(x, y)] = action == 'turn on'
            else:
                grid[(x, y)] = not grid[(x, y)]

on = {k: v for k, v in grid.items()
      if v and 0 <= k[0] < 1000 and 0 <= k[1] < 1000}
print(f"Part 1: {len(on)}")

# Part 2
actions = {'turn on': 1, 'turn off': -1, 'toggle': 2}
grid = defaultdict(int)
for line in lines:
    m = pattern.match(line)
    action, x1, y1, x2, y2 = m.groups()
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            grid[(x, y)] = max(actions[action] + grid[(x, y)], 0)

on = sum([v for k, v in grid.items()])
print(f"Part 2: {on}")
