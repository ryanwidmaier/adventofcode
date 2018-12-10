from datetime import datetime, timedelta
import logging
from Queue import PriorityQueue
import math
from collections import defaultdict, namedtuple
import string

logger = logging.getLogger(__name__)


class Coord(object):
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def move(self, x=0, y=0, z=0):
        return Coord(self.x + x, self.y + y, self.z + z)

    def manhattan(self, target=None):
        target = Coord(0, 0, 0) if target is None else target
        return abs(self.x - target.x) + abs(self.y - target.y) + abs(self.z - target.z)

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z

        return self

    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y, self.z - other.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other):
        return not (self.x == other.x and self.y == other.y and self.z == other.z)

    def __hash__(self):
        """Overrides the default implementation"""
        return hash(tuple(sorted(self.__dict__.items())))

    def __str__(self):
        if self.z:
            return "({}, {}, {})".format(self.x, self.y, self.z)

        return "({}, {})".format(self.x, self.y)

    def __repr__(self):
        return str(self)

class CoordMat(object):
    def __init__(self, r=0, c=0):
        self.r = r
        self.c = c

    def move(self, r=0, c=0):
        return CoordMat(self.r + r, self.c + c)

    def manhattan(self, target=None):
        target = CoordMat(0, 0) if target is None else target
        return abs(self.r - target.r) + abs(self.c - target.c)

    def __add__(self, other):
        return CoordMat(self.r + other.r, self.c + other.c)

    def __iadd__(self, other):
        self.r += other.r
        self.c += other.c

        return self

    def __sub__(self, other):
        return CoordMat(self.r - other.r, self.c - other.c)

    def __eq__(self, other):
        return self.r == other.r and self.c == other.c

    def __ne__(self, other):
        return not (self.r == other.r and self.c == other.c)

    def __hash__(self):
        """Overrides the default implementation"""
        return hash(tuple(sorted(self.__dict__.items())))


class Timer:
    """ Utility class for measuring elapsed time """

    def __init__(self):
        self.start = datetime.now()

    def reset(self):
        """ Reset the timer back to 0.0 elapsed """
        self.start = datetime.now()

    def elapsed(self):
        """
        Elapsed time since object construction or last reset call
        :return: A timedelta object repesenting the elapsed time
        """
        return datetime.now() - self.start

    def elapsed_secs(self):
        """
        Return how many seconds have elapsed
        :return: A float of elapsed seconds
        """
        return (datetime.now() - self.start).total_seconds()


def cartesian_distance(pos, goal):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(pos, goal)]))


def a_star(start, goal, possible_moves_fn, distance_remaining_fn=None):
    """

    :param start:
    :param goal:
    :param possible_moves_fn: func(current_position) -> iterable of (new_pos, move_cost)
    :param distance_remaining_fn: func(pos, goal) -> estimated cost to finish
    :return:
    """
    states_tried = 0

    if distance_remaining_fn is None:
        distance_remaining_fn = cartesian_distance

    # Encode start/end state so we can easily compare and store in sets
    start = start

    # Setup structures to track our progress
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    timer = Timer()

    # Loop checking possibilities
    while not frontier.empty():
        _, current = frontier.get()

        states_tried += 1
        if timer.elapsed_secs() > 5:
            timer.reset()
            print("States tried: {}, Dist: {}".format(states_tried, distance_remaining_fn(current, goal)))

        if current == goal:
            break

        for move, move_cost in possible_moves_fn(current):
            new_cost = cost_so_far[current] + move_cost
            if move not in cost_so_far or new_cost < cost_so_far[move]:
                cost_so_far[move] = new_cost
                priority = new_cost + distance_remaining_fn(move, goal)
                frontier.put((priority, move))
                came_from[move] = current

    # Walk back the path
    current = goal
    solution = []
    while current != start:
        solution.append(current)
        current = came_from[current]

    # Print it
    return solution[::-1]


AsmCommand = namedtuple('AsmCommand', 'cmd reg value')


class Assembler(object):
    """
    Framework for implementing assembly command simulation.  Override execute command to handle the different
    commands.
    """

    def __init__(self):
        self.registers = defaultdict(lambda: 0)
        self.commands = []
        self.index = 0
        self.instructions_run = 0

    def parse(self, filename):
        fin = open(filename)
        for line in fin:
            line = line.rstrip()

            tokens = line.split()

            cmd = tokens[0]
            reg = tokens[1] if len(tokens) > 1 else None
            val = tokens[2] if len(tokens) > 2 else None

            self.commands.append(AsmCommand(cmd, reg, val))

    def read_register(self, register):
        """ Return the value of a register, or the value if it is a literal """
        if register in string.ascii_letters:
            return self.registers[register]

        return int(register)

    def run(self):
        """ Run the simulation """
        while 0 <= self.index < len(self.commands):
            command = self.commands[self.index]

            self.execute(command.cmd, command.reg, command.value)
            self.index += 1
            self.instructions_run += 1

    def execute(self, command, register, value):
        pass

    def jump(self, amount):
        self.index += self.read_register(amount) - 1  # -1 b/c we always do + 1 after each instruction


def argmax(seq, key=None):
    """
    Return the index of the max element on a list, or the key w/ the max value on a dict.  key can take a lambda
    that will be given the value and can return a derived key
     """
    if isinstance(seq, dict):
        seq = seq.items()
    else:
        seq = enumerate(seq)

    m = max(seq, key=lambda x: key(x[1]) if key else x[1])
    return m[0]


def argmin(seq, key=None):
    """
    Return the index of the max element on a list, or the key w/ the max value on a dict.  key can take a lambda
    that will be given the value and can return a derived key
     """
    if isinstance(seq, dict):
        seq = seq.items()
    else:
        seq = enumerate(seq)

    m = min(seq, key=lambda x: key(x[1]) if key else x[1])
    return m[0]


def point_in_triangle(point, tri, boundary_counts=False):
    """ return true if a point is inside a triangle """
    def sign(p1, p2, p3):
        return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

    d1 = sign(point, tri[0], tri[1])
    d2 = sign(point, tri[1], tri[2])
    d3 = sign(point, tri[2], tri[0])

    if not boundary_counts:
        if d1 == 0 or d2 == 0 or d3 == 0:
            return False

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)


class RateLogger(object):
    """
    Helper class for printing status when processing lots of records. You can use this class to keep track of
    how many records you have processed and print every N records so you can get a rough feel of how far the process
    is and how fast it is going.
    """
    def __init__(self, log_every_n=1000, log_fn=None):
        self.total = 0
        self.diff = 0
        self.log_every_n = log_every_n
        self.timer = Timer()

        self.log_fn = log_fn
        if not self.log_fn:
            self.log_fn = lambda r: "Processing {} records took {}s.  Total={}".format(r.log_every_n,
                                                                                       r.timer.elapsed_secs(),
                                                                                       r.total)

    def inc(self, n=1):
        self.diff += n

        # start total used to store the original total so we can have it at the correct values both at the end of this
        # fn and in the loop.
        start_total = self.total
        self.total = int(self.total / self.log_every_n) * self.log_every_n

        while self.diff >= self.log_every_n:
            self.diff -= self.log_every_n

            # Incrementing total here so available for log with correct value. Needs to be done here in case
            # n is greater than the log_every_n size.
            self.total += self.log_every_n
            print self.log_fn(self)

            # Reset the timer for the next block
            self.timer.reset()

        # Set total to the correct final total which may not line up with the block size
        self.total = start_total + n

    def total_time(self):
        return self.timer.elapsed()
