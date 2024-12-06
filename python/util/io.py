from pathlib import Path


def read_input(p: Path, tx=None):
    def noop(x):
        return x

    lines = []
    tx = tx or noop
    with p.open() as f:
        for line in f:
            line = line.strip()
            lines.append(tx(line))

    return lines
