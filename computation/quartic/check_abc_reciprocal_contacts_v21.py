#!/usr/bin/env python3
"""Independent reciprocal-contact, field-row and full coefficient audit for abc87."""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd
from pathlib import Path
import json

from check_fixed_difference_v18 import (PARAMETER, canonical, decode, linear,
                                       product, variable, scalar, field_mul, field_sum)

HERE = Path(__file__).resolve().parent
SOURCE = 'family_abc89_v21/quadratic-family-abc89-v21.json'
PIN = '30778238b1409e06e5856400122cdaea302241f9912a888e4b303a5f86e68c6a'


def pair(i, multiplier=1):
    return variable(i), linear((multiplier, variable(i+1)))


def sf(i, value):
    return tuple(product(variable(i), part) for part in value)


def power(p, n):
    answer = scalar(1)
    for _ in range(n):
        answer = product(answer, p)
    return answer


def contact_identities():
    r, z, s, x = [variable(i) for i in range(1, 5)]
    P = scalar(1)
    for root in (1, 4, 9, 36):
        P = product(P, linear((1, r), (-root, scalar(1))))
    assert P == linear((1, power(r, 4)), (-50, power(r, 3)),
                       (553, power(r, 2)), (-1800, r), (1296, scalar(1)))
    first = linear((1, product(r, z)), (-1, power(r, 2)), (-36, scalar(1)))
    quotient = linear((1, power(z, 2)), (-50, z), (481, scalar(1)))
    other = linear((1, product(r, z)), (1, power(r, 2)), (36, scalar(1)), (-50, r))
    assert linear((1, product(power(r, 2), quotient)), (-1, P)) == product(first, other)
    R = linear((1, r), (-1, scalar(1)))
    Z = linear((1, z), (-37, scalar(1)))
    assert first == linear((1, product(R, Z)), (1, Z), (-1, power(R, 2)), (35, R))
    assert linear((1, product(r, s)), (-1, quotient)) == linear(
        (1, product(linear((1, R), (1, scalar(1))), s)), (-1, power(Z, 2)), (-24, Z))
    # Check the contact factorization in the actual detector argument.
    actual_r = power(linear((1, x), (-1, scalar(1))), 2)
    from_r = scalar(1)
    for root in (1, 4, 9, 36):
        from_r = product(from_r, linear((1, actual_r), (-root, scalar(1))))
    contacts = [-5, -2, -1, 0, 2, 3, 4, 7]
    from_contacts = scalar(1)
    for theta in contacts:
        from_contacts = product(from_contacts, linear((1, x), (-theta, scalar(1))))
    assert from_r == from_contacts
    assert len(set(contacts)) == 8 and 0 in contacts and 1 not in contacts
    assert sorted(2-theta for theta in contacts) == contacts
    assert max(abs(a-b) for a in contacts for b in contacts) == 12 < 76176
    assert max(abs(1-a) for a in contacts) == 6 < 76176
    # The allowed squared distances are units at every consumed contact prime.
    assert all(root and (root+Q(36, root)) in (13, 37) for root in (1, 4, 9, 36))
    return contacts


def verify(source_root=HERE, output_root=HERE):
    raw = (source_root/SOURCE).read_bytes()
    assert sha256(raw).hexdigest() == PIN
    source = json.loads(raw)
    old_ids = {c['id']: c['sourceId'] for c in source['coordinates']}
    source_rows = {row['name']: canonical(decode(row, old_ids)) for row in source['residuals']}
    folder = output_root/'family_abc87_v21'
    system_raw = (folder/'quadratic-family-abc87-v21.json').read_bytes()
    polynomial_raw = (folder/'polynomial-family-abc87-v21.json').read_bytes()
    system, polynomial = json.loads(system_raw), json.loads(polynomial_raw)
    report = json.loads((folder/'construction-report-abc87-v21.json').read_text())
    ids = {c['id']: c['sourceId'] for c in system['coordinates']}
    removed = {30012, 30034}
    assert list(ids) == list(range(1, 88))
    assert list(ids.values()) == [x for x in old_ids.values() if x not in removed]
    assert system['variables'] == polynomial['variables'] == report['variables'] == 87
    assert system['coordinates'] == polynomial['coordinates']
    assert system['fixedParameter'] == polynomial['fixedParameter'] == source['fixedParameter']
    changes, removals = {}, set()
    for j, q in enumerate((30010, 30032)):
        R, Z, s2, s, s3 = q-1, q+1, q+3, q+4, 51000+j
        prefix = f'detector{j}.'
        changes[prefix+'contactFourthPower.definition'] = canonical(
            linear((1, product(variable(R), variable(Z))), (1, variable(Z)),
                   (-1, power(variable(R), 2)), (35, variable(R))))
        changes[prefix+'contactQuotient.definition'] = canonical(
            linear((1, product(linear((1, variable(R)), (1, scalar(1))), variable(s))),
                   (-1, power(variable(Z), 2)), (-24, variable(Z))))
        changes[prefix+'inverseWeightRelation'] = canonical(
            linear((1, variable(s3)), (-1, product(variable(s), variable(s2)))))
        changes[prefix+'inverseWeightFourthPower.definition'] = canonical(
            linear((1, variable(s2)), (-1, power(variable(s), 2))))
        removals.add(prefix+'contactNormalization')
        for k, (comparison_square, reference_square, numerator_square) in enumerate([
                (pair(305, 2), pair(311, 2), pair(255, 2)),
                (pair(30000), pair(178, -2), pair(190, -2))]):
            value = field_sum((1, (power(variable(s2), 2), {})),
                              (1, sf(s3, comparison_square)), (1, sf(s2, reference_square)),
                              (1, field_mul(numerator_square, numerator_square)),
                              (-1, sf(s3, pair(q+5+2*k))))
            changes[prefix+f'factor{k}.0.scaled.definition'] = canonical(value[0])
            # The imaginary row has no constant term and is unchanged.
            assert source_rows[prefix+f'factor{k}.1.scaled.definition'] == canonical(value[1])
        # Both normalizations needed by the arithmetic proof remain literal.
        product_rows = field_sum((1, field_mul(pair(q+5), pair(q+7))),
                                 (-1, sf(R, pair(q+9))), (-1, pair(q+9)))
        for part in range(2):
            assert source_rows[prefix+f'product.{part}.normalized.definition'] == canonical(product_rows[part])
        assert source_rows[prefix+'poleInput.normalized.definition'] == canonical(
            linear((1, product(variable(s3), variable(q+12))), (-1, power(variable(q+11), 2))))
    for omitted in removed:
        uses = {row['name'] for row in source['residuals'] if any(omitted in m for m in decode(row, old_ids))}
        assert uses.issubset(set(changes) | removals)
    expected, changed, unchanged = [], 0, 0
    for row in source['residuals']:
        if row['name'] in removals:
            continue
        if row['name'] in changes:
            expected.append(changes.pop(row['name']))
            changed += 1
        else:
            expected.append(source_rows[row['name']])
            unchanged += 1
    actual = [decode(row, ids) for row in system['residuals']]
    assert not changes and actual == expected and len(actual) == 75
    assert changed == 12 and unchanged == 63
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
    assert len(profiles) == 918 == report['ordinaryMonomialsForEveryPositiveParameter']
    assert len(expanded) == 919 == report['symbolicTerms']
    assert profiles[()] == {0: 797681, 2: 1}
    assert all(set(p) in ({0}, {1}, {0, 2}) for p in profiles.values())
    C = max(abs(p[0]) for p in profiles.values() if set(p) == {0})
    assert C == 4153456 and str(C) == report['constantCoefficientMaximum']
    assert {m: p[1] for m, p in profiles.items() if set(p) == {1}} == {
        (0, 0): 4, (232,): -2, (248,): 2}
    assert 1833**2+797681 >= C > 1831**2+797681
    contacts = contact_identities()
    assert report['contacts'] == contacts
    certificate = {
        'status': 'PASS', 'variables': 87, 'quadraticRows': 75, 'degree': 4, 'content': 1,
        'ordinaryMonomialsForEveryPositiveParameter': 918, 'symbolicTerms': 919,
        'sourceSha256': PIN, 'systemSha256': sha256(system_raw).hexdigest(),
        'polynomialSha256': sha256(polynomial_raw).hexdigest(),
        'changedRowsReconstructedFromFieldAndContactFormulas': 12,
        'unchangedSourceRowsComparedExactly': 63,
        'imaginaryFactorAndProductPoleRowsAlsoReconstructed': True,
        'omittedContactOutputsHaveNoOtherSourceUses': True,
        'generalReciprocalContactAndShiftIdentitiesVerified': True,
        'contacts': contacts, 'contactPolynomialDegree': 8,
        'maximumNonzeroContactDifference': 12, 'maximumDistanceFromCenter': 6,
        'zeroWeightStratum': 'Excluded by the unchanged pair-chart contradiction.',
        'zeroContactStratum': 'Excluded by r*(z-r)=36.',
        'coefficientHeight': 'max(4153456,B^2+797681)',
        'coefficientHeightThresholdOddB': 1833,
        'arithmeticScope': 'Exact algebra and coefficients certified for the new contact set. The defining theorem uses ordinary rational abc and the retained elliptic, pole, height and arbitrary-coefficient prime-pattern premises. Its sufficient odd B remains ineffective.',
    }
    (folder/'independent-verification-abc87-v21.json').write_text(json.dumps(certificate, indent=2)+'\n')
    print(json.dumps(certificate, sort_keys=True))


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--source-root', type=Path, default=HERE)
    p.add_argument('--output-root', type=Path, default=HERE)
    a = p.parse_args()
    verify(a.source_root, a.output_root)
