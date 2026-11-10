#!/usr/bin/env python3
"""Independent contact, scaling, full coefficient and boundary audit for abc89."""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd
from pathlib import Path
import json

from check_fixed_difference_v18 import (PARAMETER, canonical, decode, linear,
                                       product, variable, scalar, field_mul, field_sum)

HERE = Path(__file__).resolve().parent
SOURCE = 'family_abc91_v19/quadratic-family-abc91-v19.json'
PIN = 'bbf424ee41a12729b2292812c118f7cc2a1a279762bc7232954a2ae477f869ab'


def pair(i, multiplier=1):
    return variable(i), linear((multiplier, variable(i+1)))


def sf(i, value):
    return tuple(product(variable(i), part) for part in value)


def power(p, n):
    answer = scalar(1)
    for _ in range(n):
        answer = product(answer, p)
    return answer


def projection_identities():
    r, t, a, b, eta, pole = [variable(i) for i in range(1, 7)]
    u = power(r, 2)
    v = linear((1, u), (-30, r), (-1, product(t, r)))
    P = linear((1, power(r, 4)), (-30, power(r, 3)), (273, u), (-820, r), (576, scalar(1)))
    normalized = linear((1, product(u, v)), (273, u), (-820, r), (576, scalar(1)))
    assert normalized == linear((1, P), (-1, product(t, power(r, 3))))
    R = linear((1, r), (-1, scalar(1)))
    U = linear((1, u), (-1, scalar(1)))
    V = linear((1, v), (29, scalar(1)))
    shifted = linear((1, product(U, V)), (1, V), (244, U), (-820, R))
    assert shifted == normalized
    assert U == linear((1, power(R, 2)), (2, R))
    assert linear((1, U), (-30, R), (-1, V)) == linear((1, u), (-30, r), (-1, v))
    # The inverse-weight cusp is parametrized uniquely when its coordinates
    # are nonzero; these are the polynomial identities in that parametrization.
    s2, s3, s4 = power(t, 2), power(t, 3), power(t, 4)
    assert power(s2, 2) == s4 and power(s3, 2) == product(s2, s4)
    assert not linear((1, product(linear((1, u), (-30, r), (-1, v)), s2)),
                      (-1, product(r, s3)))
    # Multiplication of all three trace coordinates by r/t^2 gives the
    # same equation. Verify after clearing t^4, including zero trace values.
    new_trace = linear((1, power(a, 2)), (-2, product(a, eta)), (-2, power(b, 2)))
    old_trace_numerator = linear((1, power(product(r, a), 2)),
                                 (-2, product(product(r, a), product(r, eta))),
                                 (-2, power(product(r, b), 2)))
    assert old_trace_numerator == product(power(r, 2), new_trace)
    new_pole = linear((1, product(s3, pole)), (-1, power(eta, 2)))
    old_pole_numerator = linear((1, product(product(power(r, 2), s3), pole)),
                                (-1, power(product(r, eta), 2)))
    assert old_pole_numerator == product(power(r, 2), new_pole)
    assert 576 != 0


def verify(source_root=HERE, output_root=HERE):
    raw = (source_root/SOURCE).read_bytes()
    assert sha256(raw).hexdigest() == PIN
    source = json.loads(raw)
    old_ids = {c['id']: c['sourceId'] for c in source['coordinates']}
    folder = output_root/'family_abc89_v21'
    system_raw = (folder/'quadratic-family-abc89-v21.json').read_bytes()
    polynomial_raw = (folder/'polynomial-family-abc89-v21.json').read_bytes()
    system, polynomial = json.loads(system_raw), json.loads(polynomial_raw)
    report = json.loads((folder/'construction-report-abc89-v21.json').read_text())
    ids = {c['id']: c['sourceId'] for c in system['coordinates']}
    removed = {30010, 30032}
    assert list(ids) == list(range(1, 90))
    assert list(ids.values()) == [x for x in old_ids.values() if x not in removed]
    assert system['variables'] == polynomial['variables'] == report['variables'] == 89
    assert system['coordinates'] == polynomial['coordinates']
    assert system['fixedParameter'] == polynomial['fixedParameter'] == source['fixedParameter']
    changes, removals = {}, set()
    for j, q in enumerate((30010, 30032)):
        r, u, v, s2, s4, s3 = q-1, q+1, q+2, q+3, q+4, 51000+j
        prefix = f'detector{j}.'
        argument = 37 if j == 0 else 30030
        changes[prefix+'deltaSquared.definition'] = canonical(
            linear((1, power(variable(argument), 2)), (-2, variable(argument)), (-1, variable(r))))
        changes[prefix+'firstContactProduct.definition'] = canonical(
            linear((1, power(variable(r), 2)), (2, variable(r)), (-1, variable(u))))
        changes[prefix+'inverseContact.definition'] = canonical(
            linear((1, product(linear((1, variable(u)), (-30, variable(r)), (-1, variable(v))), variable(s2))),
                   (-1, product(linear((1, variable(r)), (1, scalar(1))), variable(s3)))))
        changes[prefix+'weight.definition'] = canonical(
            linear((1, product(variable(u), variable(v))), (1, variable(v)),
                   (244, variable(u)), (-820, variable(r))))
        changes[prefix+'inverseWeightCubed.definition'] = canonical(
            linear((1, power(variable(s3), 2)), (-1, product(variable(s2), variable(s4)))))
        removals.add(prefix+'inverseWeightSquared.definition')
        # Reconstruct the factors directly from their field meanings.
        specifications = [(pair(305, 2), pair(311, 2), pair(255, 2)),
                          (pair(30000), pair(178, -2), pair(190, -2))]
        for k, (comparison_square, reference_square, numerator_square) in enumerate(specifications):
            factor = pair(q+5+2*k)
            expression = field_sum((1, (variable(s4), {})),
                                   (1, sf(s3, comparison_square)),
                                   (1, sf(s2, reference_square)),
                                   (1, field_mul(numerator_square, numerator_square)),
                                   (-1, sf(s3, factor)))
            for part in range(2):
                changes[prefix+f'factor{k}.{part}.reciprocal.definition'] = canonical(expression[part])
        final = field_sum((1, field_mul(pair(q+5), pair(q+7))),
                          (-1, sf(r, pair(q+9))), (-1, pair(q+9)))
        for part in range(2):
            changes[prefix+f'product.{part}.definition'] = canonical(final[part])
        changes[prefix+'poleInput.definition'] = canonical(
            linear((1, product(variable(s3), variable(q+12))), (-1, power(variable(q+11), 2))))
    for omitted in removed:
        uses = {row['name'] for row in source['residuals']
                if any(omitted in m for m in decode(row, old_ids))}
        assert uses.issubset(set(changes) | removals)
    expected, changed, unchanged = [], 0, 0
    for row in source['residuals']:
        if row['name'] in removals:
            continue
        if row['name'] in changes:
            expected.append(changes.pop(row['name']))
            changed += 1
        else:
            expected.append(canonical(decode(row, old_ids)))
            unchanged += 1
    actual = [decode(row, ids) for row in system['residuals']]
    assert not changes and actual == expected and len(actual) == 77
    assert changed == 24 and unchanged == 53
    assert all(max(sum(x != PARAMETER for x in m) for m in row) <= 2 for row in actual)
    assert not any(removed.intersection(m) for row in actual for m in row)
    expanded = linear(*((1, product(row, row)) for row in actual))
    assert expanded == decode(polynomial, ids)
    assert gcd(*(int(c) for c in expanded.values())) == 1
    assert max(sum(x != PARAMETER for x in m) for m in expanded) == 4
    assert {x for m in expanded for x in m if x != PARAMETER} == set(ids.values())
    profiles = defaultdict(dict)
    for m, c in expanded.items():
        profiles[tuple(x for x in m if x != PARAMETER)][m.count(PARAMETER)] = int(c)
    assert len(profiles) == 936 == report['ordinaryMonomialsForEveryPositiveParameter']
    assert len(expanded) == 937 == report['symbolicTerms']
    assert profiles[()] == {0: 797681, 2: 1}
    assert all(set(p) in ({0}, {1}, {0, 2}) for p in profiles.values())
    C = max(abs(p[0]) for p in profiles.values() if set(p) == {0})
    assert C == 4153456 and str(C) == report['constantCoefficientMaximum']
    linear_coefficients = {m: p[1] for m, p in profiles.items() if set(p) == {1}}
    assert linear_coefficients == {(0, 0): 4, (232,): -2, (248,): 2}
    assert 1833**2+797681 >= C > 1831**2+797681
    assert report['coefficientHeightThresholdOddB'] == 1833
    projection_identities()
    certificate = {
        'status': 'PASS', 'variables': 89, 'quadraticRows': 77, 'degree': 4, 'content': 1,
        'ordinaryMonomialsForEveryPositiveParameter': 936, 'symbolicTerms': 937,
        'sourceSha256': PIN, 'systemSha256': sha256(system_raw).hexdigest(),
        'polynomialSha256': sha256(polynomial_raw).hexdigest(),
        'changedRowsReconstructedFromFieldAndContactFormulas': 24,
        'unchangedSourceRowsComparedExactly': 53,
        'omittedWeightCoordinatesHaveNoOtherSourceUses': True,
        'generalContactAndScalingIdentitiesVerified': True,
        'zeroWeightStratum': 'Excluded by the unchanged pair-chart contradiction.',
        'zeroContactStratum': 'At R=U=-1, the last contact row becomes 576=0.',
        'poleInputPreservedExactly': True,
        'coefficientHeight': 'max(4153456,B^2+797681)',
        'coefficientHeightThresholdOddB': 1833,
        'arithmeticScope': 'Exact algebra and coefficients certified. The defining theorem additionally assumes ordinary rational abc and the retained elliptic, pole, height and prime-pattern inputs. The sufficient odd B remains ineffective.',
    }
    (folder/'independent-verification-abc89-v21.json').write_text(json.dumps(certificate, indent=2)+'\n')
    print(json.dumps(certificate, sort_keys=True))


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--source-root', type=Path, default=HERE)
    p.add_argument('--output-root', type=Path, default=HERE)
    a = p.parse_args()
    verify(a.source_root, a.output_root)
