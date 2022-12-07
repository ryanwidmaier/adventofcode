
def twist(hbuf, start, length_):
    if length_ == 0:
        return hbuf

    if length_ > len(hbuf):
        print "Invalid length: {}".format(length_)
        return hbuf

    end = (start + length_) % len(hbuf)

    # Case 1: Length doesn't wrap
    if start < end:
        before, reverse, after = hbuf[:start], hbuf[start:end], hbuf[end:]
        return before + list(reversed(reverse)) + after

    # Case 2: Length does wrap
    rev_tail, middle, rev_head = hbuf[:end], hbuf[end:start], hbuf[start:]
    reverse = list(reversed(rev_head + rev_tail))
    new_head, new_tail = reverse[:len(rev_head)], reverse[len(rev_head):]
    return new_tail + middle + new_head


def twist_pass(hbuf, pos, skip, lengths_):
    for length in lengths_:
        hbuf = twist(hbuf, pos, length)
        pos = (pos + skip + length) % len(hbuf)
        skip += 1

    return hbuf, pos, skip


def twist_full(lengths_str):
    skip = 0
    pos = 0
    hbuf = list(xrange(256))

    # Convert input string to lengths string and add std suffix
    lengths_ = [ord(c) for c in lengths_str] + [17, 31, 73, 47, 23]

    # Do passes of the hash
    for _ in xrange(64):
        hbuf, pos, skip = twist_pass(hbuf, pos, skip, lengths_)

    # Dense hash
    dense = [reduce(lambda a, b: a ^ b, hbuf[idx:idx+16]) for idx in xrange(0, len(hbuf), 16)]

    return ''.join(['{:02x}'.format(x) for x in dense])


def test(s, expected):
    print ''
    print 'String: ' + s
    print 'Expected: ' + expected
    print 'Actual:   ' + twist_full(s)


# Example test case
test('',         'a2582a3a0e66e6e86e3812dcb672a272')
test('AoC 2017', '33efeb34ea91902bb2f59c9920caa6cd')
test('1,2,3',    '3efbe78a8d82f29979031a4aa0b16a9d')
test('1,2,4',    '63960835bcdc130f0b66d7ff4f6a5a8e')

# Actual run
test('192,69,168,160,78,1,166,28,0,83,198,2,254,255,41,12', '???')
