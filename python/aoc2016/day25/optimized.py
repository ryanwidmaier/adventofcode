
loop = 15
check = 30

tx = [0]
expected = ['0', '1'] * (check / 2)
expected2 = ['1', '0'] * (check / 2)
idx = 0

while tx[:check] != expected and tx[:check] != expected2:
    tx = []
    a = idx
    b = 0
    c = 0
    d = 0

    # 01: cpy a d
    # 02: cpy 11 c
    d = a
    c = 11

    # 03: cpy 231 b
    b = 231

    # 04: inc d
    # 05: dec b
    # 06: jnz b -2
    d += 231 * c
    c = 0

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

            b -= c
            c = 0

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
