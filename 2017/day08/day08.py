import re
from pprint import pprint
from collections import defaultdict
import string

line_re = re.compile(
    r'(?P<register>\w+) '
    r'(?P<op>\w+) '
    r'(?P<amount>-?\d+) '
    r'if '
    r'(?P<left>\w+) '
    r'(?P<condition>[=<>]+) '
    r'(?P<right>\w+)'
)


def is_register(name):
    left.isalpha()


def test_condition(registers, left, condition, right):
    left = registers[left] if left[0] in string.ascii_letters else int(left)
    right = registers[right] if right[0] in string.ascii_letters else int(right)

    if condition == '==':
        return left == right
    elif condition == '>':
        return left > right
    elif condition == '<':
        return left < right
    elif condition == '>=':
        return left >= right
    elif condition == '<=':
        return left <= right
    elif condition == '!=':
        return left != right

    raise ValueError("Unknown condition: {}".format(condition))


registers = defaultdict(lambda: 0)

fin = open('input.txt')
running_max = 0

for line in fin:
    line = line.rstrip()
    register, op, amount, _, left, condition, right = line.split()
    if test_condition(registers, left, condition, right):
        if op == 'inc':
            registers[register] += int(amount)
        elif op == 'dec':
            registers[register] -= int(amount)

        running_max = max(running_max, max(registers.itervalues()))

pprint(dict(registers))
print "Max: ", max(registers.iteritems(), key=lambda a: a[1])
print "Running Max: ", running_max