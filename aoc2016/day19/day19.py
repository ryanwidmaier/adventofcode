from collections import deque
from util import Timer

num_elves = 3004953
elves = []


# Init
for i in xrange(1, num_elves+1):
    elves.append(i)


timer = Timer()
i = 0
while len(elves) > 1:
    if timer.elapsed_secs() > 5:
        timer.reset()
        print "Elves left: {}".format(len(elves))

    keep = elves[i]

    # Steal from
    steal_from = (i + len(elves) / 2) % len(elves)
    del elves[steal_from]

    # Only increment if we removed one after the current elf
    if i < steal_from:
        i = (i + 1) % len(elves)
    else:
        i = i % len(elves)




print elves[0]
