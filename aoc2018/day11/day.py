from collections import defaultdict, namedtuple
import numpy as np
from scipy import signal
import itertools


SEED = 7857
MAX_SIZE = 300
MAX_X = 300
MAX_Y = 300


def level(x, y):
    rack_id = x + 10
    result = (rack_id * y + SEED) * rack_id
    result = (result / 100) % 10
    return result - 5


def build():
    matrix = np.zeros((301, 301), dtype=np.int16)
    for x in xrange(1, 300+1):
        for y in xrange(1, 300+1):
            matrix[x][y] = level(x, y)
    return matrix


def convolve_(matrix, x, y, size):
    return sum(matrix.get(x+dx, {}).get(y+dy, 0) for dx in xrange(size) for dy in xrange(size))


def dicts_method():
    matrix = defaultdict(lambda: {})
    for x in xrange(1, 300+1):
        for y in xrange(1, 300+1):
            matrix[x][y] = level(x, y)

    result = (0, (0, 0))
    for s in xrange(3, 4):
        print "S: " + str(s)
        new_result = max([(convolve_(matrix, x, y, s), (x, y)) for x in xrange(1, 301-s + 1) for y in xrange(1, 301-s + 1)])
        result = max(result, new_result)

    print result


def convolve_method(matrix):
    print matrix[1:10, 1:10]

    result = (0, (0, 0), 0)
    for s in xrange(1, MAX_SIZE+1):
        conv_filter = np.ones((s, s))
        boxes = signal.convolve2d(matrix, conv_filter, 'valid')

        largest = np.unravel_index(np.argmax(boxes, axis=None), boxes.shape)
        largest_val = matrix[largest[0], largest[1]]

        new_result = (largest_val, largest, s)

        result = max(new_result, result)
        print "S={}, max={}, UL={}".format(s, largest_val, largest)
        print boxes[1:10, 1:10]

    print result


def update_method(matrix):
    boxes = np.zeros((301, 301))
    result = (0, (0, 0), 0)

    for s in xrange(1, MAX_SIZE+1):
        offset = s - 1

        for x, y in itertools.product(xrange(1, MAX_X+1), xrange(1, MAX_Y+1)):
            if x >= 301 - s or y >= 301 - s:
                boxes[x, y] = 0
            else:
                aa = matrix[x+offset, y:y+offset+1]
                bb = matrix[x:x + offset, y+offset]
                boxes[x, y] += sum(aa)
                boxes[x, y] += sum(bb)

        ind = np.unravel_index(np.argmax(boxes, axis=None), boxes.shape)
        new_result = (matrix[ind[0], ind[1]], ind, s)

        result = max(new_result, result)
        print "S={}, max={}, UL={}".format(s, matrix[ind[0], ind[1]], ind)

    print result


def view_method(matrix):
    max_value = -99999999
    max_coord = (0, 0, 1)

    for s in xrange(1, MAX_SIZE+1):
        for x, y in itertools.product(xrange(1, MAX_X+1), xrange(1, MAX_Y+1)):
            val = matrix[x:x+s, y:y+s].sum()

            if val > max_value:
                max_value = val
                max_coord = (x, y, s)

        print "S={}".format(s)

    print max_coord
    print max_value


m_ = build()

view_method(m_)
# update_method(m_)


