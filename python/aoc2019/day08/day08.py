import numpy as np

with open('input.txt') as f:
    data = f.read()
    data = [int(c) for c in data]

DIM1 = 25
DIM2 = 6


def part1():
    layers = len(data) // (DIM1 * DIM2)
    array = np.array(data).reshape(layers, DIM1 * DIM2)

    min_layer = np.argmin(np.count_nonzero(array == 0, axis=1))
    ones = np.count_nonzero(array[min_layer, ...] == 1)
    twos = np.count_nonzero(array[min_layer, ...] == 2)

    print(f"{ones * twos}")


def project(array, x, y):
    for l in range(array.shape[0]):
        if array[l, y, x] != 2:
            d = array[l, y, x]
            if d == 0:
                return ' '
            return '*'

    return None


def part2():
    layers = len(data) // (DIM1 * DIM2)
    array = np.array(data).reshape(layers, DIM2, DIM1)

    for y in range(DIM2):
        for x in range(DIM1):
            print(project(array, x, y), end='')
        print()


part2()
