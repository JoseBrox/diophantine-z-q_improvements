"""Exact prepared scalar counterexample; NOT an actual detector realization.

Run with:
PYTHONPATH=/workspace/scratch/7ac4dd889cf6/math-packages python \
  v83_search_breakthrough/raw_square_v0_certificate.py
"""
from fractions import Fraction as Q
from itertools import product
import json
import sympy as sp
from sage.libs.pari import pari


def squareclass(value):
    value = Q(value)
    assert value
    out = 1 if value > 0 else -1
    for p, exponent in sp.factorint(abs(value.numerator * value.denominator)).items():
        if exponent % 2:
            out *= int(p)
    return out


def valuation(value, p):
    value = Q(value)
    answer = 0
    a, b = abs(value.numerator), value.denominator
    while a % p == 0:
        a //= p
        answer += 1
    while b % p == 0:
        b //= p
        answer -= 1
    return answer


def is_square(value):
    value = Q(value)
    return value >= 0 and sp.integer_nthroot(value.numerator, 2)[1] and sp.integer_nthroot(value.denominator, 2)[1]


def product_class(left, right):
    return tuple(squareclass(a * b) for a, b in zip(left, right))


d, V, e = Q(112, 729), Q(10, 9), Q(112, 225)
assert e == 4 * d / V**2
assert 1 + d == Q(29, 27)**2
assert d == 7 * Q(4, 27)**2
assert e == 7 * Q(4, 15)**2
assert 0 < d < 1 and 0 < e < 1 and 0 < V < 2
assert is_square(d.denominator) and is_square(e.denominator)
assert valuation(d, 2) == valuation(e, 2) == 4
assert valuation(V, 2) == 1
N, lam = 791, Q(4, 405)
assert d * (1 - e) == N * lam**2
assert not is_square(1 - e)

# E_{d(1-e)} is isomorphic to E_N by x=lam^2 x_N, y=lam^3 y_N.
# If y^2=d(s^4-(1-e)^2), then x=d s^2 and y_E=d s y
# yield a point on E_{d(1-e)} with nonzero x-class 7 unless s=0.
# s=0 is impossible by the negative right hand side. The y=0 case
# would force s^2=1-e, excluded above.
E = pari(f'ellinit([0,0,0,-{N*N},0])')
rank = E.ellrank(4)
torsion = E.elltors()
assert int(rank[0]) == int(rank[1]) == 1
assert int(torsion[0]) == 4
xR, yR = -784, 2940
assert yR*yR == xR**3 - N*N*xR
assert int(E.ellisoncurve(pari([xR, yR]))) == 1

# Standard full rational 2-descent with coordinates (x,x-N), using
# the usual limiting values at the three nontrivial 2-torsion points.
T0 = (-1, -N)
TN = (N, 2)
R = (squareclass(xR), squareclass(xR-N))
assert R == (-1, -7)
classes = {(1, 1)}
for generator in (T0, TN, R):
    classes |= {product_class(c, generator) for c in tuple(classes)}
assert len(classes) == 8
# Rank 1 and E[2](Q) of dimension 2 imply |E(Q)/2E(Q)|=8.
# Hence these eight Kummer classes are the full image, not just samples.
xclasses = {c[0] for c in classes}
assert xclasses == {-N, -1, 1, N}
assert 7 not in xclasses

certificate = {
    'scope': 'Prepared scalar counterexample only; no actual detector or proposed t-map realization is asserted.',
    'd': str(d), 'V': str(V), 'e': str(e),
    'sqrt_1_plus_d': '29/27',
    'd_squareclass': squareclass(d), 'e_squareclass': squareclass(e),
    'v2': {'d': valuation(d,2), 'V': valuation(V,2), 'e': valuation(e,2)},
    'one_minus_e': str(1-e),
    'isomorphism_scale': str(lam), 'twist': N,
    'pari_rank_result': str(rank), 'pari_torsion_result': str(torsion),
    'exact_point': [xR, yR],
    'kummer_generators': [list(T0), list(TN), list(R)],
    'full_kummer_image': [list(c) for c in sorted(classes)],
    'full_x_squareclass_image': sorted(xclasses),
    'required_x_squareclass': 7,
    'conclusion': 'No rational point on y^2=d(s^4-(1-e)^2); raw 1+d being a square does not justify the v=0 slice.'
}
print(json.dumps(certificate, indent=2))
