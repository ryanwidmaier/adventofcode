import re
from util import Coord


class Particle(object):
    def __init__(self, idx, pos, v, a):
        self.idx = idx
        self.pos = pos
        self.velocity = v
        self.accel = a

    def update(self):
        self.velocity += self.accel
        self.pos += self.velocity
        self.distance = self.pos.manhattan()


pattern = re.compile(
    r'p=<(?P<px>-?\d+),(?P<py>-?\d+),(?P<pz>-?\d+)>, '
    r'v=<(?P<vx>-?\d+),(?P<vy>-?\d+),(?P<vz>-?\d+)>, '
    r'a=<(?P<ax>-?\d+),(?P<ay>-?\d+),(?P<az>-?\d+)>'
)


# Read in the particles
particles = {}
fin = open('input.txt')
for idx, line in enumerate(fin):
    line = line.rstrip()

    match = pattern.match(line)
    if match:
        pos = Coord(int(match.group('px')), int(match.group('py')), int(match.group('pz')))
        vel = Coord(int(match.group('vx')), int(match.group('vy')), int(match.group('vz')))
        acc = Coord(int(match.group('ax')), int(match.group('ay')), int(match.group('az')))

        particles[idx] = Particle(idx, pos, vel, acc)

# Run the simulation
for x in xrange(5000):
    positions = {}
    to_delete = set()

    for p in particles.itervalues():
        p.update()

        if p.pos in positions:
            to_delete.add(p.idx)
            to_delete.add(positions[p.pos])
        else:
            positions[p.pos] = p.idx

    for p_idx in to_delete:
        print "Deleting ", p_idx
        del particles[p_idx]

    if x % 100 == 0:
        print "{} iterations".format(x)


closest = min(particles.values(), key=lambda p: p.distance)
print closest.idx


print len(particles)
