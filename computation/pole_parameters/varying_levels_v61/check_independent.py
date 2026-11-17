#!/usr/bin/env python3
"""Independent exact fixtures for the varying-level pole-fiber theorem."""
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path
import argparse
import hashlib
import json


def val(x, p):
    x = Q(x)
    assert x
    def integer_val(a):
        a = abs(a)
        n = 0
        while a % p == 0:
            a //= p
            n += 1
        return n
    return integer_val(x.numerator) - integer_val(x.denominator)


def residue(x, p):
    x = Q(x)
    assert x.denominator % p
    return x.numerator * pow(x.denominator, -1, p) % p


def chi(x, p):
    x %= p
    if not x:
        return 0
    return 1 if pow(x, (p - 1) // 2, p) == 1 else -1


def sqrt_q(x):
    x = Q(x)
    assert x >= 0
    a, b = isqrt(x.numerator), isqrt(x.denominator)
    assert a * a == x.numerator and b * b == x.denominator
    return Q(a, b)


def add(P, R, n):
    if P is None:
        return R
    if R is None:
        return P
    x, y = P
    z, w = R
    if x == z and y == -w:
        return None
    slope = (w - y) / (z - x) if x != z else (3*x*x-n*n)/(2*y)
    a = slope*slope-x-z
    return a, slope*(x-a)-y


base = Path(__file__).resolve().parent
source = Path(__file__).resolve().parents[3] / 'papers/pole_parameters/varying_level_pole_fibers_20261117_v61.tex'

even_valuation_cases = 0
for p in (5, 13, 17):
    for D in range(1, p):
        if chi(D, p) != -1 or chi(-D, p) != -1:
            continue
        for a in range(-3, 4):
            d = Q(p) ** (2*a) * D
            eta = 1-d
            for b in range(-4, 5):
                r = Q(p) ** b
                ratio = (d+r*r)/(d-r*r)
                assert val(ratio, p) == 0
                assert val(eta, p) == 2*min(a, 0)
                assert val(eta*ratio, p) == 2*min(a, 0)
                even_valuation_cases += 1

positive_odd_cases = 0
for p in (3, 5, 7, 11, 13, 17):
    for D in range(1, p):
        for a in range(3):
            d = Q(p) ** (2*a+1) * D
            for b in range(-3, 4):
                r = Q(p) ** b
                k = (1-d)*(d+r*r)/(d-r*r)
                assert val(k, p) == 0
                assert residue(k, p) in (1, p-1)
                assert chi(residue(k, p), p) == 1 or chi(-residue(k, p), p) == 1
                positive_odd_cases += 1

good_reduction_curves = 0
for p in (5, 13, 17, 29, 37, 41):
    for D in range(1, p):
        if chi(D, p) != -1 or chi(-D, p) != -1:
            continue
        for K in range(1, p):
            # The points at infinity number 1+chi(-D,p)=0 in this case.
            count = sum(1+chi(D*(K*K-s**4), p) for s in range(p))
            assert count > 0 and (count-(p+1))**2 <= 4*p
            # An affine singularity would require s=y=0, which is not on the curve.
            assert D*K*K % p != 0
            good_reduction_curves += 1

negative_odd_cases = 0
for nu in range(-31, 0, 2):
    for val_s in range(-20, 21):
        left, right = 3*nu, nu+4*val_s
        assert left != right and min(left, right) % 2 == 1
        negative_odd_cases += 1

# An exact prepared example, with independent odd multiples on the two twists.
d, n = Q(112, 841), Q(21)
eta, scale = 1-d, Q(27, 29)
assert eta == scale*scale and d/7 == Q(4,29)**2 and val(d,2) == 4
P = (Q(28), Q(98))
twice = add(P, P, n)
points = [P]
for _ in range(3):
    points.append(add(points[-1], twice, n))
fibers = []
global_pairs = 0
for xprime, yprime in points:
    xprime, yprime = scale**2*xprime, scale**3*yprime
    b = sqrt_q(xprime/d)
    V = abs(yprime/b)
    k = d*b*b/n
    h = V/n
    r = V/(d*b*b+n*eta)
    assert 0 < r and r*r < d and k > eta
    assert k == eta*(d+r*r)/(d-r*r)
    assert h == 2*d*eta*r/(d-r*r)
    assert d*k == n*(d*b/n)**2
    s_values = []
    for x, ypoint in points:
        a = sqrt_q(x/d)
        U = ypoint/a
        s = b/a
        y = k*U/(d*a*a)
        assert y*y == d*(k*k-s**4)
        assert h*h == d*(k*k-eta*eta)
        v = y/(k+s*s)
        Y = 2*d*s*s*h/(k+s*s)
        assert Y*Y == d*(d+v*v)**2*s**4-d*(d-v*v)**2*eta**2
        cleared_y = (d-r*r)*y
        assert cleared_y**2 == d*eta**2*(d+r*r)**2-d*(d-r*r)**2*s**4
        curve_X, curve_Y = -d*s*s, d*s*y
        assert curve_Y**2 == curve_X**3-(d*k)**2*curve_X
        s_values.append(s)
        global_pairs += 1
    assert len(set(s_values)) == len(points)
    fibers.append(r)
assert len(set(fibers)) == len(points)

certificate = {
    'status': 'PASS',
    'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'even_valuation_unit_ratio_cases': even_valuation_cases,
    'positive_odd_valuation_cases': positive_odd_cases,
    'smooth_genus_one_reduction_fixtures': good_reduction_curves,
    'negative_odd_pole_cases': negative_odd_cases,
    'exact_prepared_rational_fibers': len(fibers),
    'exact_rational_witness_pairs': global_pairs,
    'benchmark': {'d': str(d), 'n': str(n), 'r': '4/29',
                  'k': '972/841', 's': '27/29',
                  'y_and_h': '6804/24389',
                  'reconstructed_v': '4/29',
                  'reconstructed_Y': '653184/20511149'},
    'arbitrary_prescribed_r_realized': False,
    'new_variable_bound_claimed': False,
    'infinite_fiber_claim_verified_by_mathematical_audit_not_finite_search': True,
    'primary_reference': 'Burungale arXiv2611.16130v1, Theorem B, p.2',
}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,default=base/'independent_certificate.json')
output=parser.parse_args().output
output.parent.mkdir(parents=True,exist_ok=True)
output.write_text(json.dumps(certificate, indent=2)+'\n')
print(json.dumps(certificate, indent=2))
