#!/usr/bin/env python3
"""Independent exact verification of the ABC78 rational row-basis change."""
from collections import defaultdict
from hashlib import sha256
from math import isqrt
from pathlib import Path
import argparse
import json
import sympy as sp

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / 'abc78_reduced_v40'
HASH = '1bdc8f27946ecb31bb536946279455597b00028510a43e5d7634fb28acc52591'


def require(ok, reason):
    if not ok:
        raise AssertionError(reason)


def parse(terms):
    ans = {}
    for t in terms:
        key = t['parameterPower'], tuple(t['monomial'])
        require(key not in ans, 'Distinct monomials')
        ans[key] = int(t['coefficient'])
    return ans


def check(output=HERE):
    p = PARENT / 'quadratic-family.json'
    require(sha256(p.read_bytes()).hexdigest() == HASH, 'Pinned parent system')
    old = json.loads(p.read_text())
    new = json.loads((HERE / 'quadratic-family.json').read_text())
    polynomial = json.loads((HERE / 'polynomial-family.json').read_text())
    report = json.loads((HERE / 'construction-report.json').read_text())
    certificate = json.loads((HERE / 'basis-certificate.json').read_text())
    require(certificate['sourceSha256'] == HASH, 'Certificate source binding')
    require(new['coordinates'] == old['coordinates'] == polynomial['coordinates'], 'Coordinates unchanged')
    require(new['fixedParameter'] == old['fixedParameter'] == polynomial['fixedParameter'], 'Parameter unchanged')
    names = certificate['sourceRowNames']
    require(len(names) == len(set(names)) == 8, 'Eight distinct source rows')
    require(names == [r['name'] for r in old['residuals'] if r['name'].startswith('common.')],
            'Exactly the reference block is replaced')
    matrix = sp.Matrix([[sp.Rational(x) for x in row] for row in certificate['matrix']])
    inverse = sp.Matrix([[sp.Rational(x) for x in row] for row in certificate['inverseMatrix']])
    require(matrix.shape == (8, 8) and matrix * inverse == sp.eye(8) and inverse * matrix == sp.eye(8),
            'Certified invertible rational change of basis')
    require(str(matrix.det()) == certificate['determinant'], 'Exact nonzero determinant')
    oldbyname = {r['name']: r for r in old['residuals']}
    newbyname = {r['name']: r for r in new['residuals']}
    columns = sorted({key for name in names for key in parse(oldbyname[name]['terms'])})
    source = sp.Matrix([[parse(oldbyname[name]['terms']).get(key, 0) for key in columns] for name in names])
    target = sp.Matrix([[parse(newbyname[f'common.primitive.{i + 1}']['terms']).get(key, 0)
                         for key in columns] for i in range(8)])
    require(matrix * source == target and inverse * target == source, 'All basis identities in both directions')
    require(all(set(parse(newbyname[f'common.primitive.{i + 1}']['terms'])) <= set(columns)
                for i in range(8)), 'No unchecked target monomials')
    for r in old['residuals']:
        if r['name'] not in names:
            require(newbyname[r['name']] == r, 'Every other row is literal')
    require(len(new['residuals']) == 68, 'Quadratic row count')
    B = sp.Symbol('B')
    variables = sp.symbols('x1:79')
    expanded = defaultdict(int)
    for row in new['residuals']:
        coefficients = [int(t['coefficient']) for t in row['terms']]
        require(sp.igcd(*coefficients) == 1, 'Each row is primitive integral')
        row_profiles = defaultdict(dict)
        for term in row['terms']:
            row_profiles[tuple(term['monomial'])][term['parameterPower']] = int(term['coefficient'])
        fixed_coefficients = [profile[0] for profile in row_profiles.values() if set(profile) == {0}]
        require(sp.igcd(*fixed_coefficients) == 1,
                'Parameter-independent coefficients certify primitivity at every integer B')
        require(max(len(t['monomial']) for t in row['terms']) <= 2, 'Each row is quadratic')
        ids = sorted({i for t in row['terms'] for i in t['monomial']})
        expression = sum(sp.Integer(t['coefficient']) * B**t['parameterPower'] *
                         sp.prod(variables[i - 1] for i in t['monomial']) for t in row['terms'])
        poly = sp.Poly(expression**2, B, *(variables[i - 1] for i in ids), domain=sp.ZZ)
        for exponents, coefficient in poly.terms():
            monomial = tuple(i for i, e in zip(ids, exponents[1:]) for _ in range(e))
            expanded[exponents[0], monomial] += int(coefficient)
    expanded = {key: value for key, value in expanded.items() if value}
    require(expanded == parse(polynomial['terms']), 'Independent quartic expansion')
    require({i for _, m in expanded for i in m} == set(range(1, 79)), 'All coordinates occur')
    require(expanded[0, (1, 1, 1, 1)] == 1 and max(len(m) for _, m in expanded) == 4,
            'Exact degree four and content one for every B')
    profiles = defaultdict(dict)
    for (j, m), c in expanded.items():
        profiles[m][j] = c
    K = max(abs(p[0]) for p in profiles.values() if set(p) == {0})
    C0 = profiles[()][0]
    require(K == int(report['largestFixedCoefficient']) and C0 == int(report['constantCoefficient']),
            'Exact fixed height and constant coefficient')
    require(profiles[()] == {0: C0, 2: 1}, 'Constant profile')
    switch = isqrt(max(0, K - C0)) + 1
    for m, p in profiles.items():
        if set(p) == {0} or m == ():
            continue
        require(set(p) <= {0, 1}, 'Only constant profile contains B squared')
        require(all(c >= 0 for c in p.values()) or all(c <= 0 for c in p.values()),
                'No positive-parameter coefficient cancellation')
        a, c = abs(p.get(1, 0)), abs(p.get(0, 0))
        require(a * (switch - 1) + c <= K, 'Height below switch')
        require(switch**2 + C0 >= a * switch + c and 2 * switch >= a, 'Height above switch')
    require(len(profiles) == report['ordinaryMonomialsForEveryPositiveB'], 'Exact support for all positive B')
    # Two independent corruption controls: a changed transformation coefficient
    # violates the source identities, and a missing target term changes expansion.
    corrupt = matrix.copy()
    corrupt[0, 0] += 1
    require(corrupt * source != target, 'Corrupt matrix rejection')
    bad_terms = dict(expanded)
    bad_terms.pop((0, (1, 1, 1, 1)))
    require(bad_terms != parse(polynomial['terms']), 'Corrupt coefficient rejection')
    receipt = dict(schema='abc78-primitive-basis-independent-verification/v40', passed=True,
                   sourceQuadraticSha256=HASH, exactRationalMatrixDimension=8,
                   determinant=certificate['determinant'], variables=78, quadraticRows=68,
                   degree=4, integerContentForEveryPositiveB=1,
                   ordinaryMonomialsForEveryPositiveB=len(profiles),
                   exactHeight=report['exactHeight'],
                   scope='Exact invertible row-basis certificate, literal preservation of other rows, independent expansion and all-positive-B coefficient bounds. No new arithmetic premise or numerical defining threshold is certified.')
    output.mkdir(parents=True, exist_ok=True)
    (output / 'independent-verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=HERE)
    check(parser.parse_args().output)
