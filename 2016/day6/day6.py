import re
from collections import namedtuple
from itertools import chain


IPGroup = namedtuple('IPGroup', 'supernet hypernet')


def parse(ip):
    # Use an RE to find the hypernet strings
    hypernet_re = re.compile(r'\[.*?\]')
    hypernets = hypernet_re.findall(ip)

    # Strip out the hypernet strings to get the outer parts
    outer = ip
    for hyp in hypernets:
        outer = outer.replace(hyp, ' ')

    # Finally, remove the square brackets from the hypernets
    hypernets = [h[1:-1] for h in hypernets]
    return IPGroup(outer.split(' '), hypernets)


def has_abba(snippet):
    for i in xrange(len(snippet)-3):
        abba = snippet[i:i+4]
        if abba == abba[::-1] and abba[0] != abba[1]:
            return True

    return False


def get_aba(snippet):
    abas = []
    for i in xrange(len(snippet)-2):
        aba = snippet[i:i+3]
        if aba[0] == aba[2]:
            abas.append(aba)

    return abas




count = 0

infile = open('input.txt')
for line in infile:
    line = line.rstrip()
    ip = parse(line)

    abas = set(chain(*[[ss[0:2] for ss in get_aba(s)] for s in ip.supernet]))
    babs = set(chain(*[[ss[1::-1] for ss in get_aba(s)] for s in ip.hypernet]))

    if abas.intersection(babs):
        count += 1

print count