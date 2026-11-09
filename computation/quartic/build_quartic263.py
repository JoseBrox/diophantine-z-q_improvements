#!/usr/bin/env python3
"""Symmetric contact sets and direct normalization give a263-variable quartic.

Four affine images of the five retained contacts are symmetric about1.
Their degree20 product is degree10 in r=(t-1)^2. Five quadratic outputs
evaluate this product and r^9; no separate normalization variable e is needed.
"""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd
from pathlib import Path
import json
from build_quartic273 import add, scale, mul, primitive, terms, v, one, pmul

HERE = Path(__file__).resolve().parent
PIN = '54c242476e796404131eb09099bd2c134adf2358e1129a112cd2b47f996ab6c7'
DELETED_COORDINATES = {350, 398, 20002, 20022}
DELETED_ROWS = {302, 352, 20002, 20022}


def build(source_root=HERE, output_root=HERE):
    raw = (source_root/'family267/quadratic-family267.json').read_bytes()
    assert sha256(raw).hexdigest() == PIN
    source = json.loads(raw)
    old_ids = {c['id']: c['sourceId'] for c in source['coordinates']}
    theta = [Q(0), Q(-1, 2), Q(-1), Q(1, 2399), Q(-32, 407)]
    groups = [theta, [2-x for x in theta], [x+5 for x in theta], [-3-x for x in theta]]
    contacts = sorted(x for group in groups for x in group)
    assert len(set(contacts)) == 20 and 0 in contacts and 1 not in contacts
    assert [2-x for x in contacts] == list(reversed(contacts))
    squared_roots = sorted({(x-1)**2 for x in contacts})
    assert len(squared_roots) == 10
    contact = [Q(1)]
    for root in squared_roots:
        contact = pmul(contact, [-root, Q(1)])

    changes = {}
    renames = {}
    for d in range(2):
        t, r, r2, ff, r4, r5, q, k = ((37, 346, 347, 348, 20000, 20001, 352, 384)
                                      if d == 0 else (391, 392, 393, 394, 20020, 20021, 400, 432))
        delta = add(v(t), scale(one, -1))
        prefix = 'symmetric.detector'+str(d)
        base = {0: one, 1: v(r), 2: v(r2), 4: v(r4), 5: v(r5)}
        value = []
        for power, coefficient in enumerate(contact):
            if power in base:
                term = base[power]
            else:
                a, b = next((a, b) for a in sorted(base) for b in sorted(base)
                            if a <= b and a+b == power)
                term = mul(base[a], base[b])
            value.append(scale(term, coefficient))
        changes.update({
            298+48*d: (prefix+'.deltaSquared.definition', add(mul(delta, delta), scale(v(r), -1))),
            299+48*d: (prefix+'.deltaFourthPower.definition', add(mul(v(r), v(r)), scale(v(r2), -1))),
            20000+20*d: (prefix+'.deltaEighthPower.definition', add(mul(v(r2), v(r2)), scale(v(r4), -1))),
            20001+20*d: (prefix+'.deltaTenthPower.definition', add(mul(v(r), v(r4)), scale(v(r5), -1))),
            300+48*d: (prefix+'.contactPolynomial.definition', add(*value, scale(v(ff), -1))),
            304+50*d: (prefix+'.weight.definition', add(mul(v(ff), v(q)), scale(mul(v(r4), v(r5)), -1))),
            336+50*d: (prefix+'.inverseContact.definition', add(mul(v(q), v(r2)), scale(v(k), -1)))})
        for sid, suffix in [(r, 'deltaSquared'), (r2, 'deltaFourthPower'), (r4, 'deltaEighthPower'),
                            (r5, 'deltaTenthPower'), (ff, 'contactPolynomial'), (k, 'inverseContact')]:
            renames[sid] = prefix+'.'+suffix
    coords = [dict(c, id=i+1, name=renames.get(c['sourceId'], c['name'])) for i, c in
              enumerate(c for c in source['coordinates'] if c['sourceId'] not in DELETED_COORDINATES)]
    mapping = {c['sourceId']: c['id'] for c in coords}
    rows = []
    expanded = defaultdict(int)
    changed = []
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
        rows.append(dict(row, name=name, terms=terms(p)))
        for (a, m), c in p.items():
            for (b, n), e in p.items():
                expanded[a+b, tuple(sorted(m+n))] += c*e
    assert not changes, changes
    expanded = {key: c for key, c in expanded.items() if c}
    ordinary = defaultdict(dict)
    for (a, m), c in expanded.items():
        ordinary[m][a] = c
    assert len(coords) == 263 and len(rows) == 237
    assert gcd(*expanded.values()) == 1 and max(len(m) for a, m in expanded) == 4
    assert {i for a, m in expanded for i in m} == set(range(1, 264))
    assert ordinary[(mapping[489], mapping[489])] == {0: 1, 2: 1}
    assert all(set(p) in ({0}, {1}, {0, 2}) for p in ordinary.values())
    C = max(abs(p[0]) for p in ordinary.values() if set(p) == {0})
    L = max(abs(p[1]) for p in ordinary.values() if set(p) == {1})
    assert C > L*L
    threshold = next(n for n in range(1, 100) if 80989**(4*n+2)+1 > C)
    system = dict(source, format='integer-quadratic-family-v11', variables=263,
                  source={'construction': 'quartic-family267', 'sha256': PIN},
                  coordinates=coords, residuals=rows)
    polynomial = {'format': 'integer-quartic-family-v11', 'variables': 263, 'degree': 4,
                  'inputCoordinate': 1, 'fixedParameter': source['fixedParameter'],
                  'coordinates': coords, 'terms': terms(expanded)}
    report = {'status': 'Exact polynomial specification; the projection theorem uses the stated inherited arithmetic inputs and symmetric contact normalization.',
              'variables': 263, 'quadraticResiduals': 237, 'degree': 4, 'content': 1,
              'ordinaryMonomialsForEveryPositiveParameter': len(ordinary), 'symbolicTerms': len(expanded),
              'sourceSha256': PIN, 'removedSourceCoordinates': sorted(DELETED_COORDINATES),
              'removedSourceRows': sorted(DELETED_ROWS), 'changedSourceRows': changed,
              'contactGroups': [[str(x) for x in group] for group in groups],
              'contacts': [str(x) for x in contacts], 'squaredDistancesFromOne': [str(x) for x in squared_roots],
              'degreeTenPolynomialCoefficients': [str(x) for x in contact],
              'contactCircuit': {'baseExponentsInR': [0, 1, 2, 4, 5], 'coordinatesPerDetector': 5,
                                'normalization': 'F20*q=r^4*r^5; inverseR=q*r^2; r=(t-1)^2'},
              'detectorNormalization': {'R': 'F20(t)/(t-1)^22', 'q': '(t-1)^18/F20(t)',
                                        'scales': ['1', 'T'],
                                        'T': 'one quarter of the trace of the sum of four root abscissas'},
              'heightExponentOfContactRadical': '19/4',
              'constantCoefficientMaximum': str(C), 'constantCoefficientMaximumBits': C.bit_length(),
              'linearCoefficientMultiplierMaximum': L,
              'heightFormulaForEveryPositiveParameter': 'max(C,A^2+1)',
              'exactHeightThresholdN': threshold, 'exactHeightForNAtLeastThreshold': '80989^(4*N+2)+1',
              'effectiveness': 'Every sufficiently large N under the stated arithmetic inputs; no numerical sufficient threshold is asserted.'}
    folder = output_root/'family263'
    folder.mkdir(parents=True, exist_ok=True)
    for name, obj in [('quadratic-family263.json', system), ('polynomial-family263.json', polynomial),
                      ('construction-report263.json', report)]:
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
