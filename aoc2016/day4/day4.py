from collections import defaultdict, namedtuple
import re

Room = namedtuple('Room', 'id sector checksum')


def parse_room(line):
    room, _, end = line.rpartition('-')
    sector, _, checksum = end.partition('[')
    checksum = checksum[:-1]  # Strip trailing ]

    return Room(room, int(sector), checksum)


def compute_checksum(room):
    # Strip dashes
    room_chars = room.id.translate(None, '-')

    # Count characters
    chars = defaultdict(lambda: 0)
    for ch in room_chars:
        chars[ch] += 1

    ordered = sorted(chars.items(), key=lambda x: (x[1],  ord(x[0]) * -1), reverse=True)
    return ''.join([o[0] for o in ordered[:5]])


def shift_char(ch, amount):
    if ch == '-':
        return ' '

    shifted = (ord(ch) - ord('a')) + amount
    new_ch = (shifted % 26) + ord('a')
    return chr(new_ch)


def shift_room(room):
    return ''.join([shift_char(ch, room.sector) for ch in room.id])



value = 0

infile = open('input.txt')
for line in infile:
    line = line.rstrip()

    room = parse_room(line)
    checksum = compute_checksum(room)

    # If valid
    if room.checksum == checksum:
        decrypted = shift_room(room)
        print "{} - {}".format(decrypted, room.sector)
        value += room.sector


print "Summed: {}".format(value)
