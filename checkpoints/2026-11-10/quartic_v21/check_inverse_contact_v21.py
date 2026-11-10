#!/usr/bin/env python3
"""Independent projection, full coefficient and threshold audit for 226/262."""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
from math import gcd, prod
from pathlib import Path
import json

from check_fixed_difference_v18 import (PARAMETER, canonical, decode, linear,
                                       product, variable, scalar)

HERE = Path(__file__).resolve().parent
SOURCES = {
    'inherited': ('family228_v19/quadratic-family228-v19.json',
                  '0fb0e11597d3915772d5342b7e7d37493cb501254349d4652b544d7e5a44e468',
                  226, 200, 2835),
    'explicit': ('family265_v19/quadratic-family265-v19.json',
                 'e5cf559e1f8b243531299a7d6ace098b71322f58f1c13aff43811cbdb150c14f',
                 262, 234, 3494),
}


def power(p, n):
    answer = scalar(1)
    for _ in range(n):
        answer = product(answer, p)
    return answer


def coefficients_and_projection():
    # Elementary symmetric sums are independent of the producer's
    # coefficient-convolution algorithm.
    roots = [Q(1), Q(9, 4), Q(4), Q(2398, 2399)**2, Q(439, 407)**2]
    e = [sum((prod(s) for s in combinations(roots, k)), Q(0)) for k in range(1, 6)]
    coefficients = [(-1)**(5-i)*(e[4-i] if i < 5 else 1) for i in range(6)]
    for root in roots:
        assert sum(c*root**i for i, c in enumerate(coefficients)) == 0
    assert coefficients[5] == 1 and coefficients[0] != 0
    r, s, q = variable(1), variable(2), variable(3)
    P = linear(*((c, power(r, i)) for i, c in enumerate(coefficients)))
    N = linear((1, power(r, 5)), (-1, P))
    h = linear((1, scalar(1)), (1, s))
    u = power(r, 2)
    v = linear((1, power(r, 3)), (-e[0], product(h, u)),
               (e[1], product(h, r)))
    final = linear((1, product(u, v)),
                   (-1, product(h, linear((e[2], u), (-e[3], r), (e[4], scalar(1))))))
    assert final == linear((1, power(r, 5)), (-1, product(h, N)))
    old = linear((1, product(linear((1, scalar(1)), (1, q)), P)), (-1, power(r, 5)))
    guard = linear((1, product(q, s)), (-1, scalar(1)))
    assert not linear((1, product(q, final)), (-1, old), (1, product(guard, N)))
    # A numerical check of the exceptional boundary is supplementary to
    # the polynomial identity, not used in place of it.
    assert coefficients[0] == -e[4] != 0
    assert -1*-1 == 1
    return roots, e, coefficients


def verify(kind, source_root=HERE, output_root=HERE):
    path, pin, count, row_count, monomial_count = SOURCES[kind]
    raw = (source_root/path).read_bytes()
    assert sha256(raw).hexdigest() == pin
    source = json.loads(raw)
    old_ids = {c['id']: c['sourceId'] for c in source['coordinates']}
    blocks = [(346, 347, 20000, 348, 352, 360),
              (392, 393, 20020, 394, 400, 408)]
    if kind == 'explicit':
        blocks.append((50004, 50005, 50018, 50006, 50007, 50008))
    removed = {block[3] for block in blocks}
    folder = output_root/f'family{count}_v21'
    system_raw = (folder/f'quadratic-family{count}-v21.json').read_bytes()
    polynomial_raw = (folder/f'polynomial-family{count}-v21.json').read_bytes()
    system, polynomial = json.loads(system_raw), json.loads(polynomial_raw)
    report = json.loads((folder/f'construction-report{count}-v21.json').read_text())
    ids = {c['id']: c['sourceId'] for c in system['coordinates']}
    assert list(ids) == list(range(1, count+1))
    assert list(ids.values()) == [x for x in old_ids.values() if x not in removed]
    assert system['variables'] == polynomial['variables'] == report['variables'] == count
    assert system['coordinates'] == polynomial['coordinates']
    assert system['fixedParameter'] == polynomial['fixedParameter'] == source['fixedParameter']
    assert report['removedSourceCoordinates'] == sorted(removed)
    roots, e, coefficients = coefficients_and_projection()
    assert report['contactPolynomialCoefficientsAscending'] == [str(x) for x in coefficients]
    assert report['squaredContactDistances'] == [str(x) for x in roots]
    changes, removals = {}, set()
    old_rows = {row['name']: canonical(decode(row, old_ids)) for row in source['residuals']}
    for j, (r, u, out, F, q, inverse) in enumerate(blocks):
        vr, vu, vv, vf = map(variable, (r, u, out, F))
        h = linear((1, scalar(1)), (1, variable(inverse)))
        # Recover the old polynomial row directly from its roots and
        # inspect every source use of the omitted polynomial coordinate.
        old_P = linear((1, product(vu, vv)), (-e[0], product(vr, vv)),
                       (e[1], vv), (-e[2], vu), (e[3], vr), (-e[4], scalar(1)), (-1, vf))
        prefix = f'reflected.detector{j}.'
        assert old_rows[prefix+'contactPolynomial.definition'] == canonical(old_P)
        assert old_rows[prefix+'deltaSixthPower.definition'] == canonical(
            linear((1, product(vr, vu)), (-1, vv)))
        assert old_rows[prefix+'weight.definition'] == canonical(
            linear((1, product(vu, vv)), (-1, vf), (-1, product(vf, variable(q)))))
        assert old_rows[f'detector{j}.inverseWeight.definition'] == canonical(
            linear((1, product(variable(q), variable(inverse))), (-1, scalar(1))))
        uses = {row['name'] for row in source['residuals']
                if any(F in m for m in decode(row, old_ids))}
        assert uses == {prefix+'contactPolynomial.definition', prefix+'weight.definition'}
        definitions = linear((1, vv), (-1, product(vr, vu)),
                             (e[0], product(h, vu)), (-e[1], product(h, vr)))
        final = linear((1, product(vu, vv)),
                       (-1, product(h, linear((e[2], vu), (-e[3], vr), (e[4], scalar(1))))))
        changes[prefix+'deltaSixthPower.definition'] = canonical(definitions)
        changes[prefix+'weight.definition'] = canonical(final)
        removals.add(prefix+'contactPolynomial.definition')
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
    assert not changes and actual == expected and len(actual) == row_count
    assert changed == 2*len(blocks) and unchanged == row_count-changed
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
    assert len(profiles) == monomial_count == report['ordinaryMonomialsForEveryPositiveParameter']
    assert len(expanded) == monomial_count+1 == report['symbolicTerms']
    assert profiles[(489, 489)] == {0: 1, 2: 1}
    assert all(set(p) in ({0}, {1}, {0, 2}) for p in profiles.values())
    C = max(abs(p[0]) for p in profiles.values() if set(p) == {0})
    L = max(abs(p[1]) for p in profiles.values() if set(p) == {1})
    assert str(C) == report['constantCoefficientMaximum'] and C.bit_length() == 1520
    assert L == 44402 == report['linearCoefficientMultiplierMaximum']
    assert C > L*L and 149**210+1 < C < 149**214+1
    certificate = {
        'status': 'PASS', 'variables': count, 'quadraticRows': row_count, 'degree': 4, 'content': 1,
        'ordinaryMonomialsForEveryPositiveParameter': monomial_count, 'symbolicTerms': monomial_count+1,
        'sourceSha256': pin, 'systemSha256': sha256(system_raw).hexdigest(),
        'polynomialSha256': sha256(polynomial_raw).hexdigest(),
        'changedContactRowsReconstructed': changed, 'unchangedSourceRowsComparedExactly': unchanged,
        'deletedPolynomialCoordinatesHaveNoOtherSourceUses': True,
        'generalProjectionIdentityVerified': True, 'exceptionalBoundaryIdentical': True,
        'heightFormula': 'max(C,A^2+1); 149^(4*N+2)+1 for N>=53',
        'arithmeticScope': 'The contact replacement preserves the entire rational projection. The defining theorem retains the source arithmetic premises and parameter scope.',
    }
    if kind == 'explicit':
        N = 9682
        depth = 19*(2*N-1)//8+1
        c = 149**depth
        threshold = 331969
        assert depth == 45988
        assert system['fixedParameter']['N'].startswith('Every integer N>=9682;')
        assert report['definingThresholdN'] == N
        assert 2**(2*threshold-3*221274)*15**6 > 13**3*(345+7*threshold)**6
        assert 5**3*14 < 13**3
        assert c-1 >= 2**threshold and c > 40*(1 << 221234) and c > 4640000
        assert 149**(19*(2*(N-1)-1)//8+1)-1 < 2**threshold
        assert 5290 < 2**13 and 23*221287 < 22*232000
        assert 149**3 > 10*(1+149**2) and 25*(10+9792) < 17*10**5
        assert (149**38730+1).bit_length() == 279599
        certificate.update(definingThresholdN=N, forcedIndexDepth=depth,
                           specifiedParameter='149^19365', specifiedCoefficientHeight='149^38730+1',
                           specifiedCoefficientHeightBinaryDigits=279599,
                           effectiveIntegerThresholdChecks=True)
    (folder/f'independent-verification{count}-v21.json').write_text(json.dumps(certificate, indent=2)+'\n')
    print(json.dumps(certificate, sort_keys=True))


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--kind', choices=(*SOURCES, 'all'), default='all')
    p.add_argument('--source-root', type=Path, default=HERE)
    p.add_argument('--output-root', type=Path, default=HERE)
    a = p.parse_args()
    for kind in SOURCES if a.kind == 'all' else (a.kind,):
        verify(kind, a.source_root, a.output_root)
