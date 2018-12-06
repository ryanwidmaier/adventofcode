from util import a_star
from collections import namedtuple
import math
import itertools

Coord = namedtuple('Coord', 'x y')




class Map(object):
    def __init__(self, filename):
        self.m = open(filename).readlines()

    def can_move(self, x, y):
        return self.m[y][x] != '#'

    def get_all_points(self):
        for y, line in enumerate(self.m):
            for x, ch in enumerate(line):
                try:
                    i = int(ch)
                    yield (i, Coord(x, y))
                except:
                    pass

    def get_waypoints(self):
        return {d[0]: d[1] for d in self.get_all_points()}


def pairs(path):
    for i in xrange(len(path)-1):
        yield path[i], path[i+1]


# Create the map now so we can use it in the closure
map = Map('input.txt')


def possible_moves(pos):
    c = Coord(pos.x + 1, pos.y)
    if map.can_move(c.x, c.y):
        yield c, 1

    c = Coord(pos.x - 1, pos.y)
    if map.can_move(c.x, c.y):
        yield c, 1

    c = Coord(pos.x, pos.y + 1)
    if map.can_move(c.x, c.y):
        yield c, 1

    c = Coord(pos.x, pos.y - 1)
    if map.can_move(c.x, c.y):
        yield c, 1


# Figure out the graph of shortest paths
waypoints = map.get_waypoints()

graph = {}
paths = {}
for i in xrange(len(waypoints)):
    paths[i] = {}
    graph[i] = {}

    for j in xrange(len(waypoints)):
        if i == j:
            paths[i][j] = []
            graph[i][j] = 0
        else:
            paths[i][j] = a_star(waypoints[i], waypoints[j], possible_moves)
            graph[i][j] = len(paths[i][j])


print "Graph built: {} nodes".format(len(waypoints))

# Travelling salesman time!
shortest_steps = 99999999999
shortest_path = None

visit_orders = list(itertools.permutations([a for a in waypoints.keys() if a != 0]))
for ordering in visit_orders:
    ordering = [0] + list(ordering) + [0]
    steps = sum([graph[a][b] for a, b in pairs(ordering)])

    if steps < shortest_steps:
        shortest_steps = steps
        shortest_path = ordering

print "Path: " + str(shortest_path)
print "Steps: {}".format(shortest_steps)
