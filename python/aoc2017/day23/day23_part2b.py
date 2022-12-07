import numpy as np


start = 108400
end = start + 18000

# Seive of eratosthenes
sieve = np.ones((end))

for i in xrange(2, end):
    if sieve[i] == 1:
        print "Prime ", i
        for x in xrange(i*2, end, i):
            sieve[x] = 0

# 108400 ... 125,400 125,401


target = sieve[start:start+17001:17]

prime_count = np.count_nonzero(target)
total = target.shape[0]
composite_count = total - prime_count

print "Total: ", total
print "Prime: ", prime_count
print "Composite: ", composite_count


