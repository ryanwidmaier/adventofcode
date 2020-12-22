import hashlib


data = 'iwrupvqb'

for i in range(1, 999999999999):
    hash = hashlib.md5(f'{data}{i}'.encode()).hexdigest()
    if hash.startswith('000000'):
        print(f"Part 1: {i} -> {hash}")
        break

