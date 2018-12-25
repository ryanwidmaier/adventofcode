import re
import networkx as nx

X, Y, Z, RANGE = 0, 1, 2, 3
ORIGIN = (0, 0, 0, 0)



def part2(bots):
    # build a graph with edges between overlapping nanobots
    graph = nx.Graph()
    for bot in bots:
        # two bots overlap if their distance is smaller or equal than the sum of their ranges
        overlaps = [(bot, other) for other in bots if manhattan(bot, other) <= bot[RANGE] + other[RANGE]]
        graph.add_edges_from(overlaps)

    # find sets of overlapping nanobots (i.e. fully-connected sub-graphs)
    cliques = list(nx.find_cliques(graph))
    cliques_size = [len(c) for c in cliques]

    assert len([s for s in cliques_size if s == max(cliques_size)]) == 1

    # select the largest cluster of overlapping nanobots (maximum clique sub-graph)
    clique = max(cliques, key=len)

    # calculate the point on the nanobots surface which is closest to the origin
    surfaces = [manhattan(ORIGIN, bot) - bot[RANGE] for bot in clique]

    # the furthest away surface point is the minimum manhattan distance
    return max(surfaces)


def manhattan(a, b):
    (x1, y1, z1, _), (x2, y2, z2, _) = a, b
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


# pos=<-27072311,19664231,23616729>, r=91300896
parse_re = re.compile(r'pos=<(?P<x>-?\d+),(?P<y>-?\d+),(?P<z>-?\d+)>, r=(?P<r>-?\d+)')


def parse(fname):
    transmitters = []

    f = open(fname)
    for line in f:
        line = line.rstrip()

        m = parse_re.search(line)
        if m:
            transmitters.append((int(m.group('x')), int(m.group('y')), int(m.group('z')), int(m.group('r'))))

    return transmitters


if __name__ == "__main__":
    print(part2(parse("input.txt")))