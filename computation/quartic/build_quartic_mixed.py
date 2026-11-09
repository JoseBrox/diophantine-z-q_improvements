#!/usr/bin/env python3
"""Specify the 301- and 351-variable quartics using mixed local test orders.

This is an exact algebraic constructor.  The projection theorem additionally
requires the arithmetic premises and the proof in the accompanying paper.
No numerical search is used to choose any polynomial coefficient.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from math import gcd, lcm
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
PINS = {
    317: '21ba60789e880826dff7298301ffcda1f33e465ed09a45ecf93170069deb9157',
    370: 'd4b9505504345de00c5b4493f32fa1a725405fa631e1226e178280831c078624',
}
SHARED_DELETED = {608, 609, 610, 611, 614, 615, 616, 617, 620, 621, 622, 623,
                  624, 625, 626, 627, 628, 629, 630, 631, 632, 633}


def add(*polynomials):
    out = defaultdict(F)
    for poly in polynomials:
        for monomial, coefficient in poly.items():
            out[monomial] += coefficient
    return {m: c for m, c in out.items() if c}


def scale(poly, coefficient):
    return {m: c * coefficient for m, c in poly.items() if c * coefficient}


def mul(left, right):
    out = defaultdict(F)
    for (a, m), c in left.items():
        for (b, n), d in right.items():
            out[a + b, tuple(sorted(m + n))] += c * d
    return {m: c for m, c in out.items() if c}


def var(i):
    return {(0, (i,)): F(1)}


ONE = {(0, ()): F(1)}


def primitive(poly):
    denominator = lcm(*(c.denominator for c in poly.values()))
    out = {m: int(c * denominator) for m, c in poly.items()}
    content = gcd(*out.values())
    if out[min(out)] < 0:
        content = -content
    return {m: c // content for m, c in sorted(out.items())}


def terms(poly):
    return [{'parameterPower': a, 'monomial': list(m), 'coefficient': str(c)}
            for (a, m), c in sorted(poly.items())]


def fourth_power_from_source(u, v):
    """Conjugate of f^4, where w^2 = 193*u - 132*v*sqrt(2)."""
    return (scale(add(scale(var(u), 37249), scale(var(v), -34848)), F(1, 2401)),
            scale(add(var(u), scale(var(v), -1)), F(-25476, 2401)))


def eighth_power_from_source(u, v):
    """Conjugate of f^8, where w^4 = u + v*sqrt(2)."""
    return (scale(add(scale(var(u), 72097), scale(var(v), 101904)), F(1, 5764801)),
            scale(add(scale(var(u), 50952), scale(var(v), 72097)), F(-1, 5764801)))


def fieldmul(left, right):
    return (add(mul(left[0], right[0]), scale(mul(left[1], right[1]), 2)),
            add(mul(left[0], right[1]), mul(left[1], right[0])))


def construct(baseline):
    raw = (HERE / f'family{baseline}' / f'quadratic-family{baseline}.json').read_bytes()
    assert sha256(raw).hexdigest() == PINS[baseline]
    old = json.loads(raw)
    old_source = {c['id']: c['sourceId'] for c in old['coordinates']}
    old_by_source = {c['sourceId']: c for c in old['coordinates']}
    detector_count = 2 if baseline == 317 else 3
    groups = ([['H', 'C1', 'V0'], ['C2', 'I', 'V2'], ['C3', 'U2', 'V3'],
               ['C4', 'U3', 'V4'], ['F', 'U4'], ['U1', 'V1']] if baseline == 317 else
              [['H', 'C1', 'V1', 'V0'], ['C2', 'I', 'V2'], ['C3', 'U2', 'V3'],
               ['C4', 'U3', 'V4'], ['F', 'U4', 'U1']])
    group_count = len(groups)
    deleted = set(SHARED_DELETED)
    for k in range(detector_count):
        deleted.update([374 + 48 * k, 375 + 48 * k])
        if group_count == 5:
            deleted.update(range(650 + 20 * k, 654 + 20 * k))
    assert deleted <= set(old_by_source)
    old_rows = []
    for row in old['residuals']:
        poly = {(t['parameterPower'], tuple(sorted(old_source[i] for i in t['monomial']))):
                F(int(t['coefficient'])) for t in row['terms']}
        old_rows.append((row, poly))

    orders = {name: 1 for name in ['U1', 'U2', 'U3', 'U4', 'V0', 'V1', 'V2', 'V3', 'V4']}
    orders.update(C1=10, I=10, H=40, C2=40, C3=40, C4=40, F=40)
    assert sorted(name for group in groups for name in group) == sorted(orders)
    powers = {}
    for i, sid in enumerate([255, 257, 259, 261], 1):
        powers[f'U{i}', 0] = var(sid), scale(var(sid + 1), 2)
    for i, (f, w2, w4) in enumerate([(178, 180, 182), (190, 192, 0),
                                    (196, 198, 200), (208, 210, 212), (220, 222, 224)]):
        powers[f'V{i}', 0] = var(f), scale(var(f + 1), -2)
        powers[f'V{i}', 1] = fourth_power_from_source(w2, w2 + 1)
        if w4:
            powers[f'V{i}', 2] = eighth_power_from_source(w4, w4 + 1)
    for name, sid in [('C1', 305), ('H', 311), ('C2', 313), ('C3', 315), ('C4', 317)]:
        powers[name, 0] = var(sid), scale(var(sid + 1), 2)
    powers['I', 0] = (add(var(307), scale(var(232), -6), scale(var(248), 306), scale(ONE, 15015)),
                       add(scale(var(308), 2), scale(var(233), -6)))
    powers['F', 0] = (add(var(319), scale(var(253), -2), ONE),
                       add(scale(var(320), 4), scale(var(254), -4)))

    new_coordinates = []
    new_rows = []
    power_specification = []

    def need_power(name, level):
        if (name, level) in powers:
            return powers[name, level]
        previous = need_power(name, level - 1)
        value = fieldmul(previous, previous)
        sources = [800 + len(new_coordinates), 801 + len(new_coordinates)]
        assert all(sid not in old_by_source for sid in sources)
        for component, sid in enumerate(sources):
            new_coordinates.append({'sourceId': sid, 'name': f'mixed.{name}.power{2**(level+1)}.{component}', 'kind': 'gate'})
            new_rows.append(({'sourceId': sid, 'name': f'mixed.{name}.power{2**(level+1)}.{component}.definition'},
                             primitive(add(value[component], scale(var(sid), -1)))))
        powers[name, level] = tuple(var(sid) for sid in sources)
        power_specification.append({'test': name, 'power': 2**(level+1), 'sourceCoordinates': sources})
        return powers[name, level]

    for group in groups:
        for level, name in enumerate(group):
            need_power(name, level)
    expected_field = 5 if baseline == 317 else 9
    assert len(new_coordinates) == 2 * expected_field
    changes = {}
    removed_rows = []
    for row, poly in old_rows:
        if row['name'].startswith(('hybrid.1.', 'hybrid.10.', 'hybrid.40.', 'hybrid.det')) or '.E40.power' in row['name']:
            removed_rows.append(row['sourceId'])
    assert len(removed_rows) == 22 + 24 * detector_count

    for detector in range(detector_count):
        off = 48 * detector
        q, q2, q4 = 352 + off, 361 + off, 362 + off
        c, d = 355 + off, 356 + off
        changes[f'detector{detector}.E1.power3.definition'] = (
            f'detector{detector}.E1.power4.definition',
            add(mul(var(q2), var(q2)), scale(var(q4), -1)))
        changes[f'detector{detector}.toric.d.definition'] = (
            f'detector{detector}.toric.d.definition',
            add(mul(var(c), var(d)), scale(mul(var(q), var(q4)), -1)))
        weights = {(1, 0): var(q), (1, 1): var(q2), (1, 2): var(q4),
                   (10, 0): var(359 + off), (10, 1): var(369 + off), (40, 0): var(360 + off)}
        if group_count == 5:
            sid = 850 + detector
            new_coordinates.append({'sourceId': sid, 'name': f'mixed.det{detector}.q1Power8', 'kind': 'gate'})
            new_rows.append(({'sourceId': sid, 'name': f'mixed.det{detector}.q1Power8.definition'},
                             primitive(add(mul(var(q4), var(q4)), scale(var(sid), -1)))))
            weights[1, 3] = var(sid)
        start = 634 + 20 * detector
        for g, group in enumerate(groups):
            for component in range(2):
                poly = add(ONE if component == 0 else {},
                           *(mul(weights[orders[name], level], powers[name, level][component])
                             for level, name in enumerate(group)),
                           scale(var(start + 2 * g + component), -1))
                new_rows.append(({'sourceId': 900 + 30 * detector + 2 * g + component,
                                  'name': f'mixed.det{detector}.factor{g}.{component}.definition'}, primitive(poly)))
        accumulator = var(start), var(start + 1)
        for step in range(1, group_count):
            target = (380 + off if step == group_count - 1 else start + 2 * group_count + 2 * (step - 1))
            value = fieldmul(accumulator, (var(start + 2 * step), var(start + 2 * step + 1)))
            for component in range(2):
                new_rows.append(({'sourceId': 900 + 30 * detector + 2 * group_count + 2 * (step - 1) + component,
                                  'name': f'mixed.det{detector}.product{step}.{component}.definition'},
                                 primitive(add(value[component], scale(var(target + component), -1)))))
            accumulator = var(target), var(target + 1)

    assembled = []
    changed_rows = []
    for row, poly in old_rows:
        if row['sourceId'] in removed_rows:
            continue
        if row['name'] in changes:
            new_name, poly = changes.pop(row['name'])
            row = dict(row, name=new_name)
            changed_rows.append(row['sourceId'])
        assert all(i not in deleted for (a, m) in poly for i in m), row['name']
        assembled.append((row, primitive(poly)))
    assert not changes, changes
    assembled.extend(new_rows)

    coordinates = []
    for coord in old['coordinates']:
        if coord['sourceId'] in deleted:
            continue
        name = coord['name']
        if coord['sourceId'] in {362, 410, 458}:
            name = name.replace('.power3.', '.power4.')
        if name.startswith('hybrid.det'):
            name = f'mixed.private.{coord["sourceId"]}'
        coordinates.append(dict(coord, id=len(coordinates) + 1, name=name))
    for coord in new_coordinates:
        coordinates.append(dict(coord, id=len(coordinates) + 1))
    mapping = {c['sourceId']: c['id'] for c in coordinates}
    rows = []
    coefficient_table = defaultdict(int)
    for metadata, poly in assembled:
        transported = {(a, tuple(sorted(mapping[i] for i in m))): c for (a, m), c in poly.items()}
        assert max(len(m) for a, m in transported) <= 2
        rows.append(dict(metadata, terms=terms(transported)))
        for (a, m), c in transported.items():
            for (b, n), d in transported.items():
                coefficient_table[a + b, tuple(sorted(m + n))] += c * d
    coefficient_table = {m: c for m, c in coefficient_table.items() if c}
    saving = 16 if baseline == 317 else 19
    number = baseline - saving
    assert len(coordinates) == number
    assert len(rows) == len(old['residuals']) - saving
    output = HERE / f'family{number}'
    output.mkdir(exist_ok=True)
    system = dict(old, format='integer-quadratic-family-v4', variables=number,
                  source={'construction': f'quartic-family{baseline}', 'sha256': PINS[baseline]},
                  coordinates=coordinates, residuals=rows)
    polynomial = {'format': 'integer-quartic-family-v4', 'variables': number, 'degree': 4,
                  'inputCoordinate': 1, 'fixedParameter': old['fixedParameter'],
                  'coordinates': coordinates, 'terms': terms(coefficient_table)}
    ordinary = defaultdict(dict)
    for (a, m), c in coefficient_table.items():
        ordinary[m][a] = c
    height = max(sum(abs(c) for c in part.values()) for part in ordinary.values())
    report = {
        'status': 'Exact algebraic specification; projection theorem requires the stated arithmetic premises.',
        'baselineVariables': baseline, 'variables': number, 'quadraticResiduals': len(rows),
        'degree': max(len(m) for a, m in coefficient_table),
        'symbolicTerms': len(coefficient_table),
        'ordinaryMonomialsForSufficientlyLargeN': len(ordinary),
        'deletedSourceCoordinates': sorted(deleted), 'newSourceCoordinates': [c['sourceId'] for c in new_coordinates],
        'deletedSourceRows': removed_rows, 'changedSourceRows': changed_rows,
        'newSourceRows': [r['sourceId'] for r, p in new_rows],
        'groups': groups, 'testOrders': orders, 'newFieldPowers': power_specification,
        'factor': '1+sum_j q_mj^(2^j)*D_j^(2^(j+1))',
        'toricReplacement': {'fourthPower': 'q4=q2^2', 'unchangedFifthPower': 'c*d=q*q4'},
        'heightBound': {'coefficientSumBitLength': height.bit_length(),
                        'formula': f'H(P_N)<2^{height.bit_length()}*80989^(4*N+2)'},
    }
    for filename, data in [(f'quadratic-family{number}.json', system),
                           (f'polynomial-family{number}.json', polynomial),
                           (f'construction-report{number}.json', report)]:
        (output / filename).write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ['baselineVariables', 'variables', 'quadraticResiduals',
                                          'degree', 'symbolicTerms', 'ordinaryMonomialsForSufficientlyLargeN',
                                          'heightBound']}, indent=2))


if __name__ == '__main__':
    for count in [317, 370]:
        construct(count)
