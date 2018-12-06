import re
from collections import deque
from collections import namedtuple

Tag = namedtuple('Tag', 'start end count repeat')


def decompress(line):
    tag_re = re.compile(r'^\((\d+)x(\d+)\)')

    remaining = line
    decompressed_len = 0

    # Loop through string, finding consecutive open parens

    start = remaining.find('(')
    while start != -1:
        # Store the characters before this compression tag
        decompressed_len += start
        remaining = remaining[start:]

        # Interpret the compression tag
        match = tag_re.search(remaining)
        tag_len, length, repeat = int(len(match.group(0))), int(match.group(1)), int(match.group(2))

        # Apply the decompress op specified
        decompressed_len += decompress(remaining[tag_len:tag_len+length]) * repeat

        # Find the next tag
        remaining = remaining[tag_len+length:]
        start = remaining.find('(')

    return decompressed_len + len(remaining)


# sample_lines = [
#     '(3x3)XYZ',
#     'X(8x2)(3x3)ABCY',
#     '(27x12)(20x12)(13x14)(7x10)(1x12)A',
#     '(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN'
# ]
# for line in sample_lines:
#     print "input : {}".format(line)
#     print "output: {}".format(decompress(line))

line = open('input.txt').read().rstrip()
print "Len: {}".format(decompress(line))