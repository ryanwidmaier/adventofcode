from util import a_star, Coord, shortest_path
from collections import defaultdict
from itertools import groupby
import unittest

ADJACENT = [Coord(1, 0), Coord(-1, 0), Coord(0, 1), Coord(0, -1)]


class NPC(object):
    next_id = 1

    def __init__(self, start, npc_type, attack=3):
        self.pos = start
        self.type = npc_type
        self.health = 200
        self.attack_amount = attack

        self.id = self.next_id
        NPC.next_id += 1

    def move(self, cave, enemies):
        def possible_moves_cost(current):
            # Cost cheaper when moving in reading order
            for a in ADJACENT:
                if cave.is_open(current + a):
                    yield current + a, 1

        def possible_moves(current):
            for a, cost in possible_moves_cost(current):
                yield a

        def score_path(p):
            adj = {
                Coord(0, -1): 1.00,
                Coord(-1, 0): 1.01,
                Coord(1, 0): 1.02,
                Coord(0, 1): 1.03
            }

            score = 0
            for i in xrange(1, len(p)):
                diff = p[i] - p[i-1]
                score += abs(adj[diff] * -1) * (len(p) - i)

            return score

        def prune(paths):
            grouped = defaultdict(lambda: [])
            for p in paths:
                grouped[p[-1]].append(list(p))

            for target, candidates in grouped.iteritems():
                yield min(candidates, key=lambda p: score_path(p))

        # print "{}{}  @ {}".format(self.type, self.id, self.pos)

        # If any enemies adjacent already..
        if len(self.adjacent_enemies(enemies)) > 0:
            # print "   already adjacent".format(self.type, self.id)
            return

        # Find attack squares
        attack_positions = [e.pos + a for e in enemies for a in ADJACENT]
        attack_positions = [a for a in attack_positions if cave.is_open(a)]
        # print "    {} potential destinations".format(len(attack_positions))

        # Filter by reachable
        closest = [a_star(self.pos, a, possible_moves_cost, lambda c, g: c.manhattan(g))
                   for a in attack_positions]
        closest = [c for c in closest if c]
        # print "    {} reachable".format(len(closest))

        if len(closest) == 0:
            return

        closest_path = min(closest, key=lambda p: (len(p), p[-1].y, p[-1].x))
        # print "    closest reachable target is {}".format(closest_path[-1])
        shortest = shortest_path(self.pos, closest_path[-1], possible_moves, prune)

        # Move 1
        # print "    moving {} -> {}".format(self.pos, shortest[1])
        self.pos = shortest[1]

    def attack(self, enemies):
        adj = self.adjacent_enemies(enemies)
        if len(adj) == 0:
            return None

        # We attack the weakest
        weakest = min(adj, key=lambda e: (e.health, e.pos.y, e.pos.x))

        # Attack!
        weakest.health -= self.attack_amount
        if weakest.health <= 0:
            return weakest

        return None

    def adjacent_enemies(self, enemies):
        adjacent = {self.pos + c for c in ADJACENT}
        return [e for e in enemies if e.pos in adjacent]


class Caves(object):
    def __init__(self, fname, elf_power=3, part2=False):
        self.npcs = {}
        self.cave = []
        self.tick_number = 0
        self.part2 = part2

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
                    n = NPC(start, ch, 3 if ch == 'G' else elf_power)
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
            if len(enemies) == 0:
                return True

            # Move to nearest enemy
            n.move(self, enemies)

            # Attack
            died = n.attack(enemies)

            # self.draw()
            if died:
                if self.part2 and died.type == 'E':
                    raise StopIteration("RIP Elf {}!".format(died.id))

                del self.npcs[died.id]

        return False

    def is_open(self, coord):
        return self.cave[coord.y][coord.x] == '.' and not any(n.pos == coord for n in self.npcs.itervalues())

    def draw(self):
        out = []
        critters = {n.pos: n for n in self.npcs.itervalues()}

        for y in xrange(len(self.cave)):
            line = ''

            row_healths = []
            for x, ch in enumerate(self.cave[y]):
                coord = Coord(x, y)
                if coord in critters:
                    ch = critters[coord].type
                    row_healths.append(critters[coord])

                line += ch + ' '

            line += '  '
            line += ', '.join("{}({})".format(n.type, n.health) for n in row_healths)
            out.append(line.rstrip())

        return out

    def get_winner(self):
        types = {n.type for n in self.npcs.itervalues()}
        return list(types)[0] if len(types) == 1 else None

    def remaining_hp(self):
        return sum(n.health for n in self.npcs.itervalues())


def run(filename, elf_power, part2=False):
    NPC.next_id = 1
    cave = Caves(filename, elf_power, part2)
    grid = cave.draw()

    print "Initial"
    print '\n'.join(grid)

    done = False
    while not done:
        done = cave.tick()
        grid = cave.draw()

        print ''
        print "Round {} Result".format(cave.tick_number)
        print '\n'.join(grid)
        print ''

        winner = cave.get_winner()

    round = cave.tick_number - 1
    answer = cave.remaining_hp() * round
    print "Winner is {} after {} rounds".format(winner, round)
    print "Answer is {} x {} = {}".format(cave.remaining_hp(), round, answer)

    return grid, answer


# def run_part2(filename):
#     elf_power = 100
#     lower, upper = 3, 200
#     last_success = True
#
#     attempts = [None] * 200
#     attempts[3] = False
#
#     while True:
#         print "Trying Elf Power = {}".format(elf_power)
#         elf_power = (upper - lower) / 2 + lower
#
#         try:
#             run('input.txt', elf_power)
#
#             # Success
#             attempts[elf_power] = True
#
#
#         except StopIteration, _:
#             # Fail (Elf died)
#             attempts[elf_power] = False



run('input.txt', 12, True)

# 3   - Fail
# 12  -
# 13  - True 59886
# 25  - True
# 50  - True
# 100 - True
