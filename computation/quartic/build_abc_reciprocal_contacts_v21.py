#!/usr/bin/env python3
"""An 87-coordinate abc quartic using eight reciprocal-symmetric contacts."""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd
from pathlib import Path
import json

from build_quartic273 import add, scale, mul, primitive, terms, v, one

HERE = Path(__file__).resolve().parent
SOURCE = 'family_abc89_v21/quadratic-family-abc89-v21.json'
PIN = '30778238b1409e06e5856400122cdaea302241f9912a888e4b303a5f86e68c6a'


def build(source_root=HERE, output_root=HERE):
    raw = (source_root/SOURCE).read_bytes()
    assert sha256(raw).hexdigest() == PIN
    source = json.loads(raw)
    old_ids = {c['id']: c['sourceId'] for c in source['coordinates']}
    removed = {30012, 30034}
    coordinates = [dict(c) for c in source['coordinates'] if c['sourceId'] not in removed]
    changes, removals, renames = {}, set(), {}
    for j, q in enumerate((30010, 30032)):
        R, Z, s2, s, s3 = q-1, q+1, q+3, q+4, 51000+j
        prefix = f'detector{j}.'
        changes[prefix+'contactFourthPower.definition'] = (prefix+'reciprocalContact.definition',
            add(mul(v(R), v(Z)), v(Z), scale(mul(v(R), v(R)), -1), scale(v(R), 35)))
        changes[prefix+'contactQuotient.definition'] = (prefix+'inverseContact.definition',
            add(mul(add(v(R), one), v(s)), scale(mul(v(Z), v(Z)), -1), scale(v(Z), -24)))
        removals.add(prefix+'contactNormalization')
        changes[prefix+'inverseWeightRelation'] = (prefix+'inverseWeightCubed.definition',
            add(v(s3), scale(mul(v(s), v(s2)), -1)))
        changes[prefix+'inverseWeightFourthPower.definition'] = (prefix+'inverseWeightSquared.definition',
            add(v(s2), scale(mul(v(s), v(s)), -1)))
        renames[Z] = prefix+'shiftedReciprocalContactSum'
        renames[s] = prefix+'inverseWeight'
    for i, coordinate in enumerate(coordinates):
        coordinate['id'] = i+1
        coordinate['name'] = renames.get(coordinate['sourceId'], coordinate['name'])
    ids = {c['sourceId']: c['id'] for c in coordinates}
    assert len(coordinates) == 87
    rows, changed, deleted = [], [], []
    expanded = defaultdict(int)
    for row in source['residuals']:
        old_name = row['name']
        if old_name in removals:
            deleted.append(old_name)
            continue
        name = old_name
        p = {(t['parameterPower'], tuple(sorted(old_ids[x] for x in t['monomial']))):
             Q(t['coefficient']) for t in row['terms']}
        if name in changes:
            name, p = changes.pop(name)
        else:
            for j, q in enumerate((30010, 30032)):
                if name.startswith(f'detector{j}.factor'):
                    key = (0, (q+4,))
                    if key in p:
                        coefficient = p.pop(key)
                        p = add(p, scale(mul(v(q+3), v(q+3)), coefficient))
                        name = name.replace('.scaled.definition', '.inverseScaled.definition')
        if name != old_name:
            changed.append({'sourceId': row['sourceId'], 'oldName': old_name, 'newName': name})
        assert not any(removed.intersection(m) for _, m in p)
        p = primitive(p)
        assert max(len(m) for _, m in p) <= 2
        p = {(a, tuple(sorted(ids[x] for x in m))): c for (a, m), c in p.items()}
        rows.append(dict(row, id=len(rows)+1, name=name, terms=terms(p)))
        for (a, m), c in p.items():
            for (b, n), d in p.items():
                expanded[a+b, tuple(sorted(m+n))] += c*d
    assert not changes and len(deleted) == 2 and len(changed) == 12 and len(rows) == 75
    expanded = {m: c for m, c in expanded.items() if c}
    profiles = defaultdict(dict)
    for (a, m), c in expanded.items():
        profiles[m][a] = c
    assert gcd(*expanded.values()) == 1 and max(len(m) for _, m in expanded) == 4
    assert {x for _, m in expanded for x in m} == set(range(1, 88))
    assert all(set(p) in ({0}, {1}, {0, 2}) for p in profiles.values())
    assert profiles[()] == {0: 797681, 2: 1}
    C = max(abs(p[0]) for p in profiles.values() if set(p) == {0})
    assert C == 4153456
    system = dict(source, format='integer-quadratic-family-abc-reciprocal-contacts-v21', variables=87,
                  source={'construction': SOURCE, 'sha256': PIN}, coordinates=coordinates, residuals=rows)
    polynomial = dict(format='integer-quartic-family-abc-reciprocal-contacts-v21', variables=87,
                      degree=4, inputCoordinate=1, fixedParameter=source['fixedParameter'],
                      coordinates=coordinates, terms=terms(expanded))
    report = {
        'status': 'Exact quadratic realization with a new reciprocal-symmetric set of eight contacts; arithmetic proof treats the changed contacts.',
        'variables': 87, 'quadraticResiduals': 75, 'degree': 4, 'content': 1,
        'ordinaryMonomialsForEveryPositiveParameter': len(profiles), 'symbolicTerms': len(expanded),
        'sourceSha256': PIN, 'removedSourceCoordinates': sorted(removed),
        'removedSourceRows': deleted, 'changedRows': changed,
        'contacts': [-5, -2, -1, 0, 2, 3, 4, 7], 'squaredContactDistances': [1, 4, 9, 36],
        'contactPolynomialCoefficientsAscending': [1296, -1800, 553, -50, 1],
        'contactOutputsPerDetector': 2, 'inverseWeightCoordinatesPerDetector': 3,
        'reciprocalContactIdentity': 'P(r)/r^2=z^2-50*z+481, z=r+36/r',
        'affineContactCoordinates': ['R=r-1', 'Z=z-37'],
        'inverseWeights': ['s=q^-1', 's2=s^2', 's3=s*s2'],
        'factorScaling': 'A_i=s*T_i', 'productScaling': 'Omega=s^2*W0/r',
        'poleIdentity': 's3*b=eta^2 iff b=(F/delta^10)*tau0^2, tau0=r*eta/s^2',
        'zeroWeightStratum': 's=0 forces both numerator reciprocal squares zero, contradicting the exact pair chart.',
        'zeroContactStratum': 'r=0 contradicts r*(z-r)=36.',
        'constantCoefficientMaximum': str(C), 'constantCoefficientMaximumBits': C.bit_length(),
        'constantCoefficientWithoutParameter': '797681',
        'coefficientHeightForEveryIntegerBAtLeast3': 'max(4153456,B^2+797681)',
        'coefficientHeightThresholdOddB': 1833,
        'fixture': {'B': 3, 'definesIntegersCertified': False},
        'comparisonPrecision': 1, 'inputPrecision': 1,
        'arithmeticScope': 'Ordinary rational abc and the retained elliptic, pole, height, and simultaneous-prime inputs; the new degree-eight contact set changes only fixed ineffective constants. Sufficient odd B remains ineffective.',
    }
    folder = output_root/'family_abc87_v21'
    folder.mkdir(parents=True, exist_ok=True)
    for name, data in [('quadratic-family-abc87-v21.json', system),
                       ('polynomial-family-abc87-v21.json', polynomial),
                       ('construction-report-abc87-v21.json', report)]:
        (folder/name).write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ('variables', 'quadraticResiduals', 'degree',
                                           'ordinaryMonomialsForEveryPositiveParameter', 'symbolicTerms',
                                           'coefficientHeightForEveryIntegerBAtLeast3')}))


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--source-root', type=Path, default=HERE)
    p.add_argument('--output-root', type=Path, default=HERE)
    a = p.parse_args()
    build(a.source_root, a.output_root)
