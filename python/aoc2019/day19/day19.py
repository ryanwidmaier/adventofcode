from aoc2019.int_code import IntComputerFinal


def part1(comp):

    cnt = 0
    for y in range(50):
        for x in range(50):

            comp.restart()
            comp.add_input(x, y)
            prog = comp.run()
            output = next(prog)

            print('#' if output == 1 else '.', end='')
            cnt += output

        print()
    print(cnt)


def part2(comp):
    rights = {}
    left = None

    for y in range(800, 10000):
        rights[y] = 0
        output = 0
        x = left or 0
        left = None
        skipped = False

        # Loop until we've seen one 1, and we've reached a 0
        one_seen = False
        while not one_seen or output == 1:

            comp.restart()
            comp.add_input(x, y)
            prog = comp.run()
            output = next(prog)

            if output == 1:
                one_seen = True
                if left is None:
                    left = x
                rights[y] = x

            # skip over the width of the previous row - 1, width change is always one of -1,0,1
            if not skipped and one_seen and rights.get(y-1, 0) > 2:
                x = rights[y-1]
                skipped = True
            else:
                x += 1

        print(f"{y}, width={rights[y] - left + 1}, @ y={y-99} need right={left + 99}, actual={rights.get(y - 99)}")
        if y - 99 in rights and left + 99 <= rights[y-99]:
            ans_x = left
            ans_y = y - 99
            answer = (ans_x * 10000) + ans_y
            print(f"({ans_x}, {ans_y}) -> {answer}")
            break


    # print(cnt)

comp_ = IntComputerFinal()
comp_.program(comp_.load_memory('input.txt'))

# part1(comp_)
part2(comp_)