from aoc2019.int_code import IntComputerFinal
from util import Coord, GridWalker, print_dict_grid
from itertools import combinations, chain
import re

try_re = re.compile(r'try (\w) \[(.+)\]')

# xxx xxxx xxxxx xx x

"""
    too light - [sand]    - required
    too light - [boulder]
    too light - [ice cream]  - required
    too light - [mutex]
    too light - [festive hat]
    
    too heavy - [mug]
    too heavy - [prime number] 
    too heavy - [weather machine]
"""

# - astronaut ice cream
# - festive hat
# - mug
# - sand
# - mutex
# - prime number
# - weather machine
# - boulder
aliases = {'n': 'north', 'w': 'west', 'e': 'east', 's': 'south', 'i': 'inv'}


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in rangee(len(s)+1))


def output_room(prog, print_output=True):
    output = ''
    ch = ''
    try:
        while ch is not None:
            ch = next(prog)
            if ch is not None:
                output += chr(ch)
    except StopIteration:
        print(output)

    if print_output:
        print(output, end='')

    return output


def run_commands(comp, prog, commands, print_output=True):
    output = None
    for cmd in commands:
        # apply command
        command = aliases.get(cmd, cmd)
        for ch in command:
            comp.add_input(ord(ch))

        comp.add_input(10)

        # Output room
        output = output_room(prog, print_output=print_output)

    return output



def main():
    macro_commands = [
        'n', 'take festive hat',
        'w', 'take sand',
        'e', 'e', 'take prime number',
        'w', 's',
        # Start,
        'e', 'n', 'take weather machine',
        'n', 'take mug',
        's', 's',
        'e', 'n', 'e', 'e', 'take astronaut ice cream',
        'w', 'w', 's', 'w', 'w',
        # Start
        's', 's', 'take mutex',
        's', 'take boulder',
        'e', 's',
        # Pressure-sensitive room, e
        # sand, astronaut ice cream, boulder, mutex
        'drop mug', 'drop prime number', 'drop festive hat', 'drop weather machine'
    ]

    comp = IntComputerFinal()
    comp.program(comp.load_memory('input.txt'))
    prog = comp.run()

    # Output the initial room
    output_room(prog)

    while True:
        # Apply any macro'ed commands
        if macro_commands:
            run_commands(comp, prog, macro_commands)
            macro_commands = []

        # Get input
        command = input("> ")
        command = aliases.get(command, command)

        # Try various combinations until something works
        m = try_re.match(command)
        if m:
            all_items = m.group(2).split(', ')
            for comb in powerset(all_items):
                print(f"Trying: {', '.join(comb)}")
                commands = [f'drop {i}' for i in all_items]
                commands += [f'take {i}' for i in comb]
                commands += [m.group(1)]

                output = run_commands(comp, prog, commands, print_output=False)
                print(output)

                if 'ejected' not in output:
                    print(f"Success with: {', '.join(comb)}")
                    break

        else:
            macro_commands.append(command)


main()