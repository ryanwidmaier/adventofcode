import re
from collections import defaultdict, namedtuple
import itertools
from util import argmax, argmin, a_star, Coord

parse_re = re.compile(r'')


f = open('input.txt')
for line in f:
    line = line.rstrip()

    match = parse_re.search(line)
    if match:
        pass


# If the Elves think their skill will improve after making 9 recipes, the scores of the ten recipes after the
# first nine on the scoreboard would be 5158916779 (highlighted in the last line of the diagram).
#
# After 5 recipes, the scores of the next ten would be 0124515891.
# After 9 recipses, the scores of the next ten would be 5158916779
# After 18 recipes, the scores of the next ten would be 9251071085.
# After 2018 recipes, the scores of the next ten would be 5941429882.

#  0 #   (3) [7]
#  1 #   (3) [7] 1  0
#  2 #   3    7  1 [0] (1) 0
#  3 #   3    7  1  0  [1] 0 (1)
#  4 #   (3)  7  1  0   1  0 [1] 2
#  5 #   3    7  1  0  (1) 0  1  2 [4]
#  6 #   3    7  1 [0]  1  0 (1) 2  4   5
#  7 #   3    7  1  0  [1] 0  1  2 (4)  5   1
#  8 #   3   (7) 1  0   1  0 [1] 2  4   5   1  5
#  9 #   3    7  1  0   1  0  1  2 [4] (5)  1  5  8
# 10 #   3   (7) 1  0   1  0  1  2  4   5   1  5  8  [9]
# 11 #   3    7  1  0   1  0  1 [2] 4  (5)  1  5  8   9  1  6
# 12 #   3    7  1  0   1  0  1  2  4   5  [1] 5  8   9  1 (6) 7
# 13 #   3    7  1  0  (1) 0  1  2  4   5   1  5 [8]  9  1  6  7  7
# 14 #   3    7 [1] 0   1  0 (1) 2  4   5   1  5  8   9  1  6  7  7  9
# 15 #   3    7  1  0  [1] 0  1  2 (4)  5   1  5  8   9  1  6  7  7  9  2


def run():
    puzzle_input_check = [0, 7, 4, 5, 0, 1]
    # puzzle_input_check = [5,1,5,8,9]
    check_len = len(puzzle_input_check)

    elf1 = 0
    elf2 = 1

    scores = [3, 7]
    while True:
        # Update recipes
        new_score = scores[elf1] + scores[elf2]
        if new_score > 9:
            scores.append(1)
            new_score %= 10

            if scores[-check_len:] == puzzle_input_check:
                return len(scores) - check_len

        scores.append(new_score)
        if scores[-check_len:] == puzzle_input_check:
            return len(scores) - check_len

        # Update elfs
        elf1 = (elf1 + scores[elf1] + 1) % len(scores)
        elf2 = (elf2 + scores[elf2] + 1) % len(scores)


# print ''.join([str(d) for d in scores[puzzle_input:puzzle_input+10]])
print run()