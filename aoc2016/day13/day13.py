from Queue import PriorityQueue

DEST = (31, 39)


def is_room(x, y):
    seed = 1350
    val = x*x + 3*x + 2*x*y + y + y*y + seed

    count = 0
    while val > 0:
        count += 0 if val % 2 == 0 else 1
        val >>= 1

    return count % 2 == 0


def possible_moves(pos):
    if is_room(pos[0] + 1, pos[1]):
        yield pos[0] + 1, pos[1]

    if pos[0] > 0 and is_room(pos[0] - 1, pos[1]):
        yield pos[0] - 1, pos[1]

    if is_room(pos[0], pos[1] + 1):
        yield pos[0], pos[1] + 1

    if pos[1] > 0 and is_room(pos[0], pos[1] - 1):
        yield pos[0], pos[1] - 1


def distance_remaining(pos):
    return abs(DEST[0] - pos[0]) + abs(DEST[1] - pos[1])


def a_star():
    # Encode start/end state so we can easily compare and store in sets
    start = (1, 1)

    # Setup structures to track our progress
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {start: None}
    cost_so_far = {start: 0}

    # Loop checking possibilities
    while not frontier.empty():
        current = frontier.get()
        if current == DEST:
            break

        for move in possible_moves(current):
            new_cost = cost_so_far[current] + 1
            if move not in cost_so_far or new_cost < cost_so_far[move]:
                cost_so_far[move] = new_cost
                priority = new_cost + distance_remaining(move)
                frontier.put(move, priority)
                came_from[move] = current

    # Walk back the path
    current = DEST
    solution = []
    while current != start:
        solution.append(current)
        current = came_from[current]

    solution.append(current)

    # Print it
    for idx, x in enumerate(solution):
        print idx, x


def paths(start_from, visited, distance):
    if distance == 50:
        return 1

    count = 0
    for move in possible_moves(start_from):
        if move not in visited:
            visited.add(move)
            count += paths(move, visited, distance + 1)

    return count + 1

# a_star()
result = paths((1, 1), set(), 0)
print result
