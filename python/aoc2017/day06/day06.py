input_val = '4	1	15	12	0	9	9	5	5	8	7	3	14	5	12	3'
board = [int(a) for a in input_val.split()]

def rebalance(b):
    idx, val = max(enumerate(b), key=lambda a: a[1])

    b[idx] = 0
    while val > 0:
        idx = (idx + 1) % len(b)
        b[idx] += 1
        val -= 1

def to_key(b):
    return ','.join([str(a) for a in b])

seen = {to_key(board): 0}

print '0', board
i = 0
while True:
    i += 1

    rebalance(board)
    print i, board

    key = to_key(board)
    if key in seen:
        print "Cycle length: ", i - seen[key]
        break

    seen[key] = i
