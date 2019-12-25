from datetime import datetime, timedelta
import logging
from queue import PriorityQueue
import math
from collections import defaultdict, namedtuple
import string

logger = logging.getLogger(__name__)


class Coord(object):
    def __init__(self, x=0, y=0, z=0):
        if isinstance(x, str):
            x = int(x)

        if isinstance(y, str):
            y = int(y)

        if isinstance(z, str):
            z = int(z)

        self.x = x
        self.y = y
        self.z = z

    def move(self, x=0, y=0, z=0):
        return Coord(self.x + x, self.y + y, self.z + z)

    def manhattan(self, target=None):
        target = Coord(0, 0, 0) if target is None else target
        return abs(self.x - target.x) + abs(self.y - target.y) + abs(self.z - target.z)

    def cartesian(self, target=None):
        target = Coord(0, 0, 0) if target is None else target
        return cartesian_distance((self.x, self.y, self.z),
                                  (target.x, target.y, target.z))

    def neighbors(self, diagnol=False):
        yield self + Coord(1, 0)
        if diagnol:
            yield self + Coord(1, 1)

        yield self + Coord(0, 1)
        if diagnol:
            yield self + Coord(-1, 1)

        yield self + Coord(-1, 0)
        if diagnol:
            yield self + Coord(-1, -1)

        yield self + Coord(0, -1)
        if diagnol:
            yield self + Coord(1, -1)

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z
        raise KeyError()

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z

        return self

    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        """ Multiply by scalar """
        ret = self.copy()
        ret.x *= other
        ret.y *= other
        ret.z *= other
        return ret

    def __div__(self, other):
        ret = self.copy()
        ret.x /= other
        ret.y /= other
        ret.z /= other
        return ret

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x

        return self.y < other.y

    def __ne__(self, other):
        return not (self.x == other.x and self.y == other.y and self.z == other.z)

    def __hash__(self):
        """Overrides the default implementation"""
        return hash((self.x, self.y, self.z))

    def __str__(self):
        if self.z:
            return "({:,}, {:,}, {:,})".format(self.x, self.y, self.z)

        return "({:,}, {:,})".format(self.x, self.y)

    def __repr__(self):
        return 'Coord' + str(self)

    def copy(self):
        return Coord(x=self.x, y=self.y, z=self.z)

    @staticmethod
    def minmax(*coords):
        min_y = min(c.y for c in coords)
        max_y = max(c.y for c in coords)
        min_x = min(c.x for c in coords)
        max_x = max(c.x for c in coords)

        return Coord(min_x, min_y), Coord(max_x, max_y)


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


class GridWalker(object):
    """ Grid coordinate that can move in cardinal directions. """
    def __init__(self, start, track_path=False):
        self.position = start.copy()
        self.previous = None
        self.track_path = track_path
        self.path = [start]
        self.steps = 0

    def move(self, direction, n=1):
        d = direction.upper()
        if d in {'W', 'WEST'}:
            self.west(n)
        elif d in {'E', 'EAST'}:
            self.east(n)
        elif d in {'N', 'NORTH'}:
            self.north(n)
        elif d in {'S', 'SOUTH'}:
            self.south(n)

    def north(self, n=1):
        self._do_move(Coord(0, n))

    def south(self, n=1):
        self._do_move(Coord(0, -n))

    def east(self, n=1):
        self._do_move(Coord(n, 0))

    def west(self, n=1):
        self._do_move(Coord(-n, 0))

    def _do_move(self, offset):
        self.previous = self.position.copy()
        self.position += offset
        self.steps += offset.manhattan()

        if self.track_path:
            self.path.append(self.position.copy())

    def __repr__(self):
        return 'GridWalker({})'.format(repr(self.position))


class GridCar(object):
    """ Grid coordinate with associated facing direction that can move forward/backward and turn. """
    dirs = ['north', 'east', 'south', 'west']

    def __init__(self, start, facing, invert_y=False):
        """
        Args:
            start (Coord)
            facing (str): North, South, East, West
        """
        self.position = start
        self.facing = facing.lower()
        self.invert_y = invert_y
        self.path = [start]

    def forward(self, amount=1):
        for x in range(amount):
            self.position = self._next_coord_in_dir(self.facing)
            self.path.append(self.position.copy())

    def _next_coord_in_dir(self, direction):
        shift = Coord(0, 0)
        if direction == 'north':
            shift = Coord(0, -1 if self.invert_y else 1)
        elif direction == 'south':
            shift = Coord(0, 1 if self.invert_y else -1)
        elif direction == 'east':
            shift = Coord(1, 0)
        elif direction == 'west':
            shift = Coord(-1, 0)

        return self.position + shift

    def backward(self, amount=1):
        self.forward(amount * -1)

    def left(self):
        self.facing = self.dirs[(self.dirs.index(self.facing) - 1) % 4]

    def right(self):
        self.facing = self.dirs[(self.dirs.index(self.facing) + 1) % 4]

    def forward_coord(self):
        return self._next_coord_in_dir(self.facing)

    def left_coord(self):
        left_dir = self.dirs[(self.dirs.index(self.facing) - 1) % 4]
        return self._next_coord_in_dir(left_dir)

    def right_coord(self):
        right_dir = self.dirs[(self.dirs.index(self.facing) + 1) % 4]
        return self._next_coord_in_dir(right_dir)

    def backward_coord(self):
        back_dir = self.dirs[(self.dirs.index(self.facing) + 2) % 4]
        return self._next_coord_in_dir(back_dir)

    def reverse(self):
        self.facing = self.dirs[(self.dirs.index(self.facing) + 2) % 4]

    def turn_to(self, direction):
        self.facing = direction.lower()


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
    Find the shortest path

    Args:
        start: Starting state
        goal: Target state
        possible_moves_fn: func(current_position) -> iterable of (new_pos, move_cost)
        distance_remaining_fn: func(pos, goal) -> estimated cost to finish
    Returns:

    """
    states_tried = 0

    if distance_remaining_fn is None:
        distance_remaining_fn = cartesian_distance

    # Setup structures to track our progress
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    timer = Timer()
    found = False

    # Loop checking possibilities
    while not frontier.empty():
        _, current = frontier.get()

        states_tried += 1
        if timer.elapsed_secs() > 5:
            timer.reset()
            print("States tried: {}, Dist: {}".format(states_tried, distance_remaining_fn(current, goal)))

        if current == goal:
            found = True
            break

        for move, move_cost in possible_moves_fn(current):
            new_cost = cost_so_far[current] + move_cost
            if move not in cost_so_far or new_cost < cost_so_far[move]:
                cost_so_far[move] = new_cost
                priority = new_cost + distance_remaining_fn(move, goal)
                frontier.put((priority, move))
                came_from[move] = current

    if not found:
        return None

    # Walk back the path
    current = goal
    solution = []
    while current != start:
        solution.append(current)
        current = came_from[current]

    # Print it
    return solution[::-1]


def shortest_path_bfs(start, goal, possible_moves, prune_paths):
    """
    Compute all shortest paths.  Assumes each move is the same cost.  Not as efficient as A* !!

    Args:
         start: Starting state/position
         goal: lambda, returns true when goal reached
         possible_moves: func(current, goal) -> [next_move1, next_move2]
         prune_paths: func(paths: list(list(state))) -> list(list(state)).  Lets you remove partial paths from
            further consideration
    Returns:
        list[list[state]]: List of shortest paths
    """
    visited = {start}
    paths = [[start]]

    #               .
    #    .        . x .
    #  . x .    . x - x .
    #    .        . x .
    #               .

    while any(goal(p[-1]) for p in paths):
        new_paths = []

        # Add all possible 1 move paths from frontier that don't have a shorter path
        for path in paths:
            possible_dests = possible_moves(path[-1])
            for pd in possible_dests:
                if pd not in visited:
                    new_paths.append(path + [pd])

        if not new_paths:
            return None

        # Let the caller prune paths if they want
        new_paths = prune_paths(new_paths)

        # Throw out remaining duplicates
        collapse = {}
        for p in new_paths:
            if p[-1] not in collapse:
                collapse[p[-1]] = p
                visited.add(p[-1])

        paths = collapse.values()

    return next(p for p in paths if p[-1] == goal)


def all_shortest_paths(start, possible_moves):
    """
    Compute all shortest paths.  Assumes each move is the same cost.  Not as efficient as A* !!

    Args:
         start: Starting state/position
         possible_moves: func(current) -> [next_move1, next_move2]
    Returns:
        list[list[state]]: List of shortest paths
    """
    shortest = {start: [start]}
    frontier = [start]

    while len(frontier) > 0:
        new_frontier = set()
        for point in frontier:
            next_points = possible_moves(point)

            for np in next_points:
                # If we are backtracking, ignore this one
                if np in shortest.keys():
                    continue

                new_frontier.add(np)
                shortest[np] = shortest[point] + [np]

        frontier = new_frontier

    return shortest.values()


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

class Memoize:
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}

    def __call__(self, *args):
        if args not in self.memo:
            self.memo[args] = self.fn(*args)
        return self.memo[args]


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


def minmax(seq, key=None):
    key = key if key else lambda v: v

    min_v = None
    min_k = None
    max_v = None
    max_k = None

    for v in seq:
        k = key(v)
        if min_k is None or k < min_k:
            min_v = v
            min_k = k

        if max_k is None or k > max_k:
            max_v = v
            max_k = k

    return (min_v, max_v)


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
            print(self.log_fn(self))

            # Reset the timer for the next block
            self.timer.reset()

        # Set total to the correct final total which may not line up with the block size
        self.total = start_total + n

    def total_time(self):
        return self.timer.elapsed()


def grid_walk(grid):
    for y, row in enumerate(grid):
        for x, d in enumerate(row):
            yield Coord(x, y), d


def print_dict_grid(grid, y_up=False):
    if len(grid) == 0:
        print()
        return


    min_x = min(h.x for h in grid)
    min_y = min(h.y for h in grid)
    max_x = max(h.x for h in grid)
    max_y = max(h.y for h in grid)

    if y_up:
        for y in range(max_y, min_y - 1, -1):
            for x in range(min_x, max_x + 1):
                c = grid.get(Coord(x, y), ' ')
                print(c, end='')

            print()
    else:
        for y in range(min_y, max_y+1):
            for x in range(min_x, max_x+1):
                c = grid.get(Coord(x, y), ' ')
                print(c, end='')

            print()