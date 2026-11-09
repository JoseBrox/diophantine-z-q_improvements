#!/usr/bin/env python3
"""Exact quadratic source for a quartic family under the rational abc conjecture.

The finite certificate verifies the polynomial and the displayed algebraic
identities.  The integer-projection theorem also uses the arithmetic hypotheses
specified in the accompanying paper; no numerical sufficient input shift is
claimed.
"""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd
from pathlib import Path
import json

from build_quartic273 import add, scale, mul, fm, primitive, terms, v, one

HERE = Path(__file__).resolve().parent
PIN = '54c242476e796404131eb09099bd2c134adf2358e1129a112cd2b47f996ab6c7'
RETAINED_ROWS = (0, 1, 2, 3, 34, 35, 92, 93, 112, 113, 116, 117,
                 130, 131, 142, 143, 184, 185, 200, 207, 208,
                 257, 258, 263, 264, 661, 662, *range(700, 708))
PARAMETER = {(1, ()): Q(1)}


def build(source_root=HERE, output_root=HERE):
    raw = (source_root/'family267/quadratic-family267.json').read_bytes()
    assert sha256(raw).hexdigest() == PIN
    old = json.loads(raw)
    source_ids = {c['id']: c['sourceId'] for c in old['coordinates']}
    source_rows = {r['sourceId']: r for r in old['residuals']}
    coordinates = {c['sourceId']: dict(c) for c in old['coordinates']}
    rows = []

    def emit(name, value, source_id=None):
        value = primitive(value)
        assert max(len(m) for a, m in value) <= 2, name
        assert max(a for a, m in value) <= 2, name
        rows.append({'sourceId': source_id, 'name': name, 'polynomial': value})

    for sid in RETAINED_ROWS:
        r = source_rows[sid]
        p = {(t['parameterPower'], tuple(sorted(source_ids[i] for i in t['monomial']))):
             Q(t['coefficient']) for t in r['terms']}
        assert all(a == 0 for a, m in p)
        emit(r['name'], p, sid)

    next_id = 30000

    def coordinate(name):
        nonlocal next_id
        sid = next_id
        next_id += 1
        coordinates[sid] = {'sourceId': sid, 'name': name, 'kind': 'gate'}
        return v(sid)

    def gate(name, value):
        output = coordinate(name)
        emit(name+'.definition', add(value, scale(output, -1)))
        return output

    def field_gate(name, value):
        return tuple(gate(name+'.'+str(j), value[j]) for j in range(2))

    # z(H-P)=N/D on the admissible H chart.  Both N and D are affine
    # functions of the already retained S_H and g coordinates.  The
    # common unit 3+2*sqrt(2) reduces their integer coefficients.
    S = (v(142), v(143))
    g = (v(700), v(701))
    N = (add(scale(one, -312), scale(S[0], -236), scale(S[1], -240)),
         add(scale(one, -69), scale(S[0], -120), scale(S[1], -236)))
    D0 = (add(scale(one, -576), scale(S[0], 312), scale(S[1], 138),
              scale(g[0], 504), scale(g[1], -2688)),
          add(scale(one, -256), scale(S[0], 69), scale(S[1], 312),
              scale(g[0], -1344), scale(g[1], 504)))
    left = fm((v(234), v(235)), N)
    right = fm((v(164), v(165)), D0)
    for j in range(2):
        emit('alternateRatio.cleared.'+str(j), add(left[j], scale(right[j], -1)))

    beta = add(scale(v(248), 2), PARAMETER)
    L = (v(232), v(233))
    I = (add(L[0], scale(beta, -1)), L[1])
    I2 = field_gate('inputComparison.square', fm(I, I))
    C2 = (v(305), scale(v(306), 2))
    H2 = (v(311), scale(v(312), 2))
    U2 = (v(255), scale(v(256), 2))
    B02 = (v(178), scale(v(179), -2))
    B12 = (v(190), scale(v(191), -2))
    U4 = field_gate('primaryNumerator.fourthPower', fm(U2, U2))
    B14 = field_gate('alternateNumerator.fourthPower', fm(B12, B12))
    beta2 = gate('height.betaSquared', mul(beta, beta))
    trace2 = gate('height.traceSquared', scale(mul(v(82), v(82)), 4))
    comparison_scale = gate('height.comparisonScale', add(mul(beta2, beta2),
                                                        mul(trace2, trace2)))

    detector_specs = []
    for d in range(2):
        prefix = 'detector'+str(d)
        t = v(37) if d == 0 else gate(prefix+'.argument', mul(v(37), comparison_scale))
        delta = add(t, scale(one, -1))
        r = gate(prefix+'.deltaSquared', mul(delta, delta))
        s = gate(prefix+'.deltaFourthPower', mul(r, r))
        contact = gate(prefix+'.contactPolynomial', add(mul(s, s), scale(mul(r, s), -30),
                        scale(s, 273), scale(r, -820), scale(one, 576)))
        q = coordinate(prefix+'.weight')
        emit(prefix+'.weight.definition', add(mul(contact, q), scale(mul(r, s), -1)))
        q2 = gate(prefix+'.weightSquared', mul(q, q))
        q4 = gate(prefix+'.weightFourthPower', mul(q2, q2))
        factors = []
        for k, triple in enumerate(((C2, H2, U4), (I2, B02, B14))):
            value = tuple(add(one if j == 0 else {}, mul(q, triple[0][j]),
                              mul(q2, triple[1][j]), mul(q4, triple[2][j])) for j in range(2))
            factors.append(field_gate(prefix+'.factor'+str(k), value))
        W = field_gate(prefix+'.product', fm(factors[0], factors[1]))
        tau = coordinate(prefix+'.reciprocalTrace')
        emit(prefix+'.reciprocalTrace.definition', add(mul(W[0], W[0]),
             scale(mul(W[1], W[1]), -2), scale(mul(W[0], tau), -2)))
        k = gate(prefix+'.inverseContact', mul(q, s))
        b = coordinate(prefix+'.poleInput')
        emit(prefix+'.poleInput.definition', add(mul(k, b), scale(mul(tau, tau), -1)))

        # The normalized factored source pole system.  These seven
        # coordinates are independent for each detector.
        e, u, p, w = (coordinate(prefix+'.pole.'+n) for n in ('scaledE', 's', 'p', 'q'))
        p2 = gate(prefix+'.pole.pSquared', mul(p, p))
        emit(prefix+'.pole.firstConic', add(scale(one, 289), scale(e, 34),
             scale(mul(e, e), -3), scale(mul(b, p2), -17)))
        v0 = coordinate(prefix+'.pole.v')
        emit(prefix+'.pole.factor', add(scale(e, 17), scale(mul(e, b), -1),
             scale(mul(u, v0), -17)))
        w2 = gate(prefix+'.pole.qSquared', mul(w, w))
        emit(prefix+'.pole.secondConic', add(mul(u, u), scale(mul(u, v0), 34),
             scale(mul(b, w2), -17), scale(mul(v0, v0), -867)))
        detector_specs.append({'detector': d, 'argument': 'lambda' if d == 0 else 'a*lambda',
            'contactDegree': 8, 'R': 'F8(t)/(t-1)^10', 'q': '(t-1)^6/F8(t)',
            'inverseR': 'q*(t-1)^4', 'tests': [['C^2', 'f(H)^2', 'f(U)^4'],
                                                   ['I^2', 'sigma(f(H-P))^2', 'sigma(f(U-A))^4']]})

    used = {i for row in rows for a, m in row['polynomial'] for i in m}
    coords = [dict(coordinates[sid], id=i+1) for i, sid in enumerate(sorted(used))]
    mapping = {c['sourceId']: c['id'] for c in coords}
    residuals = []
    expanded = defaultdict(int)
    for index, row in enumerate(rows):
        p = {(a, tuple(sorted(mapping[i] for i in m))): c for (a, m), c in row['polynomial'].items()}
        residuals.append({'id': index+1, 'sourceId': row['sourceId'], 'name': row['name'], 'terms': terms(p)})
        for (a, m), c in p.items():
            for (b, n), e in p.items():
                expanded[a+b, tuple(sorted(m+n))] += c*e
    expanded = {key: c for key, c in expanded.items() if c}
    ordinary = defaultdict(dict)
    for (a, m), c in expanded.items():
        ordinary[m][a] = c
    assert len(coords) == 99, len(coords)
    assert gcd(*expanded.values()) == 1
    assert max(len(m) for a, m in expanded) == 4
    assert {i for a, m in expanded for i in m} == set(range(1, 100))
    assert ordinary[()] == {0: 833549, 4: 2}
    constant_maximum = max(abs(p[0]) for p in ordinary.values() if set(p) == {0})
    assert constant_maximum == 11600064
    fixed_parameter = {'symbol': 'B', 'domain': 'Odd integers B>=3',
                       'quantified': False, 'sufficientThreshold': 'Ineffective; every sufficiently large odd B'}
    system = {'format': 'integer-quadratic-family-abc-v1', 'variables': len(coords),
              'inputCoordinate': 1, 'fixedParameter': fixed_parameter,
              'source': {'construction': 'quartic-family267', 'sha256': PIN,
                         'retainedSourceRows': list(RETAINED_ROWS)},
              'coordinates': coords, 'residuals': residuals}
    polynomial = {'format': 'integer-quartic-family-abc-v1', 'variables': len(coords),
                  'degree': 4, 'inputCoordinate': 1, 'fixedParameter': fixed_parameter,
                  'coordinates': coords, 'terms': terms(expanded)}
    fixture = {m: sum(c*3**a for a, c in p.items()) for m, p in ordinary.items()}
    fixture = {m: c for m, c in fixture.items() if c}
    report = {'status': 'Exact polynomial specification; arithmetic projection requires rational abc and the separately stated source inputs.',
              'variables': len(coords), 'quadraticResiduals': len(residuals), 'degree': 4,
              'symbolicContent': 1, 'symbolicTerms': len(expanded),
              'ordinaryMonomialPositions': len(ordinary), 'sourceSha256': PIN,
              'retainedSourceRows': list(RETAINED_ROWS),
              'contacts': [-3, -2, -1, 0, 2, 3, 4, 5],
              'heightScale': 'beta^4+(Tr x(A))^4', 'beta': '2*X^2+B',
              'abcContactHeightCoefficient': '2/7', 'abcPairHeightCoefficient': '3/2',
              'combinedNumeratorCoefficient': '6/7',
              'coefficientHeightForEveryIntegerBAtLeast3': 'max(11600064,2*B^4+833549)',
              'coefficientHeightForEveryOddBAtLeast49': '2*B^4+833549',
              'coefficientHeightThresholdOddB': 49,
              'contentForEveryIntegerShift': 1,
              'ordinaryMonomialsForEveryPositiveShift': 881,
              'detectors': detector_specs,
              'normalization': ['r=(t-1)^2', 's=r^2', 'F8=s^2-30*r*s+273*s-820*r+576',
                                'F8*q=r*s', 'k=q*s', 'k*b=tau^2'],
              'finiteChecksScope': 'Exact coefficient reconstruction and polynomial identities, not a numerical verification of abc or an effective sufficient shift.',
              'fixture': {'B': 3, 'ordinaryMonomials': len(fixture),
                          'coefficientHeight': str(max(abs(c) for c in fixture.values())),
                          'definesIntegersCertified': False}}
    out = output_root/'family_abc99'
    out.mkdir(parents=True, exist_ok=True)
    for name, obj in [('quadratic-family-abc99.json', system), ('polynomial-family-abc99.json', polynomial),
                      ('construction-report-abc99.json', report)]:
        (out/name).write_text(json.dumps(obj, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ('variables', 'quadraticResiduals', 'degree',
                                           'symbolicTerms', 'ordinaryMonomialPositions', 'fixture')}))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', type=Path, default=HERE)
    parser.add_argument('--output-root', type=Path, default=HERE)
    args = parser.parse_args()
    build(args.source_root, args.output_root)
