import re
from collections import namedtuple

Node = namedtuple('Node', 'id used avail x y')


def is_viable(a, b):
    if a.id == b.id:
        return False

    if a.used == 0:
        return False

    if a.used > b.avail:
        return False

    return True


def parse_nodes():
    # Filesystem              Size  Used  Avail  Use%
    # /dev/grid/node-x0-y0     85T   65T    20T   76%
    pattern = re.compile(r'/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%')

    nodes = []

    infile = open('input.txt')
    for line in infile:
        line = line.rstrip()

        match = pattern.match(line)
        if not match:
            continue

        x, y, size, used, avail, use_pct = match.groups()
        nodes.append(Node('node-x{}-y{}'.format(x, y), int(used), int(avail), int(x), int(y)))
    return nodes


if __name__ == "__main__":
    viable = []
    for i in xrange(len(nodes)):
        for j in range(i+1, len(nodes)):
            a = nodes[i]
            b = nodes[j]

            if is_viable(a, b):
                viable.append((a, b))

            if is_viable(b, a):
                viable.append((b, a))



    for v in viable:
        print v[0], '-->', v[1]

    # for idx, n in enumerate(sorted(nodes, key=lambda x: x.avail)):
    #     print idx+1, n

    print "# viable: {}".format(len(viable))

