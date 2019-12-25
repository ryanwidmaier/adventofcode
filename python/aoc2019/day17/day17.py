from aoc2019.int_code import IntComputerFinal
from util import Coord, GridCar
from collections import defaultdict


def get_map(comp):
    grid = {}

    c = Coord(0, 0)

    for output in comp.run():
        ch = chr(output)
        if ch == '\n':
            c = Coord(-1, c.y+1)
            print()
        else:
            if ch != '.':
                grid[c.copy()] = ch

            print(ch, end='')

        c += Coord(1, 0)

    return grid


def part1(comp):
    grid = get_map(comp)

    alignments = []
    for c in grid.keys():
        neighbor_match = 0
        for n in c.neighbors():
            if n in grid:
                neighbor_match += 1

        if neighbor_match > 2:
            alignments.append(c)

    print(sum(c.x * c.y for c in alignments))





def trace_path(comp):
    comp.restart()
    grid = get_map(comp)
    path = []

    # Map ascii art to facing
    dir = {
        '^': 'NORTH',
        '<': 'WEST',
        '>': 'EAST',
        'v': 'SOUTH'
    }

    # Step one, just print the full path required
    robot_pos = next(c for c, ch in grid.items() if ch in dir)
    car = GridCar(robot_pos, dir[grid[robot_pos]], invert_y=True)

    while True:
        if car.forward_coord() in grid:
            car.forward()
            path[-1] += 1
        elif car.left_coord() in grid:
            car.left()
            path += ['L', 0]
        elif car.right_coord() in grid:
            car.right()
            path += ['R', 0]
        else:
            break

    print(path)


def find_commands(path):
    counts = defaultdict(lambda: 0)
    for sz in range(1, 20):
        for i in range(len(path) - sz + 1):
            ngram = tuple(path[i:i+sz])
            counts[ngram] += 1

    for ngram, count in counts.items():
        if count <= 3:
            continue

        if len(ngram) == 1:
            continue

        if len(ngram) > 10:
            continue

        print(f'{count:>3} {ngram}')


def apply_subpaths(path, a=None, b=None, c=None):
    i = 0
    new_path = []
    while i < len(path):
        if a and path[i:i+len(a)] == a:
            new_path.append('A')
            i += len(a)
        elif b and path[i:i + len(b)] == b:
            new_path.append('B')
            i += len(b)
        elif c and path[i:i + len(c)] == c:
            new_path.append('C')
            i += len(c)
        else:
            new_path.append(path[i])
            i += 1

    for x in new_path:
        print(f"{x}, ", end='')


def part2(comp):
    comp.restart()
    comp.memory[0] = 2

    comp = program_paths(comp)

    comp.run_and_print()


def program_paths(comp):
    def to_ints(seq):
        first = True
        int_seq = []
        for x in seq:
            if not first:
                int_seq.append(44)

            first = False
            if isinstance(x, str):
                int_seq.append(ord(x))
            else:
                int_seq.append(ord(str(x)))

        int_seq.append(10)
        return int_seq

    p = to_ints(['A', 'B', 'A', 'B', 'C', 'C', 'B', 'A', 'C', 'A'])
    A = to_ints(['L', 5, 5, 'R', 8, 'R', 6, 'R', 5, 5])
    B = to_ints(['L', 6, 6, 'R', 8, 'L', 6, 6])
    C = to_ints(['L', 5, 5, 'R', 8, 'R', 8])

    for x in p:
        comp.add_input(x)
    for x in A:
        comp.add_input(x)
    for x in B:
        comp.add_input(x)
    for x in C:
        comp.add_input(x)

    comp.add_input(ord('n'))
    comp.add_input(10)

    return comp


comp = IntComputerFinal()
comp.program(comp.load_memory('input.txt'))

# # part2(comp)
#
#
# p = ['L', 10, 'R', 8, 'R', 6, 'R', 10, 'L', 12, 'R', 8, 'L', 12, 'L', 10, 'R', 8, 'R', 6, 'R', 10, 'L', 12, 'R', 8, 'L', 12, 'L', 10, 'R', 8, 'R', 8, 'L', 10, 'R', 8, 'R', 8, 'L', 12, 'R', 8, 'L', 12, 'L', 10, 'R', 8, 'R', 6, 'R', 10, 'L', 10, 'R', 8, 'R', 8, 'L', 10, 'R', 8, 'R', 6, 'R', 10]
# A, B, C = None, None, None
#
# A = ['L', 10, 'R', 8, 'R', 6, 'R', 10]
# B = ['L', 12, 'R', 8, 'L', 12]
# C = ['L', 10, 'R', 8, 'R', 8]
# # B = ['R', 8]
#
#
# find_commands(p)
# apply_subpaths(p, A, B, C)

part2(comp)