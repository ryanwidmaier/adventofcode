import numpy as np


def extend(tape_, pos_):
    """
    Args:
         tape_ (np.ndarray):
    """
    if pos < 0:
        new_tape = np.concatenate((np.zeros((1000)), tape_))
        return new_tape, pos_ + 1000

    if pos >= tape_.shape[0]:
        new_tape = np.concatenate((tape_, np.zeros((1000))))
        return new_tape, pos_

    return tape_, pos_


tape = np.zeros((1000, ))
pos = 500
state = 'A'

for i in xrange(12261543):
    tape, pos = extend(tape, pos)
    value = tape[pos]

    ###### STATE A #############
    if state == 'A':
        if value == 0:
            tape[pos] = 1
            pos += 1
            state = 'B'
        else:
            tape[pos] = 0
            pos -= 1
            state = 'C'
    ###### STATE B #############
    elif state == 'B':
        if value == 0:
            tape[pos] = 1
            pos -= 1
            state = 'A'
        else:
            tape[pos] = 1
            pos += 1
            state = 'C'
    ###### STATE C #############
    elif state == 'C':
        if value == 0:
            tape[pos] = 1
            pos += 1
            state = 'A'
        else:
            tape[pos] = 0
            pos -= 1
            state = 'D'
    ###### STATE D #############
    elif state == 'D':
        if value == 0:
            tape[pos] = 1
            pos -= 1
            state = 'E'
        else:
            tape[pos] = 1
            pos -= 1
            state = 'C'
    ###### STATE E #############
    elif state == 'E':
        if value == 0:
            tape[pos] = 1
            pos += 1
            state = 'F'
        else:
            tape[pos] = 1
            pos += 1
            state = 'A'
    ###### STATE F #############
    elif state == 'F':
        if value == 0:
            tape[pos] = 1
            pos += 1
            state = 'A'
        else:
            tape[pos] = 1
            pos += 1
            state = 'E'

    if i % 10000 == 0:
        print "{} iterations".format(i)


print "1's: ", np.count_nonzero(tape)
