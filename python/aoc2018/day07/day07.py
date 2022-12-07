import re
from collections import defaultdict
from Queue import PriorityQueue


parse_re = re.compile(r'Step (\w+) must be finished before step (\w+) can begin.')

FILE = 'input.txt'
DELAY = 60
WORKERS = 5


def parse_dag():
    requires = defaultdict(lambda: set())

    # Build the dag
    f = open(FILE)
    for line in f:
        line = line.rstrip()

        match = parse_re.search(line)
        if match:
            before, after = match.groups()
            requires[after].add(before)
            _ = requires[before]

    return requires


def find_starts(requires, q):
    # Find starting points (ones with no predecessor)
    start = [n for n, nn in requires.iteritems() if len(nn) == 0]
    for n in start:
        q.put(n)
        del requires[n]


def add_satisfied(requires, q, processed):
    # Add nodes whose requirements have been met
    for k, v in requires.copy().iteritems():
        if all([vv in processed for vv in v]):
            print "  {} available".format(k)

            q.put(k)
            del requires[k]

    return requires


def required_time(stage):
    return DELAY + ord(stage) - ord('A') + 1


def update_workers(workers, tick, ordered):
    for w, v in workers.iteritems():
        if not v:
            continue

        stage, finished = v
        if finished <= tick:
            print "Tick {}: Worker {} finished {}".format(tick, w, stage)
            ordered.append(stage)
            workers[w] = None

    return [w for w, v in workers.iteritems() if v is None]


q_ = PriorityQueue()
ordered = []
workers = {w: None for w in xrange(WORKERS)}

# Do
requires_ = parse_dag()
find_starts(requires_, q_)

# Now walk the DAG

tick = -1
while not q_.empty() or any([v is not None for v in workers.values()]):
    tick += 1
    available = update_workers(workers, tick, ordered)
    add_satisfied(requires_, q_, ordered)

    # Get next node to process
    while len(available) and not q_.empty():
        n = q_.get()

        w = available.pop()
        workers[w] = (n, tick + required_time(n))
        print "Tick {}: Worker {} starting on {}".format(tick, w, n)


print ordered
print tick
