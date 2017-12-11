
class State(object):
    def __init__(self):
        self.state = 'BLOCK'
        self.escaping = False
        self.groups_found = 0
        self.depth = 0
        self.score = 0
        self.garbage_size = 0

    def update(self, ch):
        if self.state == 'BLOCK':
            self.update_block(ch)
        elif self.state == 'GARBAGE':
            self.update_garbage(ch)

    def update_block(self, ch):
        if ch == '{':
            self.groups_found += 1
            self.depth += 1
            self.score += self.depth
        elif ch == '}':
            self.depth -= 1
        elif ch == '<':
            self.state = 'GARBAGE'
            self.escaping = False

    def update_garbage(self, ch):
        if self.escaping:
            self.escaping = False
        elif ch == '!':
            self.escaping = True
        elif ch == '>':
            self.state = 'BLOCK'
        else:
            self.garbage_size += 1


# Examples
# {}, score of 1.
# {{{}}}, score of 1 + 2 + 3 = 6.
# {{},{}}, score of 1 + 2 + 2 = 5.
# {{{},{},{{}}}}, score of 1 + 2 + 3 + 3 + 3 + 4 = 16.
# {<a>,<a>,<a>,<a>}, score of 1.
# {{<ab>},{<ab>},{<ab>},{<ab>}}, score of 1 + 2 + 2 + 2 + 2 = 9.
# {{<!!>},{<!!>},{<!!>},{<!!>}}, score of 1 + 2 + 2 + 2 + 2 = 9.
# {{<a!>},{<a!>},{<a!>},{<ab>}}, score of 1 + 2 = 3.

test_cases = [
    ('{}', 1),
    ('{{{}}}', 6),
    ('{{},{}}', 5),
    ('{{{},{},{{}}}}', 16),
    ('{<a>,<a>,<a>,<a>}', 1),
    ('{{<ab>},{<ab>},{<ab>},{<ab>}}', 9),
    ('{{<!!>},{<!!>},{<!!>},{<!!>}}', 9),
    ('{{<a!>},{<a!>},{<a!>},{<ab>}}', 3),
    (open('input.txt').read().rstrip(), 0)
]


for (stream, expected) in test_cases:
    state = State()
    for ch in stream:
        state.update(ch)

    print "{}, Expected={}, Actual={}, Garbage={}".format(stream[:20], expected, state.score, state.garbage_size)
