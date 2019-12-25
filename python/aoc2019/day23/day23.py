from aoc2019.int_code import IntComputerFinal


program = IntComputerFinal.load_memory('input.txt')

hosts = [IntComputerFinal() for _ in range(50)]
for idx, h in enumerate(hosts):
    h.program(program)
    h.add_input(idx)

progs = [h.run() for h in hosts]
sending = [False] * len(hosts)

dest, x, y = None, None, None
idx = 0
last_nat = None
last_sent = 0

while True:  # not (dest == 255 and last_nat and y == last_nat[1]):
    # Update last nat
    if dest == 255:
        last_nat = (x, y)

    # If all hosts idle, send nat message to 0
    if all(len(h.input) == 0 for h in hosts) and last_sent >= 100:
        hosts[0].add_input(last_nat[0], last_nat[1])
        last_sent = 0

    host = hosts[idx]
    prog = progs[idx]

    # No input, or only host ID input
    if len(host.input) <= 1:
        host.add_input(-1)

    # Run to next output instructions
    dest = next(prog)
    if dest is not None:
        x = next(prog)
        y = next(prog)

        if dest != 255:
            hosts[dest].add_input(x, y)
            last_sent = 0
    else:
        last_sent += 1

    if dest == 255:
        print(f" Send to 255, {x}, {y}")
        here = 0
        here += 1

    # Mark host as sending (or not) a message
    sending[idx] = dest is not None

    # Move to next host
    idx = (idx + 1) % len(hosts)

print(dest, x, y)

# ! 255 31063 11509