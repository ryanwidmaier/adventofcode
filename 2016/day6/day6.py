from collections import defaultdict

infile = open('input.txt')
counts = []

for line in infile:
    line = line.rstrip()
    if not line:
        continue

    for idx, ch in enumerate(line):
        if idx >= len(counts):
            counts.append(defaultdict(lambda: 0))

        counts[idx][ch] += 1


def get_char(pos_count):
    most_frequent = min(pos_count.items(), key=lambda x: x[1])
    return most_frequent[0]


message = ''.join([get_char(d) for d in counts])
print message
