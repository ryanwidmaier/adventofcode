from util import GridWalker, Coord


with open('input.txt') as f:
    lines = [l.strip().split(',') for l in f.readlines()]
    raw_lines = f.readlines()

tx_dir = {
    'R': 'E',
    'U': 'N',
    'D': 'S',
    'L': 'W'
}

dists = []
path1 = {}

# Process wire 1
gw = GridWalker(Coord(0, 0), True)
for move in lines[0]:
    direction, amount = tx_dir[move[0]], int(move[1:])

    for x in range(amount):
        gw.move(direction, 1)
        path1[gw.position.copy()] = gw.steps

# Process wire 2
gw2 = GridWalker(Coord(0, 0), True)
for move in lines[1]:
    direction, amount = tx_dir[move[0]], int(move[1:])

    for x in range(amount):
        gw2.move(direction, 1)
        if gw2.position in path1:
            dists.append(gw2.steps + path1[gw2.position])

print(sorted(dists))
