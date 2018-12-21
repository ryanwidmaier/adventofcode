import re
from collections import defaultdict, namedtuple, deque
import itertools
from util import argmax, argmin, a_star, Coord, all_shortest_paths, GridWalker



moves = {
    'N': Coord(0, 1),
    'S': Coord(0, -1),
    'E': Coord(1, 0),
    'W': Coord(-1, 0)
}


class Map(object):
    def __init__(self):
        self.edges = defaultdict(lambda: set())

    def add_edges(self, walker):
        self.edges[walker.position.copy()].add(walker.previous.copy())
        self.edges[walker.previous.copy()].add(walker.position.copy())

    def walk(self, pattern, walkers, idx=0):
        """
        (AAAA|BBBB)
        NNNNN(EEE|WWW)SSSSS

        :param pattern:
        :return:
        """
        start = Coord(0, 0)
        pos = start.copy()

        # Copy the walkers, we need to advance a full set for each group
        active_walkers = [GridWalker(w.position) for w in walkers]
        all_walkers = []

        while idx < len(pattern):
            ch = pattern[idx]

            if ch == '^':
                active_walkers.append(GridWalker(pos))

            if ch in {'N', 'E', 'W', 'S'}:
                for w in active_walkers:
                    w.move(ch)
                    self.add_edges(w)

            if ch == '(':
                idx, sub_walkers = self.walk(pattern, active_walkers, idx+1)
                active_walkers = sub_walkers
            if ch == '|':
                all_walkers += active_walkers
                active_walkers = [GridWalker(w.position) for w in walkers]
            if ch == ')':
                all_walkers += active_walkers

                # Dedupe
                deduped = {gw.position: gw for gw in all_walkers}
                all_walkers = deduped.values()

                return idx, all_walkers

            idx += 1

    def longest_shortest_path(self):
        start = Coord(0, 0)

        def possible(c):
            return list(self.edges[c])

        paths = all_shortest_paths(start, possible)
        return max(paths, key=lambda p: len(p))

    def part2(self):
        start = Coord(0, 0)

        def possible(c):
            return list(self.edges[c])

        paths = all_shortest_paths(start, possible)
        return len([p for p in paths if len(p)-1 >= 1000])


# pattern = '^WNE$'  # Should be 3
# pattern = '^EEE(SS)E$'  # Should be 3
# pattern = '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$'  # Should be 18
# pattern = '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$'   # Should be 31
pattern = open('input.txt').read().strip()

m = Map()
m.walk(pattern, [])
longest = m.longest_shortest_path()

print "Length: {}".format(len(longest))
print "Part2: {}".format(m.part2())
