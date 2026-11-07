#!/usr/bin/env python3
"""Standalone exact certificates for the elliptic chart obstruction.

Requires only Python's standard library; no source polynomial or other project
file is read. Theorems concerning isogenies, formal groups, and rational points
on curves are mathematical inputs proved or cited in the accompanying note.
"""
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import json


def add(x, y): return x[0]+y[0], x[1]+y[1]
def neg(x): return -x[0], -x[1]
def sub(x, y): return add(x, neg(y))
def mul(x, y): return x[0]*y[0]+2*x[1]*y[1], x[0]*y[1]+x[1]*y[0]
def scale(c, x): return Q(c)*x[0], Q(c)*x[1]
def inv(x):
    n = x[0]*x[0]-2*x[1]*x[1]
    assert n
    return x[0]/n, -x[1]/n
def div(x, y): return mul(x, inv(y))
def sq(x): return mul(x, x)
def cube(x): return mul(sq(x), x)


D = Q(11), Q(-6)
P = ((Q(57, 8), Q(-7, 2)), (Q(-165, 8), Q(417, 32)))
R = ((Q(1), Q(1)), (Q(0), Q(2)))


def curve(point):
    x, y = point
    return sq(y) == sub(cube(x), mul(D, x))


def double(point):
    x, y = point
    slope = div(sub(scale(3, sq(x)), D), scale(2, y))
    u = sub(sq(slope), scale(2, x))
    return u, sub(mul(slope, sub(x, u)), y)


def v3q(q):
    if not q: return float('inf')
    def valuation(n):
        v = 0
        while n % 3 == 0: v, n = v+1, n//3
        return v
    return valuation(abs(q.numerator))-valuation(q.denominator)


def v3k(x): return min(map(v3q, x))


def finite_counts():
    p = 17
    assert 6*6 % p == 2 and 4*4 % p == 16
    reports = []
    for d, expected in [(9, 20), (13, 16)]:
        assert 64*d**3 % p
        rows = []
        for x in range(p):
            rhs = (x**3-d*x) % p
            y_count = sum(y*y % p == rhs for y in range(p))
            rows.append([x, rhs, y_count])
        direct = 1+sum(row[2] for row in rows)
        # Independent Euler-criterion count, not using the root list.
        character_count = 1+sum(1 if (x**3-d*x) % p == 0 else
                                2 if pow((x**3-d*x) % p, 8, p) == 1 else 0
                                for x in range(p))
        assert direct == character_count == expected
        reports.append({'D_mod_17': d, 'point_count': direct,
                        'abscissa_rhs_root_count': rows})
    assert (11-6*6) % p == 9 and (11+6*6) % p == 13
    return reports


def exact_curve_checks():
    assert curve(P) and curve(R) and double(R) == P
    twice = double(P)
    assert curve(twice)
    certificate = {'xP': v3k(P[0]), 'yP': v3k(P[1]),
                   'tangent_numerator': v3k(sub(scale(3, sq(P[0])), D)),
                   'x2P': v3k(twice[0]), 'y2P': v3k(twice[1]),
                   'formal_parameter_2P': v3k(neg(div(twice[0], twice[1])))}
    assert certificate == {'xP': 0, 'yP': 1, 'tangent_numerator': 0,
                           'x2P': -2, 'y2P': -3, 'formal_parameter_2P': 1}
    d = Q(3), Q(-1)
    d_conjugate = Q(3), Q(1)
    assert sq(d) == D and mul(d, d_conjugate) == (Q(7), Q(0))
    assert cube(d) == (Q(45), Q(-29))
    assert div(d_conjugate, d) == div((Q(7), Q(0)), sq(d))
    # The torsion translation switches a point outside the affine Y chart
    # into that chart. The general statement is proved in the TeX note.
    x, y = R
    translated = neg(div(D, x)), div(mul(D, y), sq(x))
    assert curve(translated) and not y[0] and translated[1][0]
    for x, y in (P, translated):
        A0, A1 = sub(cube(x), mul(D, x))
        Y = 2*y[0]
        assert Y and Y**4-4*A0*Y**2+8*A1**2 == 0
        assert (Y/2, A1/Y) == y
    return certificate


def main():
    report = {'status': 'PASS', 'point_counts': finite_counts(),
              'non_torsion_valuation_certificate_at_three': exact_curve_checks(),
              'quadratic_twist_and_quartic_chart_checks': True,
              'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'scope': 'Exact point counts, exact elliptic arithmetic, valuations, and chart examples. General finiteness and sharpness statements are supplied by the accompanying mathematical proof.'}
    output = Path(__file__).with_name('elliptic-chart-verification.json')
    output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'point_counts': [r['point_count'] for r in report['point_counts']],
                      'valuation_certificate': report['non_torsion_valuation_certificate_at_three']}, indent=2))


if __name__ == '__main__': main()
