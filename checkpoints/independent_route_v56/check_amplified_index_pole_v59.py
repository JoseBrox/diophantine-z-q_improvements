#!/usr/bin/env python3
"""Exact local and formal-series certificate; no global realization claim."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent


def add(p, q):
    r = dict(p)
    for key, value in q.items():
        r[key] = r.get(key, 0) + value
        if not r[key]:
            del r[key]
    return r


def scale(p, c):
    return {k: c * v for k, v in p.items() if c * v}


def mul(p, q, cutoff):
    r = {}
    for (z, a), c in p.items():
        for (zz, aa), cc in q.items():
            if z + zz <= cutoff:
                key = z + zz, a + aa
                r[key] = r.get(key, 0) + c * cc
    return {k: v for k, v in r.items() if v}


def shift(p, z=0, a=0):
    return {(i + z, j + a): c for (i, j), c in p.items()}


def derivative(p):
    return {(z - 1, a): z * c for (z, a), c in p.items() if z}


order = 12
cutoff = 4 * order + 3
# a stands for d^2. Every coefficient identity is symbolic in both a and z.
w = {(4 * r + 3, r): (-1)**r * comb(2*r, r)//(r+1)
     for r in range(order+1)}
log_derivative = {(4*r, r): (-1)**r * comb(2*r, r)
                  for r in range(order+1)}
curve = add(add(w, shift(mul(w, w, cutoff-1), z=1, a=1)), {(3, 0): -1})
curve = {k: v for k, v in curve.items() if k[0] <= cutoff}
assert not curve
diff = add(scale(mul(w, log_derivative, cutoff), 2),
           add(scale(shift(derivative(w), z=1), -1), w))
assert not diff

rows = []
valuation_fixtures = 0
for T in range(1, 65):
    k = 8*T-7
    assert k > 0 and k % 2 == 1
    assert F(k, 8) > T-1 and F(k, 8) < T
    assert min(k, 8*T-k) > 0
    for e in range(1, 24, 2):
        nu = k*e
        # Completeness: v(C1)>=2Te, v(C2)>=Te.
        for v1 in range(2*T*e, 2*T*e+4):
            for v2 in range(T*e, T*e+4):
                d1, d2 = 2*v1, 2*v2
                vw = min(0, 2*d1-nu) + min(0, 2*d2-nu)
                vb = nu+2*vw
                assert vb >= min(k, 8*T-k)*e > 0
                valuation_fixtures += 1
    # Soundness at a simple denominator prime e=1. Any failed T-fold
    # congruence forces a negative odd b valuation, already from that factor.
    for v2 in range(-2*T-3, T):
        d2 = max(2*v2, -k)
        vw = min(0, 2*d2-k)
        vb_upper = k+2*vw
        assert vb_upper < 0 and vb_upper % 2 == 1
        valuation_fixtures += 1
    rows.append({'T': T, 'odd_weight_power': k,
                 'completeness_odd_valuation_lower_multiple': min(k, 8*T-k),
                 'height_coefficient_under_weak_four_thirds': str(F(T, 2))})

log_terms = [
    {'z_degree': 4*r+1, 'd_degree': 2*r,
     'coefficient': str(F((-1)**r*comb(2*r,r), 4*r+1))}
    for r in range(order+1)
]
certificate = {
    'status': 'PASS',
    'formal_series_terms_verified': order+1,
    'formal_curve_identity_verified_symbolically_through_z_degree': cutoff,
    'invariant_differential_identity_verified_symbolically_through_z_degree': cutoff,
    'valuation_fixtures': valuation_fixtures,
    'amplification_rows': rows,
    'formal_logarithm_terms': log_terms,
    'free_coordinates_added': 0,
    'external_input_equality_proved': False,
    'growth_condition_existentially_encoded': False,
    'new_defining_variable_bound_claimed': False,
}
out = ROOT / 'amplified_index_pole_v59_certificate.json'
out.write_text(json.dumps(certificate, indent=2)+'\n')
print(json.dumps({k: certificate[k] for k in
                 ('status', 'formal_series_terms_verified', 'valuation_fixtures',
                  'free_coordinates_added', 'external_input_equality_proved')}))
