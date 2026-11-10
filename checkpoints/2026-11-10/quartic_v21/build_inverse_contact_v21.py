#!/usr/bin/env python3
"""Use the existing inverse weight to remove one contact output per detector."""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd
from pathlib import Path
import json

from build_quartic273 import add, scale, mul, primitive, terms, v, one

HERE = Path(__file__).resolve().parent
SOURCES = {
    'inherited': ('family228_v19/quadratic-family228-v19.json',
                  '0fb0e11597d3915772d5342b7e7d37493cb501254349d4652b544d7e5a44e468', 226),
    'explicit': ('family265_v19/quadratic-family265-v19.json',
                 'e5cf559e1f8b243531299a7d6ace098b71322f58f1c13aff43811cbdb150c14f', 262),
}
CONTACTS = (Q(0), Q(-1, 2), Q(-1), Q(1, 2399), Q(-32, 407))


def contact_polynomial():
    coefficients = [Q(1)]
    for theta in CONTACTS:
        root = (1-theta)**2
        new = [Q(0)]*(len(coefficients)+1)
        for i, coefficient in enumerate(coefficients):
            new[i] -= root*coefficient
            new[i+1] += coefficient
        coefficients = new
    assert len(coefficients) == 6 and coefficients[-1] == 1
    return coefficients


def build(kind, source_root=HERE, output_root=HERE):
    path, pin, count = SOURCES[kind]
    raw = (source_root/path).read_bytes()
    assert sha256(raw).hexdigest() == pin
    source = json.loads(raw)
    old_ids = {c['id']: c['sourceId'] for c in source['coordinates']}
    # r, r^2, old r^3 (now the new quadratic output), old P(r), q, q^-1.
    detectors = [(346, 347, 20000, 348, 352, 360),
                 (392, 393, 20020, 394, 400, 408)]
    if kind == 'explicit':
        detectors.append((50004, 50005, 50018, 50006, 50007, 50008))
    coefficients = contact_polynomial()
    e1, e2, e3, e4, e5 = (-coefficients[4], coefficients[3],
                         -coefficients[2], coefficients[1], -coefficients[0])
    assert e5 != 0
    removed = {block[3] for block in detectors}
    coords = [dict(c) for c in source['coordinates'] if c['sourceId'] not in removed]
    changes = {}
    removed_names = set()
    for j, (r, u, out, F, q, inverse) in enumerate(detectors):
        h = add(one, v(inverse))
        definition = add(v(out), scale(mul(v(r), v(u)), -1),
                         scale(mul(h, v(u)), e1),
                         scale(mul(h, v(r)), -e2))
        normalization = add(mul(v(u), v(out)),
                            scale(mul(h, add(scale(v(u), e3),
                                             scale(v(r), -e4), scale(one, e5))), -1))
        changes[f'reflected.detector{j}.deltaSixthPower.definition'] = (
            f'inverseContact.detector{j}.quadraticOutput.definition', definition)
        changes[f'reflected.detector{j}.weight.definition'] = (
            f'inverseContact.detector{j}.normalization', normalization)
        removed_names.add(f'reflected.detector{j}.contactPolynomial.definition')
        for c in coords:
            if c['sourceId'] == out:
                c['name'] = f'inverseContact.detector{j}.quadraticOutput'
    for i, c in enumerate(coords):
        c['id'] = i+1
    identifiers = {c['sourceId']: c['id'] for c in coords}
    assert len(coords) == count
    rows, changed, removed_rows = [], [], []
    expanded = defaultdict(int)
    for row in source['residuals']:
        if row['name'] in removed_names:
            removed_rows.append(row['name'])
            continue
        p = {(t['parameterPower'], tuple(sorted(old_ids[x] for x in t['monomial']))):
             Q(t['coefficient']) for t in row['terms']}
        name = row['name']
        if name in changes:
            name, p = changes.pop(name)
            changed.append({'sourceId': row['sourceId'], 'oldName': row['name'], 'newName': name})
        assert not any(removed.intersection(m) for _, m in p)
        p = primitive(p)
        assert max(len(m) for _, m in p) <= 2
        p = {(a, tuple(sorted(identifiers[x] for x in m))): c for (a, m), c in p.items()}
        rows.append(dict(row, id=len(rows)+1, name=name, terms=terms(p)))
        for (a, m), c in p.items():
            for (b, n), d in p.items():
                expanded[a+b, tuple(sorted(m+n))] += c*d
    assert not changes and len(removed_rows) == len(detectors)
    expanded = {m: c for m, c in expanded.items() if c}
    profiles = defaultdict(dict)
    for (a, m), c in expanded.items():
        profiles[m][a] = c
    assert len(rows) == {'inherited': 200, 'explicit': 234}[kind]
    assert gcd(*expanded.values()) == 1 and max(len(m) for _, m in expanded) == 4
    assert {x for _, m in expanded for x in m} == set(range(1, count+1))
    assert all(set(p) in ({0}, {1}, {0, 2}) for p in profiles.values())
    assert profiles[(identifiers[489], identifiers[489])] == {0: 1, 2: 1}
    C = max(abs(p[0]) for p in profiles.values() if set(p) == {0})
    L = max(abs(p[1]) for p in profiles.values() if set(p) == {1})
    assert C > L*L and 149**210+1 < C < 149**214+1
    system = dict(source, format='integer-quadratic-family-inverse-contact-v21',
                  variables=count, source={'construction': path, 'sha256': pin},
                  coordinates=coords, residuals=rows)
    polynomial = dict(format='integer-quartic-family-inverse-contact-v21', variables=count,
                      degree=4, inputCoordinate=1, fixedParameter=source['fixedParameter'],
                      coordinates=coords, terms=terms(expanded))
    report = {
        'status': 'Exact rational projection with the inverse-weight contact circuit; no arithmetic change.',
        'variables': count, 'quadraticResiduals': len(rows), 'degree': 4, 'content': 1,
        'ordinaryMonomialsForEveryPositiveParameter': len(profiles), 'symbolicTerms': len(expanded),
        'sourceSha256': pin, 'removedSourceCoordinates': sorted(removed),
        'removedSourceRows': removed_rows, 'changedRows': changed,
        'contactPolynomialCoefficientsAscending': [str(x) for x in coefficients],
        'squaredContactDistances': [str((1-theta)**2) for theta in CONTACTS],
        'contactOutputsPerDetector': 3, 'contactEquationsPerDetector': 4,
        'exactProjectionIdentity': 'r^5-(1+s1)*(r^5-P(r))=0, q*s1=1 iff (1+q)*P(r)=r^5',
        'boundaryStratum': 'r=0 forces q=s1=-1, exactly as in the source; P(r)=0 is impossible.',
        'constantCoefficientMaximum': str(C), 'constantCoefficientMaximumBits': C.bit_length(),
        'linearCoefficientMultiplierMaximum': L,
        'heightFormulaForEveryPositiveParameter': 'max(C,A^2+1)',
        'exactHeightThresholdN': 53, 'exactHeightForNAtLeastThreshold': '149^(4*N+2)+1',
        'comparisonPrecision': 3, 'inputPrecision': 1,
        'arithmeticScope': 'Full retained normalized modular, elliptic, pole and simultaneous-prime premises; no additional abc hypothesis.',
        'definingParameterEffectivity': 'Ineffective sufficient N, from aggregate trace height.' if kind == 'inherited'
                                        else 'Every integer N>=9682, with the effective abscissa-sum height theorem.',
    }
    if kind == 'explicit':
        report.update(definingThresholdN=9682, forcedIndexDepthAtThreshold=45988,
                      specifiedParameter='149^19365', specifiedCoefficientHeight='149^38730+1',
                      specifiedCoefficientHeightBinaryDigits=279599,
                      tenContactHeightConstantUpperBound='2^221274',
                      tenContactHeightExponent='1 with (22+log(M)/2)^2',
                      factorsPerDetector=4, scales=['1', 'S0^2', '(S0+S1)^2'])
    else:
        report.update(factorsPerDetector=5, scales=['1', 'T'])
    folder = output_root/f'family{count}_v21'
    folder.mkdir(parents=True, exist_ok=True)
    for filename, data in [(f'quadratic-family{count}-v21.json', system),
                           (f'polynomial-family{count}-v21.json', polynomial),
                           (f'construction-report{count}-v21.json', report)]:
        (folder/filename).write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ('variables', 'quadraticResiduals', 'degree',
                                           'ordinaryMonomialsForEveryPositiveParameter',
                                           'symbolicTerms', 'constantCoefficientMaximumBits')}))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--kind', choices=(*SOURCES, 'all'), default='all')
    parser.add_argument('--source-root', type=Path, default=HERE)
    parser.add_argument('--output-root', type=Path, default=HERE)
    args = parser.parse_args()
    for kind in SOURCES if args.kind == 'all' else (args.kind,):
        build(kind, args.source_root, args.output_root)
