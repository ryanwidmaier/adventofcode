import re



def decompress(line):
    tag_re = re.compile(r'^\((\d+)x(\d+)\)')

    remaining = line
    decompressed = ''

    # Loop through string, finding consecutive open parens

    start = remaining.find('(')
    while start != -1:
        # Store the characters before this compression tag
        decompressed += remaining[:start]
        remaining = remaining[start:]

        # Interpret the compression tag
        match = tag_re.search(remaining)
        tag_len, length, repeat = int(len(match.group(0))), int(match.group(1)), int(match.group(2))

        # Apply the decompress op specified
        decompressed += remaining[tag_len:tag_len+length] * repeat

        # Find the next tag
        remaining = remaining[tag_len+length:]
        start = remaining.find('(')

    return decompressed + remaining


# sample_lines = [
#     'ADVENT',
#     'A(1x5)BC',
#     '(3x3)XYZ',
#     'A(2x2)BCD(2x2)EFG',
#     '(6x1)(1x3)A',
#     'X(8x2)(3x3)ABCY'
# ]
#
#
# for line in sample_lines:
#     print "Input : " + line
#     print "Output: " + decompress(line)

line = open('input.txt').read().rstrip()
print "Len: {}".format(len(decompress(line)))