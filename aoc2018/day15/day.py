from util import a_star, Coord, shortest_path
from collections import defaultdict
from itertools import groupby

ADJACENT = [Coord(1, 0), Coord(-1, 0), Coord(0, 1), Coord(0, -1)]


class NPC(object):
    next_id = 1

    def __init__(self, start, npc_type):
        self.pos = start
        self.type = npc_type
        self.health = 200

        self.id = self.next_id
        NPC.next_id += 1

    def move(self, cave, enemies):
        def possible_moves(current):
            # Cost cheaper when moving in reading order
            for a in ADJACENT:
                if cave.is_open(current + a):
                    yield current + a

        def score_path(p):
            adj = {
                Coord(-1, 0): 1.00,
                Coord(0, -1): 1.01,
                Coord(0, 1): 1.02,
                Coord(1, 0): 1.03
            }

            score = 0
            for i in xrange(1, len(p)):
                diff = p[i] - p[i-1]
                score += abs(adj[diff] * -1)

            return score

        def prune(paths):
            for target, candidate_paths in groupby(paths, key=lambda p: p[-1]):
                yield min(candidate_paths, key=lambda p: score_path(p))

        # If any enemies adjacent already..
        if len(self.adjacent_enemies(enemies)) > 0:
            return

        # Find attack squares
        attack_positions = [e.pos + a for e in enemies for a in ADJACENT]
        attack_positions = [a for a in attack_positions if cave.is_open(a)]

        # Filter by reachable
        # shortest = [a_star(self.pos, a, possible_moves, lambda c, g: c.manhattan(g))
        #             for a in attack_positions]
        shortest = [shortest_path(self.pos, a, possible_moves, prune)
                    for a in attack_positions]

        shortest = [p for p in shortest if p is not None]
        if len(shortest) == 0:
            return

        # Keep only the closest
        best = min(shortest, key=lambda p: (len(p), p[-1].y, p[-1].x))

        # Move 1
        self.pos = best[1]

    def attack(self, enemies):
        adj = self.adjacent_enemies(enemies)
        if len(adj) == 0:
            return None

        # We attack the weakest
        weakest = min(adj, key=lambda e: e.health)

        # Attack!
        weakest.health -= 3
        if weakest.health <= 0:
            return weakest

        return None

    def adjacent_enemies(self, enemies):
        adjacent = {self.pos + c for c in ADJACENT}
        return [e for e in enemies if e.pos in adjacent]


class Caves(object):
    def __init__(self, fname):
        self.npcs = {}
        self.cave = []
        self.tick_number = 0

        # Read in cave
        raw_cave = []
        with open(fname) as f:
            for line in f:
                raw_cave.append(line.rstrip())

        # Create the goblins/elves and populate the cave
        for y in xrange(len(raw_cave)):
            self.cave.append('')
            for x, ch in enumerate(raw_cave[y]):
                start = Coord(x, y)

                if ch in {'G', 'E'}:
                    n = NPC(start, ch)
                    self.npcs[n.id] = n
                    ch = '.'

                self.cave[-1] += ch

    def tick(self):
        self.tick_number += 1

        # Sort in read order
        ordered = sorted(self.npcs.itervalues(), key=lambda n: (n.pos.y, n.pos.x))

        for n in ordered:
            # If they died..
            if n.id not in self.npcs:
                continue

            enemies = [e for e in self.npcs.itervalues() if e.type != n.type]

            # Move to nearest enemy
            n.move(self, enemies)

            # Attack
            died = n.attack(enemies)

            # self.draw()
            if died:
                del self.npcs[died.id]

    def is_open(self, coord):
        return self.cave[coord.y][coord.x] == '.' and not any(n.pos == coord for n in self.npcs.itervalues())

    def draw(self):
        critters = {n.pos: n for n in self.npcs.itervalues()}

        for y in xrange(len(self.cave)):
            row_healths = []
            for x, ch in enumerate(self.cave[y]):
                coord = Coord(x, y)
                if coord in critters:
                    ch = critters[coord].type
                    row_healths.append(critters[coord])

                print ch,

            print '  ',
            print ','.join("{}({})".format(n.type, n.health) for n in row_healths)

        print ''

    def get_winner(self):
        types = {n.type for n in self.npcs.itervalues()}
        return list(types)[0] if len(types) == 1 else None

    def remaining_hp(self):
        return sum(n.health for n in self.npcs.itervalues())


cave = Caves('input.txt')

print "Initial"
cave.draw()

winner = cave.get_winner()
while winner is None:
    cave.tick()

    print "Round {}".format(cave.tick_number)
    cave.draw()

    winner = cave.get_winner()

round = cave.tick_number - 1
answer = cave.remaining_hp() * round
print "Winner is {} after {} rounds".format(winner, round)
print "Answer is {} x {} = {}".format(cave.remaining_hp(), round, answer)