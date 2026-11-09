#!/usr/bin/env python3
"""An exact small prepared input and the constant-twist conic identities.

The infinite family follows from weak approximation in the accompanying
proof.  This script uses no floating-point arithmetic or analytic rank.
"""
from fractions import Fraction as F
from hashlib import sha256
from math import gcd
from pathlib import Path
import json
from cypari2 import Pari


def val(x, prime):
    def integer_val(n):
        count = 0
        while n % prime == 0:
            count += 1
            n //= prime
        return count
    return integer_val(x.numerator)-integer_val(x.denominator)


def sf(n):
    sign = 1 if n > 0 else -1
    n = abs(n)
    p = 2
    while p*p <= n:
        while n % (p*p) == 0:
            n //= p*p
        p = 3 if p == 2 else p+2
    return sign*n


u0, v0 = F(204, 101), F(11, 101)
assert 17+3*u0*u0 == 2465*v0*v0
t0 = 3*u0/(2465*v0)


def conic(t):
    den = 3-2465*t*t
    assert den
    return ((-u0*(3+2465*t*t)+4930*v0*t)/den,
            (v0*(3+2465*t*t)-6*u0*t)/den)


assert conic(t0) == (u0, v0)
for t in [F(-7, 13), F(0), F(1), F(17, 103), t0]:
    u, v = conic(t)
    assert 17+3*u*u == 2465*v*v

# Exact precomputed rational parameter near a real zero of u(t), while
# retaining an open neighborhood of t0 at 2,3,17.  No approximation is
# used to validate this number or any assertion below.
modulus, denominator = 102**8, 10**80+1
step = -83340078930354889501694524508097867159692348405869629181181886
assert gcd(modulus, denominator) == 1
t = t0+F(modulus*step, denominator)
u, v = conic(t)
b = u*u
assert 17+3*b == 2465*v*v
assert 0 < b < F(1, 10**80)
prepared = {str(p): val(b, p) for p in (2,3,17)}
assert prepared == {'2': 4, '3': 2, '17': 2}
assert b.numerator == u.numerator**2 and b.denominator == u.denominator**2
B = 17*b
e = (17-b)/(17+3*b)
pole_p = -4*B*17/(17**2+3*B)
assert pole_p*pole_p == B*(1-e)*(1+3*e)
M = B*e*(B-b*b)
N = B*M
k = 17*u**3*(17-u*u)/(2465*v)
assert k and N == 2465*k*k
assert B == 17*u*u and B > 0 and M != 0

# Repeat the small constant-curve rank certificate independently of the
# large rational input.  No basis or saturation assumption is used.
n = 2465
px, py = 77571, 22248954
assert py*py == px*(px-n)*(px+3*n)
assert px == 51*39**2


def count(p):
    assert 6*n % p
    squares = [0]*p
    for y in range(p):
        squares[y*y % p] += 1
    return 1+sum(squares[x*(x-n)*(x+3*n) % p] for x in range(p))


counts = {str(p): count(p) for p in (7,11,13,19,23,31)}
assert gcd(*counts.values()) == 4
pari = Pari()
pari.allocatemem(128000000, silent=True)
pari.setrand(1)
rank = pari.ellrank(pari.ellinit([0,2*n,0,-3*n*n,0]))
assert [int(rank[i]) for i in range(3)] == [1,1,0]
torsion_classes = {1,-3,n,sf(-3*n)}
classes = torsion_classes | {sf(51*c) for c in torsion_classes}
assert len(classes) == 8 and 17 not in classes

folder = Path(__file__).resolve().parent
rank_source = folder/'fixed-tau17-obstruction.json'
source = json.loads(rank_source.read_text())
assert source['two_selmer_rank'] == 3
assert source['elliptic_parameter'] == n
assert source['complete_x_squareclass_image'] == sorted(classes)
report = {
    'status': 'PASS',
    'scope': 'An explicit prepared counterexample with b<10^-80; the accompanying theorem proves arbitrarily small counterexamples by weak approximation. The Sun-selected subfamily is not excluded.',
    'tau': ['17','-17'],
    'conic': '17+3*u^2=2465*v^2',
    'base_point': [str(u0),str(v0)],
    'rational_parameter': str(t),
    'u': str(u), 'v': str(v), 'b': str(b),
    'rational_square_root_b': str(u),
    'prepared_valuations': prepared,
    'strict_upper_bound_for_b': '10^-80',
    'e': str(e), 'p': str(pole_p), 'scaling_k': str(k),
    'twist_identity': 'B^2*e*(B-b^2)=2465*k^2',
    'elliptic_parameter': n,
    'ellrank': str(rank),
    'explicit_infinite_order_point': [px,py],
    'good_prime_point_counts': counts,
    'complete_x_squareclass_image': sorted(classes),
    'required_squareclass': 17,
    'required_class_absent': True,
    'rank_source_certificate_sha256': sha256(rank_source.read_bytes()).hexdigest(),
    'zero_s_excluded_by_real_sign': True,
    'method': 'Exact rational identities, algebraic 2-descent, torsion bounds, and the full squareclass image size bound; no analytic rank or saturation hypothesis.',
}
out = folder/'small-fixed-tau17-obstruction.json'
out.write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({'status':'PASS','b_bound':'0<b<10^-80',
                  'prepared_valuations':prepared,'elliptic_parameter':n,
                  'squareclass_image':sorted(classes),'output':str(out)}))
