#!/usr/bin/env python3
"""Independent coefficient and explicit-parameter audit for the 276 quartic."""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd
from pathlib import Path
import json

from check_fixed_difference_v18 import (PARAMETER, canonical, decode, linear,
                                        product, variable)

HERE = Path(__file__).resolve().parent
PIN = 'bc97c0d10cd270c2bb856857eaaef7836c4a7a9a0cb039d3cd1e664e0e5db19a'
DETECTOR_IDS = [38, 39, 40, 41, 346, 347, 348, 352, 360, 361, 362,
                380, 381, 383, 385, 386, 388, 390, 20000]+list(range(22000, 22016))


def verify(source_root=HERE, output_root=HERE):
    source_raw = (source_root/'family238_v18/quadratic-family238-v18.json').read_bytes()
    assert sha256(source_raw).hexdigest() == PIN
    old = json.loads(source_raw)
    old_ids = {c['id']: c['sourceId'] for c in old['coordinates']}
    root = output_root/'family276_v19'
    system_raw = (root/'quadratic-family276-v19.json').read_bytes()
    polynomial_raw = (root/'polynomial-family276-v19.json').read_bytes()
    system, polynomial = json.loads(system_raw), json.loads(polynomial_raw)
    report = json.loads((root/'construction-report276-v19.json').read_text())
    ids = {c['id']: c['sourceId'] for c in system['coordinates']}
    assert list(ids) == list(range(1, 277))
    assert list(ids.values())[:238] == list(old_ids.values())
    assert list(ids.values())[238:] == [49001, 49002, 49000]+list(range(50000, 50035))
    assert system['variables'] == polynomial['variables'] == report['variables'] == 276
    assert system['coordinates'] == polynomial['coordinates']
    expected_parameter = dict(old['fixedParameter'],
        N='Every integer N>=7745; this effective sufficient threshold uses the abscissa-sum height theorem.')
    assert system['fixedParameter'] == polynomial['fixedParameter'] == expected_parameter
    replacement = canonical(linear((1, product(variable(37), variable(49001))),
                                   (-1, variable(391))))
    original_rows = [canonical(decode(row, old_ids)) for row in old['residuals']]
    expected = [replacement if row['sourceId'] == 345 else p
                for row, p in zip(old['residuals'], original_rows)]
    real_sum = linear((1, variable(82)), (1, variable(84)),
                      (2, variable(86)), (1, variable(88)))
    imaginary_sum = linear(*((2, variable(x)) for x in (83, 85, 87, 89)))
    # These factors account independently for the source's half-component conventions.
    source_rows = {r['sourceId']: p for r, p in zip(old['residuals'], original_rows)}
    for h, sid, multiplier in ((1, 82, 1), (5, 84, 1), (9, 86, 2), (13, 88, 1)):
        square_real = linear((1, product(variable(h), variable(h))),
                             (2, product(variable(h+1), variable(h+1))),
                             (-multiplier, variable(sid)))
        assert canonical(square_real) == source_rows[2*(h-1)]
    sum_both = linear((1, real_sum), (1, imaginary_sum))
    expected += [
        canonical(linear((1, product(real_sum, real_sum)), (-1, variable(49001)))),
        canonical(linear((1, product(sum_both, sum_both)), (-1, variable(49002)))),
        canonical(linear((1, product(variable(49002), variable(37))), (-1, variable(49000)))),
    ]
    substitution = dict(zip(DETECTOR_IDS, range(50000, 50035)))
    substitution[37] = 49000
    detector_set = set(DETECTOR_IDS)
    copied_rows = []
    for row, p in zip(old['residuals'], original_rows):
        if any(detector_set.intersection(m) for m in p):
            expected.append({tuple(sorted(substitution.get(x, x) for x in m)): c for m, c in p.items()})
            copied_rows.append(row['sourceId'])
    assert len(copied_rows) == 33 and copied_rows == report['copiedSourceRows']
    actual = [decode(row, ids) for row in system['residuals']]
    assert len(actual) == 248 and actual == expected
    assert all(max(sum(x != PARAMETER for x in m) for m in p) <= 2 for p in actual)
    expanded = linear(*((1, product(p, p)) for p in actual))
    assert expanded == decode(polynomial, ids)
    assert gcd(*(int(c) for c in expanded.values())) == 1
    assert max(sum(x != PARAMETER for x in m) for m in expanded) == 4
    assert {x for m in expanded for x in m if x != PARAMETER} == set(ids.values())
    profiles = defaultdict(dict)
    for m, c in expanded.items():
        profiles[tuple(x for x in m if x != PARAMETER)][m.count(PARAMETER)] = int(c)
    assert len(profiles) == 3594 == report['ordinaryMonomialsForEveryPositiveParameter']
    assert len(expanded) == 3595 == report['symbolicTerms']
    assert profiles[(489, 489)] == {0: 1, 2: 1}
    assert all(set(p) in ({0}, {1}, {0, 2}) for p in profiles.values())
    C = max(abs(p[0]) for p in profiles.values() if set(p) == {0})
    linear_maximum = max(abs(p[1]) for p in profiles.values() if set(p) == {1})
    assert str(C) == report['constantCoefficientMaximum'] and C.bit_length() == 1520
    assert linear_maximum == report['linearCoefficientMultiplierMaximum']
    assert C > linear_maximum**2 and 149**214+1 > C > 149**210+1
    N, H, H2 = 7745, 1 << 221234, 1 << 221284
    depth = 19*(2*N-1)//8+1
    minimum_c = 149**depth
    assert depth == 36787
    assert 2029147 < 2**21 and (1 << 221283)+2 < H2
    assert 14**7*5**24 < 12**24
    assert (minimum_c-1)**5 > (12*H2)**6
    assert minimum_c > 40*H and minimum_c > 40*265546
    assert minimum_c > 8
    previous_c = 149**(19*(2*(N-1)-1)//8+1)
    assert (previous_c-1)**5 <= (12*H2)**6
    assert 149**3 > 10*(1+149**2)
    assert 25*(10+9792) < 17*10**5
    height = 149**30982+1
    assert height.bit_length() == 223665 == report['specifiedCoefficientHeightBinaryDigits']
    certificate = {
        'status': 'PASS', 'variables': 276, 'quadraticRows': 248, 'degree': 4,
        'content': 1, 'ordinaryMonomialsForEveryPositiveParameter': 3594,
        'symbolicTerms': 3595, 'sourceSha256': PIN,
        'systemSha256': sha256(system_raw).hexdigest(),
        'polynomialSha256': sha256(polynomial_raw).hexdigest(),
        'unchangedSourceRowsComparedExactly': 211, 'changedSourceRowsReconstructed': 1,
        'newScaleAndArgumentRowsReconstructed': 3, 'duplicatedLocalRowsComparedExactly': 33,
        'sourceRealComponentConventionsChecked': True,
        'heightFormula': 'max(C,A^2+1); 149^(4*N+2)+1 for N>=53',
        'definingThresholdN': N, 'forcedIndexDepth': depth,
        'specifiedParameter': '149^15491', 'specifiedCoefficientHeight': '149^30982+1',
        'specifiedCoefficientHeightBinaryDigits': 223665,
        'integerThresholdChecks': {'lucasResidual': True, 'scalarHeight': True,
                                  'inputHeightAdditiveTerm': True, 'realCompleteness': True,
                                  'previousNDoesNotMeetThisSufficientCriterion': True},
        'arithmeticScope': 'Exact reconstruction and integer inequalities are certified. The defining theorem additionally uses the inherited elliptic, pole, and simultaneous-prime inputs, the effective abscissa sum-height theorem, and the proved modular contact-height bound with constant2^221234 and exponent7/3.',
    }
    (root/'independent-verification276-v19.json').write_text(json.dumps(certificate, indent=2)+'\n')
    print(json.dumps(certificate, sort_keys=True))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', type=Path, default=HERE)
    parser.add_argument('--output-root', type=Path, default=HERE)
    args = parser.parse_args()
    verify(args.source_root, args.output_root)
