
with open('input.txt') as f:
    lines = f.readlines()


nice = 0

for line in lines:
    line = line.strip()
    # It does not contain the strings ab, cd, pq, or xy, even if they are part of
    #    one of the other requirements.
    if 'ab' in line or \
            'cd' in line or \
            'pq' in line or \
            'xy' in line:
        continue

    vowels = 0
    double = False
    for idx, ch in enumerate(line):
        # It contains at least three vowels (aeiou only), like aei, xazegov,
        #    or aeiouaeiouaeiou.
        if ch in {'a', 'e', 'i', 'o', 'u'}:
            vowels += 1
        # It contains at least one letter that appears twice in a row, like xx, abcdde (dd),
        #    or aabbccdd (aa, bb, cc, or dd).
        if idx > 0 and ch == line[idx-1]:
            double = True

    if not double or vowels < 3:
        continue

    nice += 1

print("Part 1: ", nice)



nice = 0
for line in lines:
    # It contains a pair of any two letters that appears at least twice in the string without
    #     overlapping, like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
    found = False
    for i in range(len(line)-1):
        for j in range(i+2, len(line) - 1):
            if line[i:i+2] == line[j:j+2]:
                found = True
                break
        if found:
            break

    if not found:
        continue

    # It contains at least one letter which repeats with exactly one letter
    #     between them, like xyx, abcdefeghi (efe), or even aaa.
    found = False
    for i in range(len(line)-2):
        if line[i] == line[i+2]:
            found = True
            break

    if not found:
        continue

    nice += 1


print("Part 2: ", nice)
