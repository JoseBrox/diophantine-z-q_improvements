#!/usr/bin/env python3
"""Exact rational change of basis in eight reference equations."""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / 'abc78_reduced_v40'
SOURCE_HASH = '1bdc8f27946ecb31bb536946279455597b00028510a43e5d7634fb28acc52591'


def serialize(poly):
    return [dict(parameterPower=j, monomial=list(m), coefficient=str(c))
            for (j, m), c in sorted(poly.items()) if c]


def parse(terms):
    return {(t['parameterPower'], tuple(t['monomial'])): Q(t['coefficient']) for t in terms}


def build(output=HERE):
    path = PARENT / 'quadratic-family.json'
    assert sha256(path.read_bytes()).hexdigest() == SOURCE_HASH
    system = json.loads(path.read_text())
    certificate = json.loads((HERE / 'basis-certificate.json').read_text())
    names = certificate['sourceRowNames']
    old = {r['name']: r for r in system['residuals']}
    matrix = [[Q(x) for x in row] for row in certificate['matrix']]
    source_rows = [parse(old[name]['terms']) for name in names]
    target = []
    for i, coefficients in enumerate(matrix):
        row = defaultdict(Q)
        for c, p in zip(coefficients, source_rows):
            for key, value in p.items():
                row[key] += c * value
        row = {key: value for key, value in row.items() if value}
        assert all(x.denominator == 1 for x in row.values())
        target.append(dict(id=old[names[i]]['id'], name=f'common.primitive.{i + 1}',
                           terms=serialize(row)))
    mapping = dict(zip(names, target))
    system['residuals'] = [mapping.get(r['name'], r) for r in system['residuals']]
    system['format'] = 'integer-quadratic-family-abc78-primitive-v40'
    system['referenceBasisParentSha256'] = SOURCE_HASH
    expanded = defaultdict(Q)
    for row in system['residuals']:
        p = parse(row['terms'])
        for (a, m), c in p.items():
            for (b, n), d in p.items():
                expanded[a + b, tuple(sorted(m + n))] += c * d
    expanded = {key: value for key, value in expanded.items() if value}
    profiles = defaultdict(dict)
    for (j, m), value in expanded.items():
        assert value.denominator == 1
        profiles[m][j] = int(value)
    fixedmax = max(abs(p[0]) for p in profiles.values() if set(p) == {0})
    C0 = profiles[()][0]
    assert profiles[()] == {0: C0, 2: 1}
    assert expanded[0, (1, 1, 1, 1)] == 1
    assert len(system['residuals']) == 68
    assert max(len(m) for _, m in expanded) == 4
    polynomial = dict(format='integer-quartic-family-abc78-primitive-v40',
                      variables=78, degree=4, inputCoordinate=1,
                      coordinates=system['coordinates'],
                      fixedParameter=system['fixedParameter'], terms=serialize(expanded))
    report = dict(schema='abc78-primitive-basis-construction/v40', variables=78,
                  quadraticRows=68, degree=4, integerContentForEveryPositiveB=1,
                  ordinaryMonomialsForEveryPositiveB=len(profiles),
                  parameterSeparatedTerms=len(expanded),
                  largestFixedCoefficient=str(fixedmax), constantCoefficient=str(C0),
                  exactHeight=f'max({fixedmax},B^2+{C0})',
                  sourceQuadraticSha256=SOURCE_HASH,
                  transformedRows=names,
                  inputProjection='Identical full rational zero set for every fixed B.',
                  arithmeticScope='Ordinary rational abc and the unchanged group, simultaneous-prime and prepared simultaneous-twist premises of abc78_v34.',
                  definingThreshold='Same ineffective sufficient odd-B threshold as abc78_v34; B=81 remains only a reconstruction fixture.',
                  scope='Exact basis-change, coefficient and height assertions; no new global variable count or arithmetic premise.')
    output.mkdir(parents=True, exist_ok=True)
    for filename, data in [('quadratic-family.json', system),
                           ('polynomial-family.json', polynomial),
                           ('construction-report.json', report)]:
        (output / filename).write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=HERE)
    build(parser.parse_args().output)
