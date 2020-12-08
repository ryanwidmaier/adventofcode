

def decode(v):
    row = v[:7]
    col = v[-3:]

    row = row.replace('F', '0').replace('B', '1')
    col = col.replace('L', '0').replace('R', '1')

    row = int(row, 2)
    col = int(col, 2)

    seat = row * 8 + col

    return row, col, seat



# row 70, col 7, seat 567
d = 'BFFFBBFRRR'
r, c, s = decode(d)

print(d, r, c, s)


seats = set()
m = 0
with open('input.txt') as f:
    for line in f:
        line = line.strip()
        r, c, s = decode(line)
        seats.add(s)

        m = max(s, m)

print(m)


seats = sorted(seats)
for x in range(m):
    if x + 1 in seats and x - 1 in seats and x not in seats:
        print(x)

