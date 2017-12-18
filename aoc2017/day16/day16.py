import networkx as nx


def parse_input(filename):
    result = open(filename).read()
    return result.split(',')


def do_stuff(state, steps):

    for step in steps:
        # Shift
        if step.startswith('s'):
            amount = int(step[1:]) % len(state)
            state = state[-amount:] + state[:-amount]
        # Swap by pos
        elif step.startswith('x'):
            pos1, pos2 = step[1:].split('/')
            pos1, pos2 = int(pos1), int(pos2)

            swap = state[pos1]
            state[pos1] = state[pos2]
            state[pos2] = swap
        # Swap by name
        elif step.startswith('p'):
            name1, name2 = step[1:].split('/')
            pos1 = state.index(name1)
            pos2 = state.index(name2)

            swap = state[pos1]
            state[pos1] = state[pos2]
            state[pos2] = swap

    return state


def main():
    data = parse_input('input.txt')

    state = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']
    result = do_stuff(state, data)

    print "Result: ", ''.join(result)

    state = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']
    state_history = {}

    print "Result (0): ", ''.join(state)
    state_history[''.join(state)] = 0

    start = int((1000000000 / 36) * 36) + 1
    for x in xrange(start, 1000000001):
        state = do_stuff(state, data)
        state_str = ''.join(state)

        # if state_str in state_history:
        #     print "Found Cycle {} - {}, state={}".format(state_history[state_str], x, state_str)

        state_history[state_str] = x

        print "Result ({}): ".format(x), ''.join(state)



if __name__ == '__main__':
    main()

