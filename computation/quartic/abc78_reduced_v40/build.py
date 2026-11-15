#!/usr/bin/env python3
"""Remove two algebraically redundant curve rows from the abc78 family.

All coefficients are exact. This program supplies the construction; the
separate checker verifies the implication identities and expands with SymPy.
"""
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / 'abc78_v34'
PARENT_HASH = 'ceffdf6e0a38ac1c8c42812f5e7bef599231dc5bc4b5f7c4527303b81dfc11bb'
REMOVED = {'pair.cubic.0', 'pair.cubic.1'}


def build(output=HERE):
    source = PARENT / 'quadratic-family.json'
    assert sha256(source.read_bytes()).hexdigest() == PARENT_HASH
    system = json.loads(source.read_text())
    oldrows = system['residuals']
    assert {r['name'] for r in oldrows if r['name'] in REMOVED} == REMOVED
    rows = [dict(r) for r in oldrows if r['name'] not in REMOVED]
    for i, row in enumerate(rows, 1):
        row['sourceId'] = row['id']
        row['id'] = i
    system['format'] = 'integer-quadratic-family-abc78-reduced-v40'
    system['residuals'] = rows
    system['sourceSha256'] = PARENT_HASH
    system['removedRows'] = sorted(REMOVED)
    assert len(rows) == 68 and system['variables'] == 78
    expanded = defaultdict(Fraction)
    for row in rows:
        for t in row['terms']:
            for u in row['terms']:
                key = (t['parameterPower'] + u['parameterPower'],
                       tuple(sorted(t['monomial'] + u['monomial'])))
                expanded[key] += Fraction(t['coefficient']) * Fraction(u['coefficient'])
    expanded = {k: c for k, c in expanded.items() if c}
    assert all(c.denominator == 1 for c in expanded.values())
    assert expanded[0, (1, 1, 1, 1)] == 1
    assert max(len(m) for _, m in expanded) == 4
    profiles = defaultdict(dict)
    for (j, m), c in expanded.items():
        profiles[m][j] = int(c)
    assert len(profiles) == 1113
    fixedmax = max(abs(p[0]) for p in profiles.values() if set(p) == {0})
    const = profiles[()][0]
    assert profiles[()] == {0: const, 2: 1}
    parent_report = json.loads((PARENT / 'construction-report.json').read_text())
    assert fixedmax == int(parent_report['largestFixedCoefficient'])
    assert const == int(parent_report['constantCoefficient'])
    terms = [dict(parameterPower=j, monomial=list(m), coefficient=str(c))
             for (j, m), c in sorted(expanded.items())]
    polynomial = dict(format='integer-quartic-family-abc78-reduced-v40',
                      variables=78, degree=4, inputCoordinate=1,
                      fixedParameter=system['fixedParameter'],
                      coordinates=system['coordinates'], terms=terms)
    report = dict(schema='abc78-reduced-exact-construction/v40', variables=78,
                  quadraticRows=68, degree=4, integerContentForEveryPositiveB=1,
                  ordinaryMonomialsForEveryPositiveB=len(profiles),
                  parameterSeparatedTerms=len(expanded),
                  constantCoefficient=str(const), largestFixedCoefficient=str(fixedmax),
                  exactHeight=f'max({fixedmax},B^2+{const})',
                  sourceQuadraticSha256=PARENT_HASH, removedRows=sorted(REMOVED),
                  inputProjection='Exactly the parent projection for every fixed B.',
                  arithmeticScope=parent_report['arithmeticScope'],
                  definingThreshold=parent_report['definingThreshold'],
                  checksScope='Exact coefficients, universal polynomial identities and preserved source rows; external arithmetic premises are not certified.')
    output.mkdir(parents=True, exist_ok=True)
    for name, data in [('quadratic-family.json', system),
                       ('polynomial-family.json', polynomial),
                       ('construction-report.json', report)]:
        (output / name).write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=HERE)
    build(parser.parse_args().output)
