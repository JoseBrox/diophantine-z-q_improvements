#!/usr/bin/env python3
"""Exact local and formal-series certificate; no global realization claim."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
import argparse

ROOT = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[3]
_parser = argparse.ArgumentParser(description=__doc__)
_parser.add_argument("--output", type=Path, default=ROOT/"certificate.json")
OUTPUT = _parser.parse_args().output



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

# Exact monic isogeny algebras for n=2,3. Here z denotes x and a=d^2.
def pmul(p, q):
    return mul(p, q, 1000)


f_curve = {(3,0): 1, (1,1): -1}
A2 = {(4,0): 1, (2,1): 2, (0,2): 1}
B2 = scale(f_curve, 4)
psi3 = {(4,0): 3, (2,1): -6, (0,2): -1}
Q6 = {(6,0): 1, (4,1): -5, (2,2): -5, (0,3): 1}
B3 = pmul(psi3, psi3)
A3 = add(shift(B3,z=1), scale(pmul(f_curve,Q6),-8))
# This identity proves Q6 is nonzero at any root of psi3 when a!=0.
gcd_witness = add(add(scale(Q6,3),
                      scale(pmul({(2,0):1,(0,1):-3},psi3),-1)),
                  {(2,2):32})
assert not gcd_witness
isogeny_rows = []
for n, A, B in ((2,A2,B2),(3,A3,B3)):
    assert max(z for z,a in A)==n*n
    assert A[(n*n,0)]==1
    assert max(z for z,a in B)==n*n-1
    assert B[(n*n-1,0)]==n*n
    derivative_numerator = add(pmul(derivative(A),B),
                               scale(pmul(A,derivative(B)),-1))
    A3minus_aAB2 = add(pmul(pmul(A,A),A),
                       scale(shift(pmul(A,pmul(B,B)),a=1),-1))
    lhs = scale(pmul(B,A3minus_aAB2),n*n)
    rhs = pmul(f_curve,pmul(derivative_numerator,derivative_numerator))
    assert not add(lhs,scale(rhs,-1))
    isogeny_rows.append({'n':n,'monic_degree':n*n,
                         'denominator_degree':n*n-1,
                         'differential_identity_exact':True,
                         'numerator_terms':[[z,a,c] for (z,a),c in sorted(A.items())],
                         'denominator_terms':[[z,a,c] for (z,a),c in sorted(B.items())]})

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
    # Uniform preparation at two, at formal depth four, for the same
    # retained point P for every T. Equal-depth cancellation raises W.
    two_nu = 4*k
    for v1 in range(8*T,8*T+4):
        for v2 in range(4*T,4*T+4):
            assert 4*v1-two_nu > 0
            two_lower = 2+two_nu+2*min(0,4*v2-two_nu)
            assert two_lower >= 2+min(4*k,28) >= 6
            valuation_fixtures += 1
    rows.append({'T': T, 'odd_weight_power': k,
                 'completeness_odd_valuation_lower_multiple': min(k, 8*T-k),
                 'height_coefficient_under_weak_four_thirds': str(F(T, 2))})

log_terms = [
    {'z_degree': 4*r+1, 'd_degree': 2*r,
     'coefficient': str(F((-1)**r*comb(2*r,r), 4*r+1))}
    for r in range(order+1)
]
coprime_rows = []
for kappa in (F(16,15), F(121,100), F(4,3), F(3,2),
              F(5,3), F(7,4), F(19,10), F(199,100)):
    coefficient = 2/kappa-1
    R = (1/coefficient).numerator//(1/coefficient).denominator+1
    primes = [n for n in range(2,R+1)
              if all(n%d for d in range(2,int(n**0.5)+1))]
    modulus = 1
    for p in primes:
        modulus *= p
    gap = coefficient-F(1,R)
    assert gap > 0
    coprime_rows.append({'kappa': str(kappa), 'simple_support_coefficient': str(coefficient),
                         'prime_cutoff': R, 'index_modulus': modulus,
                         'old_support_upper': str(F(1,R)), 'strict_gap': str(gap)})
certificate = {
    'status': 'PASS',
    'formal_series_terms_verified': order+1,
    'formal_curve_identity_verified_symbolically_through_z_degree': cutoff,
    'invariant_differential_identity_verified_symbolically_through_z_degree': cutoff,
    'valuation_fixtures': valuation_fixtures,
    'amplification_rows': rows,
    'formal_logarithm_terms': log_terms,
    'monic_isogeny_identity_rows': isogeny_rows,
    'coprime_index_rows': coprime_rows,
    'arithmetic_hypothesis': 'fixed weak rational abc exponent 1<kappa<2',
    'index_coset_required': 'h=1 modulo the fixed primorial',
    'uniform_initial_two_adic_depth': 4,
    'free_coordinates_added': 0,
    'external_input_equality_proved': False,
    'growth_condition_existentially_encoded': False,
    'new_defining_variable_bound_claimed': False,
}
out = OUTPUT
out.write_text(json.dumps(certificate, indent=2)+'\n')
print(json.dumps({k: certificate[k] for k in
                 ('status', 'formal_series_terms_verified', 'valuation_fixtures',
                  'free_coordinates_added', 'external_input_equality_proved')}))
