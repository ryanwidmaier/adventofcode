from util import RateLogger
import logging
import string
from util import argmin

logging.basicConfig(level=logging.INFO)


protein = open('out.txt').read()

print "Protein is {} chars long".format(len(protein))


def react(protein):
    i = 0
    while i + 1 < len(protein):
        # Look for the next pair
        left, right = protein[i], protein[i+1]

        # Found a pair
        if left != right and left.upper() == right.upper():
            protein = protein[:i] + protein[i+2:]
            if i > 0:
                i -= 1
        else:
            i += 1

    return protein


reacted = react(protein)
print "Part-1 Final Length: {}".format(len(reacted))

lengths = {}

for letter in string.ascii_lowercase:
    stripped_protein = protein.replace(letter, '').replace(letter.upper(), '')
    lengths[letter] = len(react(stripped_protein))


print "part-2 length: {}, {}".format(argmin(lengths), min(lengths.values()))
