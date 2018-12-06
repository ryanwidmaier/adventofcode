
loop = 100
tx = [0, 0] * (loop / 2)
expected = ['0', '1'] * (loop / 2)
idx = 0

while tx != expected:
    tx = []
    a = idx
    b = 0
    c = 0
    d = 0

    # 01: cpy a d
    # 02: cpy 11 c
    d = a
    c = 11

    while True:
        # 03: cpy 231 b
        b = 231

        # 04: inc d
        # 05: dec b
        # 06: jnz b -2
        while True:
            d += 1
            b -= 1

            if b == 0:
                break

        # 07: dec c
        # 08: jnz c -5
        c -= 1
        if c == 0:
            break

    for i in xrange(loop):
        # 09: cpy d a
        a = d

        while True:
            # 10: jnz 0 0
            # 11: cpy a b
            # 12: cpy 0 a
            # 13: cpy 2 c
            b = a
            a = 0
            c = 2

            while True:
                # 14: jnz b 2
                # 15: jnz 1 6
                if b == 0:
                    break

                # 16: dec b
                # 17: dec c
                b -= 1
                c -= 1

                # 18: jnz c -4
                if c == 0:
                    # 19: inc a
                    a += 1

                    # 20: jnz 1 -7
                    # 13 (rerun): cpy 2 c
                    c = 2

            # 21: cpy 2 b
            b = 2

            while True:
                # 22: jnz c 2
                # 23: jnz 1 4
                if c == 0:
                    break

                # 24: dec b
                # 25: dec c
                # 26: jnz 1 -4
                b -= 1
                c -= 1

            # 27: jnz 0 0
            # 28: out b
            tx.append(str(b))

            # 29: jnz a -19
            if a == 0:
                break

        # 30: jnz 1 -21
        pass

    print "IDX={}, A={}, TX={}".format(idx, a, ''.join(tx))
    idx += 1
