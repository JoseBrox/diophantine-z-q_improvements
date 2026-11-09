#!/usr/bin/env python3
"""Independent reconstruction of the balanced 259-variable quartic family.

No producer is imported. The degree-ten contact polynomial is recovered
by finite differences, and its degree-twenty identity is checked separately.
All rational arithmetic, exceptional-prime factorizations and coefficient
expansions use the Python standard library.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, product as cartesian_product
from math import factorial, gcd, prod
from pathlib import Path
import json
from check_quartic273 import (linear, product, variable, ONE, normalize, decode,
                              univariate_add, univariate_product)

HERE = Path(__file__).resolve().parent
PIN = '54c242476e796404131eb09099bd2c134adf2358e1129a112cd2b47f996ab6c7'


def factor_integer(n):
    n = abs(n)
    answer = {}
    trial = 2
    while trial*trial <= n:
        exponent = 0
        while n % trial == 0:
            n //= trial
            exponent += 1
        if exponent: answer[trial] = exponent
        trial += 1
    if n > 1: answer[n] = 1
    return answer


def evaluate(p, x):
    result = F(0)
    for coefficient in reversed(p): result = result*x+coefficient
    return result


def valuation(x, prime):
    assert x and prime > 1
    numerator, denominator = abs(x.numerator), x.denominator
    result = 0
    while numerator % prime == 0:
        numerator //= prime
        result += 1
    while denominator % prime == 0:
        denominator //= prime
        result -= 1
    return result


def check_local_packing():
    # Entries are (test, test power, weight power, even valuation).
    factors = [
        [('C2', 2, 19, False), ('H', 2, 10, True), ('B1', 4, 4, True)],
        [('G', 2, 19, False), ('A3', 2, 2, True), ('B0', 4, 4, True)],
        [('I', 4, 19, False), ('A2', 2, 1, True), ('A4', 2, 2, True), ('B3', 4, 4, True)],
        [('C3', 2, 19, False), ('C1', 4, 10, False), ('B4', 4, 4, True)],
        [('C4', 2, 19, False), ('A1', 2, 2, True), ('B2', 4, 4, True)]]
    checked = 0
    bounds = {}
    complete_orders = {'C1': 4, 'C2': 10, 'C3': 10, 'C4': 10,
                       'G': 10, 'I': 5, 'H': 6}
    complete_orders.update({name+str(i): 2 for name, indices in
                            [('A', range(1, 5)), ('B', range(5))] for i in indices})
    positive_term_valuations = []
    for factor in factors:
        for nu in (1, 3, 5, 7):
            residue_ranges = [range(0, 8, 2 if even else 1)
                              for _, _, _, even in factor]
            for values in cartesian_product(*residue_ranges):
                residues = [0]+[(power*v-weight*nu) % 8
                                 for (_, power, weight, _), v in zip(factor, values)]
                assert len(set(residues)) == len(residues)
                checked += 1
        positive_term_valuations.append([])
        for name, power, weight, even in factor:
            bound = F(2*weight-1, 2*power)
            minimum = bound.numerator//bound.denominator+1
            if even and minimum % 2:
                minimum += 1
            bounds[name] = {'strictLowerBoundDividedByNu': str(bound),
                            'minimumIntegralOrder': minimum,
                            'valuationEven': even}
            term_value = power*complete_orders[name]-weight
            assert term_value > 0
            positive_term_valuations[-1].append(term_value)
    assert checked == 4608
    assert all(bounds[name]['minimumIntegralOrder'] == 10
               for name in ('C2', 'C3', 'C4', 'G'))
    assert bounds['I']['minimumIntegralOrder'] == 5
    assert bounds['C1']['minimumIntegralOrder'] == 3
    assert bounds['H']['minimumIntegralOrder'] == 6
    assert 12 >= 10 and F(19, 4)*4/10 == F(19, 10) < 2
    return {'completeValuationResidueCases': checked,
            'zeroTests': 'Omitting terms preserves distinctness of the remaining residues.',
            'extractionBounds': bounds,
            'sufficientCompletenessOrders': complete_orders,
            'positiveCompletenessTermValuations': positive_term_valuations,
            'formalApproximationOrder': 12,
            'integralLucasResidualOrder': 10,
            'lucasHeightExponent': '19/10',
            'inputResidualOrder': 3}


def verify(source_root=HERE, output_root=HERE):
    raw = (source_root/'family267/quadratic-family267.json').read_bytes()
    assert sha256(raw).hexdigest() == PIN
    source = json.loads(raw)
    source_ids = {c['id']: c['sourceId'] for c in source['coordinates']}
    folder = output_root/'family259_v17'
    system_path = folder/'quadratic-family259-v17.json'
    polynomial_path = folder/'polynomial-family259-v17.json'
    system = json.loads(system_path.read_text())
    polynomial = json.loads(polynomial_path.read_text())
    report = json.loads((folder/'construction-report259-v17.json').read_text())
    ids = {c['id']: c['sourceId'] for c in system['coordinates']}

    theta = [F(0), F(-1, 2), F(-1), F(1, 2399), F(-32, 407)]
    affine_maps = [(1, 0), (-1, 2), (1, -5), (-1, -3)]
    groups = [[(root-b)/a for root in theta] for a, b in affine_maps]
    roots = sorted(sum(groups, []))
    assert len(set(roots)) == 20 and F(1) not in roots
    assert sorted(2-root for root in roots) == roots
    squared_roots = sorted({(root-1)**2 for root in roots})
    assert len(squared_roots) == 10

    # Independent Newton interpolation, rather than coefficient multiplication.
    values = [prod(F(i)-root for root in squared_roots) for i in range(11)]
    contact = [F(0)]
    falling = [F(1)]
    for degree in range(11):
        contact = univariate_add(contact, [values[0]*c/factorial(degree) for c in falling])
        values = [values[i+1]-values[i] for i in range(len(values)-1)]
        falling = univariate_product(falling, [-degree, F(1)])
    assert len(contact) == 11 and contact[-1] == 1
    assert all(evaluate(contact, root) == 0 for root in squared_roots)
    direct_twenty = [F(1)]
    for root in roots: direct_twenty = univariate_product(direct_twenty, [-root, F(1)])
    composed = [F(0)]
    for coefficient in reversed(contact):
        composed = univariate_add(univariate_product(composed, [1, -2, 1]), [coefficient])
    while composed and not composed[-1]: composed.pop()
    assert composed == direct_twenty

    bad_primes = set()
    extra_witnesses = defaultdict(set)
    values_to_factor = ([root for root in roots if root]
                        + [1-root for root in roots]
                        + [a-b for a, b in combinations(roots, 2)])
    for value in values_to_factor:
        assert value
        for integer in (abs(value.numerator), value.denominator):
            factors = factor_integer(integer)
            assert prod(prime**power for prime, power in factors.items()) == integer
            bad_primes.update(factors)
            for prime in factors:
                if prime > 76176: extra_witnesses[prime].add(str(value))
    extra = sorted(prime for prime in bad_primes if prime > 76176)
    assert extra == [247957, 368323, 2029147]
    F_one = evaluate(direct_twenty, F(1))
    assert F_one == contact[0] != 0
    F_one_factors = factor_integer(F_one.numerator)
    assert all(prime <= 76176 for prime in F_one_factors)
    height_matrices = []
    for a, b in affine_maps:
        forward = [[2*a, 2*b+1], [a, b]]
        inverse_projective = [[b, -(2*b+1)], [-a, 2*a]]
        assert forward[0][0]*forward[1][1]-forward[0][1]*forward[1][0] == -a
        assert [[sum(forward[i][k]*inverse_projective[k][j] for k in range(2))
                 for j in range(2)] for i in range(2)] == [[-a, 0], [0, -a]]
        height_matrices.append({'affineMap': [a, b], 'contactMobiusMatrix': forward,
                                'inverseProjectiveMatrix': inverse_projective,
                                'maximumAbsoluteRowSum': max(sum(map(abs, row)) for row in inverse_projective)})
    assert [item['maximumAbsoluteRowSum'] for item in height_matrices] == [3, 7, 14, 8]

    gamma = F(408, 409)
    real_limit = gamma**2/4
    prepared_valuations = [2*valuation(gamma, p)+2*valuation(F(1, 2), p)
                          for p in (2, 3, 17)]
    assert prepared_valuations == [4, 2, 2] and 0 < real_limit < 17
    gamma_bad_primes = sorted(set(factor_integer(gamma.numerator))
                             | set(factor_integer(gamma.denominator)))
    assert gamma_bad_primes == [2, 3, 17, 409]
    assert max(gamma_bad_primes) < 76176
    # R=product(1-s/δ²), so the first term of q=R^-1-1 is positive.
    assert contact[-2] == -sum(squared_roots) < 0
    assert report['gamma'] == str(gamma)
    assert report['preparedPoleValuationsAt2_3_17'] == prepared_valuations
    assert report['realPoleInputLimit'] == str(real_limit)

    removed_coordinates = {350, 398, 20002, 20022, 384, 432, 355, 403}
    removed_rows = {302, 352, 20002, 20022, 336, 386, 544, 550}
    changes = {}
    renames = {360: 'detector0.weightPower19', 408: 'detector1.weightPower19'}
    for d in range(2):
        t, r, r2, ff, r4, r5, q, tau, pole = (
            (37, 346, 347, 348, 20000, 20001, 352, 383, 385) if d == 0 else
            (391, 392, 393, 394, 20020, 20021, 400, 431, 433))
        basis = {0: ONE, 1: variable(r), 2: variable(r2), 4: variable(r4), 5: variable(r5)}
        assert {i+j for i in basis for j in basis} == set(range(11))
        expression = {}
        for degree, coefficient in enumerate(contact):
            if not coefficient: continue
            if degree in basis: term = basis[degree]
            else:
                i, j = min((i, j) for i in basis for j in basis if i <= j and i+j == degree)
                term = product(basis[i], basis[j])
            expression = linear((expression, 1), (term, coefficient))
        delta = linear((variable(t), 1), (ONE, -1))
        prefix = 'symmetric.detector'+str(d)
        q19, q10 = (360, 369) if d == 0 else (408, 417)
        changes.update({
            526+7*d: ('balanced.detector'+str(d)+'.weightPower19.definition',
                      linear((product(variable(q), variable(q19)), 1),
                             (product(variable(q10), variable(q10)), -1))),
            298+48*d: (prefix+'.deltaSquared.definition', linear((product(delta, delta), 1), (variable(r), -1))),
            299+48*d: (prefix+'.deltaFourthPower.definition', linear((product(variable(r), variable(r)), 1), (variable(r2), -1))),
            20000+20*d: (prefix+'.deltaEighthPower.definition', linear((product(variable(r2), variable(r2)), 1), (variable(r4), -1))),
            20001+20*d: (prefix+'.deltaTenthPower.definition', linear((product(variable(r), variable(r4)), 1), (variable(r5), -1))),
            300+48*d: (prefix+'.contactPolynomial.definition', linear((expression, 1), (variable(ff), -1))),
            304+50*d: ('balanced.detector'+str(d)+'.weight.definition',
                       linear((product(variable(ff), linear((ONE, 1), (variable(q), 1))), 1),
                              (product(variable(r5), variable(r5)), -1))),
            337+50*d: ('balanced.detector'+str(d)+'.poleInput.definition',
                       linear((product(linear((ONE, 1), (variable(q), 1)), variable(pole)), 1),
                              (product(variable(tau), variable(tau)), -F(408, 409)**2)))})
        for sid, suffix in [(r, 'deltaSquared'), (r2, 'deltaFourthPower'), (r4, 'deltaEighthPower'),
                            (r5, 'deltaTenthPower'), (ff, 'contactPolynomial')]:
            renames[sid] = prefix+'.'+suffix
    expected = {}
    for row in source['residuals']:
        sid = row['sourceId']
        if sid in removed_rows: continue
        name, expression = changes.pop(sid) if sid in changes else (row['name'], decode(row, source_ids))
        assert all(not removed_coordinates.intersection(m) for m in expression)
        expected[sid] = (name, normalize(expression))
    assert not changes
    actual = {row['sourceId']: (row['name'], decode(row, ids)) for row in system['residuals']}
    assert actual == expected and len(actual) == 233
    expected_coordinates = [dict(c, id=i+1, name=renames.get(c['sourceId'], c['name']))
                            for i, c in enumerate(c for c in source['coordinates']
                                                  if c['sourceId'] not in removed_coordinates)]
    assert system['coordinates'] == polynomial['coordinates'] == expected_coordinates
    assert system['variables'] == polynomial['variables'] == len(ids) == 259
    assert sorted(ids) == list(range(1, 260)) and ids[1] == 0

    expanded = defaultdict(int)
    for name, row in actual.values():
        assert max(sum(i != -1 for i in m) for m in row) <= 2
        for m, n in combinations_with_replacement(row, 2):
            expanded[tuple(sorted(m+n))] += row[m]*row[n]*(1 if m == n else 2)
    expanded = {m: c for m, c in expanded.items() if c}
    assert expanded == decode({'terms': polynomial['terms']}, ids)
    assert gcd(*expanded.values()) == 1 and max(sum(i != -1 for i in m) for m in expanded) == 4
    assert {i for m in expanded for i in m if i != -1} == set(ids.values())
    ordinary = defaultdict(dict)
    for m, c in expanded.items(): ordinary[tuple(i for i in m if i != -1)][m.count(-1)] = c
    assert ordinary[(489, 489)] == {0: 1, 2: 1}
    assert all(set(p) in ({0}, {1}) for m, p in ordinary.items() if m != (489, 489))
    C = max(abs(p[0]) for p in ordinary.values() if set(p) == {0})
    L = max(abs(p[1]) for p in ordinary.values() if set(p) == {1})
    assert C.bit_length() == 1520 and L == 13118436242 and C > L*L
    assert 80989**90+1 < C < 80989**94+1
    assert len(ordinary) == 3308 and len(expanded) == 3309
    assert report['variables'] == 259 and report['quadraticResiduals'] == 233
    assert report['ordinaryMonomialsForEveryPositiveParameter'] == len(ordinary)
    assert report['symbolicTerms'] == len(expanded)
    assert report['constantCoefficientMaximum'] == str(C)
    assert report['linearCoefficientMultiplierMaximum'] == L
    assert report['exactHeightThresholdN'] == 23
    local_packing = check_local_packing()
    result = {
        'status': 'PASS', 'variables': 259, 'quadraticResiduals': 233, 'degree': 4, 'content': 1,
        'ordinaryMonomialsForEveryPositiveParameter': 3308, 'symbolicTerms': 3309,
        'allRowsIndependentlyReconstructed': True, 'completeUnorderedPairExpansion': True,
        'allCoordinatesUsed': True, 'sourceQuadraticTableSha256': PIN,
        'contactPolynomialReconstruction': 'Exact Newton interpolation at 11 values, all ten roots, and independent degree-twenty composition identity.',
        'contactGroups': [[str(x) for x in group] for group in groups],
        'extraExceptionalPrimesAbove76176': extra,
        'extraPrimeWitnesses': {str(prime): sorted(values) for prime, values in extra_witnesses.items()},
        'completeContactBadPrimeSet': sorted(bad_primes),
        'normalizingValueF1': str(F_one),
        'normalizingNumeratorFactorization': {str(prime): power for prime, power in F_one_factors.items()},
        'normalizingContactRadicalIsOne': True,
        'heightMobiusMatrices': height_matrices,
        'contactHeightBound': 'h(t)<=log(14)+H*E^19*M(t)^(19/4), E=247957*368323*2029147',
        'exceptionalPrimeProduct': str(prod(extra)),
        'normalization': {'equations': ['r=(t-1)^2', 'F*(1+q)=(r^5)^2',
                                        '(1+q)*b=(408/409)^2*tau^2'],
                          'R': 'F20(t)/(t-1)^20', 'q': '(t-1)^20/F20(t)-1',
                          'zeroStrata': 'F=0 is impossible. If q=0 or t=1, the contact radical is1; no reciprocal interpretation is used on these strata.'},
        'gamma': str(gamma),
        'gammaPrimeDivisors': gamma_bad_primes,
        'preparedPoleValuationsAt2_3_17': prepared_valuations,
        'realPoleInputLimit': str(real_limit),
        'positiveLeadingRealCoefficientOfWeight': str(sum(squared_roots)),
        'weightRelations': ['q2=q^2', 'q4=q2^2', 'q5=q*q4', 'q10=q5^2', 'q*q19=q10^2'],
        'localPackingCertificate': local_packing,
        'constantCoefficientMaximum': str(C), 'constantCoefficientMaximumBits': 1520,
        'linearCoefficientMultiplierMaximum': L,
        'heightFormulaForEveryPositiveParameter': 'max(C,A^2+1)',
        'exactHeightThresholdN': 23, 'exactHeightForNAtLeast23': '80989^(4*N+2)+1',
        'quadraticTableSha256': sha256(system_path.read_bytes()).hexdigest(),
        'polynomialTableSha256': sha256(polynomial_path.read_bytes()).hexdigest(),
        'arithmeticScope': 'Finite coefficient and contact verification. The projection proof still uses the stated inherited arithmetic premises and an ineffective sufficient parameter.'}
    (folder/'independent-verification259-v17.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['status', 'variables', 'quadraticResiduals',
                                          'ordinaryMonomialsForEveryPositiveParameter',
                                          'extraExceptionalPrimesAbove76176',
                                          'quadraticTableSha256', 'polynomialTableSha256']}))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', type=Path, default=HERE)
    parser.add_argument('--output-root', type=Path, default=HERE)
    args = parser.parse_args()
    verify(args.source_root, args.output_root)
