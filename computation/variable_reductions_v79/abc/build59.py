#!/usr/bin/env python3
"""Construct the 59-coordinate ordinary-abc quartic from its pinned chart.

The chart and Laurent packing derive from Gabe Conant's notes with Astra 6.2,
audited in v78.  The single derivative contact and gate below are new v79 work.
Only exact integer polynomial arithmetic is used; arithmetic premises are in
the accompanying paper, not established by this coefficient computation.
"""
from collections import defaultdict
from itertools import product
from math import gcd
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PARENT = ROOT / 'computation/coauthor_audit_v78/work_abc/small_gate62/primitive/quadrics.json'
SHIFTS = [-8, -7, -2, -1, 3, 4, 5, 6]
KEEP = [1, *range(3, 32), *range(36, 47), 59, 61, 62]
NEW = ['M', 'M2', 'x', 'y', 'x2', 'x4', 'Gx', 'Gpx',
       'y2', 'y4', 'Gy', 'Gpy', 'Ha', 'D2', 'lambda']
assert len(KEEP) == 44 and len(NEW) == 15
IDS = {old: i + 1 for i, old in enumerate(KEEP)}
N = {name: len(KEEP) + i + 1 for i, name in enumerate(NEW)}


def add(*polys):
    out = defaultdict(int)
    for poly in polys:
        for key, value in poly.items():
            out[key] += value
    return {key: value for key, value in out.items() if value}


def term(coef=1, *monomial, bp=0):
    return {(bp, tuple(sorted(monomial))): coef} if coef else {}


def serial(poly):
    return [{'parameterPower': b, 'monomial': list(m), 'coefficient': str(v)}
            for (b, m), v in sorted(poly.items())]


def shift_polynomial():
    coeff = [1]
    for shift in SHIFTS:
        nxt = [0] * (len(coeff) + 1)
        for i, a in enumerate(coeff):
            nxt[i] += shift * a
            nxt[i + 1] += a
        coeff = nxt
    return coeff


def make_rows():
    source = json.loads(PARENT.read_text())
    rows = []
    allowed = ('reference.', 'pair.', 'product.', 'height.', 'C', 'I')
    exact = {'product0', 'product1', 'sharedD', 'shared.unit'}
    for row in source['residuals']:
        name = row['name']
        if (name.startswith(allowed) or name in exact or
                name.startswith('detector0.pole.')):
            poly = {}
            for t in row['terms']:
                key = (t['parameterPower'], tuple(sorted(IDS[i] for i in t['monomial'])))
                poly[key] = int(t['coefficient'])
            rows.append((name, poly))
    assert len(rows) == 32
    c, ci, d, tau, b = (IDS[i] for i in (61, 62, 59, 38, 39))
    rows.extend([
        ('single.errorSquare', add(term(1, N['D2']), term(-1, d, d))),
        ('single.ratioNormalizer', add(term(1, c, N['lambda']), term(-1),
             term(-1, c, N['D2']), term(1, N['lambda'], N['D2']))),
        ('single.gate', add(term(1, c, N['lambda']), term(-1, tau), term(-1, c, tau))),
        ('single.poleInput', add(term(1, b), term(-1, tau, tau))),
        ('height.M', add(term(1, N['M']), term(-1, bp=1),
                         term(-1, IDS[31], IDS[31]), term(-4, IDS[9], IDS[9]))),
        ('height.M2', add(term(1, N['M2']), term(-1, N['M'], N['M']))),
        ('contact.midpoint', add(term(1, c, N['x']), term(1, c, N['y']),
                                 term(-2, N['M2'], N['M2']))),
    ])
    coeff = shift_polynomial()
    assert coeff[7] == 0 and coeff[6] != 0
    # P=tG'-8G and Q=(4t^2+a6)G'-32tG both have degree at most six.
    pp = [(i - 8) * a for i, a in enumerate(coeff)]
    qq = [0] * 10
    for i, a in enumerate(coeff):
        if i:
            qq[i + 1] += 4 * i * a
            qq[i - 1] += coeff[6] * i * a
        qq[i + 1] -= 32 * a
    assert all(a == 0 for a in pp[7:]) and all(a == 0 for a in qq[7:])
    for side in ('x', 'y'):
        t, t2, t4 = (N[side + s] for s in ('', '2', '4'))
        gg, gp = N['G' + side], N['Gp' + side]
        rows.extend([
            (f'contact.{side}.square', add(term(1, t2, ci), term(-1, t, t))),
            (f'contact.{side}.fourth', add(term(1, t4, ci), term(-1, t2, t2))),
        ])
        powers = [(ci, ci), (t, ci), (t2, ci), (t, t2), (t4, ci),
                  (t, t4), (t2, t4), None, (t4, t4)]
        rows.append((f'contact.{side}.value', add(term(1, gg, ci),
                    *(term(-a, *powers[i]) for i, a in enumerate(coeff) if a))))
        rows.append((f'contact.{side}.derivative1', add(term(1, t, gp), term(-8, gg, ci),
                    *(term(-a, *powers[i]) for i, a in enumerate(pp[:7]) if a))))
        rows.append((f'contact.{side}.derivative2', add(term(4, t2, gp), term(coeff[6], gp, ci),
                    term(-32, t, gg), *(term(-a, *powers[i]) for i, a in enumerate(qq[:7]) if a))))
    rows.extend([
        ('contact.derivativeSum', add(term(1, N['Ha']),
              term(-1, N['Gpx'], N['Gy']), term(-1, N['Gx'], N['Gpy']))),
        ('contact.derivativeQuotient', add(term(1, N['Ha'], ci),
              term(16, N['Gx'], N['Gy']))),
    ])
    assert len(rows) == 51
    assert all(len(m) <= 2 for _, p in rows for _, m in p)
    assert {i for _, p in rows for _, m in p for i in m} == set(range(1, 60))
    return rows


def main():
    rows = make_rows()
    poly = defaultdict(int)
    for _, row in rows:
        for ((e, m), a), ((f, n), b) in product(row.items(), repeat=2):
            poly[e + f, tuple(sorted(m + n))] += a * b
    poly = {k: v for k, v in poly.items() if v}
    content = gcd(*poly.values())
    assert content == 1
    profiles = defaultdict(dict)
    for (e, m), a in poly.items():
        profiles[m][e] = a
    constants = {m: p[0] for m, p in profiles.items() if set(p) == {0}}
    mixed = [{'monomial': list(m), 'coefficients': p} for m, p in profiles.items() if len(p) > 1]
    out = HERE / 'quartic59'
    out.mkdir(parents=True, exist_ok=True)
    files = {
        'quadrics.json': {'variables': 59, 'parameter': 'B', 'input': 1,
                         'residuals': [{'name': n, 'terms': serial(p)} for n, p in rows]},
        'polynomial.json': {'variables': 59, 'parameter': 'B', 'terms': serial(poly)},
        'maps.json': {'parent': str(PARENT.relative_to(ROOT)), 'parent_sha256': hashlib.sha256(PARENT.read_bytes()).hexdigest(),
                     'old_to_new': IDS, 'new_coordinates': N,
                     'physical_scaling': {'c': IDS[61], 'c_inverse': IDS[62],
                         'unscaled_tau': IDS[38], 'M': N['M'], 'M2': N['M2'],
                         'contact_degree_one_weight': [N[s] for s in NEW if s not in ('M', 'M2', 'Ha', 'D2', 'lambda')],
                         'contact_derivative_sum_weight': {'coordinate': N['Ha'], 'power': 2}},
                     'shifts': SHIFTS, 'G_coefficients': shift_polynomial()},
        'certificate.json': {'schema': 'ordinary-abc-quartic59/v79', 'variables': 59,
                     'quadrics': 51, 'degree': 4, 'content': content,
                     'monomials': len(profiles), 'parameter_separated_terms': len(poly),
                     'maximum_fixed_coefficient': max(map(abs, constants.values())),
                     'mixed_profiles': mixed,
                     'height_parameters': {'contact_count': 8, 'midpoint_power': 4,
                         'epsilon': '1/100', 'mixed_power_abc_exponent': '1001/1000',
                         'radical_height_rate': '193/100', 'input_height_rate': '501/997',
                         'strict_margin': '92221/99700'},
                     'defining_parameter': 'Every sufficiently large odd B; threshold ineffective',
                     'arithmetic_premises': 'Retained elliptic, formal-comparison, trace-index, simultaneous prime-pattern and simultaneous-twist premises, plus ordinary rational abc',
                     'attribution': "The translated-secant chart and Laurent packing derive from notes of Gabe Conant with Astra 6.2, audited in v78; the one-pole derivative transfer is v79."}
    }
    for name, data in files.items():
        (out / name).write_text(json.dumps(data, indent=2 if name in ('maps.json', 'certificate.json') else None,
            separators=None if name in ('maps.json', 'certificate.json') else (',', ':')) + '\n')
    print(json.dumps(files['certificate.json'], indent=2))


if __name__ == '__main__':
    main()
