#!/usr/bin/env python3
"""Independent reconstruction of the abc-conditional 99-variable quartic.

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
    folder = output_root/'family_abc99'
    system_path = folder/'quadratic-family-abc99.json'
    poly_path = folder/'polynomial-family-abc99.json'
    system = json.loads(system_path.read_text())
    polynomial = json.loads(poly_path.read_text())
    report = json.loads((folder/'construction-report-abc99.json').read_text())
    ids = {c['id']: c['sourceId'] for c in system['coordinates']}
    named = {c['name']: c['sourceId'] for c in system['coordinates']}
    actual = {r['name']: decode(r, ids) for r in system['residuals']}
    expected = {}

    retained = (0, 1, 2, 3, 34, 35, 92, 93, 112, 113, 116, 117,
                130, 131, 142, 143, 184, 185, 200, 207, 208,
                257, 258, 263, 264, 661, 662, 700, 701, 702, 703, 704, 705, 706, 707)
    for sid in retained:
        row = old_rows[sid]
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

    beta = S((2, variable(248)), (1, variable(-1)))
    input_difference = (S((1, variable(232)), (-1, beta)), variable(233))
    field_equality('inputComparison.square', field_product(input_difference, input_difference))
    C2 = variable(305), S((2, variable(306)))
    H2 = variable(311), S((2, variable(312)))
    U2 = variable(255), S((2, variable(256)))
    B02 = variable(178), S((-2, variable(179)))
    B12 = variable(190), S((-2, variable(191)))
    field_equality('primaryNumerator.fourthPower', field_product(U2, U2))
    field_equality('alternateNumerator.fourthPower', field_product(B12, B12))
    equality('height.betaSquared', product(beta, beta))
    equality('height.traceSquared', S((4, product(variable(82), variable(82)))))
    equality('height.comparisonScale', S((1, product(V('height.betaSquared'), V('height.betaSquared'))),
                                          (1, product(V('height.traceSquared'), V('height.traceSquared')))))

    contact_coefficients = [Q(1)]
    for j in range(1, 5):
        contact_coefficients = univariate_product(contact_coefficients, [-j*j, 1])
    assert contact_coefficients == [576, -820, 273, -30, 1]
    normalizations = []
    for d in range(2):
        prefix = 'detector'+str(d)
        if d:
            equality(prefix+'.argument', product(variable(37), V('height.comparisonScale')))
        t = variable(37) if d == 0 else V(prefix+'.argument')
        delta = S((1, t), (-1, ONE))
        r, s, ff, q = [V(prefix+'.'+n) for n in
                       ('deltaSquared', 'deltaFourthPower', 'contactPolynomial', 'weight')]
        equality(prefix+'.deltaSquared', product(delta, delta))
        equality(prefix+'.deltaFourthPower', product(r, r))
        equality(prefix+'.contactPolynomial', S((1, product(s, s)), (-30, product(r, s)),
                                                (273, s), (-820, r), (576, ONE)))
        record(prefix+'.weight.definition', S((1, product(ff, q)), (-1, product(r, s))))
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
        equality(prefix+'.inverseContact', product(q, s))
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
                               'contactNonzero': 'F8=0 would force t=1, but F8(1)=576',
                               'deltaNonzero': 't=1 forces q=0,W=1,tau=1/2,k=0, contradicting k*b=tau^2'})

    assert expected == actual
    assert len(actual) == 87 and len(ids) == 99
    assert system['variables'] == polynomial['variables'] == 99
    assert sorted(ids) == list(range(1, 100)) and ids[1] == 0
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
    assert len(expanded) == 883 and len(ordinary) == 881
    assert ordinary[(0, 0, 0, 0)] == {0: 1}
    assert ordinary[()] == {0: 833549, 4: 2}
    assert ordinary[(248, 248)] == {0: 1, 2: 48}
    assert all(len(p) == 1 for m, p in ordinary.items() if m not in ((), (248, 248)))
    coefficient_maximum = max(abs(p[0]) for p in ordinary.values() if set(p) == {0})
    assert coefficient_maximum == 11600064
    parameter_maxima = {a: max(abs(p.get(a, 0)) for p in ordinary.values()) for a in (1, 2, 3)}
    assert parameter_maxima == {1: 64, 2: 48, 3: 16}
    # For B>=8 the leading term 2B^4 dominates these three profiles;
    # the remaining finite interval is checked exactly.
    for B in range(3, 9):
        assert 2*B**4+833549 >= max(64*B, 48*B*B+1, 16*B**3)
    assert 2*47**4+833549 < coefficient_maximum < 2*49**4+833549
    assert all(sum(c*3**a for a, c in p.items()) != 0 for p in ordinary.values())
    assert gcd(*expanded.values()) == 1

    result = {'status': 'PASS', 'variables': 99, 'quadraticResiduals': 87, 'degree': 4,
              'contentForEveryIntegerShift': 1,
              'ordinaryMonomialsForEveryPositiveShift': 881, 'symbolicTerms': 883,
              'allRowsIndependentlyReconstructed': True,
              'completeUnorderedPairExpansion': True, 'allCoordinatesUsed': True,
              'sourceQuadraticTableSha256': PIN,
              'fixedSubtractionReconstruction': 'Plain z(H-P) recovered from pinned rows140,141, then both numerator and denominator multiplied by the unit3+2sqrt(2).',
              'normalizationRowsIndependentlyChecked': normalizations,
              'coefficientHeightForEveryIntegerBAtLeast3': 'max(11600064,2*B^4+833549)',
              'coefficientHeightForEveryOddBAtLeast49': '2*B^4+833549',
              'noSupportCancellationForPositiveShift': True,
              'quadraticTableSha256': sha256(system_path.read_bytes()).hexdigest(),
              'polynomialTableSha256': sha256(poly_path.read_bytes()).hexdigest(),
              'arithmeticScope': 'Finite algebra only; the integer projection additionally assumes rational abc and the specified elliptic-group, pole and simultaneous prime-pattern inputs. The sufficient odd shift is ineffective.'}
    assert report['variables'] == 99 and report['quadraticResiduals'] == 87
    assert report['symbolicTerms'] == 883 and report['ordinaryMonomialPositions'] == 881
    (folder/'independent-verification-abc99.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ('status', 'variables', 'quadraticResiduals',
                'ordinaryMonomialsForEveryPositiveShift', 'quadraticTableSha256', 'polynomialTableSha256')}))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', type=Path, default=HERE)
    parser.add_argument('--output-root', type=Path, default=HERE)
    args = parser.parse_args()
    verify(args.source_root, args.output_root)
