#!/usr/bin/env python3
"""Exact identities supporting the native square-complement theorem.

This is not a search for actual native detector complements. It checks the
free-input section, prepared examples, and all four character maps of a
rank-four point block. The general valuation and splitting arguments are
given in the accompanying manuscript.
"""
from fractions import Fraction
from math import isqrt
import json
from pathlib import Path

import sympy as sp


def valuation(q, p):
    q = Fraction(q)
    assert q
    a, b = abs(q.numerator), q.denominator
    out = 0
    while a % p == 0:
        out += 1
        a //= p
    while b % p == 0:
        out -= 1
        b //= p
    return out


def local_square(q, p):
    v = valuation(q, p)
    if v % 2:
        return False
    unit = Fraction(q) / Fraction(p) ** v
    modulus = 8 if p == 2 else p
    residue = unit.numerator * pow(unit.denominator, -1, modulus) % modulus
    return residue == 1 if p == 2 else pow(residue, (p - 1) // 2, p) == 1


checks = []
u, v = sp.symbols('u v')
rt = sp.sqrt(2)
j, jb = u + v * rt, u - v * rt
A, B = u*u + 2*v*v, 2*u*v
for ep in (1, -1):
    for em in (1, -1):
        U = ep*j + em*jb
        V = (ep*j - em*jb)/rt
        W = ep*em*(u*u - 2*v*v)
        residuals = (
            U*U - 2*A - 2*W,
            V*V - A + W,
            U*V - 2*B,
            U*W - A*U + 2*B*V,
            V*W - B*U + A*V,
            W*W - A*A + 2*B*B,
        )
        assert all(sp.expand(z) == 0 for z in residuals)
        checks.append(f'point-block character ({ep},{em}): 6 identities')

h, D, tau = sp.symbols('h D tau', nonzero=True)
w = D/68
b = 68*D*h*h/(1+D*h*h)**2
s = 17*(1-D*h*h)/(1+D*h*h)
V = (1+D*h*h)/(34*h)
C = 17*(17-b)
e = (tau*tau-D)/(tau*tau+3*D)
p = -4*D*tau/(tau*tau+3*D)
q = p*s*s
identities = {
    'detector square class': b - w*(68*h/(1+D*h*h))**2,
    'trace relation': b - 4*w/(V*V),
    'complement square': C - s*s,
    'first pole': p*p - D*(1-e)*(1+3*e),
    'second pole': q*q - D*(s*s-e*C)*(s*s+3*e*C),
}
for name, residual in identities.items():
    assert sp.cancel(residual) == 0
    checks.append(name)

examples = []
for w0 in (Fraction(1), Fraction(409)):
    # 409 is a nonsquare in Q and a square at 2, 3, and 17.
    assert all(local_square(w0, ell) for ell in (2, 3, 17))
    D0 = 68*w0
    h0 = Fraction(3, 41719)  # 41719 = 1 + 2*3*17*409.
    b0 = 68*D0*h0*h0/(1+D0*h0*h0)**2
    s0 = 17*(1-D0*h0*h0)/(1+D0*h0*h0)
    V0 = (1+D0*h0*h0)/(34*h0)
    tau0 = Fraction(1)
    e0 = (tau0*tau0-D0)/(tau0*tau0+3*D0)
    p0 = -4*D0*tau0/(tau0*tau0+3*D0)
    q0 = p0*s0*s0
    C0 = 17*(17-b0)
    assert 0 < b0 < 17
    assert isqrt(b0.denominator)**2 == b0.denominator
    assert all(local_square(b0, ell) for ell in (2, 3, 17))
    assert all(valuation(b0, ell) >= n for ell, n in ((2, 3), (3, 1), (17, 2)))
    assert b0 == 4*w0/(V0*V0)
    assert C0 == s0*s0
    assert q0*q0 == D0*(s0*s0-e0*C0)*(s0*s0+3*e0*C0)
    assert s0 and p0 and q0
    examples.append({
        'w': str(w0), 'h': str(h0), 'tau': str(tau0),
        'b': str(b0), 's': str(s0), 'V': str(V0),
        'v2_b': valuation(b0, 2), 'v3_b': valuation(b0, 3),
        'v17_b': valuation(b0, 17),
        'square_denominator_root': isqrt(b0.denominator),
        'prepared': True,
    })

certificate = {
    'status': 'PASS',
    'scope': 'Free-input preparation and point-block splitting identities only; no native rational-complement realization.',
    'symbolic_scalar_identities': 24+len(identities),
    'checks': checks,
    'prepared_common_tau_examples': examples,
    'native_variable_counts_unchanged': True,
}
import argparse
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", type=Path)
args = parser.parse_args()
text = json.dumps(certificate, indent=2)+"\n"
if args.output:
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text)
else:
    print(text, end="")
