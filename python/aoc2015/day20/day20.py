
import math
from pathlib import Path
from util import read_input
from util import RateLogger


def sum_divisors(n):
    tally = 0
    for i in range(1, n+1):
        frac = n / i - math.floor(n/i)
        sign = 0 if frac == 0 else int(frac / math.fabs(frac))
        tally += i * ((sign + 1) % 2)

    return tally * 10


def divisors(n):
    small = [i for i in range(1, int(math.sqrt(n)) + 1) if n % i == 0]
    large = [n / d for d in small if n != d * d]
    return small + large


def run(inp):
    part1_answer, part2_answer = None, None
    rate_logger = RateLogger(log_every_n=100000)
    for n in range(1, inp):
        rate_logger.inc()

        divs = divisors(n)
        if not part1_answer:
            if sum(divs) * 10 >= inp:
                part1_answer = n

        if not part2_answer:
            if sum(d for d in divs if n / d <= 50) * 11 >= inp:
                part2_answer = n

        if part1_answer and part2_answer:
            return part1_answer, part2_answer



# input_ = 8
input_ = 29000000

p1, p2 = run(input_)
print(f'{p1}')
print(f'{p2}')
