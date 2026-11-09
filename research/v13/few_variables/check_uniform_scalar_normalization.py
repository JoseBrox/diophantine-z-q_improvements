#!/usr/bin/env python3
"""Exact certificate for the uniform real scalar normalization.

Standard library only.  The finite checks verify the concrete constants;
the all-input valuation and real assertions are proved in the companion TeX.
"""
from fractions import Fraction
from math import isqrt, lcm
from pathlib import Path
import json


def multiply(a, b):
    c = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        for j, v in enumerate(b):
            c[i + j] += u * v
    return c


def evaluate(a, x, modulus=None):
    result = 0
    for c in reversed(a):
        if modulus:
            c = c.numerator * pow(c.denominator, -1, modulus)
            result = (result * x + c) % modulus
        else:
            result = result * x + c
    return result


def ceil_fraction(x):
    return -((-x.numerator) // x.denominator)


def valuation(n, p):
    assert n
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def prime(p):
    return p > 1 and all(p % d for d in range(2, isqrt(p) + 1))


def determinant_bareiss(matrix):
    a = [row[:] for row in matrix]
    n = len(a)
    previous, sign = 1, 1
    for k in range(n - 1):
        pivot_row = next(i for i in range(k, n) if a[i][k])
        if pivot_row != k:
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = pivot * a[i][j] - a[i][k] * a[k][j]
                assert numerator % previous == 0
                a[i][j] = numerator // previous
            a[i][k] = 0
        previous = pivot
    return sign * a[-1][-1]


def resultant(f, g):
    m, n = len(f) - 1, len(g) - 1
    fh, gh = list(reversed(f)), list(reversed(g))
    matrix = []
    for i in range(n):
        matrix.append([0] * i + fh + [0] * (n - 1 - i))
    for i in range(m):
        matrix.append([0] * i + gh + [0] * (m - 1 - i))
    return determinant_bareiss(matrix)


ell, q = 76249, 1021
assert prime(ell) and prime(q)
beta = list(map(Fraction, [450459, 0, 0, 0, 216]))
factors, rho = [], [Fraction(1)]
for scale, shift in [(1, 0), (1, -1), (1, -2401), (32, 343), (2, -1)]:
    factor = [scale * c for c in beta]
    factor[0] += shift
    factors.append(factor)
    rho = multiply(rho, factor)

alpha = 8 * 6**7
b6 = rho[16] / (12 * alpha)
b2 = (rho[12] - 6 * b6**2) / (12 * alpha)
assert (alpha, b6, b2) == (
    2239488, Fraction(11663498286), Fraction(9330368884708461, 512)
)
h0 = [Fraction(0)] * 11
h0[10], h0[6], h0[2] = Fraction(alpha), b6, b2
h02 = multiply(h0, h0)
F = [a - 6 * b for a, b in zip(rho, h02)]
assert all(F[i] == 0 for i in range(9, 21))
assert all(F[i] >= 0 for i in range(9))
N = sum(F)
assert N == Fraction(154868645108828900703280020135040197, 131072)
threshold = max(ceil_fraction(N) + 1, alpha)
T = 2 + ell * (-((2 - threshold) // ell))
assert T >= N + 1 and T >= alpha and T % ell == 2
h = h0[:]
h[0] = Fraction(T)
d = lcm(*(c.denominator for c in h))
assert d == 512
H = [int(d * c) for c in h]
h2 = multiply(h, h)
delta = [a - 6 * b for a, b in zip(rho, h2)]
assert all(delta[i] == 0 for i in range(11, 21))
delta = delta[:11]
assert delta[10] == -12 * T * alpha

# Independent exact evaluations of the resultant: closed product and Sylvester.
Ah, Bh, Ch, Dh = H[10], H[6], H[2], H[0]
J_product = 1
for factor in factors:
    a, b = int(factor[4]), int(factor[0])
    k = Ah * b**2 - Bh * b * a + Ch * a**2
    result = Dh**2 * a**5 + b * k**2
    assert result == resultant([b, 0, a], H[::2])
    assert result**2 == resultant(list(map(int, factor)), H)
    J_product *= result
J = resultant(list(map(int, rho[::2])), H[::2])
J_full = resultant(list(map(int, rho)), H)
assert J == J_product and J > 0 and J_full == J**2

# The two fixed avoidance-prime assertions and the fixed delta congruence.
for p in [ell, q]:
    assert all(evaluate(rho, x, p) != 0 for x in range(p))
assert all(evaluate(delta, x, ell) != 0 for x in range(ell))
assert delta[10].numerator % ell != 0

# The local square conditions for rho at every integer input.
# At 2 it is enough to use beta=3 (mod 8), checking r(beta)/4 modulo 8.
def contact(t):
    return t * (t - 1) * (t - 2401) * (32 * t + 343) * (2 * t - 1)

for t in range(3, 32, 8):
    r = contact(t)
    assert valuation(abs(r), 2) == 2 and (r // 4) % 8 == 1
# beta/9=2 (mod 3), and the other four factors give unit product 1.
assert 450459 % 27 == 18 and 216 % 27 == 0
assert (2 * (-1) * (-2401) * 343 * (-1)) % 3 == 1
squares17 = {x*x % 17 for x in range(1, 17)}
for x in range(1, 17):
    r = int(evaluate(rho, x))
    assert r % 17 in squares17
r0 = int(rho[0])
assert valuation(r0, 17) == 2 and (r0 // 17**2) % 17 in squares17
# If 17|x, rho(x)=rho(0) mod 17^4, enough for the preceding depth/unit.
assert all(i == 0 or i >= 4 for i, c in enumerate(rho) if c)
assert ell % 8 == 1 and ell % 3 == 1 and ell % 17 in squares17
assert 6 % 17 not in squares17

# Uniform real constants, independent of L.
a0 = 8 * 108**5
A0 = 66 * 450459**5
mu = Fraction(3 * alpha, 8)
Dnorm = ceil_fraction(sum(abs(c) for c in delta))
lower = Fraction(a0, Dnorm**2)
upper = Fraction(A0, mu**2)
R_min = lower / (q*q*upper)
assert 0 < R_min < 1 and upper > 1
cstar = 102**6 * J**2

def normalization_exponent(L):
    assert L >= 3 and L % 2 == 1
    numerator = cstar * pow(ell, L) * upper.numerator
    denominator = upper.denominator
    low, high = 0, 1
    while pow(q, 2*high) * denominator <= numerator:
        high *= 2
    while low + 1 < high:
        mid = (low + high) // 2
        if pow(q, 2*mid) * denominator > numerator:
            high = mid
        else:
            low = mid
    k = high
    assert pow(q, 2*k) * denominator > numerator
    assert pow(q, 2*(k-1)) * denominator <= numerator
    return k

# Exact small representative exponents; the proof applies to every odd L.
exponents = {str(L): normalization_exponent(L) for L in [3, 5, 101]}
W_bound = Fraction(293, 256)**2 + Fraction(20, 256)**2
assert W_bound == Fraction(86249, 65536) and W_bound < Fraction(3, 2)

certificate = {
    "status": "passed",
    "scope": "exact constants and finite residues; all-input proofs are in TeX",
    "ell": ell, "second_avoidance_prime": q,
    "h0_coefficients": {str(i): str(c) for i, c in enumerate(h0) if c},
    "remainder_coefficients": {str(i): str(c) for i, c in enumerate(F) if c},
    "N": str(N), "T": T, "H_denominator": d,
    "resultant_J": str(J), "resultant_J_bits": J.bit_length(),
    "resultant_in_X": str(J_full), "resultant_in_X_bits": J_full.bit_length(),
    "resultant_checked_by": ["Sylvester determinant with Bareiss elimination", "five quadratic-factor formulas", "squared resultant after X² substitution"],
    "rho_avoidance_residues_checked": {str(ell): ell, str(q): q},
    "delta_avoidance_residues_checked": ell,
    "local_square_conditions": {"2": "v=2, unit=1 modulo8", "3": "v=2, unit=1 modulo3", "17": "v in {0,2}, unit square modulo17"},
    "delta_coefficient_norm_upper": Dnorm,
    "uniform_R_lower_bound": str(R_min),
    "R_upper_bound": "1 (strict)",
    "norm_tree_bound": str(W_bound),
    "sample_normalization_exponents": exponents,
    "arithmetical_limitation": "No variable reduction; prescribed indices still need reduction-order divisibility at contact primes."
}
path = Path(__file__).with_name("uniform-scalar-normalization-certificate.json")
path.write_text(json.dumps(certificate, indent=2) + "\n")
print(json.dumps({"status": "passed", "certificate": str(path), "J_bits": J.bit_length(), "T": T, "sample_exponents": exponents}, indent=2))
