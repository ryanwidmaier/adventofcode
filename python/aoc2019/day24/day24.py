from util import Coord, print_dict_grid


def neighbors(c):
    # Neighbors per position, assume z=0 and adjust at the end
    # + = deeper, - = shallower
    NORTH = Coord(2, 1, -1)
    WEST = Coord(1, 2, -1)
    EAST = Coord(3, 2, -1)
    SOUTH = Coord(2, 3, -1)

    IN_NORTH = [Coord(x, 0, 1) for x in range(5)]
    IN_WEST = [Coord(0, y, 1) for y in range(5)]
    IN_EAST = [Coord(4, y, 1) for y in range(5)]
    IN_SOUTH = [Coord(x, 4, 1) for x in range(5)]

    neighbors = {
        Coord(0, 0): [NORTH, WEST, Coord(1, 0), Coord(0, 1)],
        Coord(1, 0): [NORTH, Coord(0, 0), Coord(2, 0), Coord(1, 1)],
        Coord(2, 0): [NORTH, Coord(1, 0), Coord(3, 0), Coord(2, 1)],
        Coord(3, 0): [NORTH, Coord(2, 0), Coord(4, 0), Coord(3, 1)],
        Coord(4, 0): [NORTH, EAST, Coord(3, 0), Coord(4, 1)],

        Coord(0, 1): [WEST, Coord(0, 0), Coord(1, 1), Coord(0, 2)],
        Coord(1, 1): [Coord(1, 0), Coord(0, 1), Coord(2, 1), Coord(1, 2)],
        Coord(2, 1): IN_NORTH + [Coord(1, 1), Coord(2, 0), Coord(3, 1)],
        Coord(3, 1): [Coord(3, 0), Coord(2, 1), Coord(4, 1), Coord(3, 2)],
        Coord(4, 1): [EAST, Coord(4, 0), Coord(3, 1), Coord(4, 2)],

        Coord(0, 2): [WEST, Coord(0, 1), Coord(1, 2), Coord(0, 3)],
        Coord(1, 2): IN_WEST + [Coord(1, 1), Coord(0, 2), Coord(1, 3)],
        Coord(3, 2): IN_EAST + [Coord(3, 1), Coord(4, 2), Coord(3, 3)],
        Coord(4, 2): [EAST, Coord(4, 1), Coord(3, 2), Coord(4, 3)],

        Coord(0, 3): [WEST, Coord(0, 2), Coord(1, 3), Coord(0, 4)],
        Coord(1, 3): [Coord(1, 2), Coord(0, 3), Coord(2, 3), Coord(1, 4)],
        Coord(2, 3): IN_SOUTH + [Coord(1, 3), Coord(2, 4), Coord(3, 3)],
        Coord(3, 3): [Coord(3, 2), Coord(2, 3), Coord(4, 3), Coord(3, 4)],
        Coord(4, 3): [EAST, Coord(4, 2), Coord(3, 3), Coord(4, 4)],

        Coord(0, 4): [SOUTH, WEST, Coord(0, 3), Coord(1, 4)],
        Coord(1, 4): [SOUTH, Coord(0, 4), Coord(1, 3), Coord(2, 4)],
        Coord(2, 4): [SOUTH, Coord(1, 4), Coord(2, 3), Coord(3, 4)],
        Coord(3, 4): [SOUTH, Coord(2, 4), Coord(3, 3), Coord(4, 4)],
        Coord(4, 4): [SOUTH, EAST, Coord(4, 3), Coord(3, 4)]
    }
    lookup = Coord(c.x, c.y)
    found = neighbors[lookup]

    # z is an offset, need to apply it
    found = [Coord(f.x, f.y, f.z + c.z) for f in found]
    return found


def update(grid, pos):
    # A bug dies (becoming an empty space) unless there is exactly one bug adjacent to it.
    # An empty space becomes infested with a bug if exactly one or two bugs are adjacent to it.
    # Otherwise, a bug or empty space remains the same.
    adjacent = len([c for c in neighbors(pos) if grid.get(c) == '#'])
    if grid.get(pos) == '#':
        if adjacent != 1:
            return '.'
    else:
        if adjacent == 1 or adjacent == 2:
            return '#'

    return grid.get(pos, '.')


def calc_score(grid):
    return sum(2 ** (c.y * 5 + c.x) for c, v in grid.items() if v == '#')


def print_depths(grid, i):
    min_depth = min(c.z for c, v in grid.items() if v == '#')
    max_depth = max(c.z for c, v in grid.items() if v == '#')

    print(f"Minute = {i}")
    for d in range(min_depth, max_depth+1):
        g = {Coord(c.x, c.y): v for c, v in grid.items() if c.z == d}
        print(f"Depth {d}")
        print_dict_grid(g)
        print()


grid = {}

with open('input.txt') as f:
    for y, line in enumerate(f):
        for x, ch in enumerate(line.strip()):
            c = Coord(x, y)
            grid[c] = ch

print_depths(grid, -1)

for i in range(200):
    print(i)
    new_grid = {}

    # Need to do all levels with bugs, and one before and after
    min_depth = min(c.z for c, v in grid.items() if v == '#') - 1
    max_depth = max(c.z for c, v in grid.items() if v == '#') + 1

    # Loop through all depths, and all cells in those depths
    for d in range(min_depth, max_depth+1):
        for y in range(5):
            for x in range(5):
                # Don't do the middle cell
                if (x, y) == (2, 2):
                    continue

                c = Coord(x, y, d)
                new_grid[c] = update(grid, c)

    grid = new_grid
    # print_depths(grid, i)


print(len({c for c, v in grid.items() if v == '#'}))
