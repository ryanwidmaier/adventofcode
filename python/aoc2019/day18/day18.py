from util import Coord, a_star, print_dict_grid, Memoize
import string
from collections import defaultdict

WALL = '#'
ROBOT = '@'
OPEN = '.'
DOORS = string.ascii_uppercase
KEYS = string.ascii_lowercase



def parse(filename):
    grid = {}
    robot = None

    with open(filename) as f:
        for y, line in enumerate(f):
            line = line.strip()
            for x, ch in enumerate(line):
                if ch == ROBOT:
                    robot = Coord(x, y)

                grid[Coord(x, y)] = ch

    return grid, robot


# Funcs for path finding
def possible_moves(grid_, pos):
    for c in pos.neighbors():
        cell = grid_.get(c)
        if cell != WALL:
            yield c, 1


def remaining(pos, goal):
    return pos.manhattan(goal)


def part1(grid, robot_pos):
    graph = build_graph(grid)
    print("Done building graph")

    keys = {v for v in grid.values() if v in KEYS}

    min_dist = search(('@',), tuple(keys), graph)
    print(min_dist)


def part2(grid, robot_pos):
    grid[robot_pos] = '#'
    grid[robot_pos + Coord(1, 0)] = '#'
    grid[robot_pos + Coord(-1, 0)] = '#'
    grid[robot_pos + Coord(0, 1)] = '#'
    grid[robot_pos + Coord(0, -1)] = '#'
    grid[robot_pos + Coord(-1, -1)] = '1'
    grid[robot_pos + Coord(-1, 1)] = '2'
    grid[robot_pos + Coord(1, -1)] = '3'
    grid[robot_pos + Coord(1, 1)] = '4'

    print_dict_grid(grid)

    graph = build_graph(grid)
    print("Done building graph")

    keys = {v for v in grid.values() if v in KEYS}

    min_dist = search(('1', '2', '3', '4'), tuple(keys), graph)
    print(min_dist)


def build_graph(grid):
    """
    Compute graph figuring out distance and requirements for moving between every key combination
    """
    goals = {v: k for k, v in grid.items() if v in KEYS or v in {'@', '1', '2', '3', '4'}}

    graph = defaultdict(lambda: {})
    for k, start in goals.items():
        print(f"Processing {k}")
        for kk, target in goals.items():
            if k >= kk:
                continue

            # Find the path
            p = a_star(start, target, lambda pos: possible_moves(grid, pos), remaining)
            if p is None:
                continue

            # Find any keys required
            required = set()
            for c in p:
                if grid[c] in DOORS:
                    required.add(grid[c].lower())

            # Store distance and keys needed in both dirs
            graph[k][kk] = (len(p), required)
            graph[kk][k] = (len(p), required)

    return graph


def search(start_keys, remaining_keys, graph):
    @Memoize
    def search_(start_keys, remaining_keys):
        if len(remaining_keys) == 0:
            return 0

        remaining_keys = set(remaining_keys)

        min_dist = 9999999999999999
        hop_dist = None
        min_skey = None
        min_next_key = None

        for skey in start_keys:
            here = 0
            for next_key in remaining_keys:
                if next_key not in graph[skey]:
                    continue

                dist, required_keys = graph[skey][next_key]
                if len(required_keys & remaining_keys) > 0:
                    continue

                # Replace the start key we used w/ the destination
                new_start_keys = tuple(sorted([x for x in start_keys if x != skey] + [next_key]))

                # Figure out min distance from this step
                total = dist + search_(new_start_keys, tuple(remaining_keys - {next_key}))

                if total < min_dist:
                    min_dist = total
                    hop_dist = dist
                    min_skey = skey
                    min_next_key = next_key

        print(f"{min_skey} -> {min_next_key}, {hop_dist}")
        return min_dist

    return search_(start_keys, remaining_keys)



grid_, robot_ = parse('input.txt')
part2(grid_, robot_)
