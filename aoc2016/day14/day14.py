import hashlib
from collections import deque

salt = 'abc'


def get_sequence(value, min_length=3):
    cnt = 0
    last_ch = None

    for ch in value:
        if ch == last_ch:
            cnt += 1
        else:
            if cnt >= min_length:
                yield last_ch * cnt
            last_ch = ch
            cnt = 1

    if cnt >= 3:
        yield last_ch * cnt


def get_first_sequence_3(value):
    seqs = list(get_sequence(value, 3))
    if len(seqs) > 0:
        return seqs[0]

    return None


def gen_candidates(seed, count):
    for idx_ in xrange(count):
        m = hashlib.md5()
        m.update(seed + str(idx_))
        digest = m.hexdigest()

        seq = get_first_sequence_3(digest)
        if seq:
            yield idx_, digest, seq

        idx_ += 1


def get_sequence_5s(seed, count):
    for idx_ in xrange(count):
        m = hashlib.md5()
        m.update(seed + str(idx_))
        digest = m.hexdigest()

        for seq in get_sequence_5s(digest):
            yield idx_, digest, seq

        idx_ += 1


def is_key(key_seq, start_idx, long_seqs):
    ch = key_seq[0]

    i = 0
        cand_idx, _, cand_seq = candidates[i]
        if cand_seq[0]

    return False


queue = deque()
keys = []
stop_at = None


candidates = gen_candidates(salt, 200000)

for idx, candidate in enumerate(candidates):


    # if it's a 5-sequence, we should check the previous 1000 for possible keys
    if len(sequence) >= 5:
        found = find_key(queue, sequence[0])
        if found and found not in keys:
            keys.append(found)

        if stop_at is None and len(keys) > 64:
            stop_at = i + 1000

        if stop_at is not None and i >= stop_at:
            break

    # Add to the queue
    queue.append((i, hash_val, sequence))


for i, r in enumerate(sorted(keys)):
    print i, r
