import re

deal_re = re.compile(r'deal into new stack')
inc_re = re.compile(r'deal with increment (\d+)')
cut_re = re.compile(r'cut (-?\d+)')


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


D = 119315717514047  # deck size


def reverse_deal(i):
    return D - 1 - i


def reverse_cut(i, N):
    return (i + N + D) % D


def reverse_increment(i, N):
    return modinv(N, D) * i % D  # modinv is modular inverse


# Loop through the lines in reverse, building a combined linear function
with open('input.txt') as f:
    lines = f.readlines()


def f(i):
    for line in lines[::-1]:
        m = deal_re.match(line)
        if m:
            i = reverse_deal(i)

        m = cut_re.match(line)
        if m:
            i = reverse_cut(i, int(m.group(1)))

        m = inc_re.match(line)
        if m:
            increment = int(m.group(1))
            i = reverse_increment(i, increment)

    return i


X = 2020
Y = f(X)
Z = f(Y)
A = (Y-Z) * modinv(X-Y+D, D) % D
B = (Y-A*X) % D
print(A, B)

n = 101741582076661
print((pow(A, n, D)*X + (pow(A, n, D)-1) * modinv(A-1, D) * B) % D)