
fin = open('input.txt')

#
# G = nx.MultiGraph()
#
# for line in fin:
#     line = line.rstrip()
#     start, end = line.split('/')
#
#     G.add_edge(start, end)
#
#
# print is_eulerian(G)
# nx.draw(G)
# plt.show()


edges = []
for line in fin:
    line = line.rstrip()
    start, end = line.split('/')
    edges.append((int(start), int(end)))


def walk(edges, node, weight):
    # Add left side of connection weight
    weight += node

    max_weight = weight
    max_path = []

    # Look for connectors we can add
    for edge in edges:
        # This one doesn't fit..
        if edge[0] != node and edge[1] != node:
            continue

        next_node = edge[0] if edge[1] == node else edge[1]
        remaining = [e for e in edges if e != edge]
        assert len(edges) == (len(remaining) + 1)

        # Add right side of connection weight
        walk_path, walk_weight = walk(remaining, next_node, weight + node)

        if len(walk_path) >= len(max_path) and walk_weight > max_weight:
            max_path = walk_path
            max_weight = walk_weight

    return [node] + max_path, max_weight


max_path, max_weight = walk(edges, 0, 0)
print max_weight
print max_path
