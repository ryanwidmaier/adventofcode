import re


def parse(text):
    rules_txt, _, inputs_txt = text.partition('\n\n')
    rules = {line.partition(': ')[0]: line.partition(': ')[2] for line in rules_txt.split('\n')}
    rules = {r: [vv.split() for vv in v.split(' | ')] for r, v in rules.items()}

    return rules, inputs_txt.split('\n')


def part1(rules, inputs):
    # Seed terminals
    lookup = {r: v[0][0][1] for r, v in rules.items() if v[0][0].startswith('"')}

    # Loop until 0 is converted
    while '0' not in lookup:
        for ridx, groups in rules.items():
            if ridx in lookup:
                continue

            translated = translate_rule(lookup, groups)
            if translated:
                lookup[ridx] = translated

    pattern = re.compile(f"^{lookup['0']}$")

    # re31 = re.compile(f"{lookup['31']}")
    # re42 = re.compile(f"{lookup['42']}")
    # for line in inputs:
    #     m = re31.search(line)
    #     if m:
    #         line2 = line.replace(m.group(0), ' <' + m.group(0) + '> ')
    #         print(f'31 -> {line2}')
    #     m = re42.search(line)
    #     if m:
    #         line2 = line.replace(m.group(0), ' <' + m.group(0) + '> ')
    #         print(f'42 -> {line2}')

    answer = len([li for li in inputs if pattern.match(li)])
    print(f"Part 1: {answer}")


def part2(rules, inputs):
    rules['8'] = [['42'], ['42', '8']]
    rules['11'] = [['42', '31'], ['42', '11', '31']]

    # Seed terminals
    lookup = {r: v[0][0][1] for r, v in rules.items() if v[0][0].startswith('"')}

    # Loop until 0 is converted
    while '0' not in lookup:
        if '42' in lookup and '8' not in lookup:
            lookup['8'] = f'({lookup["42"]}+)'

        if '31' in lookup and '42' in lookup and '11' not in lookup:
            c = f'{lookup["42"]}{{%d}}{lookup["31"]}{{%d}}'
            new11 = '(' + '|'.join(c % (n, n) for n in range(1, 5)) + ')'
            lookup['11'] = new11

        for ridx, groups in rules.items():
            if ridx in lookup:
                continue

            translated = translate_rule(lookup, groups)
            if translated:
                lookup[ridx] = translated

    print(len(lookup['0']))
    pattern = re.compile(f"^{lookup['0']}$")

    answer = len([li for li in inputs if pattern.match(li)])
    print(f"Part 2: {answer}")


def translate_rule(lookup, groups):
    for group in groups:
        for x in group:
            if x not in lookup:
                return None

    inner = '|'.join(''.join(lookup[x] for x in g) for g in groups)
    return f'({inner})'


with open('input.txt') as f:
    text_ = f.read()

rules_, inputs_ = parse(text_)
part1(rules_, inputs_)
part2(rules_, inputs_)
