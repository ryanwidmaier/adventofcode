from collections import namedtuple
import hashlib

Path = namedtuple('Path', 'pos path')


open_chars = {'b', 'c', 'd', 'e', 'f'}
def next_moves(path):
    open_dirs = []
    m = hashlib.md5()
    m.update(path.path)
    hex_val = m.hexdigest()

    # Up
    if path.pos[1] > 0 and hex_val[0] in open_chars:
        open_dirs.append(Path((path.pos[0], path.pos[1]-1), path.path + 'U'))

    # Down
    if path.pos[1] < 3 and hex_val[1] in open_chars:
        open_dirs.append(Path((path.pos[0], path.pos[1]+1), path.path + 'D'))

    # Left
    if path.pos[0] > 0 and hex_val[2] in open_chars:
        open_dirs.append(Path((path.pos[0]-1, path.pos[1]), path.path + 'L'))

    # Right
    if path.pos[0] < 3 and hex_val[3] in open_chars:
        open_dirs.append(Path((path.pos[0]+1, path.pos[1]), path.path + 'R'))

    return open_dirs


seed = 'rrrbmfta'
paths = [
    Path((0, 0), 'rrrbmfta')
]

def expand_paths(paths):
    new_paths = []
    for p in paths:
        new_paths += list(next_moves(p))

    return new_paths

longest = None
while len(paths) > 0:
    if any([p.pos == (3, 3) for p in paths]):
        longest = next(p.path for p in paths if p.pos == (3, 3))
        paths = [p for p in paths if p.pos != (3, 3)]

    paths = expand_paths(paths)



print "Longest: {}".format(len(longest) - len(seed))
