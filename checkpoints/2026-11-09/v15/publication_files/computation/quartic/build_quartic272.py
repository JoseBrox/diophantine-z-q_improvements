#!/usr/bin/env python3
"""A 272-coordinate quartic by a five-coordinate degree-twenty evaluation."""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from math import gcd, lcm
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
PIN = 'c2e2ad2838e79aa38c93bd41aa079d612826b5991c19835b88e14ec12fecc18b'


def add(*polynomials):
    result = defaultdict(F)
    for p in polynomials:
        for m, c in p.items(): result[m] += c
    return {m: c for m, c in result.items() if c}


def scale(p, c): return {m: c*v for m, v in p.items() if c*v}


def product(p, q):
    result = defaultdict(F)
    for (a, m), c in p.items():
        for (b, n), d in q.items(): result[a+b, tuple(sorted(m+n))] += c*d
    return {m: c for m, c in result.items() if c}


def variable(i): return {(0, (i,)): F(1)}
ONE = {(0, ()): F(1)}


def primitive(p):
    denominator = lcm(*(c.denominator for c in p.values()))
    integer = {m: int(c*denominator) for m, c in p.items()}
    divisor = gcd(*integer.values())
    if integer[min(integer)] < 0: divisor = -divisor
    return {m: c//divisor for m, c in sorted(integer.items())}


def terms(p):
    return [{'parameterPower': a, 'monomial': list(m), 'coefficient': str(c)}
            for (a, m), c in sorted(p.items())]


def convolution(a, b):
    c = [F(0)]*(len(a)+len(b)-1)
    for i, u in enumerate(a):
        for j, v in enumerate(b): c[i+j] += u*v
    return c


def build(source_root=HERE, output_root=HERE):
    raw = (source_root/'family273/quadratic-family273.json').read_bytes()
    assert sha256(raw).hexdigest() == PIN
    source = json.loads(raw)
    source_ids = {c['id']: c['sourceId'] for c in source['coordinates']}
    contact = [F(1)]
    roots = [theta+3*j for j in range(4)
             for theta in [F(0), F(-1, 2), F(-1), F(1, 2399), F(-32, 407)]]
    for theta in roots: contact = convolution(contact, [-theta, F(1)])
    square_root = [F(0)]*11
    square_root[10] = 1
    for j in range(9, -1, -1):
        already = sum(square_root[a]*square_root[10+j-a]
                      for a in range(j+1, 10) if 0 <= 10+j-a <= 10)
        square_root[j] = (contact[10+j]-already)/2
    square = convolution(square_root, square_root)
    remainder = [contact[i]-square[i] for i in range(21)]
    assert not any(remainder[10:])
    remainder = remainder[:10]

    basis = {0: ONE, 1: variable(391), 2: variable(392),
             4: variable(393), 5: variable(20020)}

    def evaluate(coefficients):
        result = {}
        for degree, coefficient in enumerate(coefficients):
            if not coefficient: continue
            if degree in basis: value = basis[degree]
            else:
                a, b = next((a, b) for a in sorted(basis) for b in sorted(basis)
                            if a <= b and a+b == degree)
                value = product(basis[a], basis[b])
            result = add(result, scale(value, coefficient))
        return result

    edits = {
        'compressed.det1.tPower3.definition': ('single.det1.tPower4.definition',
            add(product(variable(392), variable(392)), scale(variable(393), -1))),
        'compressed.det1.tPower6.definition': ('single.det1.tPower5.definition',
            add(product(variable(391), variable(393)), scale(variable(20020), -1))),
        'compressed.det1.quotient9.definition': ('single.det1.squareRoot10.definition',
            add(evaluate(square_root), scale(variable(20021), -1))),
        'compressed.det1.contactPolynomial.definition': ('single.det1.contactPolynomial.definition',
            add(product(variable(20021), variable(20021)), evaluate(remainder), scale(variable(394), -1)))
    }
    renames = {393: 'single.det1.tPower4', 20020: 'single.det1.tPower5',
               20021: 'single.det1.squareRoot10'}
    coordinates = [dict(c, id=i+1, name=renames.get(c['sourceId'], c['name']))
                   for i, c in enumerate(c for c in source['coordinates'] if c['sourceId'] != 20022)]
    mapping = {c['sourceId']: c['id'] for c in coordinates}
    residuals, expanded = [], defaultdict(int)
    for row in source['residuals']:
        if row['sourceId'] == 20022: continue
        name = row['name']
        p = {(t['parameterPower'], tuple(sorted(source_ids[i] for i in t['monomial']))):
             F(int(t['coefficient'])) for t in row['terms']}
        if name in edits: name, p = edits.pop(name)
        p = primitive(p)
        assert all(20022 not in m for a, m in p)
        p = {(a, tuple(sorted(mapping[i] for i in m))): c for (a, m), c in p.items()}
        assert max(len(m) for a, m in p) <= 2
        residuals.append(dict(row, name=name, terms=terms(p)))
        for (a, m), c in p.items():
            for (b, n), d in p.items(): expanded[a+b, tuple(sorted(m+n))] += c*d
    assert not edits
    expanded = {m: c for m, c in expanded.items() if c}
    ordinary = defaultdict(dict)
    for (a, m), c in expanded.items(): ordinary[m][a] = c
    assert len(coordinates) == 272 and len(residuals) == 246
    assert ordinary[(mapping[489], mapping[489])] == {0: 1, 2: 1}
    assert all(set(p) in ({0}, {1}, {0, 2}) for p in ordinary.values())
    assert gcd(*expanded.values()) == 1
    assert {i for a, m in expanded for i in m} == set(range(1, 273))
    maximum = max(abs(p[0]) for p in ordinary.values() if set(p) == {0})
    multiplier = max(abs(p[1]) for p in ordinary.values() if set(p) == {1})
    assert maximum > multiplier*multiplier
    threshold = 1
    while 80989**(4*threshold+2)+1 <= maximum: threshold += 1
    system = dict(source, format='integer-quadratic-family-v9', variables=272,
                  source={'construction': 'quartic-family273', 'sha256': PIN},
                  coordinates=coordinates, residuals=residuals)
    polynomial = {'format': 'integer-quartic-family-v9', 'variables': 272, 'degree': 4,
                  'inputCoordinate': 1, 'fixedParameter': source['fixedParameter'],
                  'coordinates': coordinates, 'terms': terms(expanded)}
    report = {'status': 'Exact polynomial specification; same rational projection as the 273-coordinate family for every coefficient parameter.',
              'variables': 272, 'quadraticResiduals': 246, 'degree': 4,
              'symbolicTerms': len(expanded),
              'ordinaryMonomialsForEveryPositiveParameter': len(ordinary),
              'sourceSha256': PIN, 'removedSourceCoordinates': [20022],
              'removedSourceRows': [20022], 'changedSourceRows': [347, 348, 20020, 20021],
              'contactEvaluation': {'detector': 1, 'basisExponents': [0, 1, 2, 4, 5],
                  'coordinateCount': 5, 'contactCoefficients': [str(c) for c in contact],
                  'squareRoot10Coefficients': [str(c) for c in square_root],
                  'remainder9Coefficients': [str(c) for c in remainder],
                  'identity': 'F20(t)=S10(t)^2+R9(t)',
                  'lowerBoundForSequentialQuadraticEvaluation': 5,
                  'domain': 'Every rational input, with no divisions by variables'},
              'constantCoefficientMaximum': str(maximum),
              'constantCoefficientMaximumBits': maximum.bit_length(),
              'linearCoefficientMultiplierMaximum': multiplier,
              'heightFormulaForEveryPositiveParameter': 'max(C,A^2+1)',
              'exactHeightThresholdN': threshold,
              'exactHeightForNAtLeastThreshold': '80989^(4*N+2)+1',
              'effectiveness': 'Every sufficiently large N; arithmetic defining threshold remains ineffective.'}
    output = output_root/'family272'
    output.mkdir(parents=True, exist_ok=True)
    for filename, data in [('quadratic-family272.json', system), ('polynomial-family272.json', polynomial),
                           ('construction-report272.json', report)]:
        (output/filename).write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ['variables', 'quadraticResiduals', 'degree', 'symbolicTerms',
        'ordinaryMonomialsForEveryPositiveParameter', 'constantCoefficientMaximumBits', 'exactHeightThresholdN']}))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', type=Path, default=HERE)
    parser.add_argument('--output-root', type=Path, default=HERE)
    args = parser.parse_args()
    build(args.source_root, args.output_root)
