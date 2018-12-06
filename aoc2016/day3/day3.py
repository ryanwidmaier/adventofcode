

def is_triangle(side1, side2, side3):
    if side1 + side2 <= side3:
        return False

    if side1 + side3 <= side2:
        return False

    if side2 + side3 <= side1:
        return False

    return True

def row_reader(infile):
    for line in infile:
        line = line.strip()
        sides = [int(s) for s in line.split()]
        yield sides[0], sides[1], sides[2]


def column_reader(infile):
    rows = []

    for row in row_reader(infile):
        rows.append(row)

        # When we have enough rows, emit the columns
        if len(rows) == 3:
            for i in xrange(3):
                yield rows[0][i], rows[1][i], rows[2][i]

            rows = []


infile = open('input.txt')
count = len([s1 for s1, s2, s3 in column_reader(infile) if is_triangle(s1, s2, s3)])

print count
