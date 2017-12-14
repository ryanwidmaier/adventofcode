
file_in = open('input.txt')

cnt = 0
total = 0

for line in file_in:
    line = line.rstrip()
    words = line.split()

    tokens = set()
    is_valid = True

    for w in words:
        sort_w = ''.join(sorted(w))
        if sort_w in tokens:
            is_valid = False
            break

        tokens.add(sort_w)

    cnt += 1 if is_valid else 0
    total += 1

print "{} of {}".format(cnt, total)
