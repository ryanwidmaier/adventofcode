from util import a_star
import math
from collections import namedtuple
import re


Node = namedtuple('Node', 'id used avail x y')
Coord = namedtuple('Coord', 'x y')


def parse_nodes(filename):
    # Filesystem              Size  Used  Avail  Use%
    # /dev/grid/node-x0-y0     85T   65T    20T   76%
    pattern = re.compile(r'/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%')

    nodes = []

    infile = open(filename)
    for line in infile:
        line = line.rstrip()

        match = pattern.match(line)
        if not match:
            continue

        x, y, size, used, avail, use_pct = match.groups()
        nodes.append(Node('node-x{}-y{}'.format(x, y), int(used), int(avail), int(x), int(y)))
    return nodes


class Grid(object):
    def __init__(self, nodes, data_node):
        self.width = max([n.x for n in nodes]) + 1
        self.height = max([n.y for n in nodes]) + 1
        self.grid = [['.' for y in xrange(self.height)] for x in xrange(self.width)]

        empty_count = 0
        full_count = 0
        norm_count = 0
        for n in nodes:
            if n.used == 0:
                ch = '_'
                empty_count += 1
            elif n.used > 100:
            # elif n.used > 27:
                ch = '#'
                full_count += 1
            else:
                ch = '.'
                norm_count += 1

            self.grid[n.x][n.y] = ch

        print "Empties: {}".format(empty_count)
        print "Fulls: {}".format(full_count)
        print "Normals: {}".format(norm_count)

        self.data_node = data_node
        self.grid[self.data_node.x][self.data_node.y] = 'D'

    def get_data_node(self):
        return self.data_node

    def set_data_node(self, pos):
        self.grid[self.data_node.x][self.data_node.y] = '_'
        self.grid[pos.x][pos.y] = 'D'
        self.data_node = pos

    def can_move(self, x, y):
        if x < 0 or x >= self.width:
            return False

        if y < 0 or y >= self.height:
            return False

        return self.grid[x][y] not in '#D'


def possible_moves(pos):
    if not isinstance(pos, Coord):
        raise ValueError()

    c = Coord(pos.x + 1, pos.y)
    if grid.can_move(c.x, c.y):
        yield c, 1

    c = Coord(pos.x - 1, pos.y)
    if grid.can_move(c.x, c.y):
        yield c, 1

    c = Coord(pos.x, pos.y + 1)
    if grid.can_move(c.x, c.y):
        yield c, 1

    c = Coord(pos.x, pos.y - 1)
    if grid.can_move(c.x, c.y):
        yield c, 1


def distance_remaining(pos, goal):
    x = goal[0] - pos[0]
    y = goal[1] - pos[1]
    return math.sqrt(x * x + y * y)


def solve(grid, empty_node_):
    # First, figure out the path the data needs to take
    data_path = a_star(grid.get_data_node(), Coord(0, 0), possible_moves, distance_remaining)

    # Then repeatedly move the empty space into position, then shift the data node one closer
    segments = []
    empty_pos = empty_node_
    for empty_dest in data_path:

        # Move empty into position for swap
        answer = a_star(empty_pos, empty_dest, possible_moves, distance_remaining)
        segments.append(answer)

        # Swap empty and data
        segments.append([grid.get_data_node()])
        empty_pos = grid.get_data_node()
        grid.set_data_node(empty_dest)

    # Print the paths
    for path in segments:
        print path

    # Print answer!
    steps = sum([len(p) for p in segments])
    print "Fewest steps: {}".format(steps)


# Init data
empty_node = Coord(22, 25)
data_node = Coord(36, 0)
nodes = parse_nodes('input.txt')
# empty_node = Coord(1, 1)
# data_node = Coord(2, 0)
# nodes = parse_nodes('sample.txt')

grid = Grid(nodes, data_node)

solve(grid, empty_node)
