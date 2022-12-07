import hashlib
from datetime import datetime, timedelta


seed = 'jlmsuwbz'


def gen_lines(seed, count):
    last = datetime.now()

    for i in xrange(count):
        value = seed + str(i)
        for x in xrange(2017):
            m = hashlib.md5()
            m.update(value)

            value = m.hexdigest()

        if datetime.now() - last > timedelta(seconds=5):
            print "{} lines generated".format(i+1)
            last = datetime.now()

        yield value


def get_sequence(value):
    last_ch = None
    cnt = 0

    for ch in value:
        if ch == last_ch:
            cnt += 1
        else:
            if cnt >= 3:
                return last_ch

            last_ch = ch
            cnt = 1

    if cnt >= 3:
        return last_ch

    return None


def find_long_seq(lines, start_at, target):
    for i in xrange(start_at, start_at+1000):
        if target in lines[i]:
            return True

    return False


found = 1

all_lines = list(gen_lines(seed, 50000))
for idx, line in enumerate(all_lines):
    seq_ch = get_sequence(line)
    if seq_ch is not None:
        long_seq = seq_ch * 5

        if find_long_seq(all_lines, idx+1, long_seq):
            print "{}: {} {} {}".format(found, idx, line, seq_ch * 3)
            found += 1

    if found > 66:
        break



