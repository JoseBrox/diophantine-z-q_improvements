#!/usr/bin/env python3
"""Specify the explicit quartic with a four-coordinate common point.

Numerator logarithms are divided by their common approximation factor
before their final quotient is formed.  This removes four rational
coordinates from the hash-pinned explicit 322-variable source.
"""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd
from pathlib import Path
import json

from build_quartic273 import add, scale, mul, fm, primitive, terms, v, one
from build_fixed_difference_v18 import common_rows, ROW_BASIS, fadd, fs

HERE = Path(__file__).resolve().parent
SOURCE = 'family322/quadratic-family322.json'
PIN = '93f4aaac68efaba7654f3682d404e38c913dc05bd273d1e5f0e3c6cdd744ecde'


def approximation(i):
    if i == 0:
        return (add(one, scale(v(190), Q(-22, 5)), scale(v(191), Q(48, 5)),
                    scale(v(192), Q(-386, 15))),
                add(scale(v(190), Q(12, 5)), scale(v(191), Q(-44, 5)),
                    scale(v(193), Q(88, 5))))
    return v(192+12*i), v(193+12*i)


def build(source_root=HERE, output_root=HERE):
    raw = (source_root/SOURCE).read_bytes()
    assert sha256(raw).hexdigest() == PIN
    source = json.loads(raw)
    old_ids = {c['id']: c['sourceId'] for c in source['coordinates']}
    deleted_coordinates = {188, 189, 700, 701}
    deleted_rows = {140, 141, 661, 662}
    changes = dict(zip((34, 35, 92, 93, 112, 113), common_rows()))
    A0, T = (v(186), v(187)), (v(90), v(91))
    for i in range(4):
        Z = v(164+4*i), v(165+4*i)
        QI = v(110+8*i), v(111+8*i)
        KI = v(114+8*i), v(115+8*i)
        LP = v(234+4*i), v(235+4*i)
        normalized = fadd(fm(A0, Z), fs(fm(QI, approximation(i)), -1))
        quotient = fadd(fm(LP, KI), fs(fm(Z, T), -1))
        for j in range(2):
            changes[116+4*i+j] = (f'normalizedLogNumerator{i+1}.definition.{j}', normalized[j])
            changes[146+12*i+j] = (f'alternateLogRatio{i+1}.definition.{j}', quotient[j])
    coordinates = [dict(c, id=i+1) for i, c in enumerate(c for c in source['coordinates']
                    if c['sourceId'] not in deleted_coordinates)]
    for c in coordinates:
        sid = c['sourceId']
        if sid in (90, 91):
            c['name'] = 'alternate.negativeReciprocalZ0.'+str(sid-90)
        if sid in {164+4*i+j for i in range(4) for j in (0, 1)}:
            c['name'] = f'normalizedLogNumerator{(sid-164)//4+1}.{sid%2}'
    mapping = {c['sourceId']: c['id'] for c in coordinates}
    rows, changed, expanded = [], [], defaultdict(int)
    for old in source['residuals']:
        sid = old['sourceId']
        if sid in deleted_rows:
            continue
        if sid in changes:
            name, p = changes.pop(sid)
            changed.append({'sourceId': sid, 'oldName': old['name'], 'newName': name})
        else:
            name = old['name']
            p = {(t['parameterPower'], tuple(sorted(old_ids[x] for x in t['monomial']))):
                 Q(t['coefficient']) for t in old['terms']}
        assert all(not deleted_coordinates.intersection(m) for _, m in p), name
        p = primitive(p)
        p = {(a, tuple(sorted(mapping[x] for x in m))): c for (a, m), c in p.items()}
        assert max(len(m) for _, m in p) <= 2
        rows.append(dict(old, id=len(rows)+1, name=name, terms=terms(p)))
        for (a, m), c in p.items():
            for (b, n), d in p.items():
                expanded[a+b, tuple(sorted(m+n))] += c*d
    assert not changes
    expanded = {key: value for key, value in expanded.items() if value}
    profiles = defaultdict(dict)
    for (a, m), c in expanded.items():
        profiles[m][a] = c
    assert len(coordinates) == 318 and len(rows) == 290
    assert gcd(*expanded.values()) == 1
    assert max(len(m) for _, m in expanded) == 4
    assert {i for _, m in expanded for i in m} == set(range(1, 319))
    assert profiles[(mapping[489], mapping[489])] == {0: 1, 2: 1}
    assert all(set(p) in ({0}, {1}, {0, 2}) for p in profiles.values())
    C = max(abs(p[0]) for p in profiles.values() if set(p) == {0})
    L = max(abs(p[1]) for p in profiles.values() if set(p) == {1})
    assert L == 2*80989**2 and C > L*L
    assert 80989**94+1 > C > 80989**90+1
    system = dict(source, format='integer-quadratic-family-fixed-difference-v18', variables=318,
                  source={'construction': SOURCE, 'sha256': PIN},
                  coordinates=coordinates, residuals=rows)
    polynomial = dict(format='integer-quartic-family-fixed-difference-v18', variables=318,
                      degree=4, inputCoordinate=1, fixedParameter=source['fixedParameter'],
                      coordinates=coordinates, terms=terms(expanded))
    report = {
        'status': 'Exact algebraic specification. The source arithmetic premises and effective threshold N>=27464 are retained.',
        'variables': 318, 'quadraticResiduals': 290, 'degree': 4, 'content': 1,
        'symbolicTerms': len(expanded), 'ordinaryMonomialsForEveryPositiveParameter': len(profiles),
        'sourceSha256': PIN, 'removedSourceCoordinates': sorted(deleted_coordinates),
        'removedSourceRows': sorted(deleted_rows), 'changedRows': changed,
        'rationalComponentRowBasis': ROW_BASIS,
        'rationalComponentRowBasisDeterminant': '-1/362963666515968',
        'commonPointFieldCoordinates': ['S', 'T', 'f', 'g'],
        'normalizedLogNumeratorEquation': 'A0*Zi=Qi*Ai',
        'alternateLogRatioEquation': 'LPi*Ki=Zi*T',
        'projectionScope': 'On T!=0 this is an exact chart substitution. The inherited effective reciprocal-abscissa exclusion rules out T=0 at every defining parameter N>=27464 before logarithmic quotients are used.',
        'constantCoefficientMaximum': str(C), 'constantCoefficientMaximumBits': C.bit_length(),
        'linearCoefficientMultiplierMaximum': L,
        'heightFormulaForEveryPositiveParameter': 'max(C,A^2+1)',
        'exactHeightThresholdN': 23,
        'exactHeightForNAtLeastThreshold': '80989^(4*N+2)+1',
        'definingThresholdN': 27464, 'specifiedParameter': '80989^54929',
        'specifiedCoefficientHeight': '80989^109858+1',
    }
    output = output_root/'family318_v18'
    output.mkdir(parents=True, exist_ok=True)
    for name, data in [('quadratic-family318-v18.json', system),
                       ('polynomial-family318-v18.json', polynomial),
                       ('construction-report318-v18.json', report)]:
        (output/name).write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps({key: report[key] for key in ('variables', 'quadraticResiduals', 'degree',
          'ordinaryMonomialsForEveryPositiveParameter', 'constantCoefficientMaximumBits',
          'definingThresholdN')}))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', type=Path, default=HERE)
    parser.add_argument('--output-root', type=Path, default=HERE)
    args = parser.parse_args()
    build(args.source_root, args.output_root)
