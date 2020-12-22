from typing import NamedTuple


class Key(NamedTuple):
    ingredient: str
    allergen: str


def part1(lines):
    all_ingredients = set()
    all_allergens = set()

    # Parse all the lines first just to figure out all values
    data_lines = []
    for line in lines:
        ingredients, allergens = line.split(' (contains ')
        ingredients = ingredients.split()
        allergens = allergens.strip(')\n').split(', ')

        all_ingredients.update(ingredients)
        all_allergens.update(allergens)
        data_lines.append((set(ingredients), set(allergens)))

    possibles = {a: all_ingredients for a in all_allergens}

    # Givens:
    #   I1 I2 I3 (A1, A2)
    #   AX implies IX
    #   IX does not imply AX

    # Part 1
    # Update the grid, clearing combinations that aren't possible
    changed = True
    while changed:
        changed = False
        for ingredients, allergens in data_lines:
            # Allergen has to be one in the ingredient list
            for alg in allergens:
                changed |= not ingredients.issuperset(possibles[alg])
                possibles[alg] = possibles[alg].intersection(ingredients)

        # Check for solved and remove from others
        solved = {x for a, ins in possibles.items() if len(ins) == 1
                  for x in ins}
        for alg, ings in possibles.items():
            if len(ings) > 1:
                for x in solved:
                    changed |= x in ings
                    ings.discard(x)

    has_allergens = {x for v in possibles.values() for x in v}
    count = 0
    for ings, _ in data_lines:
        count += len(set(ings).difference(has_allergens))

    print(f"Part 1: {count}")

    ordered = sorted(possibles.items(), key=lambda e: e[0])
    answer = ','.join(list(e[1])[0] for e in ordered)

    print(f"Part 2: {answer}")


if __name__ == '__main__':
    with open('input.txt') as f:
        part1(f.readlines())
