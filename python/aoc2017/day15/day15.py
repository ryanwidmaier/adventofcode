

gen1, gen2 = 512, 191
factor1, factor2 = 16807, 48271
count = 0

for i in xrange(5000000):
    gen1 = (gen1 * factor1) % 0x7FFFFFFF
    gen2 = (gen2 * factor2) % 0x7FFFFFFF

    while gen1 % 4 != 0:
        gen1 = (gen1 * factor1) % 0x7FFFFFFF

    while gen2 % 8 != 0:
        gen2 = (gen2 * factor2) % 0x7FFFFFFF

    cmp1 = (gen1 & 0xFFFF)
    cmp2 = (gen2 & 0xFFFF)
    if cmp1 == cmp2:
        count += 1

    if i % 50000 == 0:
        print "{} steps, Count {}".format(i, count)


print "Matches: ", count