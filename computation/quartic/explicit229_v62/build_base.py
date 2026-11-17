#!/usr/bin/env python3
"""Construct the complete 229-coordinate three-detector candidate.

The finite algebra and expansion are exact. The effective arithmetic
threshold is a separate proof obligation, not an output of this script.
"""
from collections import defaultdict
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from math import gcd
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def read_poly(row):
    return {(t['parameterPower'], tuple(t['monomial'])):
            Fraction(t['coefficient']) for t in row['terms']}


def serial(poly):
    return [{'parameterPower': a, 'monomial': list(m), 'coefficient': str(c)}
            for (a, m), c in sorted(poly.items()) if c]


def dump(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2) + '\n')


def build_base():
    raw = (HERE / 'source/quadratic195.json').read_bytes()
    source = json.loads(raw)
    assert source['variables'] == 195 and len(source['residuals']) == 175
    local = [c for c in source['coordinates']
             if 'detector1' in c['name'] or 'det1' in c['name']]
    assert len(local) == 34
    mapping = {c['id']: 196 + j for j, c in enumerate(local)}
    name = lambda n: n.replace('detector1', 'detector2').replace('det1', 'det2')
    result = deepcopy(source)
    result['format'] = 'three-detector-quartic229/v62'
    result['variables'] = 229
    result['arithmeticStatus'] = 'The defining threshold N>=15 is proved in the accompanying manuscript under its retained arithmetic premises.'
    result.pop('transformation', None)
    result['coordinates'] += [dict(id=mapping[c['id']], name=name(c['name']),
                                   clonedFrom195Id=c['id']) for c in local]
    cloned_rows = []
    for old in source['residuals']:
        if 'detector1' not in old['name'] and 'det1' not in old['name']:
            continue
        row = deepcopy(old)
        row.update(id=len(result['residuals']) + 1, name=name(old['name']),
                   clonedFrom195Row=old['id'])
        for term in row['terms']:
            term['monomial'] = sorted(mapping.get(i, i) for i in term['monomial'])
        result['residuals'].append(row)
        cloned_rows.append({'source_row': old['id'], 'target_row': row['id']})
    assert len(cloned_rows) == 31
    q, w, t0, t1, t2 = 77, 78, 2, 86, mapping[86]
    aggregate = result['residuals'][174]
    assert aggregate['name'] == 'inverse_vieta.unweighted.aggregate'
    ap = read_poly(aggregate)
    assert ap[(0, (q, q))] == 14
    ap[(0, (q, q))] = 26
    aggregate['terms'] = serial(ap)
    aggregate['name'] = 'inverse_vieta.shifted.aggregate.component0'

    # These are q^2 times the two components of sum x(Q_i).
    # All coordinates below are the final parameter-scaled 195 coordinates.
    # Pair recovery: x(Q)=s^2 + (11-6*rho)(f+g), rho^2=2.
    s0, s1 = defaultdict(Fraction), defaultdict(Fraction)
    for f0, f1, g0, g1, a, b, cpower in [
            (152, 153, 156, 157, 160, 161, 0),
            (162, 163, 166, 167, 170, 171, 1),
            (172, 173, 176, 177, 180, 181, 1)]:
        # Only f in pairs 3,4 carries C; the corresponding g does not.
        for i, j, power in [(f0, f1, cpower), (g0, g1, 0)]:
            s0[(power, (q, i))] += 11
            s0[(power, (q, j))] -= 12
            s1[(power, (q, i))] -= 6
            s1[(power, (q, j))] += 11
        s0[(0, (a, a))] += 1
        s0[(0, (b, b))] += 2
        s1[(0, (a, b))] += 2
    s0[(0, (q, 192))] += 1
    s1[(0, (q, 193))] += 1
    oldagg = read_poly(source['residuals'][174])
    expected = dict(s0)
    expected.update({(0, (t0, q)): Fraction(2),
                     (0, (q, q)): Fraction(14),
                     (0, (q, t1)): Fraction(-2)})
    assert oldagg == expected
    shift = dict(s1)
    shift.update({(0, (t0, q)): Fraction(2),
                  (0, (q, t1)): Fraction(-4),
                  (0, (q, t2)): Fraction(2),
                  (0, (q, q)): Fraction(-8)})
    result['residuals'].append(dict(id=207,
        name='inverse_vieta.shifted.aggregate.component1', terms=serial(shift)))
    assert len(result['residuals']) == 207

    expanded = defaultdict(Fraction)
    for row in result['residuals']:
        p = read_poly(row)
        assert all(len(m) <= 2 and c.denominator == 1 for (a, m), c in p.items())
        for (a, m), c in p.items():
            for (b, n), d in p.items():
                expanded[(a + b, tuple(sorted(m + n)))] += c * d
    expanded = {key: c for key, c in expanded.items() if c}
    profiles = defaultdict(dict)
    for (a, m), c in expanded.items():
        profiles[m][a] = int(c)
    assert {i for a, m in expanded for i in m} == set(range(1, 230))
    assert max(len(m) for a, m in expanded) == 4
    assert gcd(*(int(c) for c in expanded.values())) == 1
    assert expanded[(0, (1, 1, 1, 1))] == 1
    poly = dict(format='sum-of-207-quadratic-squares/v62', variables=229,
                degree=4, inputCoordinate=1, fixedParameter=result['fixedParameter'],
                terms=serial(expanded))
    certificate = dict(schema='detector-graft/v62',
        source_sha256=sha256(raw).hexdigest(),
        source_variables=195, source_rows=175,
        cloned_coordinate_map={str(k): v for k, v in mapping.items()},
        cloned_row_map=cloned_rows,
        changed_rows=[175], new_shift_row=207,
        retained_guard_ids=[26, 38], new_guard_id=next(
            row['id'] for row in result['residuals']
            if row['name'] == 'detector2.inverseWeight.definition'),
        physical_arguments={'t0': 'x2/x77', 't1': 'x86/x77',
                            't2': f'x{t2}/x77'},
        sum_components_numerators=[serial(s0), serial(s1)],
        sum_components_denominator='x77^2',
        physical_shifts=['t1-t0=13+S0/2', 't2-t1=17+(S0-S1)/2'],
        new_coordinates=34, new_rows=32, new_guards=1,
        variables=229, quadratic_rows=207, degree=4, content=1,
        coordinate_monomials=len(profiles), parameter_terms=len(expanded),
        arithmetic_status='Complete three-detector family; N>=15 is proved in the accompanying manuscript under retained arithmetic premises.',
        local_chart_status='Complete literal clone, no new square or recovery coordinate.')
    return result, certificate
