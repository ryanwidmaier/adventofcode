from typing import Optional, Iterable
from util import RateLogger, Timer
import time


class Node:
    def __init__(self, prev=None, next_=None, value: int = None):
        self.next = next_ or self
        self.prev = prev or self
        self.value = value

    def insert_after(self, val: int) -> 'Node':
        new_node = Node(prev=self, next_=self.next, value=val)
        self.next.prev = new_node
        self.next = new_node
        return new_node

    def insert_after_seq(self, vals: Iterable[int]):
        current = self
        for v in vals:
            current = current.insert_after(v)

    def snip(self, length: int) -> 'Node':
        start = self.next
        last = self.next
        for _ in range(length-1):
            last = last.next

        # Remove from this list
        last.next.prev = self
        self.next = last.next

        # Make removed consistent
        start.prev = last
        last.next = start
        return start

    def reinsert(self, node: 'Node'):
        after = self.next

        self.next = node
        after.prev = node.prev
        after.prev.next = after
        node.prev = self

    def remove(self) -> 'Node':
        self.prev.next = self.next
        self.next.prev = self.prev
        return self

    def rfind(self, val: int) -> Optional['Node']:
        """ Search list backwards for a value, returning the node. """
        current = self.prev
        while val != current.value:
            if current == self:
                return None
            current = current.prev

        return current

    def __iter__(self):
        current = self
        yield self

        current = current.next
        while current != self:
            yield current
            current = current.next

    def values(self):
        """ Iterate over all values, starting from this node """
        for n in self:
            yield n.value


def play(cups, max_val, rounds) -> Node:
    nodes = {n.value: n for n in cups}
    for i in range(rounds):
        # print()
        # print(f'-- move {i+1} --')
        # print(f'cups: (' + ' '.join(str(x) for x in cups.values()))

        # The crab picks up the three cups that are immediately clockwise of the current cup. They are removed from
        # the circle; cup spacing is adjusted as necessary to maintain the circle
        removed = cups.snip(3)

        # print(f'pick up: ' + ', '.join(str(x) for x in removed.values()))

        # The crab selects a destination cup: the cup with a label equal to the current cup's label minus
        # one. If this would select one of the cups that was just picked up, the crab will keep subtracting
        # one until it finds a cup that wasn't just picked up. If at any point in this process the value goes
        # below the lowest value on any cup's label, it wraps around to the highest value on any cup's label instead
        target = (((cups.value - 1) - 1) % max_val) + 1
        while target in removed.values():
            target = (((target - 1) - 1) % max_val) + 1

        # print(f'destination: {target}')

        # The crab places the cups it just picked up so that they are immediately clockwise of the destination
        # cup. They keep the same order as when they were picked up.
        dest = nodes[target]
        dest.reinsert(removed)

        # The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
        cups = cups.next

        # rate_logger.inc()

    # print()
    # print('-- final --')
    # print(f'cups: (' + ' '.join(str(x) for x in cups.values()))

    return cups


def part1(data):
    cups = Node(value=data[0])
    cups.insert_after_seq(data[1:])
    max_val = max(data)

    cups = play(cups, max_val, 10)

    # Rotate 1 to the front, then remove it
    one = cups.rfind(1)
    answer = list(one.values())[1:]
    print(f'Part 1:', ''.join(str(x) for x in answer))


def part2(data):
    max_val = 1000000
    cups = Node(value=data[0])
    cups.insert_after_seq(data[1:])
    cups.prev.insert_after_seq(range(max(data) + 1, max_val+1))

    cups = play(cups, max_val, 10000000)

    # Part 2 - answer
    one = cups.rfind(1)
    # print_n(one.prev.prev.prev.prev.prev.prev.prev, 20)
    # print_n(cups.rfind(934001), 10)
    # print_n(cups.rfind(159792), 10)

    plus1 = one.next.value
    plus2 = one.next.next.value
    print(f'Part 2: {plus1} x {plus2} = {plus1*plus2}')


def print_n(node: Node, max_num):
    for idx, n in enumerate(node):
        if idx == max_num:
            print()
            return

        print(n.value, end=' ')


if __name__ == '__main__':
    input_ = '653427918'
    sample = '389125467'

    data = [int(x) for x in input_]
    # part1(data)

    timer = Timer()
    part2(data)
    print(f"Took {timer.elapsed_secs()}s")

