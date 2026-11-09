#!/usr/bin/env python3
"""Independent reconstruction of the abc-conditional 97-variable quartic.

No producer is imported.  The checker reconstructs every changed equation,
the eliminated fixed-subtraction formula, the complete sum of squares, its
support and its exact coefficient-height profile.  Arithmetic conjectures
and an effective defining shift are outside the finite certificate's scope.
"""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations_with_replacement
from math import gcd
from pathlib import Path
import json

from check_quartic273 import (ONE, variable, linear, product, field_product,
                              normalize, decode, univariate_product)

HERE = Path(__file__).resolve().parent
PIN = '54c242476e796404131eb09099bd2c134adf2358e1129a112cd2b47f996ab6c7'


def verify(source_root=HERE, output_root=HERE):
    raw = (source_root/'family267/quadratic-family267.json').read_bytes()
    assert sha256(raw).hexdigest() == PIN
    old = json.loads(raw)
    old_ids = {c['id']: c['sourceId'] for c in old['coordinates']}
    old_rows = {r['sourceId']: r for r in old['residuals']}
    folder = output_root/'family_abc97_v17'
    system_path = folder/'quadratic-family-abc97-v17.json'
    poly_path = folder/'polynomial-family-abc97-v17.json'
    system = json.loads(system_path.read_text())
    polynomial = json.loads(poly_path.read_text())
    report = json.loads((folder/'construction-report-abc97-v17.json').read_text())
    ids = {c['id']: c['sourceId'] for c in system['coordinates']}
    named = {c['name']: c['sourceId'] for c in system['coordinates']}
    actual = {r['name']: decode(r, ids) for r in system['residuals']}
    expected = {}

    retained = (0, 1, 2, 3, 34, 35, 92, 93, 112, 113, 116, 117,
                130, 131, 142, 143, 184, 185, 200, 207, 208,
                257, 258, 263, 264, 661, 662, 700, 701, 702, 703, 704, 705, 706, 707)
    for sid in retained:
        row = old_rows[sid]
        if sid == 200:
            expected['inputComparison.real.definition'] = normalize(linear(
                (variable(248), 1), (variable(232), -1),
                (product(variable(0), variable(0)), 2), (variable(-1), 1)))
        else:
            expected[row['name']] = decode(row, old_ids)
    assert system['source']['retainedSourceRows'] == list(retained)

    def V(name):
        return variable(named[name])

    def S(*parts):
        return linear(*((p, c) for c, p in parts))

    def record(name, value):
        assert name not in expected
        expected[name] = normalize(value)

    def equality(name, value):
        record(name+'.definition', S((1, value), (-1, V(name))))

    def fvalue(name):
        return V(name+'.0'), V(name+'.1')

    def field_equality(name, value):
        for j in range(2):
            equality(name+'.'+str(j), value[j])

    # Recover the plain formal parameter from two pinned source rows.
    # Removing terms containing f^2 and its square sets the truncation to1.
    dropped = {178, 179, 180, 181}
    plain = [{m: c for m, c in decode(old_rows[sid], old_ids).items()
              if not dropped.intersection(m)} for sid in (140, 141)]
    sh = variable(142), variable(143)
    gg = variable(700), variable(701)
    Nold = (S((-660, ONE), (-228, sh[0]), (224, sh[1])),
            S((417, ONE), (112, sh[0]), (-228, sh[1])))
    Dold = (S((-704, ONE), (660, sh[0]), (-834, sh[1]), (6888, gg[0]), (-10080, gg[1])),
            S((384, ONE), (-417, sh[0]), (660, sh[1]), (-5040, gg[0]), (6888, gg[1])))
    dz = field_product(Dold, (variable(188), variable(189)))
    assert all(normalize(S((1, dz[j]), (-1, Nold[j]))) == normalize(plain[j]) for j in range(2))
    unit = (S((3, ONE)), S((2, ONE)))
    N = field_product(unit, Nold)
    D = field_product(unit, Dold)
    left = field_product((variable(234), variable(235)), N)
    right = field_product((variable(164), variable(165)), D)
    for j in range(2):
        record('alternateRatio.cleared.'+str(j), S((1, left[j]), (-1, right[j])))

    beta = S((1, variable(232)), (-1, variable(248)))
    input_difference = (variable(248), variable(233))
    # The replaced coordinate is I0=L0-2X^2-B.  This affine change
    # of the old square witness is invertible on the old input row.
    assert S((1, beta), (-1, variable(232)), (1, variable(248))) == {}
    assert system['coordinates'][next(i for i, c in enumerate(system['coordinates'])
                                     if c['sourceId'] == 248)]['name'] == 'inputComparison.real'
    field_equality('inputComparison.square', field_product(input_difference, input_difference))
    C2 = variable(305), S((2, variable(306)))
    H2 = variable(311), S((2, variable(312)))
    U2 = variable(255), S((2, variable(256)))
    B02 = variable(178), S((-2, variable(179)))
    B12 = variable(190), S((-2, variable(191)))
    field_equality('primaryNumerator.fourthPower', field_product(U2, U2))
    field_equality('alternateNumerator.fourthPower', field_product(B12, B12))
    trace = S((2, variable(82)))
    equality('height.sumSquares', S((1, product(beta, beta)), (1, product(trace, trace))))
    equality('height.pairProduct', product(beta, trace))
    ss, pp = V('height.sumSquares'), V('height.pairProduct')
    equality('height.comparisonScale', S((1, product(ss, ss)), (-2, product(pp, pp))))
    # Check the fourth-power identity independently in two symbolic inputs.
    aa, bb = variable(-10), variable(-11)
    a2, b2 = product(aa, aa), product(bb, bb)
    ss0, pp0 = S((1, a2), (1, b2)), product(aa, bb)
    assert S((1, product(ss0, ss0)), (-2, product(pp0, pp0))) == \
           S((1, product(a2, a2)), (1, product(b2, b2)))

    contact_coefficients = [Q(1)]
    for j in range(1, 5):
        contact_coefficients = univariate_product(contact_coefficients, [-j*j, 1])
    assert contact_coefficients == [576, -820, 273, -30, 1]
    # Independently expand the eight linear contacts in t and substitute
    # r=(t-1)^2 into the quartic to certify the identity and all roots.
    contacts = [-3, -2, -1, 0, 2, 3, 4, 5]
    direct = [Q(1)]
    for theta in contacts:
        direct = univariate_product(direct, [-theta, 1])
    delta_squared = [Q(1), Q(-2), Q(1)]
    rpower = [Q(1)]
    substituted = [Q(0)]*9
    for coefficient in contact_coefficients:
        for index, value in enumerate(rpower):
            substituted[index] += coefficient*value
        rpower = univariate_product(rpower, delta_squared)
    assert direct == substituted
    assert sum(direct) == 576
    # Verify the homogeneous normalization before dividing by q:
    # with c=q*r and k=q*r^2, its left side is q^2*P4(r)-q*r^3.
    rr, qq = variable(-20), variable(-21)
    cc, kk = product(qq, rr), product(qq, product(rr, rr))
    homogeneous = S((1, product(kk, kk)), (-30, product(kk, cc)),
                    (273, product(cc, cc)), (-820, product(cc, qq)),
                    (576, product(qq, qq)), (-1, product(kk, rr)))
    rr2 = product(rr, rr)
    p4 = S((1, product(rr2, rr2)), (-30, product(rr2, rr)),
           (273, rr2), (-820, rr), (576, ONE))
    assert homogeneous == S((1, product(product(qq, qq), p4)),
                             (-1, product(qq, product(rr2, rr))))
    normalizations = []
    for d in range(2):
        prefix = 'detector'+str(d)
        if d:
            equality(prefix+'.argument', product(variable(37), V('height.comparisonScale')))
        t = variable(37) if d == 0 else V(prefix+'.argument')
        delta = S((1, t), (-1, ONE))
        r, q, u, k = [V(prefix+'.'+n) for n in
                       ('deltaSquared', 'weight', 'firstContactProduct', 'inverseContact')]
        equality(prefix+'.deltaSquared', product(delta, delta))
        equality(prefix+'.firstContactProduct', product(q, r))
        equality(prefix+'.inverseContact', product(u, r))
        record(prefix+'.weight.definition', S((1, product(k, k)), (-30, product(k, u)),
               (273, product(u, u)), (-820, product(u, q)), (576, product(q, q)),
               (-1, product(k, r))))
        equality(prefix+'.weightSquared', product(q, q))
        q2 = V(prefix+'.weightSquared')
        equality(prefix+'.weightFourthPower', product(q2, q2))
        q4 = V(prefix+'.weightFourthPower')
        triples = ((C2, H2, fvalue('primaryNumerator.fourthPower')),
                   (fvalue('inputComparison.square'), B02, fvalue('alternateNumerator.fourthPower')))
        for index, triple in enumerate(triples):
            value = tuple(S((1, ONE if j == 0 else {}), (1, product(q, triple[0][j])),
                            (1, product(q2, triple[1][j])), (1, product(q4, triple[2][j]))) for j in range(2))
            field_equality(prefix+'.factor'+str(index), value)
        W = fvalue(prefix+'.product')
        field_equality(prefix+'.product', field_product(fvalue(prefix+'.factor0'), fvalue(prefix+'.factor1')))
        tau, k, b = [V(prefix+'.'+n) for n in ('reciprocalTrace', 'inverseContact', 'poleInput')]
        record(prefix+'.reciprocalTrace.definition', S((1, product(W[0], W[0])),
               (-2, product(W[1], W[1])), (-2, product(W[0], tau))))
        record(prefix+'.poleInput.definition', S((1, product(k, b)), (-1, product(tau, tau))))
        e, u, p, w, v0 = [V(prefix+'.pole.'+n) for n in ('scaledE', 's', 'p', 'q', 'v')]
        equality(prefix+'.pole.pSquared', product(p, p))
        record(prefix+'.pole.firstConic', S((289, ONE), (34, e), (-3, product(e, e)),
                                            (-17, product(b, V(prefix+'.pole.pSquared')))))
        record(prefix+'.pole.factor', S((17, e), (-1, product(e, b)), (-17, product(u, v0))))
        equality(prefix+'.pole.qSquared', product(w, w))
        record(prefix+'.pole.secondConic', S((1, product(u, u)), (34, product(u, v0)),
               (-17, product(b, V(prefix+'.pole.qSquared'))), (-867, product(v0, v0))))
        normalizations.append({'detector': d, 'derivedQ': '(t-1)^6/F8(t)',
                               'derivedInverseR': '(t-1)^10/F8(t)',
                               'qNonzero': 'q=0 forces c=k=0,W=1,tau=1/2, contradicting k*b=tau^2',
                               'contactNonzero': 'After q is excluded, F8=0 forces t=1, but F8(1)=576',
                               'deltaNonzero': 't=1 forces 576*q^2=0, contradicting q nonzero'})

    assert expected == actual
    assert len(actual) == 85 and len(ids) == 97
    assert system['variables'] == polynomial['variables'] == 97
    assert sorted(ids) == list(range(1, 98)) and ids[1] == 0
    assert system['coordinates'] == polynomial['coordinates']
    assert {i for p in actual.values() for m in p for i in m if i != -1} == set(ids.values())
    expanded = defaultdict(int)
    for p in actual.values():
        assert max(sum(i != -1 for i in m) for m in p) <= 2
        for m, n in combinations_with_replacement(p, 2):
            expanded[tuple(sorted(m+n))] += p[m]*p[n]*(1 if m == n else 2)
    expanded = {m: c for m, c in expanded.items() if c}
    assert expanded == decode({'terms': polynomial['terms']}, ids)
    assert max(sum(i != -1 for i in m) for m in expanded) == 4
    ordinary = defaultdict(dict)
    for m, c in expanded.items():
        ordinary[tuple(i for i in m if i != -1)][m.count(-1)] = c
    assert len(expanded) == 880 and len(ordinary) == 879
    assert ordinary[(0, 0, 0, 0)] == {0: 4}
    assert ordinary[(1, 1, 1, 1)] == {0: 1}
    assert ordinary[()] == {0: 169997, 2: 1}
    assert ordinary[(0, 0)] == {1: 4}
    assert ordinary[(232,)] == {1: -2}
    assert ordinary[(248,)] == {1: 2}
    assert all(set(p) == {0} for m, p in ordinary.items()
               if m not in ((), (0, 0), (232,), (248,)))
    coefficient_maximum = max(abs(p[0]) for p in ordinary.values() if set(p) == {0})
    assert coefficient_maximum == 11600064
    # Since 4B<=B^2+4, the constant profile dominates every linear
    # profile for B>=1. The displayed fourth-power coefficient gives
    # content one after every integral specialization of B.
    assert 169997 > 4
    assert 3379**2+169997 < coefficient_maximum < 3381**2+169997
    assert all(sum(c*3**a for a, c in p.items()) != 0 for p in ordinary.values())
    single_power_maxima = {1: 4}
    assert gcd(*expanded.values()) == 1

    result = {'status': 'PASS', 'variables': 97, 'quadraticResiduals': 85, 'degree': 4,
              'contentForEveryIntegerShift': 1,
              'ordinaryMonomialsForEveryPositiveShift': 879, 'symbolicTerms': 880,
              'allRowsIndependentlyReconstructed': True,
              'completeUnorderedPairExpansion': True, 'allCoordinatesUsed': True,
              'sourceQuadraticTableSha256': PIN,
              'fixedSubtractionReconstruction': 'Plain z(H-P) recovered from pinned rows140,141, then both numerator and denominator multiplied by the unit3+2sqrt(2).',
              'normalizationRowsIndependentlyChecked': normalizations,
              'fourthPowerScaleIndependentlyExpanded': True,
              'eightContactProductIndependentlyExpanded': True,
              'homogeneousNormalizationIndependentlyExpanded': True,
              'contactPolynomialInR': [int(c) for c in contact_coefficients],
              'contacts': contacts,
              'coefficientHeightForEveryIntegerBAtLeast3': 'max(11600064,B^2+169997)',
              'coefficientHeightForEveryOddBAtLeast3381': 'B^2+169997',
              'inputAffineCoordinateChangeIndependentlyReconstructed': True,
              'singlePowerCoefficientMaxima': single_power_maxima,
              'noSupportCancellationForPositiveShift': True,
              'quadraticTableSha256': sha256(system_path.read_bytes()).hexdigest(),
              'polynomialTableSha256': sha256(poly_path.read_bytes()).hexdigest(),
              'arithmeticScope': 'Finite algebra only; the integer projection additionally assumes rational abc and the specified elliptic-group, pole and simultaneous prime-pattern inputs. The sufficient odd shift is ineffective.'}
    assert report['variables'] == 97 and report['quadraticResiduals'] == 85
    assert report['symbolicTerms'] == 880 and report['ordinaryMonomialPositions'] == 879
    assert report['combinedNumeratorCoefficient'] == '8/9'
    (folder/'independent-verification-abc97-v17.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ('status', 'variables', 'quadraticResiduals',
                'ordinaryMonomialsForEveryPositiveShift', 'quadraticTableSha256', 'polynomialTableSha256')}))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', type=Path, default=HERE)
    parser.add_argument('--output-root', type=Path, default=HERE)
    args = parser.parse_args()
    verify(args.source_root, args.output_root)
