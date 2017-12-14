import math
from util import a_star


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

        dist = math.hypot(self.x, self.y)
        print "{}: Pos At=({:0.2f}, {:0.2f}), OriginDist={}".format(self.step, self.x, self.y, dist)
        self.step += 1


def possible_moves(pos):
    angle_vals = [math.radians(a) for a in xrange(30, 360, 60)]
    for a in angle_vals:
        n = (pos[0] + math.cos(a), pos[1] + math.sin(a))
        yield n, 1


def distance_remaining(pos, goal):
    r =  math.hypot(pos[0] - goal[0], pos[1] - goal[1])
    return r


fin = open('input.txt')
dirs = fin.read().split(',')
child = Pos()

dirs = ['ne', 'se'] * 10

for d in dirs:
    child.move(d)


p = a_star((child.x, child.y), (0, 0), possible_moves, distance_remaining)
print len(p)
