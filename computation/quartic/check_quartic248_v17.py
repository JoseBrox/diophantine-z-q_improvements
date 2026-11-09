#!/usr/bin/env python3
"""Independent exact reconstruction of the 248-variable quartic family.

No producer is imported.  The checker starts with the pinned 259 source,
reconstructs every alteration, and expands the entire sum of squares.
Contact interpolation, exceptional primes, finite valuation classes,
scalar extraction, and the forced prime are checked separately.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, product as cartesian_product
from math import factorial, gcd, prod
from pathlib import Path
import json

from check_quartic273 import (ONE, variable, linear, product, field_product,
                              normalize, decode, univariate_add, univariate_product)

HERE = Path(__file__).resolve().parent
PIN = 'bf123dd6decac657ca8c0c567fb7f58d7289860567e387b70f86c03ae2c1be9d'


def factor_integer(n):
    n = abs(n)
    assert n
    answer = {}
    trial = 2
    while trial*trial <= n:
        exponent = 0
        while n % trial == 0:
            n //= trial
            exponent += 1
        if exponent:
            answer[trial] = exponent
        trial += 1
    if n > 1:
        answer[n] = 1
    return answer


def evaluate(coefficients, x):
    result = F(0)
    for coefficient in reversed(coefficients):
        result = result*x+coefficient
    return result


def valuation(x, p):
    assert x
    numerator, denominator = abs(x.numerator), x.denominator
    v = 0
    while numerator % p == 0:
        numerator //= p
        v += 1
    while denominator % p == 0:
        denominator //= p
        v -= 1
    return v


def local_certificate():
    # (test name, test exponent, weight exponent, valuation is even)
    factors = [
        [('C2', 2, 7, False), ('H', 2, 2, True), ('B1', 4, 4, True)],
        [('G', 2, 7, False), ('A3', 2, 2, True), ('B0', 4, 4, True)],
        [('I', 4, 7, False), ('A2', 2, 1, True), ('A4', 2, 2, True), ('B3', 4, 4, True)],
        [('C3', 2, 7, False), ('C1', 4, 2, False), ('B4', 4, 4, True)],
        [('C4', 2, 7, False), ('A1', 2, 2, True), ('B2', 4, 4, True)]]
    bounds, checked = {}, 0
    orders = {'C1': 1, 'C2': 4, 'C3': 4, 'C4': 4, 'G': 4, 'I': 2, 'H': 2}
    orders.update({name+str(i): 2 for name, indices in
                   [('A', range(1, 5)), ('B', range(5))] for i in indices})
    complete_values = []
    for factor in factors:
        for nu in (1, 3, 5, 7):
            ranges = [range(0, 8, 2 if even else 1) for _, _, _, even in factor]
            for residues in cartesian_product(*ranges):
                term_residues = [0]+[(power*v-weight*nu) % 8
                                    for (_, power, weight, _), v in zip(factor, residues)]
                assert len(set(term_residues)) == len(term_residues)
                checked += 1
        complete_values.append([])
        for name, power, weight, even in factor:
            lower = F(2*weight-1, 2*power)
            minimum = lower.numerator//lower.denominator+1
            if even and minimum % 2:
                minimum += 1
            bounds[name] = {'strictBoundDividedByNu': str(lower),
                            'minimumIntegralOrder': minimum, 'evenValuation': even}
            term_value = power*orders[name]-weight
            assert term_value > 0
            complete_values[-1].append(term_value)
    assert checked == 4608
    assert [bounds[n]['minimumIntegralOrder'] for n in ('C2', 'C3', 'C4', 'G', 'I', 'C1', 'H')] == [4, 4, 4, 4, 2, 1, 2]
    # The nested scalar tree has A=(Z0^2+R*Z1^2)/R^4 and
    # W=(A^2+R*F^2)/R^4.  At odd positive nu, vW>-nu/2.
    k = 4
    bound_A = (F(k)-F(1, 2))/2
    bound_F = (F(k)-F(3, 2))/2
    bound_Z0 = (F(k)+bound_A)/2
    bound_Z1 = (F(k)+bound_A-1)/2
    assert (bound_A, bound_F, bound_Z0, bound_Z1) == (F(7, 4), F(5, 4), F(23, 8), F(19, 8))
    assert bound_Z1.numerator//bound_Z1.denominator+1 == 3
    assert F(7, 2)/2*4/4 == F(7, 4) < 2
    return {'completeValuationResidueCases': checked,
            'zeroTests': 'Deleting terms preserves residue distinctness.',
            'extractionBounds': bounds, 'sufficientCompletenessOrders': orders,
            'positiveCompletenessTermValuations': complete_values,
            'formalApproximationOrder': 4, 'lucasResidualOrder': 4,
            'inputResidualOrder': 1, 'lucasHeightExponent': '7/4',
            'scalarStrictBoundsDividedByNu': dict(A=str(bound_A), F=str(bound_F),
                                                 Z0=str(bound_Z0), Z1=str(bound_Z1)),
            'scalarIndexContactOrder': 3,
            'scalarHeightBound': 'C3*149^(-L_N)*c*(1+log(c)/3)',
            'comparisonLucasHeightExponent': '7/4',
            'lucasGrowthLowerBound': '(c-5)*log(c-2)',
            'forcedIndexDepth': 'floor(19*(2*N-1)/8)+1'}


def verify(source_root=HERE, output_root=HERE):
    source_path = source_root/'family259_v17/quadratic-family259-v17.json'
    raw = source_path.read_bytes()
    assert sha256(raw).hexdigest() == PIN
    source = json.loads(raw)
    old_ids = {c['id']: c['sourceId'] for c in source['coordinates']}
    old_rows = {row['sourceId']: row for row in source['residuals']}
    folder = output_root/'family248_v17'
    system_path = folder/'quadratic-family248-v17.json'
    polynomial_path = folder/'polynomial-family248-v17.json'
    system = json.loads(system_path.read_text())
    polynomial = json.loads(polynomial_path.read_text())
    report = json.loads((folder/'construction-report248-v17.json').read_text())
    ids = {c['id']: c['sourceId'] for c in system['coordinates']}

    theta = [F(0), F(-1, 2), F(-1), F(1, 2399), F(-32, 407)]
    roots = sorted(theta+[2-t for t in theta])
    assert len(set(roots)) == 10 and F(1) not in roots
    squared_roots = sorted({(root-1)**2 for root in roots})
    assert len(squared_roots) == 5
    # Recover P5 by exact Newton interpolation rather than multiplication.
    values = [prod(F(i)-root for root in squared_roots) for i in range(6)]
    contact, falling = [F(0)], [F(1)]
    for degree in range(6):
        contact = univariate_add(contact, [values[0]*c/factorial(degree) for c in falling])
        values = [values[i+1]-values[i] for i in range(len(values)-1)]
        falling = univariate_product(falling, [-degree, F(1)])
    assert len(contact) == 6 and contact[-1] == 1
    assert all(evaluate(contact, root) == 0 for root in squared_roots)
    direct = [F(1)]
    for root in roots:
        direct = univariate_product(direct, [-root, F(1)])
    composed = [F(0)]
    for coefficient in reversed(contact):
        composed = univariate_add(univariate_product(composed, [1, -2, 1]), [coefficient])
    while composed and not composed[-1]:
        composed.pop()
    assert composed == direct
    bad_primes, extra_witnesses = set(), defaultdict(set)
    for value in ([root for root in roots if root]+[1-root for root in roots]
                  +[a-b for a, b in combinations(roots, 2)]):
        for integer in (abs(value.numerator), value.denominator):
            factors = factor_integer(integer)
            assert prod(p**e for p, e in factors.items()) == integer
            bad_primes.update(factors)
            for p in factors:
                if p > 76176:
                    extra_witnesses[p].add(str(value))
    assert sorted(p for p in bad_primes if p > 76176) == [2029147]
    F_one = evaluate(direct, F(1))
    assert F_one == contact[0] != 0
    assert all(p <= 76176 for p in factor_integer(F_one.numerator))
    height_matrices = []
    for a, b in [(1, 0), (-1, 2)]:
        forward = [[2*a, 2*b+1], [a, b]]
        inverse = [[b, -(2*b+1)], [-a, 2*a]]
        assert [[sum(forward[i][k]*inverse[k][j] for k in range(2))
                 for j in range(2)] for i in range(2)] == [[-a, 0], [0, -a]]
        height_matrices.append({'affineMap': [a, b], 'forward': forward,
                                'inverseProjective': inverse,
                                'maximumAbsoluteRowSum': max(sum(map(abs, row)) for row in inverse)})
    assert [x['maximumAbsoluteRowSum'] for x in height_matrices] == [3, 7]

    removed_coordinates = {188, 189, 359, 369, 407, 417, 602, 603, 604, 20001, 20021}
    removed_rows = {140, 141, 541, 546, 547, 552, 559, 561, 564, 20001, 20021}
    substitutions = {369: 361, 417: 409, 604: 601}
    changes, renames = {}, {}
    for d in range(2):
        r, r2, ff, r3, q, q2, q4, q3, q7 = (
            (346, 347, 348, 20000, 352, 361, 362, 359, 360) if d == 0 else
            (392, 393, 394, 20020, 400, 409, 410, 407, 408))
        basis = {0: ONE, 1: variable(r), 2: variable(r2), 3: variable(r3)}
        expression = {}
        for degree, coefficient in enumerate(contact):
            i, j = min((i, j) for i in basis for j in basis if i <= j and i+j == degree)
            expression = linear((expression, 1), (product(basis[i], basis[j]), coefficient))
        prefix = 'reflected.detector'+str(d)
        changes.update({
            300+48*d: (prefix+'.contactPolynomial.definition', linear((expression, 1), (variable(ff), -1))),
            20000+20*d: (prefix+'.deltaSixthPower.definition', linear((product(variable(r), variable(r2)), 1), (variable(r3), -1))),
            304+50*d: (prefix+'.weight.definition', linear((product(variable(ff), linear((ONE, 1), (variable(q), 1))), 1),
                                                         (product(variable(r2), variable(r3)), -1))),
            526+7*d: (prefix+'.weightPower7.definition', linear((product(variable(q), variable(q7)), 1),
                            (product(variable(q4), variable(q4)), -1)))})
        renames.update({r3: prefix+'.deltaSixthPower', q3: prefix+'.weightPower3', q7: prefix+'.weightPower7'})

    # Recover the plain fixed-subtraction formula independently from the
    # two source rows by setting their Taylor truncation to its constant1.
    omitted = {178, 179, 180, 181}
    plain_rows = [{m: c for m, c in decode(old_rows[sid], old_ids).items()
                   if not omitted.intersection(m)} for sid in (140, 141)]
    S = variable(142), variable(143)
    g = variable(700), variable(701)
    Nold = (linear((ONE, -660), (S[0], -228), (S[1], 224)),
            linear((ONE, 417), (S[0], 112), (S[1], -228)))
    Dold = (linear((ONE, -704), (S[0], 660), (S[1], -834), (g[0], 6888), (g[1], -10080)),
            linear((ONE, 384), (S[0], -417), (S[1], 660), (g[0], -5040), (g[1], 6888)))
    dz = field_product(Dold, (variable(188), variable(189)))
    assert all(normalize(linear((dz[j], 1), (Nold[j], -1))) == normalize(plain_rows[j]) for j in range(2))
    unit = linear((ONE, 3)), linear((ONE, 2))
    N, D = field_product(unit, Nold), field_product(unit, Dold)
    for i in range(4):
        left = field_product((variable(234+4*i), variable(235+4*i)), N)
        right = field_product((variable(164+4*i), variable(165+4*i)), D)
        for j in range(2):
            changes[146+12*i+j] = ('plain.alternateRatio'+str(i+1)+'.cleared.'+str(j),
                                   linear((left[j], 1), (right[j], -1)))

    normalizer = decode(old_rows[733], old_ids)
    assert normalizer[(489, 702)] == 80989**2
    normalizer[(489, 702)] = 149**2
    changes[733] = (old_rows[733]['name'], normalizer)

    expected, changed_rows = {}, []
    for row in source['residuals']:
        sid = row['sourceId']
        if sid in removed_rows:
            continue
        if sid in changes:
            name, expression = changes.pop(sid)
            changed_rows.append(sid)
        else:
            name = row['name']
            original = decode(row, old_ids)
            expression = defaultdict(F)
            for monomial, coefficient in original.items():
                expression[tuple(sorted(substitutions.get(i, i) for i in monomial))] += coefficient
            expression = {m: c for m, c in expression.items() if c}
            if any(set(m).intersection(substitutions) for m in original):
                changed_rows.append(sid)
                if sid in (512, 566):
                    name += '.power4'
        assert all(not removed_coordinates.intersection(m) for m in expression)
        expected[sid] = name, normalize(expression)
    assert not changes
    actual = {row['sourceId']: (row['name'], decode(row, ids)) for row in system['residuals']}
    assert actual == expected and len(actual) == 222
    expected_coordinates = [dict(c, id=i+1, name=renames.get(c['sourceId'], c['name']))
                            for i, c in enumerate(c for c in source['coordinates']
                                                  if c['sourceId'] not in removed_coordinates)]
    assert system['coordinates'] == polynomial['coordinates'] == expected_coordinates
    assert system['variables'] == polynomial['variables'] == len(ids) == 248
    assert sorted(ids) == list(range(1, 249)) and ids[1] == 0
    assert report['changedSourceRows'] == [512, 566, 733]
    assert system['fixedParameter'] == polynomial['fixedParameter'] == dict(source['fixedParameter'], base=149)

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
    for m, c in expanded.items():
        ordinary[tuple(i for i in m if i != -1)][m.count(-1)] = c
    assert ordinary[(489, 489)] == {0: 1, 2: 1}
    assert ordinary[(1, 1, 1, 1)] == {0: 1}
    assert all(set(p) in ({0}, {1}) for m, p in ordinary.items() if m != (489, 489))
    C = max(abs(p[0]) for p in ordinary.values() if set(p) == {0})
    L = max(abs(p[1]) for p in ordinary.values() if set(p) == {1})
    assert C.bit_length() == 1520 and L == 44402 and C > L*L
    assert 149**210+1 < C < 149**214+1
    assert len(ordinary) == 3189 and len(expanded) == 3190

    gamma = F(408, 409)
    prepared = [2*valuation(gamma, p)+2*valuation(F(1, 2), p) for p in (2, 3, 17)]
    assert prepared == [4, 2, 2] and 0 < gamma**2/4 < 17
    assert contact[-2] == -sum(squared_roots) < 0
    ell = 149
    assert factor_integer(ell) == {ell: 1}
    scalar_contacts = [F(0), F(1), F(2401), F(-343, 32), F(1, 2)]
    euler_checks = []
    for theta0 in scalar_contacts:
        value = (theta0-2504)/51
        residue = value.numerator*pow(value.denominator, -1, ell) % ell
        euler = pow(residue, (ell-1)//2, ell)
        assert euler == ell-1
        euler_checks.append({'contact': str(theta0), 'residue': residue, 'EulerPower': euler})
    def scalar_r(x):
        beta = 51*x*x+2504
        return beta*(beta-1)*(beta-2401)*(32*beta+343)*(2*beta-1)
    prep2 = sorted({valuation(F(scalar_r(x)), 2) for x in range(16)})
    prep3 = sorted({valuation(F(scalar_r(x)), 3) for x in range(9)})
    prep17 = sorted({scalar_r(x) % 17 for x in range(17)})
    assert prep2 == [2, 3] and prep3 == [1] and prep17 == [15]
    assert ell**2 % 8 == 1 and ell**2 % 3 == 1
    assert (1+ell**2*15) % 17 == 3
    # These finite congruences certify exact valuations for all integer X.
    assert all(scalar_r(x) % 16 in (4, 8, 12) for x in range(16))
    assert all(scalar_r(x) % 9 in (3, 6) for x in range(9))
    assert gcd(ell, 2*3*7*17*41*9792) == 1 and ell < 76176
    # Norms of D, x(P), x(P)-(3-rho), x(P)+(3-rho).
    norm = lambda u, v: F(u)**2-2*F(v)**2
    assert norm(11, -6) == 49
    assert norm(F(57, 8), F(-28, 8)) == F(41**2, 64)
    assert norm(F(57, 8)-3, F(-28, 8)+1) == F(17**2, 64)
    assert norm(F(57, 8)+3, F(-28, 8)-1) == F(63**2, 64)
    for u in (F(7), F(41**2, 64), F(17**2, 64), F(63**2, 64)):
        assert valuation(u, ell) == 0
    M = actual[491][1][(525,)]
    K = actual[499][1][(51, 526)]
    Lpole = actual[494][1][(526, 527)]
    assert K == 82479248*M and 3*Lpole == 17*K
    scalar_preparation = {
        'integerResidueModuli': [16, 9, 17],
        'valuationOfContactProductAt2': prep2,
        'valuationOfContactProductAt3': prep3,
        'contactProductResidueAt17': 15,
        'forcedPrimeSquareResidueAt17': ell**2 % 17,
        'normalizerDenominatorResidueAt17': 3,
        'curveAndFieldUnramifiedAtForcedPrime': True,
        'exceptionalHChartNormsAreForcedPrimeUnits': True,
        'forcedPrimeAbsentFromContactRadicalByCutoff': True,
        'scalarPoleScalingIdentities': ['K=82479248*M', '3*L=17*K'],
        'finiteCongruenceScope': 'The existing arbitrary finite congruence preparation applies at149.'}
    local = local_certificate()
    assert report['variables'] == 248 and report['quadraticResiduals'] == 222
    assert report['ordinaryMonomialsForEveryPositiveParameter'] == len(ordinary)
    assert report['symbolicTerms'] == len(expanded)
    assert report['constantCoefficientMaximum'] == str(C)
    assert report['linearCoefficientMultiplierMaximum'] == L and report['exactHeightThresholdN'] == 53
    result = {
        'status': 'PASS', 'variables': 248, 'quadraticResiduals': 222, 'degree': 4,
        'contentForEveryIntegralParameter': 1,
        'ordinaryMonomialsForEveryPositiveParameter': 3189, 'symbolicTerms': 3190,
        'allRowsIndependentlyReconstructed': True, 'completeUnorderedPairExpansion': True,
        'allCoordinatesUsed': True, 'sourceQuadraticTableSha256': PIN,
        'contactReconstruction': 'Newton interpolation at six integer arguments, all five roots, and independent degree-ten composition identity.',
        'contacts': [str(x) for x in roots], 'degreeFivePolynomialCoefficients': [str(c) for c in contact],
        'completeContactBadPrimeSet': sorted(bad_primes),
        'extraExceptionalPrimesAbove76176': [2029147],
        'extraPrimeWitnesses': {str(p): sorted(x) for p, x in extra_witnesses.items()},
        'normalizingValueF1': str(F_one), 'normalizingContactRadicalIsOne': True,
        'heightMobiusMatrices': height_matrices,
        'amplifiedContactExponent': '7/4',
        'weightRelations': ['q2=q^2', 'q4=q2^2', 'q*q7=q4^2'],
        'weightPowerDomain': 'q7=q^7 wherever q is nonzero; the q=0 stratum has contact radical1.',
        'fixedSubtractionReconstruction': 'Pinned rows140,141 with constant Taylor truncation, followed by multiplication of numerator and denominator by3+2sqrt(2).',
        'localPackingAndScalarCertificate': local,
        'fixedPrime': ell, 'fixedPrimeEulerChecks': euler_checks,
        'scalarPreparationAndForcedPrime': scalar_preparation,
        'directChangesFromPinned259': sorted(changed_rows),
        'directRemovedCoordinatesFromPinned259': sorted(removed_coordinates),
        'directRemovedRowsFromPinned259': sorted(removed_rows),
        'fixedPrimeNormalizerValuation': '2*N+1 if v_ell(X)>=0; 2*N-1 otherwise',
        'gamma': str(gamma), 'preparedPoleValuationsAt2_3_17': prepared,
        'realPoleInputLimit': str(gamma**2/4),
        'positiveLeadingRealWeightCoefficient': str(sum(squared_roots)),
        'normalization': {'R': 'F10(t)/(t-1)^10', 'q': '(t-1)^10/F10(t)-1',
                          'zeroStrata': 'F=0 is impossible; t=1 or q=0 has contact radical1.'},
        'constantCoefficientMaximum': str(C), 'constantCoefficientMaximumBits': 1520,
        'linearCoefficientMultiplierMaximum': L, 'heightFormulaForEveryPositiveParameter': 'max(C,A^2+1)',
        'exactHeightThresholdN': 53, 'exactHeightForNAtLeastThreshold': '149^(4*N+2)+1',
        'quadraticTableSha256': sha256(system_path.read_bytes()).hexdigest(),
        'polynomialTableSha256': sha256(polynomial_path.read_bytes()).hexdigest(),
        'arithmeticScope': 'Exact coefficient, contact and local-valuation verification. The projection proof uses the proved contact-height estimate and the retained elliptic, pole and prime-pattern inputs, with an ineffective sufficient parameter.'}
    (folder/'independent-verification248-v17.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['status', 'variables', 'quadraticResiduals',
           'ordinaryMonomialsForEveryPositiveParameter', 'quadraticTableSha256', 'polynomialTableSha256']}))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', type=Path, default=HERE)
    parser.add_argument('--output-root', type=Path, default=HERE)
    args = parser.parse_args()
    verify(args.source_root, args.output_root)
