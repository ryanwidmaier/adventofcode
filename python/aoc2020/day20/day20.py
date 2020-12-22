import re
import math
from typing import List, Dict
from util import Coord


class Tile:
    def __init__(self,
                 num: int,
                 grid: List[List[str]],
                 rotations: int = 0,
                 flipped: bool = False):
        self.num = num
        self.rotations = rotations
        self.flipped = flipped
        self.grid = grid

    @staticmethod
    def build(tile_data):
        num = int(tile_data.partition(':')[0][5:])
        grid = [[ch for ch in line] for line in tile_data.strip().split('\n')[1:]]
        rotations = 0
        flipped = False

        return Tile(num, grid, rotations=rotations, flipped=flipped)

    def rotate(self):
        self.grid = rotate(self.grid)
        self.rotations = (self.rotations + 1) % 4

    def flip(self):
        self.grid = flip(self.grid)
        self.flipped = not self.flipped

    def north(self) -> str:
        return ''.join(self.grid[0])

    def east(self) -> str:
        return ''.join(g[-1] for g in self.grid)

    def south(self) -> str:
        return ''.join(self.grid[-1])

    def west(self) -> str:
        return ''.join(g[0] for g in self.grid)

    def __eq__(self, other):
        return self.num == other.num

    def __ne__(self, other):
        return self.num != other.num

    def __repr__(self):
        flip = 'T' if self.flipped else 'F'
        return f'{self.num} ({self.rotations}|{flip})'


def parse(lines):
    tiles = lines.split('\n\n')
    return [Tile.build(l) for l in tiles]


def part1(tiles):
    dim = int(math.sqrt(len(tiles)))
    grid = {}

    # ordered = [1951, 2311, 3079, 2729, 1427, 2473, 2971, 1489, 1171]
    # tiles = sorted(tiles, key=lambda t: ordered.index(t.num))
    # tiles[0].flip()

    result = part1_recurse(grid, tiles, Coord(0, 0), dim)

    if not result:
        print("Part 1: NO ANSWER!!")
        return

    answer = grid[Coord(0, 0)].num * grid[Coord(0, dim-1)].num * grid[Coord(dim-1, 0)].num * grid[Coord(dim-1,dim-1)].num
    print_grid(grid, dim)
    print(f"Part 1: {result}, {answer}")

    return grid


def print_grid(grid: Dict[Coord, Tile], dim):
    for y in range(dim):
        print()
        for x in range(dim):
            tile = grid.get(Coord(x, y))
            if tile:
                print("{0!r:10}".format(grid[Coord(x, y)]), end='  ')
            else:
                print("{:10}".format(' '), end='  ')
        print()

        for yy in range(10):
            for x in range(dim):
                tile = grid.get(Coord(x, y))
                if tile:
                    print(''.join(grid[Coord(x, y)].grid[yy]), end='  ')
                else:
                    print("{:10}".format(' '), end='  ')

            print()



NORTH = Coord(0, -1)
WEST = Coord(-1, 0)


def part1_recurse(placed: Dict[Coord, Tile],
                  remaining_tiles: List[Tile],
                  pos: Coord, dim: int):
    # Place all tiles successfully!
    if len(remaining_tiles) == 0:
        return True

    # Try to find a tile that we can place in pos
    for tile in remaining_tiles:
        # make a copy
        tile = Tile(tile.num, tile.grid, tile.rotations, tile.flipped)

        # Try flipped
        for _ in range(2):
            # Try all rotations
            for _ in range(4):
                # Tile can be placed here in this orientation..
                if (
                    (pos.y == 0 or tile.north() == placed[pos+NORTH].south())
                    and (pos.x == 0 or tile.west() == placed[pos+WEST].east())
                ):
                    # Check remaining..
                    remaining = [t for t in remaining_tiles if t != tile]
                    placed[pos] = tile
                    # print_grid(placed, dim)

                    next_pos = Coord((pos.x + 1) % dim, ((pos.y * dim) + pos.x + 1) // dim)
                    if part1_recurse(placed, remaining, next_pos, dim):
                        return True

                tile.rotate()

            tile.flip()

    return False


def part2(tile_grid):
    dim = max(c.y for c in tile_grid) + 1

    # Build image grid
    grid = []
    for y in range(dim):
        for yy in range(1, 9):
            grid.append([])
            for x in range(dim):
                for xx in range(1, 9):
                    grid[-1].append(tile_grid[Coord(x, y)].grid[yy][xx])

    # grid = flip(grid)
    # grid = rotate(grid)
    print()
    for y in range(len(grid)):
        print(' '.join(grid[y]))

    for _ in range(2):
        for _ in range(4):
            if is_monster(grid):
                print()
                for y_ in range(len(grid)):
                    print(' '.join(grid[y_]))

                answer = len([c for row in grid for c in row if c == '#'])
                print("Part 2 Answer: ", answer)

            grid = rotate(grid)
        grid = flip(grid)


def is_monster(grid):
    # |                    # |
    # |# #    ##    ##    ###|
    # | #  #  #  #  #  #  #  |
    snake = [
        '                  # ',
        '#    ##    ##    ###',
        ' #  #  #  #  #  #   '
    ]

    found = False

    for y in range(len(grid) - len(snake)):
        for x in range(len(grid) - len(snake[0])):
            if (
                is_match(grid, x, y, snake[0]) and
                is_match(grid, x, y+1, snake[1]) and
                is_match(grid, x, y+2, snake[2])
            ):
                found = True
                replace(grid, x, y, snake)

    return found


def is_match(grid, x, y, pattern):
    for px, x_ in enumerate(range(x, x+len(pattern))):

        try:
            if pattern[px] == '#' and grid[y][x_] != '#':
                return False
        except:
            pass

    return True


def replace(grid, x, y, snake):
    for yy, line in enumerate(snake):
        for xx, ch in enumerate(line):
            if snake[yy][xx] == '#':
                grid[y+yy][x+xx] = '\033[93mO\033[0m'


def rotate(grid):
    dim = len(grid)
    new_grid = []
    for _ in grid:
        new_grid.append([])
        for _ in grid[0]:
            new_grid[-1].append('!')

    for x in range(dim):
        for y in range(dim):
            new_y = x
            new_x = dim - y - 1
            new_grid[new_y][new_x] = grid[y][x]

    return new_grid


def flip(grid):
    dim = len(grid)
    new_grid = []
    for _ in grid:
        new_grid.append([])
        for _ in grid[0]:
            new_grid[-1].append('!')

    for x in range(dim):
        for y in range(dim):
            new_grid[dim - y - 1][x] = grid[y][x]

    return new_grid


if __name__ == '__main__':
    with open('input.txt') as f:
        lines_ = f.read()

    parsed = parse(lines_)
    result = part1(parsed)
    part2(result)


