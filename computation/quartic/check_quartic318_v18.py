#!/usr/bin/env python3
"""Independent reconstruction of the explicit 318-variable quartic.

Only standard-library algebra from an independent checker is shared;
no producer is imported. Every modified and retained row is checked.
"""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd
from pathlib import Path
import json

from check_fixed_difference_v18 import (PARAMETER, canonical, decode, determinant,
    expected_common_rows, field_constant, field_mul, field_sum, linear,
    product, scalar, variable)

HERE = Path(__file__).resolve().parent
PIN = '93f4aaac68efaba7654f3682d404e38c913dc05bd273d1e5f0e3c6cdd744ecde'


def verify(source_root=HERE, output_root=HERE):
    source_raw = (source_root/'family322/quadratic-family322.json').read_bytes()
    assert sha256(source_raw).hexdigest() == PIN
    old = json.loads(source_raw)
    root = output_root/'family318_v18'
    system_raw = (root/'quadratic-family318-v18.json').read_bytes()
    polynomial_raw = (root/'polynomial-family318-v18.json').read_bytes()
    system, polynomial = json.loads(system_raw), json.loads(polynomial_raw)
    report = json.loads((root/'construction-report318-v18.json').read_text())
    old_ids = {c['id']: c['sourceId'] for c in old['coordinates']}
    ids = {c['id']: c['sourceId'] for c in system['coordinates']}
    assert list(ids) == list(range(1, 319))
    assert set(ids.values()) == set(old_ids.values())-{188, 189, 700, 701}
    assert system['variables'] == polynomial['variables'] == report['variables'] == 318
    assert system['fixedParameter'] == polynomial['fixedParameter'] == old['fixedParameter']
    assert system['coordinates'] == polynomial['coordinates']
    replacements = dict(zip((34, 35, 92, 93, 112, 113),
                            expected_common_rows(report['rationalComponentRowBasis'])))
    d = field_constant(11, -6)
    square = (variable(190), linear((2, variable(191))))
    w = field_mul(d, square)
    w_square = linear((193, variable(192))), linear((-132, variable(193)))
    taylor = field_sum((1, field_constant(1)), (Q(-2, 5), w), (Q(-2, 15), w_square))
    approximations = [taylor]+[(variable(192+12*i), variable(193+12*i)) for i in range(1, 4)]
    A0, T = (variable(186), variable(187)), (variable(90), variable(91))
    old_rows = {row['sourceId']: decode(row, old_ids) for row in old['residuals']}
    # Check that the independently formed factors are exactly those used by
    # the source logarithm equations, including its scaled square coordinates.
    for i, ai in enumerate(approximations):
        z = variable(164+4*i), variable(165+4*i)
        q = variable(110+8*i), variable(111+8*i)
        k = variable(114+8*i), variable(115+8*i)
        lp = variable(234+4*i), variable(235+4*i)
        old_log = field_sum((1, field_mul(z, ai)),
                           (-1, field_mul((variable(188), variable(189)), lp)))
        normalization = field_sum((1, field_mul(A0, z)), (-1, field_mul(q, ai)))
        ratio = field_sum((1, field_mul(lp, k)), (-1, field_mul(z, T)))
        for j in range(2):
            assert canonical(old_log[j]) == old_rows[146+12*i+j]
            replacements[116+4*i+j] = canonical(normalization[j])
            replacements[146+12*i+j] = canonical(ratio[j])
    removed_rows = {140, 141, 661, 662}
    expected, changed, retained = [], [], []
    for row in old['residuals']:
        sid = row['sourceId']
        if sid in removed_rows:
            continue
        if sid in replacements:
            expected.append(replacements[sid])
            changed.append(sid)
        else:
            expected.append(canonical(old_rows[sid]))
            retained.append(sid)
    actual = [decode(row, ids) for row in system['residuals']]
    assert len(actual) == 290 and actual == expected
    assert len(changed) == 22 and len(retained) == 268
    assert all(max(sum(i != PARAMETER for i in m) for m in p) <= 2 for p in actual)
    expanded = linear(*((1, product(row, row)) for row in actual))
    assert expanded == decode(polynomial, ids)
    assert gcd(*(int(c) for c in expanded.values())) == 1
    assert max(sum(i != PARAMETER for i in m) for m in expanded) == 4
    assert {i for m in expanded for i in m if i != PARAMETER} == set(ids.values())
    profiles = defaultdict(dict)
    for m, c in expanded.items():
        profiles[tuple(i for i in m if i != PARAMETER)][m.count(PARAMETER)] = int(c)
    assert len(profiles) == 5060 == report['ordinaryMonomialsForEveryPositiveParameter']
    assert len(expanded) == 5061 == report['symbolicTerms']
    assert all(set(p) in ({0}, {1}, {0, 2}) for p in profiles.values())
    assert profiles[(489, 489)] == {0: 1, 2: 1}
    C = max(abs(p[0]) for p in profiles.values() if set(p) == {0})
    L = max(abs(p[1]) for p in profiles.values() if set(p) == {1})
    assert str(C) == report['constantCoefficientMaximum'] and C.bit_length() == 1520
    assert L == 2*80989**2 == report['linearCoefficientMultiplierMaximum']
    assert C > L*L and 80989**94+1 > C > 80989**90+1
    assert report['exactHeightThresholdN'] == 23
    assert report['definingThresholdN'] == 27464
    denominator = [Q(1), Q(-1526, 1073), Q(513, 1073)]
    numerator = [Q(1), Q(-9776, 5365), Q(2941, 3219), Q(-1024, 13949),
                 Q(-1920, 237133), Q(-1024, 711399), Q(-1408, 5928325),
                 Q(0), Q(2432, 103152855)]
    residue_checks = []
    for name, coefficients, prime in [('denominator', denominator, 7),
                                       ('numerator', numerator, 71)]:
        assert pow(2, (prime-1)//2, prime) == 1
        reductions = [c.numerator*pow(c.denominator, -1, prime) % prime for c in coefficients]
        assert reductions[-1]
        roots = [x for x in range(prime)
                 if sum(c*pow(x, i, prime) for i, c in enumerate(reductions)) % prime == 0]
        assert not roots
        residue_checks.append({'polynomial': name, 'prime': prime, 'roots': roots,
                               'reducedCoefficients': reductions})
    series = [Q(1), Q(-2, 5)]
    for j in range(2, 10):
        series.append(Q(4*j-5, 4*j+1)*series[-1])
    error = [sum(denominator[k]*series[j-k] for k in range(3) if 0 <= j-k < 10)
             -(numerator[j] if j < len(numerator) else 0) for j in range(12)]
    assert error[:10] == [0]*10
    assert error[10:] == [Q(2970726, 254443709), Q(-41697666, 6361092725)]
    certificate = {
        'status': 'PASS', 'variables': 318, 'quadraticRows': 290, 'degree': 4,
        'content': 1, 'ordinaryMonomialsForEveryPositiveParameter': 5060,
        'symbolicTerms': 5061, 'exactHeight': '80989^(4*N+2)+1 for N>=23',
        'specifiedCoefficientHeight': '80989^109858+1',
        'sourceSha256': PIN, 'systemSha256': sha256(system_raw).hexdigest(),
        'polynomialSha256': sha256(polynomial_raw).hexdigest(),
        'independentlyReconstructedChangedRows': 22, 'unchangedRowsComparedExactly': 268,
        'rationalRowBasisDeterminant': str(determinant(report['rationalComponentRowBasis'])),
        'logarithmApproximationResidueChecks': residue_checks,
        'logarithmApproximationError': '2970726*w^10/254443709-41697666*w^11/6361092725',
        'arithmeticScope': 'The finite check proves the specified algebraic reconstruction and coefficient claims. The chart is covered by the independent general identity certificate. The defining threshold and exclusion of the T=0 stratum use the unchanged arithmetic argument in the explicit quartic paper; they are not consequences of coefficient expansion.',
    }
    (root/'independent-verification318-v18.json').write_text(json.dumps(certificate, indent=2)+'\n')
    print(json.dumps(certificate, sort_keys=True))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', type=Path, default=HERE)
    parser.add_argument('--output-root', type=Path, default=HERE)
    args = parser.parse_args()
    verify(args.source_root, args.output_root)
