from itertools import chain
from util import a_star
import itertools
import copy


input_data = """
The first floor contains a polonium generator, a thulium generator, a thulium-compatible microchip, a promethium generator,
        a ruthenium generator, a ruthenium-compatible microchip, a cobalt generator, and a cobalt-compatible microchip.
The second floor contains a polonium-compatible microchip and a promethium-compatible microchip.
The third floor contains nothing relevant.
The fourth floor contains nothing relevant.
"""

THULIUM = 1
PROMENTHIUM = 2
RUTHENIUM = 3
COBALT = 4
POLONIUM = 5
ELERIUM = 6
DILITHIUM = 7

def GEN(element):
    return -1 * element


def MC(element):
    return element


def encode(elevator, floors_):
    floors_ = [sorted(f_) for f_ in floors_]
    floors_ = [[str(e) for e in f_] for f_ in floors_]
    floors_ = [','.join(f_) for f_ in floors_]

    return str(elevator) + '|' + ':'.join(floors_)


def decode(state_):
    elevator, _, floors_ = state_.partition('|')
    floors_ = floors_.split(':')
    floors_ = [f_.split(',') if f_ else [] for f_ in floors_]
    floors_ = [[int(e) for e in f_] for f_ in floors_]

    return int(elevator), floors_


def is_valid(floor):
    microchips = [m for m in floor if m > 0]
    generators = [m for m in floor if m < 0]

    # If there are no generators, all microchips are safe
    if len(generators) == 0:
        return True

    # Generator present, so all microchips must be plugged into their generators
    for m in microchips:
        g = m * -1
        if g not in generators:
            return False

        generators.remove(g)

    return True


def possible_moves(state_):
    elevator, floors_ = decode(state_)

    candidates = floors_[elevator]

    # Try moving 2 items
    for item1, item2 in itertools.combinations(candidates, 2):
        # Floor without the element we are moving
        new_floors = copy.deepcopy(floors_)
        new_floors[elevator].remove(item1)
        new_floors[elevator].remove(item2)

        if not is_valid(new_floors[elevator]):
            continue

        # Try to move up
        if elevator < len(floors_) - 1:
            new_floors[elevator+1].append(item1)
            new_floors[elevator+1].append(item2)

            if is_valid(new_floors[elevator+1]):
                yield encode(elevator+1, new_floors), 1

            # Restore original floor
            new_floors[elevator+1] = floors_[elevator+1]

        # Try to move down
        if elevator > 0:
            new_floors[elevator-1].append(item1)
            new_floors[elevator-1].append(item2)

            if is_valid(new_floors[elevator-1]):
                yield encode(elevator-1, new_floors), 1

    for item in candidates:
        # Floor without the element we are moving
        new_floors = copy.deepcopy(floors_)
        new_floors[elevator].remove(item)

        # Will the floor we depart from be valid if we move this?
        if not is_valid(new_floors[elevator]):
            continue

        # can we move the item up?
        if elevator < len(floors_) - 1:
            new_floors[elevator+1].append(item)
            if is_valid(new_floors[elevator+1]):
                yield encode(elevator+1, new_floors), 1

            # Restore original floor
            new_floors[elevator+1] = floors_[elevator+1]

        # Can we move the item down?
        if elevator > 0:
            new_floors[elevator-1].append(item)
            if is_valid(new_floors[elevator-1]):
                yield encode(elevator-1, new_floors), 1


def distance_remaining(state_, goal):
    elevator, floors_ = decode(state_)

    dest = len(floors_) - 1
    result = sum([(dest - i) * len(f_) for i, f_ in enumerate(floors_)])

    return result


# Init the starting state
initial_state = [
    [GEN(POLONIUM), GEN(THULIUM), MC(THULIUM), GEN(PROMENTHIUM), GEN(RUTHENIUM), MC(RUTHENIUM), GEN(COBALT), MC(COBALT),
     GEN(ELERIUM), MC(ELERIUM), GEN(DILITHIUM), MC(DILITHIUM)],
    [MC(POLONIUM), MC(PROMENTHIUM)],
    [],
    []
]
goal_state = [
    [],
    [],
    [],
    list(chain(*initial_state))
]

start = encode(0, initial_state)
goal = encode(3, goal_state)

# Find the solution!
path = a_star(start, goal, possible_moves, distance_remaining)

for state in path:
    el, floors = decode(state)

    for idx, f in enumerate(floors[::-1]):
        elems = ' '.join(['{:3d}'.format(q) for q in f])
        print "F{}: {}".format(len(floors) - idx, elems)

    print ""


print "# moves: {}".format(len(path))
