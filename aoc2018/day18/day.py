TREE = '|'
LUMB = '#'
OPEN = '.'


def parse(fname):
    state = []
    with open(fname) as f:
        for line in f:
            line = line.rstrip()
            state.append([ch for ch in line])

    return state


def update_grid(before, after):
    for y in xrange(len(before)):
        for x in xrange(len(before[y])):
            after[y][x] = update_square(before, x, y)


def update_square(state, target_x, target_y):
    trees = 0
    lumber = 0

    max_y, max_x = len(state), len(state[0])

    # Count adjacent
    for y in xrange(max(0, target_y-1), min(max_y, target_y+2)):
        for x in xrange(max(0, target_x-1), min(max_x, target_x+2)):
            if x == target_x and y == target_y:
                continue

            ch = state[y][x]
            if ch == TREE:
                trees += 1
            elif ch == LUMB:
                lumber += 1

    this = state[target_y][target_x]
    # open -> tree if len(tree) >= 3 else No change
    if this == OPEN:
        return TREE if trees >= 3 else OPEN

    # trees -> lumberyard if len(lumber> >= 3 else No change
    if this == TREE:
        return LUMB if lumber >= 3 else TREE

    # lumberyard -> lumberyard if len(lumberyard) >= 1 and len(trees) >= 1 else open
    if this == LUMB:
        if trees >= 1 and lumber >= 1:
            return LUMB

    return OPEN


def draw(state):
    for y in xrange(len(before)):
        for x in xrange(len(before[y])):
            print state[y][x],
        print ''



before = parse('input.txt')
after = [[c for c in row] for row in before]

# Store previous states
serialized = ''.join(''.join(row) for row in after)
previous_states = {
    serialized: 0
}
lumber_cnt = sum(1 for row in before for c in row if c == '#')
tree_cnt = sum(1 for row in before for c in row if c == '|')

print "Iteration {}. Result={}".format(0, lumber_cnt * tree_cnt)

for i in xrange(100000):
    update_grid(before, after)

    lumber_cnt = sum(1 for row in before for c in row if c == '#')
    tree_cnt = sum(1 for row in before for c in row if c == '|')

    print "Iteration {}. Result={}".format(i, lumber_cnt * tree_cnt)
    # draw(after)

    serialized = ''.join(''.join(row) for row in after)
    if serialized in previous_states:
        print "Cycle found: {} is repeat of {}".format(i, previous_states[serialized])
        break
    else:
        previous_states[serialized] = i

    after, before = before, after

#
# lumber_cnt = sum(1 for row in before for c in row if c == '#')
# tree_cnt = sum(1 for row in before for c in row if c == '|')
# print "Answer = {}".format(lumber_cnt * tree_cnt)

cycle_size = 444 - 416
remaining_its = 1000000000 - 444
offset = remaining_its % cycle_size

print "Cycle size: {}".format(cycle_size)
print "Answer at: {}".format(offset + 416)