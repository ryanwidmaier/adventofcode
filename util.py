from datetime import datetime, timedelta
from Queue import PriorityQueue
import math


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
        return Coord(self.x + other.x, self.y + other.y, self.z + other.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other):
        return not (self.x == other.x and self.y == other.y and self.z == other.z)

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
            print "States tried: {}, Dist: {}".format(states_tried, distance_remaining_fn(current, goal))

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

