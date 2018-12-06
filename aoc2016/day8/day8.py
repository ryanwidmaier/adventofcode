import re

class Pad(object):
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.mat = [['.' for _ in xrange(h)] for _ in xrange(w)]

    def display(self):
        s = ''
        for x in xrange(self.width):
            s += str(x % 10)

        print s
        for y in xrange(self.height):
            print ''.join(self._get_row(y))

    def rect(self, w, h):
        w = min(self.width, w)
        h = min(self.height, h)

        for x in xrange(w):
            for y in xrange(h):
                self.mat[x][y] = '#'

    def _get_row(self, y):
        return [self.mat[x][y] for x in xrange(self.width)]

    def rotate_row(self, y, amount):
        amount = amount % self.width
        chop = self.width - amount

        row = self._get_row(y)
        new_row = row[chop:] + row[0:chop]

        for x in xrange(self.width):
            self.mat[x][y] = new_row[x]

    def rotate_col(self, x, amount):
        amount = amount % self.height
        chop = self.height - amount

        row = self.mat[x]
        new_row = row[chop:] + row[0:chop]

        self.mat[x] = new_row

    def count(self):
        count = 0
        for col in self.mat:
            count += len([ch for ch in col if ch == '#'])

        return count


rect_re = re.compile(r'rect (\d+)x(\d+)')
rotate_row_re = re.compile(r'rotate row y=(\d+) by (\d+)')
rotate_col_re = re.compile(r'rotate column x=(\d+) by (\d+)')

pad = Pad(50, 6)
infile = open('input.txt')
#
# pad = Pad(7, 3)
# infile = open('sample.txt')


for line in infile:
    line = line.rstrip()
    pad.display()

    print ''
    print line

    match = rect_re.match(line)
    if match:
        pad.rect(int(match.group(1)), int(match.group(2)))
        continue

    match = rotate_row_re.match(line)
    if match:
        pad.rotate_row(int(match.group(1)), int(match.group(2)))
        continue

    match = rotate_col_re.match(line)
    if match:
        pad.rotate_col(int(match.group(1)), int(match.group(2)))
        continue

pad.display()
print "Count: {}".format(pad.count())