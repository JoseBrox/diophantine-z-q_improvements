#!/usr/bin/env python3
"""An exact inverse-weight contact and product normalization for abc89."""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd, isqrt
from pathlib import Path
import json

from build_quartic273 import add, scale, mul, primitive, terms, v, one

HERE = Path(__file__).resolve().parent
SOURCE = 'family_abc91_v19/quadratic-family-abc91-v19.json'
PIN = 'bbf424ee41a12729b2292812c118f7cc2a1a279762bc7232954a2ae477f869ab'


def build(source_root=HERE, output_root=HERE):
    raw = (source_root/SOURCE).read_bytes()
    assert sha256(raw).hexdigest() == PIN
    source = json.loads(raw)
    old_ids = {c['id']: c['sourceId'] for c in source['coordinates']}
    removed = {30010, 30032}
    coordinates = [dict(c) for c in source['coordinates'] if c['sourceId'] not in removed]
    changes, removed_rows, renamed = {}, set(), {}
    for j, q in enumerate((30010, 30032)):
        r, u, output, s2, s4, s3 = q-1, q+1, q+2, q+3, q+4, 51000+j
        prefix = f'detector{j}.'
        argument = 37 if j == 0 else 30030
        changes[prefix+'deltaSquared.definition'] = (prefix+'shiftedContactSquare.definition',
            add(mul(v(argument), v(argument)), scale(v(argument), -2), scale(v(r), -1)))
        changes[prefix+'firstContactProduct.definition'] = (prefix+'contactFourthPower.definition',
            add(mul(v(r), v(r)), scale(v(r), 2), scale(v(u), -1)))
        changes[prefix+'inverseContact.definition'] = (prefix+'contactQuotient.definition',
            add(mul(add(v(u), scale(v(r), -30), scale(v(output), -1)), v(s2)),
                scale(mul(add(v(r), one), v(s3)), -1)))
        changes[prefix+'weight.definition'] = (prefix+'contactNormalization',
            add(mul(v(u), v(output)), v(output), scale(v(u), 244), scale(v(r), -820)))
        changes[prefix+'inverseWeightCubed.definition'] = (prefix+'inverseWeightRelation',
            add(mul(v(s3), v(s3)), scale(mul(v(s2), v(s4)), -1)))
        removed_rows.add(prefix+'inverseWeightSquared.definition')
        renamed[r] = prefix+'contactShiftedSquare'
        renamed[u] = prefix+'contactShiftedFourthPower'
        renamed[output] = prefix+'contactShiftedQuadraticOutput'
        for k in range(4):
            renamed[q+5+k] = prefix+f'scaledFactor{k//2}.{k%2}'
        for k in range(2):
            renamed[q+9+k] = prefix+f'normalizedProduct.{k}'
        renamed[q+11] = prefix+'normalizedReciprocalTrace'
    for i, coordinate in enumerate(coordinates):
        coordinate['id'] = i+1
        coordinate['name'] = renamed.get(coordinate['sourceId'], coordinate['name'])
    identifiers = {c['sourceId']: c['id'] for c in coordinates}
    assert len(coordinates) == 89
    rows, changed, deleted = [], [], []
    expanded = defaultdict(int)
    for row in source['residuals']:
        name = row['name']
        if name in removed_rows:
            deleted.append(name)
            continue
        p = {(t['parameterPower'], tuple(sorted(old_ids[x] for x in t['monomial']))):
             Q(t['coefficient']) for t in row['terms']}
        old_name = name
        if name in changes:
            name, p = changes.pop(name)
        else:
            for j, q in enumerate((30010, 30032)):
                prefix = f'detector{j}.'
                r, old_k, s4, s3 = q-1, q+2, q+4, 51000+j
                if name.startswith(prefix+'factor'):
                    factor_ids = set(range(q+5, q+9))
                    result = {}
                    for (a, m), c in p.items():
                        if s4 in m and set(m).intersection(factor_ids):
                            m = tuple(sorted(s3 if x == s4 else x for x in m))
                        result[a, m] = result.get((a, m), Q(0))+c
                    p = result
                    name = name.replace('.reciprocal.definition', '.scaled.definition')
                elif name.startswith(prefix+'product.'):
                    output_ids = {q+9, q+10}
                    result = {}
                    for (a, m), c in p.items():
                        assert a == 0
                        term = (mul(add(one, v(r)), v(m[0]))
                                if len(m) == 1 and m[0] in output_ids else {(a, m): Q(1)})
                        result = add(result, scale(term, c))
                    p = result
                    name = name.replace('.definition', '.normalized.definition')
                elif name == prefix+'poleInput.definition':
                    p = {(a, tuple(sorted(s3 if x == old_k else x for x in m))): c
                         for (a, m), c in p.items()}
                    name = prefix+'poleInput.normalized.definition'
        if name != old_name:
            changed.append({'sourceId': row['sourceId'], 'oldName': old_name, 'newName': name})
        assert not any(removed.intersection(m) for _, m in p)
        p = primitive(p)
        assert max(len(m) for _, m in p) <= 2
        p = {(a, tuple(sorted(identifiers[x] for x in m))): c for (a, m), c in p.items()}
        rows.append(dict(row, id=len(rows)+1, name=name, terms=terms(p)))
        for (a, m), c in p.items():
            for (b, n), d in p.items():
                expanded[a+b, tuple(sorted(m+n))] += c*d
    assert not changes and len(deleted) == 2 and len(rows) == 77
    assert len(changed) == 24
    expanded = {m: c for m, c in expanded.items() if c}
    profiles = defaultdict(dict)
    for (a, m), c in expanded.items():
        profiles[m][a] = c
    assert gcd(*expanded.values()) == 1 and max(len(m) for _, m in expanded) == 4
    assert {x for _, m in expanded for x in m} == set(range(1, 90))
    assert all(set(p) in ({0}, {1}, {0, 2}) for p in profiles.values())
    assert profiles[()][2] == 1
    C = max(abs(p[0]) for p in profiles.values() if set(p) == {0})
    offset = profiles[()][0]
    threshold = max(3, isqrt(max(0, C-offset)))
    threshold += threshold % 2 == 0
    if threshold**2+offset < C:
        threshold += 2
    system = dict(source, format='integer-quadratic-family-abc-inverse-contact-v21', variables=89,
                  source={'construction': SOURCE, 'sha256': PIN}, coordinates=coordinates, residuals=rows)
    polynomial = dict(format='integer-quartic-family-abc-inverse-contact-v21', variables=89, degree=4,
                      inputCoordinate=1, fixedParameter=source['fixedParameter'],
                      coordinates=coordinates, terms=terms(expanded))
    report = {
        'status': 'Exact rational projection onto all unchanged elliptic and pole coordinates; original pole inputs are preserved.',
        'variables': 89, 'quadraticResiduals': 77, 'degree': 4, 'content': 1,
        'ordinaryMonomialsForEveryPositiveParameter': len(profiles), 'symbolicTerms': len(expanded),
        'sourceSha256': PIN, 'removedSourceCoordinates': sorted(removed),
        'removedSourceRows': deleted, 'changedRows': changed,
        'contactOutputsPerDetector': 3, 'inverseWeightCoordinatesPerDetector': 3,
        'contactPolynomialCoefficientsAscending': [576, -820, 273, -30, 1],
        'affineContactCoordinates': ['R=r-1', 'U=r^2-1', 'V=v+29'],
        'factorScaling': 'A_i=t*T_i, t=s3/s2=1/q',
        'productScaling': 'Wnew=t^2*Wold/r', 'traceScaling': 'tauOld=r*tauNew/t^2',
        'poleIdentity': 's3*b=tauNew^2 is equivalent to k*b=tauOld^2, k=r^2/t',
        'zeroWeightStratum': 'Impossible: both numerator reciprocal squares vanish, contradicting the exact pair chart.',
        'zeroContactStratum': 'Impossible: r=R+1=0 gives R=U=-1, and the final contact row becomes 576=0.',
        'constantCoefficientMaximum': str(C), 'constantCoefficientMaximumBits': C.bit_length(),
        'constantCoefficientWithoutParameter': str(offset),
        'coefficientHeightForEveryIntegerBAtLeast3': f'max({C},B^2+{offset})',
        'coefficientHeightThresholdOddB': threshold,
        'fixture': {'B': 3, 'definesIntegersCertified': False},
        'comparisonPrecision': 1, 'inputPrecision': 1,
        'arithmeticScope': 'Ordinary rational abc and the retained elliptic, pole, height, and simultaneous-prime inputs; sufficient odd B remains ineffective.',
    }
    folder = output_root/'family_abc89_v21'
    folder.mkdir(parents=True, exist_ok=True)
    for name, data in [('quadratic-family-abc89-v21.json', system),
                       ('polynomial-family-abc89-v21.json', polynomial),
                       ('construction-report-abc89-v21.json', report)]:
        (folder/name).write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ('variables', 'quadraticResiduals', 'degree',
                                           'ordinaryMonomialsForEveryPositiveParameter', 'symbolicTerms',
                                           'coefficientHeightForEveryIntegerBAtLeast3',
                                           'coefficientHeightThresholdOddB')}))


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--source-root', type=Path, default=HERE)
    p.add_argument('--output-root', type=Path, default=HERE)
    a = p.parse_args()
    build(a.source_root, a.output_root)
