import re

lines = open('input.txt').readlines()

# lines = [
#     r'""',
#     r'"abc"',
#     r'"aaa\"aaa"',
#     r'"\x27"',
# ]
lines = [r'"ebvptcjqjhc\"n\"p\"dxrphegr\\\\"']

# Part 1
code_len = 0
mem_lem = 0
for line in lines:
    before = line.rstrip()
    line = line.rstrip()[1:-1]
    code_len += len(line) + 2
    line_code_len = len(line)

    cnt = 0
    line = line.replace(r'\\', ' ')
    line = line.replace(r'\"', ' ')
    line = re.sub(r'\\x\d\d', ' ', line)

    mem_lem += len(line)
    line_mem_len = len(line) - 2
    print(f"{before} -> {line_code_len} - {line_mem_len} = {line_code_len-line_mem_len}")

print(f"Part 1: {code_len} - {mem_lem} = {code_len-mem_lem}")

