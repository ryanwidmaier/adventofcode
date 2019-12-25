from util import Coord, print_dict_grid
import string
import heapq


def parse(filename):
    grid = {}

    # read the raw grid first
    raw_grid = []
    with open(filename) as f:
        for line in f:
            line = line.strip('\n')
            raw_grid.append(line)

    width = max(len(l) for l in raw_grid)
    portals = []

    # Walk just the gird parts, and look for adjacent portal markers
    for y in range(len(raw_grid)):
        for x in range(width):
            c = Coord(x, y)
            grid[c] = raw_grid[y][x] if x < len(raw_grid[y]) else ' '

            if grid[c] == '.':
                for cc in c.neighbors():
                    row = raw_grid[cc.y]
                    if cc.x >= len(row):
                        continue

                    cell = row[cc.x]
                    if cell in string.ascii_uppercase:
                        diff = cc - c
                        first = cc + diff
                        second = cc

                        if cc.x > c.x or cc.y > c.y:
                            second, first = first, second

                        code = raw_grid[first.y][first.x] + raw_grid[second.y][second.x]

                        grid[c] = code
                        portals += [first, second]

    # Cap the portals
    for p in portals:
        grid[p] = '#'

    print_dict_grid({k: v[0] for k, v in grid.items()})
    print()
    return grid


def bfs(grid):
    start = next(k for k, v in grid.items() if v == 'AA')
    end = next(k for k, v in grid.items() if v == 'ZZ')

    h = []
    heapq.heappush(h, (0, start))
    visited = set()
    max_depth = 0

    while len(h) > 0:
        depth, pos = heapq.heappop(h)
        if pos in visited:
            continue

        # If we reached the end..
        if pos == end:
            return depth

        # Register this is visited, and add it's neighbors to the list
        max_depth = max(max_depth, depth)
        print(max_depth)
        visited.add(pos)

        for c in pos.neighbors():
            if not grid.get(c) in {'#'}:
                heapq.heappush(h, (depth+1, c))

        # Also check for warps
        if grid[pos][0] in string.ascii_uppercase:
            warp = [k for k, v in grid.items() if v == grid[pos] and k != pos]
            if len(warp) == 1:
                warp = warp[0]
                heapq.heappush(h, (depth+1, warp))

        # grid[pos] = str(depth)
        # print_g = {k: '.' if len(v) > 1 else v for k, v in grid.items()}
        # print_dict_grid(print_g)
        # print()


def part1(grid):
    result = bfs(grid)
    print(result)


def is_outer(grid, pos):
    if pos.x <= 2 or pos.y <= 2:
        return True

    max_x = max(c.x for c in grid)
    max_y = max(c.y for c in grid)

    if pos.x >= max_x - 2 or pos.y >= max_y - 2:
        return True

    return False



def bfs2(grid):
    start = next(k for k, v in grid.items() if v == 'AA')
    end = next(k for k, v in grid.items() if v == 'ZZ')

    h = []
    heapq.heappush(h, (0, 0, start))
    visited = set()
    max_dist = 0

    while len(h) > 0:
        dist, depth, pos = heapq.heappop(h)
        if (depth, pos) in visited:
            continue

        # If we reached the end..
        if pos == end and depth == 0:
            return dist

        # Register this is visited, and add it's neighbors to the list
        max_dist = max(max_dist, dist)
        print(f"{max_dist} - {depth}, {pos}")
        visited.add((depth, pos))

        for c in pos.neighbors():
            if not grid.get(c) in {'#'}:
                heapq.heappush(h, (dist+1, depth, c))

        # Also check for warps
        if grid[pos][0] in string.ascii_uppercase:
            warp = [k for k, v in grid.items() if v == grid[pos] and k != pos]
            if len(warp) == 1:
                warp = warp[0]
                if is_outer(grid, pos):
                    if depth > 0:
                        heapq.heappush(h, (dist + 1, depth-1, warp))
                else:
                    heapq.heappush(h, (dist+1, depth+1, warp))

        # grid[pos] = str(depth)
        # print_g = {k: '.' if len(v) > 1 else v for k, v in grid.items()}
        # print_dict_grid(print_g)
        # print()

def part2(grid):
    result = bfs2(grid)
    print(result)


grid = parse('input.txt')
portals = {k: v for k, v in grid.items() if v[0] in string.ascii_uppercase}

part2(grid)