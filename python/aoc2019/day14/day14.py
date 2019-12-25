from collections import namedtuple, defaultdict
import math

Resource = namedtuple('Resource', 'name amount')
Formula = namedtuple('Formula', 'requires creates')


def parse(fname):
    reactions = {}
    with open(fname) as f:
        for line in f:
            line = line.strip()
            inp, out = line.split(' => ')

            a, r = out.split(' ')
            out_res = Resource(r, int(a))

            requires = []
            for x in inp.split(', '):
                a, r = x.split(' ')
                requires.append(Resource(r, int(a)))

            reactions[out_res.name] = Formula(requires, out_res)

    return reactions


def part1(reactions):
    have = defaultdict(lambda: 0)
    made = defaultdict(lambda: 0)

    create(reactions, 'FUEL', 1, have, made)

    print(f'ORE: {made["ORE"]}')


def create(reactions, resource, amount, have, total_made):
    # print(f"Need: {resource} {amount}")
    if resource == 'ORE':
        total_made['ORE'] += amount
        return amount

    # Figure out the formula and how many times to apply it
    formula = reactions[resource]
    times = math.ceil(amount / formula.creates.amount)

    for req in formula.requires:
        # First use from existing pool
        used = min(req.amount * times, have[req.name])
        need = req.amount * times - used
        have[req.name] -= used

        # print(f"  Requires: {req.name} {need}, used={used}, {have}")

        # If not enough, Create resource and apply to formula
        if need > 0:
            made = create(reactions, req.name, need, have, total_made)

            # Remainder just gets stored in case someone else needs it
            # print(f"  Made: {req.name} {made}, and used {need}")
            made -= need
            have[req.name] += made

    total_made[resource] += formula.creates.amount * times
    return formula.creates.amount * times


def part2(reactions):
    # 1 FUEL -> 1920219 ORE
    made = defaultdict(lambda: 0)
    have = defaultdict(lambda: 0)

    fuel = 1330066
    create(reactions, 'FUEL', fuel, have, made)
    print(f"{made['ORE']:,} ORE makes {made['FUEL']:,}")

    # 1330067
    # i = 1
    # while made['ORE'] < 1000000000000:
    #     have = defaultdict(lambda: 0)
    #     made = defaultdict(lambda: 0)
    #
    #     create(reactions, 'FUEL', i, have, made)
    #     print(f"{i}: {made['ORE']} ORE makes {made['FUEL']}")
    #     i += 1

    # print(f'Target: 1000000000000')
    # print(f'ORE:    {made["ORE"]:>13}')
    # print(f'Diff:   {1000000000000-made["ORE"]:>13}')


reactions = parse('input.txt')
# part1(reactions)
part2(reactions)
