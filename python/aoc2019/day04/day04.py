
puzzle_input = (171309, 643603)


def test(x_str):
    last = None
    cnt = 1
    good = False

    for i in range(6):
        if x_str[i] == last:
            cnt += 1
        else:
            if cnt == 2:
                good = True
                break
            cnt = 1
        last = x_str[i]

    if not good and cnt != 2:
        return False

    # Two adjacent digits are the same (like 22 in 122345)
    # if not any(x_str[i] == x_str[i + 1] for i in range(5)):
    #     return False

    # Going from left to right, the digits never decrease; they only ever increase or stay the
    # same (like 111123 or 135679).
    if not all(x_str[i] <= x_str[i + 1] for i in range(0, 5)):
        return False

    return True


print(test('112233'))
print(test('123444'))
print(test('111122'))


match = []
for x in range(puzzle_input[0]+1, puzzle_input[1]):
    x_str = str(x)
    if test(str(x)):
        match.append(x)

print(len(match))

