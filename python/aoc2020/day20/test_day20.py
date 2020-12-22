import unittest
from aoc2020.day20.day20 import Tile


class Tests(unittest.TestCase):
    def test_dirs(self):
        target = Tile.build(
            "Tile 1:\n"
            ".#.#.#.#.#\n"
            "##.......#\n"
            "#.#.......\n"
            "...#......\n"
            "....#....#\n"
            ".....#...#\n"
            "......#...\n"
            ".......#.#\n"
            "#.#.....##\n"
            "#..####...\n"
        )

        self.assertEqual('.#.#.#.#.#', target.north())
        self.assertEqual('##..##.##.', target.east())
        self.assertEqual('#..####...', target.south())
        self.assertEqual('.##.....##', target.west())

    def test_rotate(self):
        target = Tile.build(
            "Tile 1:\n"
            ".#........\n"
            ".#........\n"
            "..#.......\n"
            "...#......\n"
            "....#.....\n"
            ".....#....\n"
            "......#...\n"
            ".......#..\n"
            "..#.....#.\n"
            ".........#\n"
        )

        target.rotate()

        actual = '\n'.join(''.join(row) for row in target.grid)
        expected = (
            "..........\n"
            "........##\n"
            ".#.....#..\n"
            "......#...\n"
            ".....#....\n"
            "....#.....\n"
            "...#......\n"
            "..#.......\n"
            ".#........\n"
            "#........."
        )
        self.assertEqual(expected, actual)

    def test_flip(self):
        target = Tile.build(
            "Tile 1:\n"
            ".#........\n"
            ".#........\n"
            "..#.......\n"
            "...#......\n"
            "....#.....\n"
            ".....#....\n"
            "......#...\n"
            ".......#..\n"
            "..#.....#.\n"
            ".........#\n"
        )

        target.flip()

        actual = '\n'.join(''.join(row) for row in target.grid)
        expected = (
            ".........#\n"
            "..#.....#.\n"
            ".......#..\n"
            "......#...\n"
            ".....#....\n"
            "....#.....\n"
            "...#......\n"
            "..#.......\n"
            ".#........\n"
            ".#........"
        )
        self.assertEqual(expected, actual)
