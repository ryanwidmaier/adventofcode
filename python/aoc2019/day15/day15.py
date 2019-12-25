from aoc2019.int_code import IntComputerFinal
from util import Coord, GridWalker, a_star, print_dict_grid
from collections import deque


OPEN = '.'
WALL = '#'
UNKNOWN = '?'
OXYGEN = 'O'
ROBOT = 'r'

directions = {
    'NORTH': 1,
    'EAST': 4,
    'SOUTH': 2,
    'WEST': 3
}

RESULT_WALL = 0
RESULT_OPEN = 1
RESULT_OXY = 2


def update_to_check(to_check, maze, pos):
    new_pos = [
        pos + Coord(0, 1),
        pos + Coord(0, -1),
        pos + Coord(1, 0),
        pos + Coord(-1, 0)
    ]

    for p in new_pos:
        if p not in maze:
            to_check.append(p)
            maze[p] = UNKNOWN


def find_input(pos, new_pos):
    if new_pos.y > pos.y:
        return 'NORTH'
    if new_pos.y < pos.y:
        return 'SOUTH'
    if new_pos.x < pos.x:
        return 'WEST'
    if new_pos.x > pos.x:
        return 'EAST'
    raise ValueError("Shouldn't get here")


# Funcs for path finding
def possible_moves(maze, pos):
    new_pos = [Coord(0, 1), Coord(0, -1), Coord(1, 0), Coord(-1, 0)]
    for p in new_pos:
        pp = pos + p
        if maze.get(pp) != WALL:
            yield pp, 1


def remaining(pos, goal):
    return pos.manhattan(goal)


def map_maze(comp):
    # Init the maze start
    maze = {Coord(0, 0): ROBOT}
    to_check = deque()
    oxygen = Coord(1000000, 100000000)

    robot = GridWalker(Coord(0, 0))
    update_to_check(to_check, maze, robot.position)

    # Start our program
    prog = comp.run()

    block_step = 0
    move_step = 0

    # 153, 1 --- (6, -8) -> (6, -8)

    # Walk until nothing left to check
    while len(to_check) > 0:
        block_step += 1
        move_step = 0

        target = to_check.pop()

        # Already resolved, just skip
        if maze.get(target) != UNKNOWN:
            continue

        # Find path to the next unresolved cell
        path = a_star(robot.position, target, lambda x: possible_moves(maze, x), remaining)
        for move_to in path:
            move_step += 1

            d = find_input(robot.position, move_to)
            comp.add_input(directions[d])
            output = next(prog)

            # Update state w/ result
            if output == RESULT_OPEN or output == RESULT_OXY:
                maze[robot.position] = OXYGEN if robot.position == oxygen else OPEN
                robot.move(d)
                maze[move_to] = ROBOT
                update_to_check(to_check, maze, robot.position)

                if output == RESULT_OXY:
                    oxygen = move_to

            elif output == RESULT_WALL:
                maze[move_to] = WALL

                # Our path was unexpectedly blocked, going to search for it again
                if move_to != target:
                    to_check.append(target)
                    break

            print(f'---------- {block_step}, {move_step} --- {robot.position} -> {target} --------------')
            print_dict_grid(maze, y_up=True)

    return maze


def part1(comp):
    maze = map_maze(comp)

    goal = next(c for c, v in maze.items() if v == OXYGEN)
    p = a_star(Coord(0, 0), goal, lambda x: possible_moves(maze, x), remaining)
    print(p)
    print(len(p))


def part2(comp):
    maze = map_maze(comp)
    oxy = next(c for c, v in maze.items() if v == OXYGEN)

    goals = [c for c, v in maze.items() if v in (OPEN, ROBOT)]

    ticks = max(len(a_star(oxy, g, lambda x: possible_moves(maze, x), remaining)) for g in goals)
    print(ticks)


comp = IntComputerFinal()
comp.program(comp.load_memory('input.txt'))
part2(comp)