from aoc2020.day23.day23 import Node
from unittest import TestCase


class Tests(TestCase):
    def test_insert(self):
        target = Node(value=1)
        target.insert_after_seq(range(1, 5))


    def test_snip(self):
        target = Node(value=1)
        target.insert_after_seq(range(1, 5))
        pass

    def test_reinsert(self):
        pass

    def test_rfind(self):
        pass
