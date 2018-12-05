from collections import defaultdict


twos = 0
threes = 0

f = open('input.txt')
for idx, row in enumerate(f):
    row = row.strip()
    d = defaultdict(lambda: 0)

    print "{}: {}".format(idx, ''.join(sorted(row)))

    for ch in row:
        d[ch] += 1

    if 2 in d.values():
        print "{} has twos: {}".format(idx, row)
        twos += 1
    if 3 in d.values():
        print "{} has threes: {}".format(idx, row)
        threes += 1

print twos
print threes
print twos * threes


def is_match(b1, b2):
    diffs = 0
    for ch1, ch2 in zip(b1, b2):
        if ch1 != ch2:
            diffs += 1

        if diffs > 1:
            return False

    if diffs == 1:
        return True

    return False


def part2():
    boxes = []

    f = open('input.txt')
    for idx, row in enumerate(f):
        row = row.strip()

        # Compare to old boxes
        for b in boxes:
            if is_match(b, row):
                print b
                print row
                return

        boxes.append(row)

part2()

# revtaubfniyh u sgxdoajwkqilp
# revtaubfniyhpsgxdoajwkqilp
