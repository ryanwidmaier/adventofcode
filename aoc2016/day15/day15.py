from util import Timer


class Disk(object):
    def __init__(self, size, start):
        self.size = size
        self.pos = start

    def rotate(self, amount=1):
        self.pos = (self.pos + amount) % self.size

    def is_open(self):
        return self.pos == 0

# Disc #1 has 17 positions; at time=0, it is at position 1.
# Disc #2 has 7 positions; at time=0, it is at position 0.
# Disc #3 has 19 positions; at time=0, it is at position 2.
# Disc #4 has 5 positions; at time=0, it is at position 0.
# Disc #5 has 3 positions; at time=0, it is at position 0.
# Disc #6 has 13 positions; at time=0, it is at position 5.
disks = [
    Disk(17, 1),
    Disk(7, 0),
    Disk(19, 2),
    Disk(5, 0),
    Disk(3, 0),
    Disk(13, 5),
    Disk(11, 0)
]

# Disc #1 has 5 positions; at time=0, it is at position 4.
# Disc #2 has 2 positions; at time=0, it is at position 1.
# disks = [
#     Disk(5, 4),
#     Disk(2, 1)
# ]

# Advance lower disks so we can just check for all holes aligned at the same time
for i in xrange(1, len(disks)):
    for j in xrange(i, len(disks)):
        disks[j].rotate()

# Now walk through the sim until everything is aligned
timestamp = 0
timer = Timer()
while not all([d.is_open() for d in disks]):
    if timer.elapsed_secs() > 5:
        timer.reset()
        print "Timestamp {}".format(timestamp)

    for d in disks:
        d.rotate()

    timestamp += 1

print "Aligned at {}".format(timestamp-1)

