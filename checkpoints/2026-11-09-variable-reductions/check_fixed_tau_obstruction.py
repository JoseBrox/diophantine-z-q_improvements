#!/usr/bin/env python3
"""Exact obstruction to fixing the retained pole-conic parameter tau=1."""
from fractions import Fraction as F
from math import gcd, isqrt
from pathlib import Path
import json
from cypari2 import Pari

pari = Pari()
pari.allocatemem(128000000, silent=True)
pari.setrand(1)
b = F(204**2, 61**2)
B = 17*b
tau = F(1)
e = (tau*tau-B)/(tau*tau+3*B)
p = -4*B*tau/(tau*tau+3*B)
M = B*e*(B-b*b)
N = B*M
n = -32380801574194567
assert e == F(-703751, 2126137)
assert p*p == B*(1-e)*(1+3*e)
assert 0 < b < 17 and isqrt(b.denominator)**2 == b.denominator
ratio = N/n
k = F(isqrt(ratio.numerator), isqrt(ratio.denominator))
assert k*k == ratio

def valuation(x, prime):
    def v_integer(a):
        value = 0
        while a % prime == 0:
            a //= prime
            value += 1
        return value
    return v_integer(x.numerator)-v_integer(x.denominator)

local = {str(prime): valuation(b, prime) for prime in (2, 3, 17)}
assert local == {'2': 4, '3': 2, '17': 2}
# b is a nonzero rational square, so all three local square conditions hold.
# x=(B/k^2)s^2, y=(B^2/k^3)sq sends the pole quartic to E_n.
assert n*k*k/B == M
assert B**3/k**6 * B == (B**2/k**3)**2
assert B == 17*F(204, 61)**2

def point_count(prime):
    assert 6*n % prime
    square_counts = [0]*prime
    for y in range(prime): square_counts[y*y % prime] += 1
    return 1 + sum(square_counts[x*(x-n)*(x+3*n) % prime]
                   for x in range(prime))

counts = {str(prime): point_count(prime) for prime in (5, 7, 11, 23, 29, 31)}
torsion_bound = gcd(*counts.values())
assert torsion_bound == 4
E = pari.ellinit([0, 2*n, 0, -3*n*n, 0])
rank = pari.ellrank(E)
assert [int(rank[i]) for i in range(3)] == [0, 0, 0]
assert int(pari.elltors(E)[0]) == 4
assert n < 0
positive_class = F(-3*n, 17)
assert isqrt(positive_class.numerator)**2 != positive_class.numerator or \
       isqrt(positive_class.denominator)**2 != positive_class.denominator
# The only nonzero torsion abscissas are n and -3n. Neither is in 17 Q^2.
# s=0 would make the original quartic B q^2=-3 M^2<0, which is impossible.
output = Path(__file__).resolve().parent / 'fixed-tau-one-obstruction.json'
report = {
    'status': 'PASS',
    'scope': 'Fixing tau=1 or tau=-1 is not complete for all prepared pole inputs; no assertion is made about the selected-prime-pattern subfamily.',
    'pari_version': str(pari('version()')),
    'b': str(b), 'B': str(B), 'tau': '1', 'e': str(e), 'p': str(p),
    'prepared_valuations': local, 'rational_square_root_b': '204/61',
    'elliptic_parameter': n, 'ellrank': str(rank),
    'unconditional_rank_upper_bound': 0,
    'rational_scaling_k': str(k),
    'map': {'x': '(B/k^2)*s^2', 'y': '(B^2/k^3)*s*q'},
    'required_x_squareclass': 17,
    'good_prime_point_counts': counts, 'torsion_order_upper_bound': torsion_bound,
    'nonidentity_torsion_points': [[0, 0], [n, 0], [-3*n, 0]],
    'nonzero_torsion_abscissas_not_in_required_squareclass': True,
    'rank_method': 'PARI ellrank: exact 2-descent; no analytic rank or BSD hypothesis.'
}
output.write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
