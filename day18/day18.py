from util import Timer


def is_safe(idx, prev_row):
    left = '.' if idx == 0 else prev_row[idx-1]
    center = prev_row[idx]
    right = '.' if (idx + 1) == len(prev_row) else prev_row[idx + 1]

    if left == '^' and center == '^' and right == '.':
        return '^'

    if left == '.' and center == '^' and right == '^':
        return '^'

    if left == '^' and center == '.' and right == '.':
        return '^'

    if left == '.' and center == '.' and right == '^':
        return '^'

    return '.'


row = '......^.^^.....^^^^^^^^^...^.^..^^.^^^..^.^..^.^^^.^^^^..^^.^.^.....^^^^^..^..^^^..^^.^.^..^^..^^^..'
count = len([x for x in row if x == '.'])
timer = Timer()

for i in xrange(1, 400000):
    if timer.elapsed_secs() > 5:
        timer.reset()
        print "{} steps".format(i)

    row = ''.join([is_safe(j, row) for j in xrange(len(row))])
    count += len([x for x in row if x == '.'])


print "Num safe: {}".format(count)
# .^^.^.^^^^
# ^^^...^..^
# ^.^^.^.^^.
# ..^^...^^^
# .^^^^.^^.^
# ^^..^.^^..
# ^^^^..^^^.
# ^..^^^^.^^
# .^^^..^.^^
# ^^.^^^..^^
