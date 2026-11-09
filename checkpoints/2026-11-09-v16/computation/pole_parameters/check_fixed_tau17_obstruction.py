#!/usr/bin/env python3
"""Exact obstruction to the factor-canceling choice tau=17 in the pole chart."""
from fractions import Fraction as F
from itertools import product
from math import gcd, isqrt
from pathlib import Path
import json
import re
import subprocess
import sys
from cypari2 import Pari

pari = Pari()
pari.allocatemem(128000000, silent=True)
pari.setrand(1)
n = 2465
E = pari.ellinit([0, 2*n, 0, -3*n*n, 0])
if '--rank-log' in sys.argv:
    pari('default(debug,3)')
    print('RANK_RESULT', pari.ellrank(E), flush=True)
    raise SystemExit(0)

b = F(204**2, 101**2)
B = 17*b
tau = F(17)
e = (tau*tau-B)/(tau*tau+3*B)
p = -4*B*tau/(tau*tau+3*B)
assert e == (17-b)/(17+3*b) == F(7753, 17545)
assert p*p == B*(1-e)*(1+3*e)
assert 0 < b < 17 and isqrt(b.denominator)**2 == b.denominator
M = B*e*(B-b*b)
N = B*M
ratio = N/n
k = F(isqrt(ratio.numerator), isqrt(ratio.denominator))
assert k*k == ratio
assert n*k*k/B == M
assert B**3/k**6 * B == (B**2/k**3)**2
assert B == 17*F(204, 101)**2

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

def point_count(prime):
    assert 6*n % prime
    square_counts = [0]*prime
    for y in range(prime): square_counts[y*y % prime] += 1
    return 1 + sum(square_counts[x*(x-n)*(x+3*n) % prime]
                   for x in range(prime))

counts = {str(prime): point_count(prime) for prime in (7, 11, 13, 19, 23, 31)}
assert gcd(*counts.values()) == 4
rank = pari.ellrank(E)
assert [int(rank[i]) for i in range(3)] == [1, 1, 0]
P = (77571, 22248954)
assert P[1]**2 == P[0]*(P[0]-n)*(P[0]+3*n)
assert P[1] and P[0] == 51*39**2

def squareclass(a):
    sign = -1 if a < 0 else 1
    a = abs(a)
    out = sign
    trial = 2
    while trial*trial <= a:
        parity = 0
        while a % trial == 0:
            a //= trial
            parity ^= 1
        if parity: out *= trial
        trial += 1
    return out*a

classes = sorted({squareclass((-3)**i*n**j*51**ell)
                  for i, j, ell in product(range(2), repeat=3)})
assert len(classes) == 8 and 17 not in classes
# Rank one and full two-torsion bound the entire x-squareclass image by 8.
# The displayed points already attain 8, so no basis or saturation claim is needed.
folder = Path(__file__).resolve().parent
run = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--rank-log'],
                     capture_output=True, text=True, check=True)
log = run.stdout + run.stderr
assert list(map(int, re.findall(r'Selmer rank: (\d+)', log))) == [3]
(folder / 'fixed-tau17-pari-descent.txt').write_text(log)
report = {
    'status': 'PASS',
    'scope': 'Fixing tau=17 or tau=-17 is not complete for all prepared inputs; the specially selected comparison-input family is not addressed.',
    'pari_version': str(pari('version()')),
    'b': str(b), 'B': str(B), 'tau': '17', 'e': str(e), 'p': str(p),
    'prepared_valuations': local, 'rational_square_root_b': '204/101',
    'simplified_twist_squareclass': 'b*(17+3*b)',
    'elliptic_parameter': n, 'ellrank': str(rank),
    'two_selmer_rank': 3, 'rational_two_torsion_rank': 2,
    'unconditional_rank_upper_bound': 1,
    'explicit_infinite_order_point': list(P),
    'rational_scaling_k': str(k),
    'map': {'x': '(B/k^2)*s^2', 'y': '(B^2/k^3)*s*q'},
    'required_x_squareclass': 17,
    'good_prime_point_counts': counts, 'torsion_order_upper_bound': 4,
    'complete_x_squareclass_image': classes,
    'squareclass_image_size_upper_bound_from_rank_and_torsion': 8,
    'completeness_argument': 'Eight known image classes attain the bound 2^(rank+2); no Mordell-Weil basis or saturation hypothesis is used.',
    'required_class_absent': True,
    'rank_method': 'Exact PARI 2-descent upper bound and explicit nontorsion point.'
}
(folder / 'fixed-tau17-obstruction.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
