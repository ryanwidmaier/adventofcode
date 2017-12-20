import string


def can_move(direction, grid_, r, c, allow_forbidden):
    r, c = move(direction, r, c)
    forbidden = {'E': '|', 'W': '|', 'S': '-', 'N': '-'}

    if r < 0 or r >= len(grid_):
        return False

    if c < 0 or c >= len(grid_[r]):
        return False

    if not allow_forbidden:
        if grid_[r][c] == forbidden[direction]:
            return False

    return grid_[r][c] != ' '


def move(direction, r, c):
    if direction == 'S':
        r += 1
    elif direction == 'N':
        r -= 1
    elif direction == 'E':
        c += 1
    elif direction == 'W':
        c -= 1

    return r, c


fin = open('input.txt')
grid = []
for line in fin:
    grid.append(line)

dirs = {
    'S': 'SEW',
    'N': 'NEW',
    'E': 'ENS',
    'W': 'WNS'
}

# Find start
r, c = 0, grid[0].find('|')


letter = []
last_dir = 'S'
while True:
    print "@ {},{}".format(r, c)

    if grid[r][c] in string.ascii_letters:
        letter.append(grid[r][c])

        print ""
        print letter
        print ""

    # First check moving straight
    cant_move = True
    for idx, try_dir in enumerate(dirs[last_dir]):
        if can_move(try_dir, grid, r, c, idx==0):
            r, c = move(try_dir, r, c)
            last_dir = try_dir
            cant_move = False
            break

    if cant_move:
        break

print letter
