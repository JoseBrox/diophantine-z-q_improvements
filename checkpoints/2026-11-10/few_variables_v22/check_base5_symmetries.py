#!/usr/bin/env python3
"""Exact rational projective symmetry and reflected reciprocal tests.

Only Python standard-library rational arithmetic is used.  Infinity is None.
"""
from fractions import Fraction as Q
from itertools import permutations
from math import gcd, lcm, isqrt
import json
from pathlib import Path

S = (None, Q(0), Q(1), Q(2401), Q(-343, 32))


def hom(x):
    return (1, 0) if x is None else (x.numerator, x.denominator)


def normalize(vec):
    den = lcm(*(x.denominator for x in vec))
    out = [int(x * den) for x in vec]
    g = gcd(*out)
    out = [x // g for x in out]
    if next(x for x in out if x) < 0:
        out = [-x for x in out]
    return tuple(out)


def null_vector(rows):
    rows = [[Q(x) for x in row] for row in rows]
    pivots = []
    for col in range(4):
        chosen = next((i for i in range(len(pivots), 3) if rows[i][col]), None)
        if chosen is None:
            continue
        i = len(pivots)
        rows[i], rows[chosen] = rows[chosen], rows[i]
        z = rows[i][col]
        rows[i] = [x / z for x in rows[i]]
        for j in range(3):
            if j != i:
                z = rows[j][col]
                rows[j] = [x - z * y for x, y in zip(rows[j], rows[i])]
        pivots.append(col)
    assert len(pivots) == 3
    free = next(i for i in range(4) if i not in pivots)
    out = [Q(0)] * 4
    out[free] = Q(1)
    for i, col in reversed(list(enumerate(pivots))):
        out[col] = -sum(rows[i][j] * out[j] for j in range(col + 1, 4))
    return normalize(out)


def transform(source, target):
    rows = []
    for x, y in zip(source, target):
        X, Z = hom(x)
        Y, W = hom(y)
        rows.append([W * X, W * Z, -Y * X, -Y * Z])
    mat = null_vector(rows)
    a, b, c, d = mat
    assert a * d != b * c
    return mat


def apply(mat, x):
    a, b, c, d = mat
    X, Z = hom(x)
    num, den = a * X + b * Z, c * X + d * Z
    return None if den == 0 else Q(num, den)


def square_root(x):
    if x < 0:
        return None
    a, b = isqrt(x.numerator), isqrt(x.denominator)
    return Q(a, b) if a * a == x.numerator and b * b == x.denominator else None


def qstr(x):
    return 'infinity' if x is None else str(x)


def determinant(x, y):
    a, b = hom(x)
    c, d = hom(y)
    return a*d-b*c


def complement_invariants():
    results = []
    for removed in S:
        a, b, c, d = [x for x in S if x != removed]
        z = Q(determinant(a,c)*determinant(b,d),
              determinant(a,d)*determinant(b,c))
        J = (z*z-z+1)**3/(z*z*(1-z)**2)
        results.append({'removed': qstr(removed), 'cross_ratio': qstr(z),
                        'anharmonic_invariant': qstr(J),
                        'invariant_integer_part': J.numerator//J.denominator})
    assert len({r['invariant_integer_part'] for r in results}) == 5
    return results


def pairings(xs):
    a, b, c, d = xs
    return (((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c)))


def reciprocal_tests():
    """All +/- pair products after the unique fixed squared root is 1.

    Move its original contact to infinity. A normalized nonconstant rational
    projective map then has f(w)=(w+A)/(w+C), with A != C.  Let V=A+C,
    D=A-C.  For a pair x,y, product +1 means V=-(x+y), while product -1
    means D^2=-V^2-2V(x+y)-4xy.  Thus every case is decided over Q.
    """
    results = []
    for fixed in S:
        others = [x for x in S if x != fixed]
        def coordinate(x):
            if fixed is None:
                return x
            return Q(0) if x is None else 1 / (x - fixed)
        ws = [coordinate(x) for x in others]
        for pairs in pairings(tuple(range(4))):
            (i, j), (k, l) = pairs
            x, y, z, w = ws[i], ws[j], ws[k], ws[l]
            p, q = x+y, z+w
            r, s = x*y, z*w
            for eps in ((1,1), (1,-1), (-1,1), (-1,-1)):
                row = {'fixed': qstr(fixed),
                       'pairs': [[qstr(others[v]) for v in pair] for pair in pairs],
                       'signs': eps}
                if eps == (1, 1):
                    row['equal_pair_sums'] = p == q
                    row['rational_candidate'] = p == q
                else:
                    if eps == (1,-1):
                        V = -p
                        D2 = -V*V-2*V*q-4*s
                    elif eps == (-1,1):
                        V = -q
                        D2 = -V*V-2*V*p-4*r
                    else:
                        if p == q:
                            assert r != s
                            row['inconsistent_equal_sums'] = True
                            row['rational_candidate'] = False
                            results.append(row)
                            continue
                        V = -2*(r-s)/(p-q)
                        D2 = -V*V-2*V*p-4*r
                    D = square_root(D2)
                    row['A_plus_C'] = qstr(V)
                    row['A_minus_C_squared'] = qstr(D2)
                    row['rational_candidate'] = D is not None and D != 0
                    if row['rational_candidate']:
                        row['A'] = qstr((V+D)/2)
                        row['C'] = qstr((V-D)/2)
                results.append(row)
    return results


def main():
    source = S[:3]
    automorphisms = []
    matrices = set()
    for target in permutations(S, 3):
        mat = transform(source, target)
        assert tuple(apply(mat, x) for x in source) == target
        matrices.add(mat)
        images = tuple(apply(mat, x) for x in S)
        if set(images) == set(S):
            automorphisms.append({'matrix': mat, 'permutation': [S.index(x) for x in images]})
    assert len(matrices) == 60
    tests = reciprocal_tests()
    assert len(tests) == 60
    assert automorphisms == [{'matrix': (1,0,0,1), 'permutation': [0,1,2,3,4]}]
    assert not any(r['rational_candidate'] for r in tests)
    report = {'contact_set': list(map(qstr, S)), 'projective_maps_tested': 60,
              'automorphisms': automorphisms, 'signed_reciprocal_cases_tested': 60,
              'independent_complement_invariants': complement_invariants(),
              'signed_reciprocal_candidates': [r for r in tests if r['rational_candidate']],
              'signed_reciprocal_case_certificate': tests}
    dest = Path(__file__).with_name('base5-symmetries-certificate.json')
    dest.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k != 'signed_reciprocal_case_certificate'}, indent=2))


if __name__ == '__main__':
    main()
