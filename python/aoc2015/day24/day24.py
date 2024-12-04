from pathlib import Path
import itertools
import functools


def part1(filename: str):
    print(f"----- {filename} ------")
    weights = Path(filename).read_text()
    weights = [int(w.strip()) for w in weights.split()]
    weights = sorted(weights, reverse=True)

    target = sum(weights) // 3
    found_len = None
    min_qe = None

    for count in range(1, len(weights)+1):
        if found_len and found_len < count:
            break

        for group1 in itertools.combinations(weights, count):
            if sum(group1) != target:
                continue

            remaining = [w for w in weights if w not in group1]
            result = balance_2_groups(target, remaining)
            if result:
                left, right = result[0], result[1]
                qe = functools.reduce(lambda a, b: a*b, group1)
                min_qe = qe if min_qe is None else min(qe, min_qe)
                # print(f"Group 1: {' '.join(str(s) for s in group1)}")
                # print(f"Group 2: {' '.join(str(s) for s in left)}")
                # print(f"Group 3: {' '.join(str(s) for s in right)}")
                # print(f"QE = {qe}")
                # print()
                found_len = len(group1)

    print(f'Part 1: {min_qe}')


def balance_2_groups(target: int, weights: list[int]) -> list[list[int]] | None:

    for count in range(1, len(weights)+1):
        for group2 in itertools.combinations(weights, count):
            if sum(group2) != target:
                continue

            group3 = [w for w in weights if w not in group2]
            if sum(group3) != target:
                continue

            return [group2, group3]

    return None


def part2(filename: str):
    print(f"----- {filename} ------")
    weights = Path(filename).read_text()
    weights = [int(w.strip()) for w in weights.split()]
    weights = sorted(weights, reverse=True)

    target = sum(weights) // 4
    found_len = None
    min_qe = None

    for count in range(1, len(weights)+1):
        if found_len and found_len < count:
            break

        for group1 in itertools.combinations(weights, count):
            if sum(group1) != target:
                continue

            remaining = [w for w in weights if w not in group1]
            result = balance_3_groups(target, remaining)
            if result:
                left, right = result[0], result[1]
                qe = functools.reduce(lambda a, b: a*b, group1)
                min_qe = qe if min_qe is None else min(qe, min_qe)
                # print(f"Group 1: {' '.join(str(s) for s in group1)}")
                # print(f"Group 2: {' '.join(str(s) for s in left)}")
                # print(f"Group 3: {' '.join(str(s) for s in right)}")
                # print(f"QE = {qe}")
                # print()
                found_len = len(group1)

    print(f'Part 1: {min_qe}')

def balance_3_groups(target: int, weights: list[int]) -> list[list[int]] | None:
    for count in range(1, len(weights)+1):
        for group4 in itertools.combinations(weights, count):
            if sum(group4) != target:
                continue

            remaining = [w for w in weights if w not in group4]
            result = balance_2_groups(target, remaining)
            if result:
                return [result[0], result[1], group4]

    return None


part1('sample.txt')
part1('input.txt')
part2('input.txt')
