import math


class Pos(object):
    def __init__(self):
        self.x = 0.
        self.y = 0.
        self.ring = 0
        self.step = 1

        # Map each direction to the radian degrees it is
        angle_vals = [math.radians(a) for a in xrange(30, 360, 60)]
        angle_labels = ['ne', 'n', 'nw', 'sw', 's', 'se']
        self.angles = dict(zip(angle_labels, angle_vals))

    def move(self, direction):
        self.x += math.cos(self.angles[direction])
        self.y += math.sin(self.angles[direction])

        dist = math.hypot(pos.x, pos.y)
        print "{}: Pos At=({:0.2f}, {:0.2f}), OriginDist={}".format(self.step, self.x, self.y, dist)
        self.step += 1


fin = open('input.txt')
dirs = fin.read().split(',')
pos = Pos()

dirs = ['ne', 'se'] * 10

for d in dirs:
    pos.move(d)