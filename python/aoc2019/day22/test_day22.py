import unittest
from aoc2019.day22.day22 import LinearFn


def example():
    m = 119315717514047
    n = 101741582076661
    pos = 2020
    shuffles = {'deal with increment ': lambda x, m, a, b: (a * x % m, b * x % m),
                'deal into new stack': lambda _, m, a, b: (-a % m, (m - 1 - b) % m),
                'cut ': lambda x, m, a, b: (a, (b - x) % m)}
    a, b = 1, 0
    with open('2019/22/input.txt') as f:
        for s in f.read().strip().split('\n'):
            for name, fn in shuffles.items():
                if s.startswith(name):
                    arg = int(s[len(name):]) if name[-1] == ' ' else 0
                    a, b = fn(arg, m, a, b)
                    break
    r = (b * pow(1 - a, m - 2, m)) % m
    print(f"Card at #{pos}: {((pos - r) * pow(a, n * (m - 2), m) + r) % m}")
    

class LinearFnTests(unittest.TestCase):
    def test_cut_simple(self):
        # start: 0 1 2 3 4 5 6 7 8 9
        # cut 3: 3 4 5 6 7 8 9 0 1 2
        target = LinearFn(10)
        target.cut(3)

        self.assertEqual(5, target.apply(2))

    def test_deal(self):
        # start: 0 1 2 3 4 5 6 7 8 9
        # deal:  9 8 7 6 5 4 3 2 1 0
        target = LinearFn(10)
        target.deal()

        self.assertEqual(6, target.apply(3))

    def test_cut_deal(self):
        # start: 0 1 2 3 4 5 6 7 8 9
        # cut 3: 3 4 5 6 7 8 9 0 1 2
        # deal:  2 1 0 9 8 7 6 5 4 3
        target = LinearFn(10)
        target.cut(3)
        deck1 = [target.apply(i) for i in range(10)]

        target.deal()
        deck2 = [target.apply(i) for i in range(10)]

        self.assertEqual(0, target.apply(2))

    def test_increment(self):
        # start: 0 1 2 3 4 5 6 7 8 9
        # inc 3: 0 7 4 1 8 5 2 9 6 3
        target = LinearFn(10)
        target.increment(3)

        self.assertEqual(4, target.apply(2))