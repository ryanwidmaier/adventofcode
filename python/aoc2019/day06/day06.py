from collections import defaultdict

graph = defaultdict(lambda: [])
not_root = set()

f = open('input.txt')
for line in f:
    line = line.strip()
    l, r = line.split(')')

    graph[l].append(r)
    not_root.add(r)

# Determine the root
roots = set(graph) - not_root
assert(len(roots) == 1)
root = list(roots)[0]
print(f"Root found: {root}")


def walk(planet, depth):
    if len(graph[planet]) == 0:
        return depth

    return depth + sum([walk(x, depth+1) for x in graph[planet]])


def search(planet, tgt):
    if len(graph[planet]) == 0:
        return None

    if tgt in graph[planet]:
        return [planet, tgt]

    for p in graph[planet]:
        path = search(p, tgt)
        if path is not None:
            return [planet] + path


print(walk(root, 0))
p1 = search(root, 'YOU')
p2 = search(root, 'SAN')

while p1[0] == p2[0]:
    p1 = p1[1:]
    p2 = p2[1:]

print(len(p1) - 1 + len(p2) - 1)