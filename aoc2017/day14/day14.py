from aoc2017.day10.day10 import twist_full
import networkx as nx
from networkx.algorithms.components.connected import number_connected_components

input_val = 'uugsqrei'


def node(r, c):
    return '{},{}'.format(r, c)

hex_to_bits = {
    '0': 0, '1': 1, '2': 1, '3': 2,
    '4': 1, '5': 2, '6': 2, '7': 3,
    '8': 1, '9': 2, 'a': 2, 'b': 3,
    'c': 2, 'd': 3, 'e': 3, 'f': 4
}

hex_to_chars = {
    '0': '0000', '1': '0001', '2': '0010', '3': '0011',
    '4': '0100', '5': '0101', '6': '0110', '7': '0111',
    '8': '1000', '9': '1001', 'a': '1010', 'b': '1011',
    'c': '1100', 'd': '1101', 'e': '1110', 'f': '1111'
}

G = nx.Graph()
G.add_nodes_from([node(r, c) for r in xrange(128) for c in xrange(128)])


bits = 0
memory = []
for r in xrange(128):
    result = twist_full('{}-{}'.format(input_val, r))
    memory.append([])

    c = 0
    for ch in result:
        bits += hex_to_bits[ch]

        new_bits = hex_to_chars[ch]
        memory[-1].append(new_bits)

        # Update the graph
        for nch in new_bits:
            if nch == '0':
                continue

            # Check Up
            if r > 0 and memory[r-1][c] == '1':
                G.add_edge(node(r, c), node(r-1, c))

            # Check left
            if c > 0 and memory[r][c-1] == '1':
                G.add_edge(node(r, c), node(r, c-1))
print bits
print number_connected_components(G)

