h = 0
start = 84 * 100 + 100000

for b in xrange(start, start+17000, 17):
    found = False

    for d in xrange(2, b):
        for e in xrange(2, b):
            if d * e == b:
                f = True

    if found:
        h += 1
