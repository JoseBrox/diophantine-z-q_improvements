#!/usr/bin/env python3
"""Construct the 56-coordinate ordinary-abc quartic from its pinned chart.

The chart and Laurent packing derive from Gabe Conant's notes with Astra 6.2,
audited in v78.  The derivative transfer and gate are v79/v80 work; the paired-contact rechart is v81 work.
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
CENTER = 16
RADII = [1, 4, 7, 8]
PADDING = 2  # The scaled trace is 2-adically integral on every integer witness.
SHIFTS = sorted([CENTER+r for r in RADII] + [CENTER-r for r in RADII])
KEEP = [1, *range(3, 32), *range(36, 47), 59, 61, 62]
NEW = ['M', 'M2', 'a', 'z', 'T', 'S', 'P', 'A1', 'A2',
       'Fbar', 'H', 'alpha']
assert len(KEEP) == 44 and len(NEW) == 12
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
        ('single.alpha', add(term(1, N['alpha']), term(-1, ci), term(-1, d, d))),
        ('single.gate', add(term(1, tau, N['alpha']), term(1, tau), term(-1, N['alpha']))),
        ('single.poleInput', add(term(1, b), term(-7, tau, tau))),
        ('height.M', add(term(1, N['M']), term(-1, bp=1),
                         term(-PADDING, IDS[31], IDS[31]), term(-4*PADDING, IDS[9], IDS[9]))),
        ('height.M2', add(term(1, N['M2']), term(-1, N['M'], N['M']))),
        ('contact.center', add(term(1, N['a']), term(-1, N['M2'], N['M2']), term(-CENTER))),
        ('contact.sum', add(term(1, N['S']), term(1, N['T']), term(-2, N['a'], N['a']))),
        ('contact.difference', add(term(1, N['S']), term(-1, N['T']), term(-2, N['z'], N['z']))),
        ('contact.square', add(term(1, N['P']), term(-1, N['T'], N['T']))),
    ])
    pp, ss = N['P'], N['S']
    # Each quadratic is the product of the two indicated linear contact factors.
    for label, r, t in [('A1', 1, 8), ('A2', 4, 7)]:
        rr, tt = r*r, t*t
        rows.append((f'contact.{label}', add(
            term(1, N[label]), term(-1, pp, pp),
            term(2*(rr+tt), pp, ss), term(-(rr*rr+tt*tt), pp),
            term(-4*rr*tt, ss, ss), term(2*(rr*tt*tt+tt*rr*rr), ss),
            term(-rr*rr*tt*tt))))
    aa, bb = N['A1'], N['A2']
    rows.extend([
        ('contact.value', add(term(1, N['a'], N['Fbar']), term(-1, aa, bb))),
        ('contact.partialCombined', add(term(1, N['H']),
            term(-4, N['T'], pp), term(260, N['T'], ss), term(-8194, N['T']),
            term(130, pp), term(-512, ss), term(8320))),
        ('contact.derivativeQuotient', add(term(1, N['H'], aa), term(1, N['H'], bb),
            term(-2880, N['T'], aa), term(5760, ss, aa), term(-93600, aa),
            term(8, c, N['Fbar']))),
    ])
    assert len(rows) == 46
    assert all(len(m) <= 2 for _, p in rows for _, m in p)
    assert {i for _, p in rows for _, m in p for i in m} == set(range(1, 57))
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
    out = HERE / 'quartic56'
    out.mkdir(parents=True, exist_ok=True)
    files = {
        'quadrics.json': {'variables': 56, 'parameter': 'B', 'input': 1,
                         'residuals': [{'name': n, 'terms': serial(p)} for n, p in rows]},
        'polynomial.json': {'variables': 56, 'parameter': 'B', 'terms': serial(poly)},
        'maps.json': {'parent': str(PARENT.relative_to(ROOT)), 'parent_sha256': hashlib.sha256(PARENT.read_bytes()).hexdigest(),
                     'old_to_new': IDS, 'new_coordinates': N,
                     'physical_scaling': {'physical_pole_input_multiplier': 7,
                         'unscaled_alpha': N['alpha'], 'c': IDS[61], 'c_inverse': IDS[62],
                         'unscaled_tau': IDS[38], 'unscaled_height_coordinates': {k: N[k] for k in ('M', 'M2')},
                         'unscaled_contact_coordinates': {k: N[k] for k in ('a', 'z', 'T', 'S', 'P', 'A1', 'A2', 'Fbar', 'H')}},
                     'shifts': SHIFTS, 'center': CENTER, 'radii': RADII, 'padding': PADDING},
        'certificate.json': {'schema': 'ordinary-abc-quartic56/v81', 'variables': 56,
                     'quadrics': 46, 'degree': 4, 'content': content,
                     'monomials': len(profiles), 'parameter_separated_terms': len(poly),
                     'maximum_fixed_coefficient': max(map(abs, constants.values())),
                     'mixed_profiles': mixed,
                     'contact_rechart': {'center': CENTER, 'radii': RADII, 'shifts': SHIFTS,
                         'height_padding': PADDING, 'variables': 9,
                         'radius_pairs': [[1, 8], [4, 7]], 'pair_square_sum': 65,
                         'paired_derivative_difference': 'H2-H1=720*(-4*T+8*S-130)',
                         'Phi': 'product(P-2*r^2*S+r^4, r=1,4,7,8)',
                         'derivative_identity': 'F_a=2*a*(2*T*Phi_P+Phi_S)',
                         'quotient_equation': 'H1*(A1+A2)+720*(-4*T+8*S-130)*A1+8*c*Fbar=0',
                         'Fbar': 'F/a'},
                     'height_parameters': {'contact_count': 8, 'midpoint_power': 4,
                         'epsilon': '1/100', 'mixed_power_abc_exponent': '1001/1000',
                         'radical_height_rate': '193/100', 'input_height_rate': '501/997',
                         'strict_margin': '92221/99700'},
                     'defining_parameter': 'Every sufficiently large odd B; threshold ineffective',
                     'normalizer': {'alpha': 'u+u^2 D^2', 'tau': 'alpha/(1+alpha)',
                         'physical_pole_input': '7 tau^2/u', 'additional_coordinate_count': 1},
                     'arithmetic_premises': 'Retained elliptic, formal-comparison, trace-index and simultaneous prime-pattern premises; ordinary rational abc; Burungale Theorem B (arXiv:2611.16130v1) only in its published beta=7 mod 8, eta=1 mod 8 square classes',
                     'attribution': "The translated-secant chart and Laurent packing derive from notes of Gabe Conant with Astra 6.2, audited in v78; the one-pole derivative transfer is v79, the one-helper normalization is v80, and the nonlinear paired-contact rechart is v81."}
    }
    for name, data in files.items():
        (out / name).write_text(json.dumps(data, indent=2 if name in ('maps.json', 'certificate.json') else None,
            separators=None if name in ('maps.json', 'certificate.json') else (',', ':')) + '\n')
    print(json.dumps(files['certificate.json'], indent=2))


if __name__ == '__main__':
    main()
