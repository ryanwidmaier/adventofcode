import networkx as nx
from networkx.algorithms.components import node_connected_component, number_connected_components

g = nx.Graph()

with open('input.txt') as fp:
    for line in fp:
        line = line.rstrip()
        node, links = line.split(' <-> ')
        g.add_node(node)

with open('input.txt') as fp:
    for line in fp:
        line = line.rstrip()
        node, links = line.split(' <-> ')

        for link in links.split(', '):
            g.add_edge(node, link)


result = node_connected_component(g, '0')

print result
print len(result)

print number_connected_components(g)
