
def build(step_size):

    target = 1
    pos = 0
    spinlock_size = 1

    # for i in xrange(50000000, 1, -1):
    for i in xrange(1, 50000001):
        insert_pos = (pos + step_size) % spinlock_size
        spinlock_size += 1
        pos = insert_pos + 1

        if pos == 1:
            target = i

        if i % 500000 == 0:
            print "{} iterations".format(i)

    print "Target: ", target


build(386)


