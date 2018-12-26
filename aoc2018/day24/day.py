import re
from collections import defaultdict, namedtuple
import itertools
from itertools import count
from util import argmax, argmin, a_star, Coord

# 2080 units each with 5786 hit points (weak to fire; immune to slashing, bludgeoning) with an attack that does 20 fire damage at initiative 7
start_re = re.compile(r'(?P<cnt>\d+) units each with (?P<hp>\d+) hit points ')
weak_re = re.compile(r'weak to ([\w, ]+)')
immune_re = re.compile(r'immune to ([\w, ]+)')
attack_re = re.compile(r'with an attack that does (?P<dmg>\d+) (?P<dmg_type>\w+) damage at initiative (?P<init>\d+)')


class Group(object):
    next_id = {'immune': count(1), 'infection': count(1)}

    def __init__(self, side, units, hp, dmg, dmg_type, initiative):
        side = side.lower()
        id_ = next(self.next_id[side])
        self.id = ('N' if side == 'infection' else 'M') + str(id_)

        self.side = side
        self.units = units
        self.hp = hp
        self.dmg = dmg
        self.dmg_type = dmg_type.lower()
        self.initiative = initiative
        self.weak = set()
        self.immune = set()

    def __str__(self):
        weak = ','.join(self.weak)
        immune = ','.join(self.immune)
        return "Group(side={}, units={}, hp={}, weak={}, immune={}, dmg={} {}, init={}" \
               .format(self.side, self.units, self.hp, weak, immune, self.dmg, self.dmg_type, self.initiative)

    def add_weak(self, types):
        self.weak.update([t.lower() for t in types])

    def add_immune(self, types):
        self.immune.update([t.lower() for t in types])

    def effective_power(self):
        return self.units * self.dmg


def parse(fname):
    f = open(fname)
    side = 'immune'
    groups = []

    for line in f:
        line = line.rstrip()
        if line.startswith('Immune'):
            side = 'immune'
            continue
        elif line.startswith('Infection'):
            side = 'infection'
            continue

        m_start = start_re.search(line)
        m_attack = attack_re.search(line)
        if m_start and m_attack:
            g = Group(side, int(m_start.group('cnt')), int(m_start.group('hp')), int(m_attack.group('dmg')),
                      m_attack.group('dmg_type'), int(m_attack.group('init')))

            m = immune_re.search(line)
            if m:
                g.add_immune(m.group(1).split(', '))

            m = weak_re.search(line)
            if m:
                g.add_weak(m.group(1).split(', '))

            groups.append(g)

    return groups


def part1(groups):
    # Loop until one side wins
    round_num = count(1)

    # combat only ends once one army has lost all of its units.
    while len({g.side for g in groups}) > 1:
        rn = next(round_num)
        print "Round {}".format(rn)

        print " Targeting:"
        targeting = determine_targeting(groups, rn)

        print " Attacking:"
        do_attacking(groups, targeting)

        groups = [g for g in groups if g.units > 0]

    winner = groups[0].side
    print "Part1: {} - {}".format(winner, sum([g.units for g in groups]))


def determine_targeting(groups, round_num):
    # In decreasing order of effective power, groups choose their targets; in a tie, the group with the higher
    #   initiative chooses first.
    ordered = sorted(groups, key=lambda g_: (g_.side != 'infection', g_.effective_power(), g_.initiative), reverse=True)
    targeting = {}
    already_targeted = set()

    for g in ordered:
        damages = {}
        for enemy in groups:
            if g.side == enemy.side:
                continue

            # Defending groups can only be chosen as a target by one attacking group.
            if enemy.id in already_targeted:
                continue

            # The attacking group chooses to target the group in the enemy army to which it would deal the most
            #   damage (after accounting for weaknesses and immunities, but not accounting for whether the defending
            #   group has enough units to actually receive all of that damage).
            # If an attacking group is considering two defending groups to which it would deal equal damage,
            #   it chooses to target the defending group with the largest effective power; if there is still a tie,
            #   it chooses the defending group with the highest initiative.
            damages[enemy.id] = (compute_damage(g, enemy), enemy.effective_power(), enemy.initiative)

        if len(damages) == 0:
            print "  {} ({} units) has no one to target".format(g.id, g.units)
            continue

        # Figure out the prioritized target.  If we can't damage anything
        target = argmax(damages)

        # If it cannot deal any defending groups damage, it does not choose a target.
        if damages[target][0] == 0:
            print "  {} ({} units) has no targets it can damage".format(g.id, g.units)
            continue

        already_targeted.add(target)
        targeting[g.id] = target
        print "  {} ({} units) targeting {}".format(g.id, g.units, target)

    return targeting


def do_attacking(groups, targeting):
    # Groups attack in decreasing order of initiative, regardless of whether they are part of the infection or \
    #   the immune system.
    ordered = sorted(groups, key=lambda g_: g_.initiative, reverse=True)

    for g in ordered:
        if g.id not in targeting:
            continue

        target = targeting[g.id]
        if not target:
            continue

        # If a group contains no units, it cannot attack.
        if g.units <= 0:
            continue

        enemy = [gg for gg in groups if gg.id == target][0]
        dmg = compute_damage(g, enemy)

        # The defending group only loses whole units from damage; damage is always dealt in such a way that it kills
        #   the most units possible, and any remaining damage to a unit that does not immediately kill it is ignored.
        killed = min(dmg / enemy.hp, enemy.units)

        enemy.units -= killed
        print "  {} attacked {} for {} damage, killing {}".format(g.id, enemy.id, dmg, killed)
        if enemy.units <= 0:
            print "  {} died.".format(enemy.id)


def compute_damage(g, enemy):
    # if the defending group is weak to the attacking group's attack type, the defending group instead takes double
    #   damage.
    if g.dmg_type in enemy.weak:
        return g.effective_power() * 2

    # However, if the defending group is immune to the attacking group's attack type, the defending group instead
    #   takes no damage
    if g.dmg_type in enemy.immune:
        return 0

    # By default, an attacking group would deal damage equal to its effective power to the defending group
    return g.effective_power()


if __name__ == '__main__':
    groups_ = parse('input.txt')

    # part1(groups_)

    boost = 84
    for gg in groups_:
        if gg.side == 'immune':
            gg.dmg += boost

    part1(groups_)