#!/usr/bin/env python3
"""Balanced contact normalization for the 259-variable quartic family.

The fixed square factor gamma^2 supplies finite and real pole preparation.
The arithmetic proof uses the same inherited premises as family263.
"""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd
from pathlib import Path
import json
from build_quartic273 import add, scale, mul, primitive, terms, v, one

HERE = Path(__file__).resolve().parent
PIN = '26876d3f9fa9a42478c4465edf36f9e8647df44ee2cc744df551300465fe58e3'
DELETED_COORDINATES = {355, 384, 403, 432}
DELETED_ROWS = {336, 386, 544, 550}
GAMMA = Q(408, 409)


def build(source_root=HERE, output_root=HERE):
    raw = (source_root/'family263/quadratic-family263.json').read_bytes()
    assert sha256(raw).hexdigest() == PIN
    source = json.loads(raw)
    old_ids = {c['id']: c['sourceId'] for c in source['coordinates']}
    changes = {}
    renames = {360: 'detector0.weightPower19', 408: 'detector1.weightPower19'}
    for d in range(2):
        ff, r5, q, tau, b = ((348, 20001, 352, 383, 385) if d == 0
                             else (394, 20021, 400, 431, 433))
        prefix = 'balanced.detector'+str(d)
        q19, q10 = ((360, 369) if d == 0 else (408, 417))
        changes[526+7*d] = (prefix+'.weightPower19.definition',
            add(mul(v(q), v(q19)), scale(mul(v(q10), v(q10)), -1)))
        changes[304+50*d] = (prefix+'.weight.definition',
            add(mul(v(ff), add(one, v(q))), scale(mul(v(r5), v(r5)), -1)))
        changes[337+50*d] = (prefix+'.poleInput.definition',
            add(mul(add(one, v(q)), v(b)), scale(mul(v(tau), v(tau)), -GAMMA**2)))
    coords = [dict(c, id=i+1, name=renames.get(c['sourceId'], c['name'])) for i, c in enumerate(c for c in source['coordinates']
              if c['sourceId'] not in DELETED_COORDINATES)]
    mapping = {c['sourceId']: c['id'] for c in coords}
    rows, changed = [], []
    expanded = defaultdict(int)
    for row in source['residuals']:
        sid = row['sourceId']
        if sid in DELETED_ROWS:
            continue
        if sid in changes:
            name, p = changes.pop(sid)
            changed.append(sid)
        else:
            name = row['name']
            p = {(t['parameterPower'], tuple(sorted(old_ids[i] for i in t['monomial']))):
                 Q(t['coefficient']) for t in row['terms']}
        assert not any(DELETED_COORDINATES.intersection(m) for a, m in p), name
        p = primitive(p)
        p = {(a, tuple(sorted(mapping[i] for i in m))): c for (a, m), c in p.items()}
        assert max(len(m) for a, m in p) <= 2
        rows.append(dict(row, id=len(rows)+1, name=name, terms=terms(p)))
        for (a, m), c in p.items():
            for (b, n), e in p.items():
                expanded[a+b, tuple(sorted(m+n))] += c*e
    assert not changes
    expanded = {key: c for key, c in expanded.items() if c}
    ordinary = defaultdict(dict)
    for (a, m), c in expanded.items():
        ordinary[m][a] = c
    assert len(coords) == 259 and len(rows) == 233
    assert gcd(*expanded.values()) == 1 and max(len(m) for a, m in expanded) == 4
    assert {i for a, m in expanded for i in m} == set(range(1, 260))
    assert ordinary[(mapping[489], mapping[489])] == {0: 1, 2: 1}
    assert all(set(p) in ({0}, {1}, {0, 2}) for p in ordinary.values())
    C = max(abs(p[0]) for p in ordinary.values() if set(p) == {0})
    L = max(abs(p[1]) for p in ordinary.values() if set(p) == {1})
    assert C > L*L
    threshold = next(n for n in range(1, 100) if 80989**(4*n+2)+1 > C)
    system = dict(source, format='integer-quadratic-family-v12', variables=259,
                  source={'construction': 'quartic-family263', 'sha256': PIN},
                  coordinates=coords, residuals=rows)
    polynomial = {'format': 'integer-quartic-family-v12', 'variables': 259, 'degree': 4,
                  'inputCoordinate': 1, 'fixedParameter': source['fixedParameter'],
                  'coordinates': coords, 'terms': terms(expanded)}
    report = {'status': 'Exact polynomial specification; the projection theorem uses the same inherited arithmetic inputs as family263.',
              'variables': 259, 'quadraticResiduals': 233, 'degree': 4, 'content': 1,
              'ordinaryMonomialsForEveryPositiveParameter': len(ordinary), 'symbolicTerms': len(expanded),
              'sourceSha256': PIN, 'removedSourceCoordinates': sorted(DELETED_COORDINATES),
              'removedSourceRows': sorted(DELETED_ROWS), 'changedSourceRows': changed,
              'gamma': str(GAMMA),
              'detectorNormalization': {'R': 'F20(t)/(t-1)^20', 'q': '(t-1)^20/F20(t)-1',
                  'inverseR': '1+q', 'poleInput': '(408/409)^2*R/Tr(W^-1)^2',
                  'quadraticRelations': ['F20*(1+q)=(r^5)^2', '(1+q)*b=(408/409)^2*tau^2'],
                  'scales': ['1', 'T'],
                  'exceptionalStrata': {'q=0': 'Contact radical equals1; the nineteenth-power auxiliary may be free.',
                     't=1': 'q=-1; contact radical equals1; reciprocal interpretation is not used.'}},
              'weightRelations': ['q2=q^2', 'q4=q2^2', 'q5=q*q4', 'q10=q5^2', 'q*q19=q10^2'],
              'requiredTestOrders': {'C2_C3_C4_G': 10, 'I': 5, 'H': 6, 'C1': 3, 'reciprocalAbscissas': 1},
              'preparedPoleValuationsAt2_3_17': [4, 2, 2],
              'realPoleInputLimit': str(GAMMA**2/4),
              'heightExponentOfContactRadical': '19/4',
              'constantCoefficientMaximum': str(C), 'constantCoefficientMaximumBits': C.bit_length(),
              'linearCoefficientMultiplierMaximum': L,
              'heightFormulaForEveryPositiveParameter': 'max(C,A^2+1)',
              'exactHeightThresholdN': threshold, 'exactHeightForNAtLeastThreshold': '80989^(4*N+2)+1',
              'effectiveness': 'Every sufficiently large N under the inherited inputs; no numerical sufficient threshold is asserted.'}
    folder = output_root/'family259_v17'
    folder.mkdir(parents=True, exist_ok=True)
    for name, obj in [('quadratic-family259-v17.json', system), ('polynomial-family259-v17.json', polynomial),
                      ('construction-report259-v17.json', report)]:
        (folder/name).write_text(json.dumps(obj, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ('variables', 'quadraticResiduals', 'degree',
                'ordinaryMonomialsForEveryPositiveParameter', 'symbolicTerms',
                'constantCoefficientMaximumBits', 'exactHeightThresholdN')}))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', type=Path, default=HERE)
    parser.add_argument('--output-root', type=Path, default=HERE)
    args = parser.parse_args()
    build(args.source_root, args.output_root)
