def is_overlap(a, b):
    not_overlap = a[0] - 1 > b[1] or a[1] + 1 < b[0]
    return not not_overlap


def union(a, b):
    return min(a[0], b[0]), max(a[1], b[1])


def print_ip(val):
    octet4 = val & 0xff
    octet3 = (val >> 8) & 0xff
    octet2 = (val >> 16) & 0xff
    octet1 = (val >> 32) & 0xff

    return "{}.{}.{}.{}".format(octet1, octet2, octet3, octet4)


ranges = []

infile = open('input.txt')
for line in infile:
    line = line.rstrip()

    left, _, right = line.partition('-')
    ranges.append((int(left), int(right)))


ranges = sorted(ranges, key=lambda x: x[0])

combined = []
for x in ranges:
    if len(combined) == 0:
        combined.append(x)
    else:
        if is_overlap(combined[-1], x):
            combined[-1] = union(combined[-1], x)
        else:
            combined.append(x)

for x in combined:
    print x


smallest = 0
if combined[0][0] == 0:
    smallest = combined[0][1] + 1


print "Val: {}".format(smallest)
print "IP: {}".format(print_ip(smallest))

excluded = sum([x[1] - x[0] + 1 for x in combined])
print "# Valid: {}".format(2**32 - excluded)
