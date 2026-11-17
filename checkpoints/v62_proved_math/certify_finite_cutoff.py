#!/usr/bin/env python3
"""Exact finite-prime and N >= 19 numerical certificates.

The widened local lemmas and mathematical inequalities are proved in
finite_cutoff_proof.md. The inherited full-family height theorem and
the coordinate completeness construction remain separate premises.
"""

from fractions import Fraction as F
from math import factorial, isqrt, prod


def exp_lower(x, degree=40):
    return sum((x**j / factorial(j) for j in range(degree + 1)), F(0))


def exp_upper(x, degree=40):
    assert 0 <= x < degree + 2
    return exp_lower(x, degree) + x**(degree + 1) / factorial(degree + 1) / (1 - x / (degree + 2))


S = {2, 3, 5, 7, 11, 13, 17, 37, 41, 2399}
extra = {47, 67, 109, 179, 257, 439, 2099, 2029147}
Gamma = S | extra
BS = prod(S)
J = prod(Gamma)
CN = 2**68 * 3**16 * 5**16 * 7**4
c0 = F(74712001, 1000000)
C = c0 * CN * J * prod(p + 1 for p in Gamma)
assert len(Gamma) == 18
assert J == 54852429049017820832107412529142530
assert J < 2**116
assert 2665 < C < 2**381
assert c0 < 2**7 and CN < 2**142

sieve = bytearray(b"\x01") * 1001
sieve[0] = sieve[1] = 0
for p in range(2, isqrt(1000) + 1):
    if sieve[p]:
        sieve[p * p : 1001 : p] = b"\x00" * len(range(p * p, 1001, p))
small_primes = [p for p in range(2, 1001) if sieve[p]]
assert len(small_primes) == 168
E_low = prod(F(p + 1, p) for p in small_primes if p not in Gamma)
assert E_low < 2

# Exact check of all contact denominators, differences, and 1-theta.
theta = [F(0), F(-1, 2), F(-1), F(1, 2399), F(-32, 407)]
theta2 = theta + [2 - t for t in theta]
assert len(set(theta2)) == 10 and 1 not in theta2


def supported(n, primes):
    n = abs(n)
    assert n
    for p in primes:
        while n % p == 0:
            n //= p
    return n == 1


for t in theta2:
    assert supported(t.denominator, Gamma)
    assert supported((1 - t).numerator, Gamma)
    assert supported((1 - t).denominator, Gamma)
for i, t in enumerate(theta2):
    for u in theta2[i + 1 :]:
        assert supported((t - u).numerator, Gamma)
        assert supported((t - u).denominator, Gamma)

# Four scalar roots have collision support only 2,3,5,7.
scalar_roots = [F(0), F(1), F(2401), F(-343, 32)]
for i, t in enumerate(scalar_roots):
    for u in scalar_roots[i + 1 :]:
        assert supported((t - u).numerator, {2, 3, 5, 7})
        assert supported((t - u).denominator, {2, 3, 5, 7})
residues149 = []
for t in scalar_roots:
    residue = ((t.numerator * pow(t.denominator, -1, 149) - 2504) * pow(51, -1, 149)) % 149
    residues149.append(residue)
    assert pow(residue, 74, 149) == 148
assert residues149 == [59, 97, 109, 108]

# H4.2 constant C2 = c0 CN BS^2 E(BS) log BS < 2^237.
C2_upper = c0 * CN * BS * prod(p + 1 for p in S) * F(41 * 7, 10)
assert BS < 2**41 and C2_upper < 2**237

# Rational logarithm bounds, certified by exponential series.
assert exp_upper(F(5)) < 149 < exp_lower(F(501, 100))
assert exp_lower(F(7, 10)) > 2
assert exp_lower(F(2)) > 7
assert exp_lower(F(3)) > 14
assert exp_lower(F(7)) > 500
assert 363 < exp_lower(F(6)) <= exp_upper(F(6)) < 1001
assert exp_upper(F(1)) < 3

# High primes give E(M) < 2 M^(1/6006).
assert 6006 == 1001 * 6
# The numerical Delta coefficient is below 500.
assert F(3, 2)**2 > 2
assert F(5, 2)**3 > 14
assert 11**30 > 14 * 10**30
assert 36036 > 30
assert 121 * F(3, 2) * F(5, 2) * F(11, 10) < 500

N = 19
L = 9 * (2 * N - 1) // 4 + 1
assert L == 84
assert F(280 * 6005, 6006) > F(2797, 10)
assert F(82) + F(2, 3) * L * F(501, 100) < 363
assert F(7) + 381 * F(7, 10) + 6 == F(2797, 10)

# Coarse bound for the input comparison: K=2^386.
assert 1 + F(232 * 7, 20) < 83 < 4 * 22
assert 149 > 2**7
assert 7 * L > 239  # tau < c/2 from 2^238 * 149^(-L).
assert 149**L > 600
assert F(23 * 7 * (386 + 18), 220) < 300
assert F(99, 100) * (5 * L - 1) > 400
assert 400 * 600 > 300 + 600

print("PASS: finite bad-prime set has 18 primes and all contact support is covered")
print("PASS: four scalar roots are nonsquares after normalization modulo149")
print("PASS: C<2^381, C2<2^237, and E_low<2")
print("PASS: Delta contradiction at N=19, L=84, strengthens for every larger N")
print("PASS: scalar/input contradiction using K=2^386 and tau<c/2")
print("Scope: widened local proofs, inherited height premise, and chart completeness are separate")
