#!/usr/bin/env python3
"""Independent exact check of the four-coordinate elliptic replacement.

The source tables are hash-pinned. This checker imports no producer and
uses only the Python standard library. It checks every changed row, every
unchanged row, the nonsingular rational row change, and the full quartic.
The separate fixed-difference-chart checker verifies the general identities.
"""
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from math import gcd, lcm, isqrt
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
PARAMETER = -1
Q = Fraction


def linear(*pairs):
    result = defaultdict(Q)
    for coefficient, polynomial in pairs:
        for monomial, value in polynomial.items():
            result[monomial] += coefficient*value
    return {m: c for m, c in result.items() if c}


def product(left, right):
    result = defaultdict(Q)
    for a, c in left.items():
        for b, d in right.items():
            result[tuple(sorted(a+b))] += c*d
    return {m: c for m, c in result.items() if c}


def variable(i):
    return {(i,): Q(1)}


def scalar(c):
    return {(): Q(c)} if c else {}


def canonical(p):
    denominator = lcm(*(c.denominator for c in p.values()))
    integers = {m: int(c*denominator) for m, c in p.items() if c}
    divisor = gcd(*integers.values())
    first = min(integers, key=lambda m: (m.count(PARAMETER), tuple(i for i in m if i != PARAMETER)))
    if integers[first] < 0:
        divisor = -divisor
    return {m: c//divisor for m, c in integers.items()}


def field_mul(x, y):
    return (linear((1, product(x[0], y[0])), (2, product(x[1], y[1]))),
            linear((1, product(x[0], y[1])), (1, product(x[1], y[0]))))


def field_sum(*pairs):
    return tuple(linear(*((coefficient, polynomial[i]) for coefficient, polynomial in pairs)) for i in range(2))


def field_constant(a, b=0):
    return scalar(a), scalar(b)


def decode(row, ids):
    result = {}
    for term in row['terms']:
        monomial = tuple(sorted([PARAMETER]*term['parameterPower']+[ids[i] for i in term['monomial']]))
        assert monomial not in result
        result[monomial] = Q(term['coefficient'])
    return result


def determinant(matrix):
    matrix = [[Q(c) for c in row] for row in matrix]
    result = Q(1)
    for i in range(len(matrix)):
        pivot = next((j for j in range(i, len(matrix)) if matrix[j][i]), None)
        if pivot is None:
            return Q(0)
        if pivot != i:
            matrix[i], matrix[pivot] = matrix[pivot], matrix[i]
            result = -result
        value = matrix[i][i]
        result *= value
        for j in range(i+1, len(matrix)):
            coefficient = matrix[j][i]/value
            matrix[j] = [x-coefficient*y for x, y in zip(matrix[j], matrix[i])]
    return result


def expected_common_rows(matrix):
    # Assemble the two quotient identities and the compatibility identity
    # from scalar field constants, independently of the producer's circuit.
    a = field_constant(Q(57, 8), Q(-7, 2))
    b = field_constant(Q(-165, 8), Q(417, 32))
    d = field_constant(11, -6)
    a2 = field_mul(a, a)
    plus = field_sum((1, a2), (1, d))
    minus = field_sum((1, a2), (-1, d))
    assert field_mul(b, b) == field_mul(a, minus)
    exceptional = field_sum((1, field_mul(d, d)),
                            (6, field_mul(a2, d)), (-3, field_mul(a2, a2)))
    assert exceptional == field_constant(Q(-94897379, 4096), Q(4195821, 256))
    norm = exceptional[0][()]**2-2*exceptional[1][()]**2
    assert norm == Q(-8203357319351, 16777216) != 0
    S = variable(142), variable(143)
    T = variable(90), variable(91)
    f = variable(140), variable(141)
    g = variable(160), variable(161)
    st = field_mul(S, T)
    two_bd = field_sum((2, field_mul(b, d)))
    ff = field_mul(two_bd, field_mul(field_sum((1, field_mul(a, T)), (-1, b)), f))
    gg = field_mul(two_bd, field_mul(field_sum((1, field_mul(a, S)), (1, b)), g))
    first = field_sum((1, ff), (-1, field_mul(field_mul(a, plus), st)),
                      (-1, field_mul(field_mul(b, plus), S)),
                      (1, field_mul(field_mul(b, minus), T)),
                      (-4, field_mul(a2, d)))
    second = field_sum((1, gg), (1, field_mul(field_mul(a, plus), st)),
                       (1, field_mul(field_mul(b, minus), S)),
                       (-1, field_mul(field_mul(b, plus), T)),
                       (4, field_mul(a2, d)))
    third = field_sum((1, field_mul(field_mul(d, d), field_mul(f, g))),
                      (1, field_mul(field_mul(a, d), field_sum((1, f), (1, g)))),
                      (1, field_mul(a, st)),
                      (1, field_mul(b, field_sum((1, S), (-1, T)))), (1, d))
    primitive = [canonical(p) for pair in (first, second, third) for p in pair]
    assert determinant(matrix) == Q(-1, 362963666515968)
    return [canonical(linear(*((Q(c), p) for c, p in zip(row, primitive)))) for row in matrix]


def verify(kind, source_root=HERE, output_root=HERE):
    if kind == 'inherited':
        old_path = 'family248_v17/quadratic-family248-v17.json'
        pin = 'b1bf58c470365a7b330af4a33a17a1f7e9aa10c997853c9078a9b8593f43a7ff'
        folder, suffix, count, pairs, row_count, monomials = 'family238_v18', '238-v18', 238, 4, 212, 2924
    else:
        old_path = 'family_abc97_v17/quadratic-family-abc97-v17.json'
        pin = 'e50b41cb15194418771262045afa97fc86ad5c47f376591b732106b690a5491b'
        folder, suffix, count, pairs, row_count, monomials = 'family_abc93_v18', '-abc93-v18', 93, 1, 81, 920
    raw = (source_root/old_path).read_bytes()
    assert sha256(raw).hexdigest() == pin
    old = json.loads(raw)
    root = output_root/folder
    system_raw = (root/('quadratic-family'+suffix+'.json')).read_bytes()
    polynomial_raw = (root/('polynomial-family'+suffix+'.json')).read_bytes()
    system, polynomial = json.loads(system_raw), json.loads(polynomial_raw)
    report = json.loads((root/('construction-report'+suffix+'.json')).read_text())
    old_ids = {c['id']: c['sourceId'] for c in old['coordinates']}
    ids = {c['id']: c['sourceId'] for c in system['coordinates']}
    assert list(ids) == list(range(1, count+1))
    removed = {700, 701}.union(164+4*i+j for i in range(pairs) for j in (0, 1))
    assert set(ids.values()) == set(old_ids.values())-removed
    assert system['variables'] == polynomial['variables'] == report['variables'] == count
    assert polynomial['coordinates'] == system['coordinates']
    assert system['fixedParameter'] == polynomial['fixedParameter'] == old['fixedParameter']
    common = expected_common_rows(report['rationalComponentRowBasis'])
    replacements = dict(zip((34, 35, 92, 93, 112, 113), common))
    for i in range(pairs):
        left = field_mul((variable(234+4*i), variable(235+4*i)),
                         (variable(114+8*i), variable(115+8*i)))
        right = field_mul((variable(110+8*i), variable(111+8*i)),
                          (variable(90), variable(91)))
        for j in range(2):
            key = 146+12*i+j if kind == 'inherited' else 'alternateRatio.cleared.'+str(j)
            replacements[key] = canonical(linear((1, left[j]), (-1, right[j])))
    removed_rows = {661, 662}.union(116+4*i+j for i in range(pairs) for j in (0, 1))
    expected, matched, changed = [], [], []
    for row in old['residuals']:
        if row['sourceId'] in removed_rows:
            continue
        key = row['sourceId'] if row['sourceId'] in replacements else row['name']
        if key in replacements:
            expected.append(replacements[key])
            changed.append(key)
        else:
            expected.append(canonical(decode(row, old_ids)))
            matched.append(row['name'])
    actual = [decode(row, ids) for row in system['residuals']]
    assert len(actual) == row_count and actual == expected
    assert len(changed) == 6+2*pairs
    assert all(max(len(tuple(i for i in m if i != PARAMETER)) for m in row) <= 2 for row in actual)
    expanded = linear(*((1, product(row, row)) for row in actual))
    assert expanded == decode(polynomial, ids)
    assert gcd(*(int(c) for c in expanded.values())) == 1
    assert max(len(tuple(i for i in m if i != PARAMETER)) for m in expanded) == 4
    assert set(i for m in expanded for i in m if i != PARAMETER) == set(ids.values())
    profiles = defaultdict(dict)
    for m, c in expanded.items():
        profiles[tuple(i for i in m if i != PARAMETER)][m.count(PARAMETER)] = int(c)
    assert len(profiles) == monomials == report['ordinaryMonomialsForEveryPositiveParameter']
    assert all(set(p) in ({0}, {1}, {0, 2}) for p in profiles.values())
    assert all(p[0] > 0 and p[2] == 1 for p in profiles.values() if set(p) == {0, 2})
    C = max(abs(p[0]) for p in profiles.values() if set(p) == {0})
    assert str(C) == report['constantCoefficientMaximum']
    L = max(abs(p[1]) for p in profiles.values() if set(p) == {1})
    if kind == 'inherited':
        assert profiles[(489, 489)] == {0: 1, 2: 1}
        assert C > L*L
        n = 53
        assert 149**(4*n+2)+1 > C >= 149**(4*(n-1)+2)+1
        assert report['exactHeightThresholdN'] == n
        height = '149^(4*N+2)+1 for N>=53'
    else:
        assert C == 4153456
        assert profiles[()] == {0: 797687, 2: 1}
        assert L == 4
        threshold = 1833
        assert threshold*threshold+797687 >= C > (threshold-2)**2+797687
        assert report['coefficientHeightThresholdOddB'] == threshold
        height = 'max(4153456,B^2+797687) for every integer B>=3'
    certificate = {
        'status': 'PASS', 'variables': count, 'quadraticRows': row_count,
        'degree': 4, 'content': 1, 'ordinaryMonomialsForEveryPositiveParameter': monomials,
        'exactHeight': height, 'sourceSha256': pin,
        'systemSha256': sha256(system_raw).hexdigest(),
        'polynomialSha256': sha256(polynomial_raw).hexdigest(),
        'independentlyReconstructedChangedRows': len(changed),
        'unchangedRowsComparedExactly': len(matched),
        'rationalRowBasisDeterminant': str(determinant(report['rationalComponentRowBasis'])),
        'exceptionalConstantNorm': '-8203357319351/16777216',
        'arithmeticScope': 'Exact algebraic reconstruction, nonsingular row change, full sum of squares, support and coefficients. The general chart identities have a separate standard-library certificate. No inherited arithmetic hypothesis or sufficient defining threshold is proved by these finite checks.'}
    (root/('independent-verification'+suffix+'.json')).write_text(json.dumps(certificate, indent=2)+'\n')
    print(json.dumps(certificate, sort_keys=True))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--kind', choices=('inherited', 'abc', 'both'), default='both')
    parser.add_argument('--source-root', type=Path, default=HERE)
    parser.add_argument('--output-root', type=Path, default=HERE)
    args = parser.parse_args()
    for kind in ('inherited', 'abc') if args.kind == 'both' else (args.kind,):
        verify(kind, args.source_root, args.output_root)
