import unittest
from day import run
from util import Coord


class Day15Tests(unittest.TestCase):
    @staticmethod
    def read_expected(fname):
        a = []
        with open(fname) as f:
            for line in f:
                a.append(line.rstrip())

            return a

    def test_f0(self):
        grid, answer = run('example0.txt')
        expected = self.read_expected('expected0.txt')

        self.assertEqual(27730, answer)
        # self.assertListEqual(expected, grid)

    def test_f1(self):
        grid, answer = run('example1.txt')
        expected = self.read_expected('expected1.txt')

        self.assertListEqual(expected, grid)
        self.assertEqual(36334, answer)

    def test_f2(self):
        grid, answer = run('example2.txt')
        expected = self.read_expected('expected2.txt')

        self.assertListEqual(expected, grid)
        self.assertEqual(39514, answer)

    def test_f3(self):
        grid, answer = run('example3.txt')
        expected = self.read_expected('expected3.txt')

        self.assertListEqual(expected, grid)
        self.assertEqual(27755, answer)

    def test_f4(self):
        grid, answer = run('example4.txt')
        expected = self.read_expected('expected4.txt')

        self.assertListEqual(expected, grid)
        self.assertEqual(28944, answer)

    def test_f5(self):
        grid, answer = run('example5.txt')
        expected = self.read_expected('expected5.txt')

        self.assertListEqual(expected, grid)
        self.assertEqual(18740, answer)

    def test_input(self):
        grid, answer = run('input.txt')
        self.assertEqual(False, True)

    def test_groupby(self):
        t = [[Coord(7, 2), Coord(6, 2), Coord(5, 2)],
             [Coord(7, 2), Coord(6, 2), Coord(6, 3)],
             [Coord(7, 2), Coord(6, 2), Coord(6, 1)],
             [Coord(7, 2), Coord(7, 3), Coord(6, 3)],
             [Coord(7, 2), Coord(7, 3), Coord(7, 4)],
             [Coord(7, 2), Coord(7, 1), Coord(6, 1)]]

        from itertools import groupby
        from collections import defaultdict

        d = defaultdict(lambda: [])
        for target, candidates in groupby(t, key=lambda p: p[-1]):
            d[target].append(list(candidates))

        q = 0