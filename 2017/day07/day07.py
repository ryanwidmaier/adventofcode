import re
from collections import namedtuple, Counter


Node = namedtuple('Node', 'name weight children')


def build_tree(input_file):
    fin = open(input_file)

    # Name -> (weight, children)
    nodes = {}

    pattern = r'^(?P<name>\w+) \((?P<weight>\d+)\)'
    start_re = re.compile(pattern)

    for line in fin:
        line = line.rstrip()

        # If this isn't a valid line
        match = start_re.search(line)
        if not match:
            continue

        # Parse out the children if there are any
        children = []
        if ' -> ' in line:
            _, child_str = line.split(' -> ')
            children = child_str.split(', ')

        # Make/store the node
        node = Node(match.group('name'), int(match.group('weight')), children)
        nodes[match.group('name')] = node

    return nodes


def find_root(nodes):
    # Loop through all name nodes
    for name in nodes.iterkeys():

        # If this name doesn't show up in any children, then it must be the root
        found = False
        for node in nodes.itervalues():
            if name in node.children:
                found = True
                break

        if not found:
            return name


def compute_balance(nodes, start):
    node = nodes[start]
    if len(node.children) == 0:
        return node.weight

    weights = {}
    for child in node.children:
        weights[child] = compute_balance(nodes, child)

    # Check if the children weights don't match
    counted = Counter(weights.itervalues())
    expected = counted.most_common(1)[0][0]

    for child, weight in weights.iteritems():
        unbalanced = '**unbalanced**' if weight != expected else ''
        print "{} -> {} {}    {}".format(start, child, weight, unbalanced)

    return sum(weights.itervalues()) + node.weight


node_lookup = build_tree('input.txt')
root = find_root(node_lookup)
compute_balance(node_lookup, root)

print 'Root: ', root