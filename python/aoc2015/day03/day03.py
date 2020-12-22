from collections import defaultdict
from util import Coord, GridWalker

with open('input.txt') as f:
    lines = f.read().strip()


translate = {'^': 'N', 'v': 'S', 'V': 'S', '<': 'W', '>': 'E'}
robot = GridWalker(Coord(0, 0))
presents = defaultdict(int)

presents[Coord(0, 0)] += 1
for m in lines:
    robot.move(translate[m])
    presents[robot.position.copy()] += 1

print("Part 1: ", len(presents))


robot = GridWalker(Coord(0, 0))
santa = GridWalker(Coord(0, 0))
presents = defaultdict(int)
presents[Coord(0, 0)] += 2
for idx, m in enumerate(lines):
    current = robot if idx % 2 == 0 else santa
    current.move(translate[m])
    presents[current.position.copy()] += 1

print("Part 2: ", len(presents))
