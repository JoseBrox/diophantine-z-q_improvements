#!/usr/bin/env python3
"""Independently verify the mixed-order 301- and 351-variable quartics.

The producer is not imported.  Field constants are reconstructed from
D=(3-sqrt(2))^2; expansion uses unordered pairs rather than the producer's
ordered-pair loops.  Arithmetic existence premises are outside this check.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations_with_replacement
from math import gcd, lcm
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
SHARED_REMOVED = {608, 609, 610, 611, 614, 615, 616, 617, 620, 621, 622, 623,
                  624, 625, 626, 627, 628, 629, 630, 631, 632, 633}


def collect(entries):
    result = defaultdict(Fraction)
    for monomial, coefficient in entries:
        result[tuple(sorted(monomial))] += coefficient
    return {m: c for m, c in result.items() if c}


def summation(*values):
    return collect(item for value in values for item in value.items())


def times(a, b):
    return collect((u + v, c * d) for u, c in a.items() for v, d in b.items())


def scalar(a, b):
    return {m: c * b for m, c in a.items() if c * b}


def symbol(index):
    return {(index,): Fraction(1)}


UNIT = {(): Fraction(1)}


def pairmul(a, b):
    return (summation(times(a[0], b[0]), scalar(times(a[1], b[1]), 2)),
            summation(times(a[0], b[1]), times(a[1], b[0])))


def constant_pairmul(a, b):
    return (a[0] * b[0] + 2 * a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def constant_power(a, n):
    b = (Fraction(1), Fraction(0))
    for _ in range(n):
        b = constant_pairmul(a, b)
    return b


def divide_by_constant(a, b):
    norm = b[0] ** 2 - 2 * b[1] ** 2
    return pairmul(a, (scalar(UNIT, b[0] / norm), scalar(UNIT, -b[1] / norm)))


def conjugate(a):
    return a[0], scalar(a[1], -1)


def normalized(poly):
    denominator = lcm(*(c.denominator for c in poly.values()))
    integers = {m: int(c * denominator) for m, c in poly.items()}
    content = gcd(*integers.values())
    # A is the distinguished token -1.  This ordering matches the format's
    # (parameterPower, coordinateMonomial) order without using its producer.
    first = min(integers, key=lambda m: (m.count(-1), tuple(i for i in m if i != -1)))
    if integers[first] < 0:
        content = -content
    return {m: c // content for m, c in integers.items()}


def decode(rows, coordinates):
    ids = {c['id']: c['sourceId'] for c in coordinates}
    return {r['sourceId']: (
        r['name'], collect((tuple([-1] * t['parameterPower'] + [ids[i] for i in t['monomial']]),
                            Fraction(int(t['coefficient']))) for t in r['terms'])) for r in rows}


def run(baseline):
    number = 301 if baseline == 317 else 351
    detector_count = 2 if baseline == 317 else 3
    groups = ([('H', 'C1', 'V0'), ('C2', 'I', 'V2'), ('C3', 'U2', 'V3'),
               ('C4', 'U3', 'V4'), ('F', 'U4'), ('U1', 'V1')] if baseline == 317 else
              [('H', 'C1', 'V1', 'V0'), ('C2', 'I', 'V2'), ('C3', 'U2', 'V3'),
               ('C4', 'U3', 'V4'), ('F', 'U4', 'U1')])
    group_count = len(groups)
    source_path = ROOT / f'family{baseline}' / f'quadratic-family{baseline}.json'
    source = json.loads(source_path.read_text())
    out = ROOT / f'family{number}'
    system = json.loads((out / f'quadratic-family{number}.json').read_text())
    polynomial = json.loads((out / f'polynomial-family{number}.json').read_text())
    assert system['source']['sha256'] == sha256(source_path.read_bytes()).hexdigest()
    old = decode(source['residuals'], source['coordinates'])
    actual = decode(system['residuals'], system['coordinates'])
    assert len(actual) == len(system['residuals'])
    assert len({name for name, p in actual.values()}) == len(actual)
    old_by_name = {name: sid for sid, (name, poly) in old.items()}
    expected = {sid: (name, poly) for sid, (name, poly) in old.items()
                if not name.startswith(('hybrid.1.', 'hybrid.10.', 'hybrid.40.', 'hybrid.det'))
                and '.E40.power' not in name}
    assert len(old) - len(expected) == 22 + 24 * detector_count
    D = (Fraction(11), Fraction(-6))
    powers = {}
    for i, sid in enumerate([255, 257, 259, 261], 1):
        powers[f'U{i}', 0] = symbol(sid), scalar(symbol(sid + 1), 2)
    for i, sid in enumerate([178, 190, 196, 208, 220]):
        powers[f'V{i}', 0] = symbol(sid), scalar(symbol(sid + 1), -2)
    for point, (u, v, r, s) in enumerate([(180, 181, 182, 183), (192, 193, 0, 0),
                                        (198, 199, 200, 201), (210, 211, 212, 213),
                                        (222, 223, 224, 225)]):
        w2 = (scalar(symbol(u), 193), scalar(symbol(v), -132))
        powers[f'V{point}', 1] = conjugate(divide_by_constant(w2, constant_power(D, 2)))
        if r:
            powers[f'V{point}', 2] = conjugate(divide_by_constant((symbol(r), symbol(s)), constant_power(D, 4)))
    for name, sid in [('C1', 305), ('H', 311), ('C2', 313), ('C3', 315), ('C4', 317)]:
        powers[name, 0] = symbol(sid), scalar(symbol(sid + 1), 2)
    # Derive the affine square corrections from (L1-beta)^2 and
    # (LucasF)^2, using the exact stored square definitions.
    powers['I', 0] = (summation(symbol(307), scalar(symbol(232), -6), scalar(symbol(248), 306), scalar(UNIT, 15015)),
                       summation(scalar(symbol(308), 2), scalar(symbol(233), -6)))
    powers['F', 0] = (summation(symbol(319), scalar(symbol(253), -2), UNIT),
                       summation(scalar(symbol(320), 4), scalar(symbol(254), -4)))
    def solve_stored_square(row_id, output):
        poly = old[row_id][1]
        pivot = poly[(output,)]
        assert all(output not in monomial for monomial in poly if monomial != (output,))
        return scalar({m: c for m, c in poly.items() if m != (output,)}, -1 / pivot)
    substitutions = {output: solve_stored_square(row_id, output)
                     for row_id, output in [(259, 307), (260, 308), (271, 319), (272, 320)]}
    def substitute(poly):
        out = {}
        for monomial, coefficient in poly.items():
            term = scalar(UNIT, coefficient)
            for variable in monomial:
                term = times(term, substitutions.get(variable, symbol(variable)))
            out = summation(out, term)
        return out
    input_test = (summation(symbol(232), scalar(symbol(248), -51), scalar(UNIT, -2504)), symbol(233))
    lucas_test = (summation(symbol(253), scalar(UNIT, -1)), scalar(symbol(254), 2))
    assert tuple(substitute(p) for p in powers['I', 0]) == pairmul(input_test, input_test)
    assert tuple(substitute(p) for p in powers['F', 0]) == pairmul(lucas_test, lucas_test)
    orders = {name: 1 for name in ['U1', 'U2', 'U3', 'U4', 'V0', 'V1', 'V2', 'V3', 'V4']}
    orders.update(C1=10, I=10, H=40, C2=40, C3=40, C4=40, F=40)
    assert sorted(x for g in groups for x in g) == sorted(orders)
    maximum = {name: j for group in groups for j, name in enumerate(group)}
    needed = {(name, level) for name, levelmax in maximum.items() for level in range(levelmax + 1)}
    new_power_keys = sorted(needed - set(powers), key=lambda pair: (pair[1], pair[0]))
    coord_by_name = {c['name']: c['sourceId'] for c in system['coordinates']}
    new_sids = set()
    for name, level in new_power_keys:
        value = pairmul(powers[name, level - 1], powers[name, level - 1])
        sids = [coord_by_name[f'mixed.{name}.power{2**(level+1)}.{component}'] for component in range(2)]
        for component, sid in enumerate(sids):
            expected[sid] = (f'mixed.{name}.power{2**(level+1)}.{component}.definition',
                             normalized(summation(value[component], scalar(symbol(sid), -1))))
        powers[name, level] = tuple(symbol(sid) for sid in sids)
        new_sids.update(sids)
    assert len(new_power_keys) == (5 if baseline == 317 else 9)
    changed = []
    for detector in range(detector_count):
        q, q2, q4 = [symbol(k + 48 * detector) for k in [352, 361, 362]]
        c, d = [symbol(k + 48 * detector) for k in [355, 356]]
        sid = old_by_name[f'detector{detector}.E1.power3.definition']
        expected[sid] = (f'detector{detector}.E1.power4.definition', normalized(summation(times(q2, q2), scalar(q4, -1))))
        changed.append(sid)
        sid = old_by_name[f'detector{detector}.toric.d.definition']
        expected[sid] = (old[sid][0], normalized(summation(times(c, d), scalar(times(q, q4), -1))))
        changed.append(sid)
        weights = {(1, 0): q, (1, 1): q2, (1, 2): q4,
                   (10, 0): symbol(359 + 48 * detector), (10, 1): symbol(369 + 48 * detector),
                   (40, 0): symbol(360 + 48 * detector)}
        if baseline == 370:
            sid = coord_by_name[f'mixed.det{detector}.q1Power8']
            new_sids.add(sid)
            expected[sid] = (f'mixed.det{detector}.q1Power8.definition',
                             normalized(summation(times(q4, q4), scalar(symbol(sid), -1))))
            weights[1, 3] = symbol(sid)
        start = 634 + 20 * detector
        for group, tests in enumerate(groups):
            for component in range(2):
                sid = 900 + 30 * detector + 2 * group + component
                expression = summation(UNIT if component == 0 else {},
                                       *(times(weights[orders[test], position], powers[test, position][component])
                                         for position, test in enumerate(tests)),
                                       scalar(symbol(start + 2 * group + component), -1))
                expected[sid] = (f'mixed.det{detector}.factor{group}.{component}.definition', normalized(expression))
        for step in range(1, group_count):
            left = start if step == 1 else start + 2 * group_count + 2 * (step - 2)
            right = start + 2 * step
            target = 380 + 48 * detector if step == group_count - 1 else start + 2 * group_count + 2 * (step - 1)
            product = pairmul((symbol(left), symbol(left + 1)), (symbol(right), symbol(right + 1)))
            for component in range(2):
                sid = 900 + 30 * detector + 2 * group_count + 2 * (step - 1) + component
                expected[sid] = (f'mixed.det{detector}.product{step}.{component}.definition',
                                 normalized(summation(product[component], scalar(symbol(target + component), -1))))
    assert set(actual) == set(expected)
    for sid, (name, poly) in expected.items():
        assert actual[sid][0] == name, (number, sid, 'name')
        assert actual[sid][1] == poly, (number, sid, 'coefficients')
        assert max(sum(i != -1 for i in m) for m in poly) <= 2
    assert len(system['coordinates']) == number
    removed = set(SHARED_REMOVED)
    for detector in range(detector_count):
        removed.update([374 + 48 * detector, 375 + 48 * detector])
        if baseline == 370:
            removed.update(range(650 + 20 * detector, 654 + 20 * detector))
    old_sids = {c['sourceId'] for c in source['coordinates']}
    actual_sids = {c['sourceId'] for c in system['coordinates']}
    assert old_sids - actual_sids == removed
    assert actual_sids - old_sids == new_sids
    assert all(i not in removed for _, poly in actual.values() for m in poly for i in m)
    assert len(actual_sids) == number
    assert system['inputCoordinate'] == polynomial['inputCoordinate'] == 1

    expanded = defaultdict(int)
    for _, poly in actual.values():
        keys = sorted(poly)
        for m, n in combinations_with_replacement(keys, 2):
            expanded[tuple(sorted(m + n))] += int(poly[m] * poly[n]) * (1 if m == n else 2)
    expanded = {m: c for m, c in expanded.items() if c}
    lookup = {c['id']: c['sourceId'] for c in polynomial['coordinates']}
    given = collect((tuple([-1] * t['parameterPower'] + [lookup[i] for i in t['monomial']]),
                     Fraction(int(t['coefficient']))) for t in polynomial['terms'])
    assert expanded == given
    assert max(sum(i != -1 for i in m) for m in given) == 4
    ordinary = defaultdict(dict)
    for m, value in expanded.items():
        ordinary[tuple(i for i in m if i != -1)][m.count(-1)] = value
    coefficient_sum = max(sum(abs(c) for c in p.values()) for p in ordinary.values())
    minimum_parameter = pow(80989, 54929)
    assert minimum_parameter > 1 + coefficient_sum
    assert any(p == {0: 1} for p in ordinary.values())
    data = {'status': 'PASS: exact rows, all coefficients, field normalizations, and quartic degree',
            'variables': number, 'quadraticResiduals': len(actual), 'symbolicTerms': len(expanded),
            'ordinaryMonomialsForSufficientlyLargeN': len(ordinary), 'degree': 4, 'content': 1,
            'heightCoefficientSumBitLength': coefficient_sum.bit_length(),
            'allNAtLeast27464HaveNoCoefficientCancellation': True,
            'coefficientRootBound': 'Every coefficient root has modulus <= 1 + max coefficient absolute sum < A_27464.',
            'modifiedSourceRows': sorted(changed),
            'groups': groups,
            'testOrders': orders,
            'newFieldPowerCount': len(new_power_keys),
            'inputAndLucasSquareCorrectionsDerivedFromSourceRows': [259, 260, 271, 272],
            'deletedSourceCoordinates': sorted(removed),
            'arithmeticScope': 'The checker does not prove elliptic-group, height, prime-pattern, or pole-realization premises.'}
    if baseline == 370:
        A = pow(80989, 54929)
        evaluated = {m: sum(c * A ** a for a, c in p.items()) for m, p in ordinary.items()}
        assert all(evaluated.values())
        height = max(abs(c) for c in evaluated.values())
        data.update(explicitParameter={'base': 80989, 'exponent': 54929, 'N': 27464},
                    ordinaryMonomialsAtExplicitParameter=len(evaluated), largestCoefficientBits=height.bit_length(),
                    largestCoefficientMonomials=[list(m) for m, c in evaluated.items() if abs(c) == height])
    (out / f'independent-verification{number}.json').write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps(data, indent=2))


def local_and_toric_checks():
    # Symbolic exponent pairs are (power of e,power of delta).
    q, q2, q4 = (1, -3), (2, -6), (4, -12)
    a, b, c, d, q10, q40 = (0, -3), (-1, -6), (-3, -9), (8, -6), (19, -3), (79, -3)
    plus = lambda u, v: tuple(a + b for a, b in zip(u, v))
    double = lambda u: plus(u, u)
    assert double(q2) == q4
    assert plus(c, d) == plus(q, q4)
    assert plus(c, q10) == double(d)
    assert plus(c, q40) == double(double(q10))
    tested = 0
    for nu in range(-15, 16, 2):
        for m in [1, 10, 40]:
            for position in range(4):
                for value in range(-50, 51):
                    valuation = 2**position * ((1 - 2*m)*nu + 2*value)
                    assert valuation % 2**(position+1) == 2**position
                    if nu > 0 and 2*valuation > -nu:
                        assert value >= m
                    tested += 1
    result = {'status': 'PASS', 'toricExponents': {'q1': q, 'q1Squared': q2, 'q1Fourth': q4,
                                                 'q10': q10, 'q40': q40},
              'finiteValuationChecks': tested,
              'scope': 'Finite checks supplement, and do not replace, the valuation proof for every odd integer nu.'}
    (ROOT / 'mixed-identities.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    local_and_toric_checks()
    for size in [317, 370]:
        run(size)
