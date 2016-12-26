from Queue import PriorityQueue
from itertools import chain, combinations

input_data = """
The first floor contains a polonium generator, a thulium generator, a thulium-compatible microchip, a promethium generator,
        a ruthenium generator, a ruthenium-compatible microchip, a cobalt generator, and a cobalt-compatible microchip.
The second floor contains a polonium-compatible microchip and a promethium-compatible microchip.
The third floor contains nothing relevant.
The fourth floor contains nothing relevant.
"""

initial_state = [
    ['polonium|G', 'thulium|G', 'thulium|M', 'promethium|G', 'ruthenium|G', 'ruthenium|M', 'cobalt|G', 'cobalt|M'],
    ['polonium|M', 'promethium|M'],
    [],
    []
]
goal_state = [
    [],
    [],
    [],
    list(chain(*initial_state))
]
person_floor = 0


class State(object):
    def __init__(self, level, floors):
        self.elevator = level
        self.floors = floors

    @staticmethod
    def from_str(value):
        split = value.split('\n')
        return int(split[0]), [set(s.split(',')) for s in split[1:]]

    def to_str(self):
        return str(self.elevator) + '\n' + '\n'.join([','.join(sorted(f)) for f in self.floors])

    def possible_moves(self):
        level = self.elevator

        # Try the 1 moves
        for thing in self.floors[level]:


            # Up
            if level < len(self.floors):


        # Try the 2 moves

    @staticmethod
    def valid_floor(floor):
        microchips = [t for t in floor if t.endswith('|M')]
        generators = [t for t in floor if t.endswith('|G')]

        if len(generators) == 0:
            return True

        # TODO should handle case with multiple of the same type?
        for m in microchips:
            generator = m[:-2] + '|G'
            if generator not in floor:
                return False

        return True


def distance_remaining(state):
    """ Score how close to being done we are, with 0 being finished """
    num_floors = len(state)
    return sum([len(state[i]) * (num_floors - i) for i in xrange(num_floors)])


def a_star(initial_state_, goal_state_):
    # Encode start/end state so we can easily compare and store in sets
    encoded_start = encode_state(initial_state_, 0)
    encoded_goal = encode_state(goal_state_, 0)

    # Setup structures to track our progress
    frontier = PriorityQueue()
    frontier.put(encoded_start, 0)
    came_from = {encoded_start: None}
    cost_so_far = {encoded_start: 0}

    # Loop checking possibilities
    while not frontier.empty():
        current = frontier.get()
        level, state = decode_state(current)

        if current == encoded_goal:
            break

        for move in possible_moves(level, state):
            new_cost = cost_so_far[current] + 1
            if move not in cost_so_far or new_cost < cost_so_far[move]:
                cost_so_far[move] = new_cost
                priority = new_cost + distance_remaining(move)
                frontier.put(move, priority)
                came_from[move] = current

    # Walk back the path
    current = encoded_goal
    solution = []
    while current != encoded_start:
        solution.append(current)
        current = came_from[current]

    solution.append(current)

    # Print it
    for idx, x in enumerate(solution):
        print idx
        print x
        print ''


a_star(initial_state, goal_state)
