import re
from collections import defaultdict, namedtuple
import itertools
from util import argmax, argmin, a_star, Coord, RateLogger
import logging
from collections import deque


logging.basicConfig(level=logging.INFO)

parse_re = re.compile(r'')



class Circle(object):
    def __init__(self):
        self.circle = deque([0])

    def insert(self, marble):
        # Move forward to insert pos
        self.move(2)
        self.circle.appendleft(marble)

    def score(self):
        self.move(-7)
        return self.circle.popleft()

    def move(self, n):
        while n > 0:
            self.circle.append(self.circle.popleft())
            n -= 1
        while n < 0:
            self.circle.appendleft(self.circle.pop())
            n += 1


class Player(object):
    def __init__(self, id):
        self.id = id
        self.score = 0
        self.last_scored = 0

    def go(self, marble, circle):
        if marble > 0 and marble % 23 == 0:
            removed = circle.score()
            self.last_scored = removed + marble
            # print "Player {} scored {} + {} = {}".format(self.id, removed, marble, self.last_scored)
            self.score += self.last_scored
        else:
            circle.insert(marble)



# Input
# 473 players; last marble is worth 70904 points

# Example
# 10 players; last marble is worth 1618 points: high score is 8317
# 13 players; last marble is worth 7999 points: high score is 146373
# 17 players; last marble is worth 1104 points: high score is 2764
# 21 players; last marble is worth 6111 points: high score is 54718
# 30 players; last marble is worth 5807 points: high score is 37305
num_players = 473

players = [Player(i) for i in xrange(1, num_players+1)]
circ = Circle()

pidx = 0
marble = 1
max_iters = 70904 * 100


rate_logger = RateLogger(log_every_n=10000)
while max_iters > marble:
    players[pidx].go(marble, circ)

    pidx = (pidx + 1) % len(players)
    marble += 1

    rate_logger.inc()
    # print circ.circle[circ.current_marble], circ.circle

players.sort(key=lambda p: p.score, reverse=True)
winner = players[0]
print "Winner is {}, with score of {}, {} iterations".format(winner.id, winner.score, marble)


