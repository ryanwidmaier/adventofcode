from collections import deque
import re


def index_of(q, letter_):
    for idx, ch in enumerate(q):
        if letter_ == ch:
            return idx

    raise ValueError("letter not found!")


def swap(q, pos1, pos2):
    if pos1 >= len(q) or pos2 >= len(q):
        raise IndexError('blarg')

    if pos1 < 0 or pos2 < 0:
        raise IndexError('blarg')

    c = q[pos1]
    q[pos1] = q[pos2]
    q[pos2] = c
    return q


def move(q, pos1, pos2):
    letter_ = q[pos1]
    new_q = deque()
    while len(q) > 0:
        if len(new_q) == pos2:
            new_q.append(letter_)
        else:
            l = q.popleft()
            if l != letter_:
                new_q.append(l)

    if len(new_q) == pos2:
        new_q.append(letter_)

    return new_q


def rotate(q, letter_):
    pos = index_of(q, letter_)
    rotate = 1 + pos + (1 if pos >= 4 else 0)
    q.rotate(rotate)
    return q


def unrotate(q, letter_):
    end_pos = index_of(q, letter_)
    # 0: s x - - - - - - : 1
    # 1: - s - x - - - - : 3
    # 2: - - s - - x - - : 5
    # 3: - - - s - - - x : 7
    # 4: - - x - s - - - : 2
    # 5: - - - - x s - - : 4
    # 6: - - - - - - x - : 6
    # 7: x - - - - - - s : 0
    d = {
        0: -1,
        1: -1,
        2: 2,
        3: -2,
        4: 1,
        5: -3,
        6: 0,
        7: 4
    }
    q.rotate(d[end_pos])
    return q


rotate_re = re.compile(r'rotate (left|right) (\d+) steps?')
rotate_letter_re = re.compile(r'rotate based on position of letter (\w+)')
swap_pos_re = re.compile(r'swap position (\d+) with position (\d+)')
swap_letter_re = re.compile(r'swap letter (\w+) with letter (\w+)')
reverse_re = re.compile(r'reverse positions (\d+) through (\d+)')
move_re = re.compile(r'move position (\d+) to position (\d+)')



# test_q = deque('abcdefgh')
# for letter in 'abcdefgh':
#     rotate(test_q, letter)
#
#     print 'rotate ' + letter
#     print '0 1 2 3 4 5 6 7'
#     print ' '.join(test_q)
#
#     unrotate(test_q, letter)
#
#     print 'unrotate ' + letter
#     print '0 1 2 3 4 5 6 7'
#     print ' '.join(test_q)
#     print ''
#
#
# import sys
# sys.exit(1)

password = deque('fbgdceah')
expected = len(password)

# Reverse input lines
lines = []
infile = open('input.txt')
for line in infile:
    lines.append(line)

lines = lines[::-1]


for line in lines:
    if len(password) != expected:
        break

    line = line.rstrip()
    print '0 1 2 3 4 5 6 7'
    print ' '.join(password)
    print ''
    print line

    match = rotate_re.match(line)
    if match:
        direction, steps = match.groups()
        steps = int(steps)
        if direction == 'right':
            steps *= -1

        password.rotate(steps)
        continue

    match = rotate_letter_re.match(line)
    if match:
        letter = match.group(1)
        password = unrotate(password, letter)
        continue

    match = swap_pos_re.match(line)
    if match:
        p1, p2 = match.groups()
        p1, p2 = int(p1), int(p2)
        password = swap(password, p1, p2)
        continue

    match = swap_letter_re.match(line)
    if match:
        l1, l2 = match.groups()
        p1 = index_of(password, l1)
        p2 = index_of(password, l2)
        password = swap(password, p1, p2)
        continue

    match = reverse_re.match(line)
    if match:
        p1, p2 = match.groups()
        left, right = int(p1), int(p2)
        while left < right:
            password = swap(password, left, right)
            left += 1
            right -= 1
        continue

    match = move_re.match(line)
    if match:
        p1, p2 = match.groups()
        p1, p2 = int(p1), int(p2)
        password = move(password, p2, p1)
        continue


print ''.join(password)
