from util import Timer


def step(a):
    b = ''.join(['1' if ch == '0' else '0' for ch in a[::-1]])
    return a + '0' + b


def checksum(val):
    return ''.join(['1' if val[i] == val[i+1] else '0' for i in xrange(0, len(val), 2)])


random_bytes = '00101000101111010'
random_len = 35651584


# Generate random bytes
timer = Timer()
while len(random_bytes) < random_len:
    if timer.elapsed_secs() > 2:
        timer.reset()
        print "Len: {}".format(len(random_bytes))

    random_bytes = step(random_bytes)

# Drop extra bytes
random_bytes = random_bytes[:random_len]

# Compute checksum
check = checksum(random_bytes)
while len(check) % 2 == 0:
    if timer.elapsed_secs() > 2:
        timer.reset()
        print "Checksum len: {}".format(len(check))

    check = checksum(check)

# print "Random bytes: {}".format(random_bytes)
print "Checksum: {}".format(check)
