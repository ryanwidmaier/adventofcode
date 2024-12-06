

def argmax(seq, key=None):
    """
    Return the index of the max element on a list, or the key w/ the max value on a dict.  key can take a lambda
    that will be given the value and can return a derived key
     """
    if isinstance(seq, dict):
        seq = seq.items()
    else:
        seq = enumerate(seq)

    m = max(seq, key=lambda x: key(x[1]) if key else x[1])
    return m[0]


def argmin(seq, key=None):
    """
    Return the index of the max element on a list, or the key w/ the max value on a dict.  key can take a lambda
    that will be given the value and can return a derived key
     """
    if isinstance(seq, dict):
        seq = seq.items()
    else:
        seq = enumerate(seq)

    m = min(seq, key=lambda x: key(x[1]) if key else x[1])
    return m[0]


def minmax(seq, key=None):
    key = key if key else lambda v: v

    min_v = None
    min_k = None
    max_v = None
    max_k = None

    for v in seq:
        k = key(v)
        if min_k is None or k < min_k:
            min_v = v
            min_k = k

        if max_k is None or k > max_k:
            max_v = v
            max_k = k

    return (min_v, max_v)
