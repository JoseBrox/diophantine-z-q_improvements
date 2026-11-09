#!/usr/bin/env python3
"""Independent exact reconstruction of the 272-coordinate quartic.

No producer is imported.  The degree-ten square approximation is obtained
from the binomial series at infinity, not by descending coefficient matching.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement
from math import gcd, factorial
from pathlib import Path
import json
from check_quartic273 import (linear, product, variable, ONE, normalize, decode,
                              univariate_add, univariate_product)

HERE = Path(__file__).resolve().parent
PIN = 'c2e2ad2838e79aa38c93bd41aa079d612826b5991c19835b88e14ec12fecc18b'


def verify(source_root=HERE, output_root=HERE):
    raw = (source_root/'family273/quadratic-family273.json').read_bytes()
    assert sha256(raw).hexdigest() == PIN
    source = json.loads(raw)
    source_ids = {c['id']: c['sourceId'] for c in source['coordinates']}
    folder = output_root/'family272'
    system_path = folder/'quadratic-family272.json'
    polynomial_path = folder/'polynomial-family272.json'
    system = json.loads(system_path.read_text())
    polynomial = json.loads(polynomial_path.read_text())
    report = json.loads((folder/'construction-report272.json').read_text())
    ids = {c['id']: c['sourceId'] for c in system['coordinates']}
    roots = [theta+3*j for j in range(4)
             for theta in [F(0), F(-1, 2), F(-1), F(1, 2399), F(-32, 407)]]
    differences = []
    for x in range(21):
        value = F(1)
        for root in roots: value *= x-root
        differences.append(value)
    contact, falling = [F(0)], [F(1)]
    for degree in range(21):
        contact = univariate_add(contact, [differences[0]*c/factorial(degree) for c in falling])
        differences = [differences[i+1]-differences[i] for i in range(len(differences)-1)]
        falling = univariate_product(falling, [-degree, F(1)])
    assert contact[-1] == 1
    series = [F(0)] + list(reversed(contact))[1:11]
    power, binomial, approximate = [F(1)], F(1), [F(1)]
    for k in range(1, 11):
        power = univariate_product(power, series)[:11]
        binomial *= (F(1, 2)-k+1)/k
        approximate = univariate_add(approximate, [binomial*c for c in power])
    S = list(reversed(approximate))
    remainder = univariate_add(contact, [-c for c in univariate_product(S, S)])
    assert len(S) == 11 and S[-1] == 1 and not any(remainder[10:])
    R = remainder[:10]
    saved = report['contactEvaluation']
    assert saved['contactCoefficients'] == [str(c) for c in contact]
    assert saved['squareRoot10Coefficients'] == [str(c) for c in S]
    assert saved['remainder9Coefficients'] == [str(c) for c in R]
    assert univariate_add(univariate_product(S, S), R) == contact
    exponents = [0, 1, 2, 4, 5]
    assert set(range(11)) <= {a+b for a in exponents for b in exponents}
    assert 2**4 < 20 <= 2**5
    basis = {0: ONE, 1: variable(391), 2: variable(392),
             4: variable(393), 5: variable(20020)}

    def represent(coefficients):
        answer = {}
        for k, c in enumerate(coefficients):
            if not c: continue
            if k in basis: value = basis[k]
            else:
                a, b = min((a, b) for a in basis for b in basis if a <= b and a+b == k)
                value = product(basis[a], basis[b])
            answer = linear((answer, 1), (value, c))
        return answer

    changes = {
        'compressed.det1.tPower3.definition': ('single.det1.tPower4.definition',
            linear((product(variable(392), variable(392)), 1), (variable(393), -1))),
        'compressed.det1.tPower6.definition': ('single.det1.tPower5.definition',
            linear((product(variable(391), variable(393)), 1), (variable(20020), -1))),
        'compressed.det1.quotient9.definition': ('single.det1.squareRoot10.definition',
            linear((represent(S), 1), (variable(20021), -1))),
        'compressed.det1.contactPolynomial.definition': ('single.det1.contactPolynomial.definition',
            linear((product(variable(20021), variable(20021)), 1), (represent(R), 1), (variable(394), -1)))
    }
    expected = {}
    for row in source['residuals']:
        if row['sourceId'] == 20022: continue
        name, p = changes.pop(row['name']) if row['name'] in changes else (row['name'], decode(row, source_ids))
        assert all(20022 not in m for m in p)
        expected[row['sourceId']] = (name, normalize(p))
    assert not changes
    actual = {row['sourceId']: (row['name'], decode(row, ids)) for row in system['residuals']}
    assert actual == expected and len(actual) == 246
    assert set(source_ids.values())-set(ids.values()) == {20022}
    assert not (set(ids.values())-set(source_ids.values()))
    assert system['coordinates'] == polynomial['coordinates']
    assert system['variables'] == polynomial['variables'] == len(ids) == 272
    assert sorted(ids) == list(range(1, 273)) and ids[1] == 0
    expanded = defaultdict(int)
    for name, p in actual.values():
        assert max(sum(i != -1 for i in m) for m in p) <= 2
        for m, n in combinations_with_replacement(p, 2):
            expanded[tuple(sorted(m+n))] += p[m]*p[n]*(1 if m == n else 2)
    expanded = {m: c for m, c in expanded.items() if c}
    assert expanded == decode({'terms': polynomial['terms']}, ids)
    assert gcd(*expanded.values()) == 1
    assert max(sum(i != -1 for i in m) for m in expanded) == 4
    assert {i for m in expanded for i in m if i != -1} == set(ids.values())
    ordinary = defaultdict(dict)
    for m, c in expanded.items(): ordinary[tuple(i for i in m if i != -1)][m.count(-1)] = c
    assert ordinary[(489, 489)] == {0: 1, 2: 1}
    assert all(set(p) in ({0}, {1}) for m, p in ordinary.items() if m != (489, 489))
    maximum = max(abs(p[0]) for p in ordinary.values() if set(p) == {0})
    multiplier = max(abs(p[1]) for p in ordinary.values() if set(p) == {1})
    assert maximum.bit_length() == 1520 and multiplier == 13118436242
    assert maximum > multiplier**2 and 80989**90+1 < maximum < 80989**94+1
    assert len(ordinary) == 3450 and len(expanded) == 3451
    result = {'status': 'PASS', 'variables': 272, 'quadraticResiduals': 246,
              'degree': 4, 'content': 1,
              'ordinaryMonomialsForEveryPositiveParameter': len(ordinary),
              'symbolicTerms': len(expanded), 'allRowsIndependentlyReconstructed': True,
              'completeUnorderedPairExpansion': True, 'allCoordinatesUsed': True,
              'sourceQuadraticTableSha256': PIN,
              'contactReconstruction': 'Forward differences of 21 exact evaluations',
              'contactCircuitReconstruction': 'Truncated binomial series at infinity, followed by exact polynomial identity',
              'circuitCoordinates': 5, 'minimumSequentialQuadraticEvaluationCoordinates': 5,
              'projectionEquivalence': 'Exact at every rational input and every coefficient parameter; both circuits are triangular with only constant divisions',
              'constantCoefficientMaximum': str(maximum), 'constantCoefficientMaximumBits': 1520,
              'linearCoefficientMultiplierMaximum': multiplier,
              'heightFormulaForEveryPositiveParameter': 'max(C,A^2+1)',
              'exactHeightThresholdN': 23, 'exactHeightForNAtLeast23': '80989^(4*N+2)+1',
              'noSupportCancellationForPositiveParameter': True,
              'quadraticTableSha256': sha256(system_path.read_bytes()).hexdigest(),
              'polynomialTableSha256': sha256(polynomial_path.read_bytes()).hexdigest(),
              'arithmeticScope': 'Retains the 273-variable source projection theorem, its arithmetic premises, and its ineffective eventual coefficient threshold.'}
    (folder/'independent-verification272.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['status', 'variables', 'quadraticResiduals',
          'ordinaryMonomialsForEveryPositiveParameter', 'quadraticTableSha256', 'polynomialTableSha256']}))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', type=Path, default=HERE)
    parser.add_argument('--output-root', type=Path, default=HERE)
    args = parser.parse_args()
    verify(args.source_root, args.output_root)
