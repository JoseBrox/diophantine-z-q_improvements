#!/usr/bin/env python3
"""Independent exact checks for the normalized derivative detector.

This verifies polynomial identities and the odd-valuation lemma.  It does
not computationally prove prime existence, abc height bounds, or the
intrinsic pole theorem.  Only the Python standard library is required.
"""
from fractions import Fraction as Q
from math import gcd
from pathlib import Path
import json
import argparse

HERE = Path(__file__).resolve().parent


def mul(a, b):
    out = {}
    for (i, j), x in a.items():
        for (r, s), y in b.items():
            key = (i+r, j+s)
            out[key] = out.get(key, 0)+x*y
    return {key: value for key, value in out.items() if value}


def derivative_a(a):
    return {(i-1, j): i*c for (i, j), c in a.items() if i}


def evaluate(a, x, z):
    return sum(c*x**i*z**j for (i, j), c in a.items())


def valuation(x, p):
    assert x
    x = Q(x)
    a, b, out = abs(x.numerator), x.denominator, 0
    while a % p == 0:
        a //= p
        out += 1
    while b % p == 0:
        b //= p
        out -= 1
    return out


polynomial_rows = []
for shifts in ((-3, 1, 2), (-10, 1, 2, 3, 4),
               (-21, 1, 2, 3, 4, 5, 6),
               (-10, -8, -5, 1, 2, 3, 4, 6, 7)):
    k = len(shifts)
    assert sum(shifts) == 0 and k % 2 == 1
    assert all(x+y != 0 for x in shifts for y in shifts)
    G, F_direct = {(0, 0): 1}, {(0, 0): 1}
    for c in shifts:
        # Independent integer dictionary multiplication, without SymPy.
        G = mul(G, {(2, 0): 1, (1, 0): 2*c,
                    (0, 0): c*c, (0, 1): -1})
        F_direct = mul(F_direct, {(2, 0): 1, (1, 0): 2*c,
                                  (0, 0): c*c, (0, 2): -1})
    GA = derivative_a(G)
    assert G[(0, k)] == -1
    assert GA[(1, k-1)] == 2*k
    assert (0, k-1) not in GA
    assert max(i+j for i, j in G) == 2*k
    assert max(i+j for i, j in GA) == 2*k-1
    # Directly differentiate F(a,z)=G(a,z^2) and compare G_A(a,z^2).
    F = {(i, 2*j): c for (i, j), c in G.items()}
    assert F == F_direct
    Fa = derivative_a(F)
    expected = {(i, 2*j): c for (i, j), c in GA.items()}
    assert Fa == expected
    content = 0
    for c in GA.values():
        content = gcd(content, abs(c))
    assert content % 2 == 0
    H = {monomial: coefficient//2 for monomial, coefficient in GA.items()}
    bound = max(map(abs, shifts))
    a, z = Q(bound+2), Q(2*bound+5)
    f, fa = evaluate(F, a, z), evaluate(Fa, a, z)
    assert f < 0 and fa > 0
    u = -2*k*f/fa
    assert u == -k*evaluate(G, a, z*z)/evaluate(H, a, z*z)
    assert u > 0
    if k == 9:
        assert content == 2
        assert len(G) == 90 and len(H) == 80
        assert max(32*i+2*j for i, j in G) == 576
        assert max(32*i+2*j for i, j in H) == 544
    polynomial_rows.append({"shifts": shifts, "number_of_shifts": k,
                            "G_monomials": len(G), "H_monomials": len(H),
                            "G_A_content": content,
                            "sum_shifts": sum(shifts),
                            "leading_G": "-1",
                            "leading_H": "%d*A" % k,
                            "sample_u": str(u)})

valuation_cases = 0
for p in (3, 5, 7, 17):
    for nu in range(-11, 12, 2):
        for c in range(-9, 10):
            for unit_u in (-2, -1, 1, 2):
                for unit_c in (1, 2):
                    u = unit_u*Q(p)**nu
                    C = unit_c*Q(p)**c
                    D = C*C/(1+u*C*C)
                    assert valuation(D, p) == max(2*c, -nu)
                    if nu < 0:
                        assert valuation(D*D/u, p) >= -3*nu > 0
                        assert valuation(1+D*D/u, p) == 0
                    else:
                        assert (valuation(D, p) > 0) == (c > 0)
                    valuation_cases += 1

real_cases = 0
for u in (Q(1, 2), Q(1), Q(2), Q(3), Q(10), Q(29), Q(100)):
    for values in ((0, 1, 2, 3, 4, 5),
                   (Q(1, 17), Q(-2, 3), 0, 100, -100, 2**20)):
        W = Q(1)
        for C in values:
            D = Q(C)**2/(1+u*Q(C)**2)
            assert 0 <= D <= 1/u
            W *= 1+D*D/u
        assert 0 <= 1-1/W <= 6/u**3
        assert 1 <= W <= (1+1/u**3)**6
        real_cases += 1

certificate = {
    "status": "PASS",
    "arithmetic": "Python standard-library integer and rational arithmetic",
    "polynomial_identities": polynomial_rows,
    "odd_valuation_fixtures": valuation_cases,
    "real_uniform_bound_fixtures": real_cases,
    "correct_uniform_bound": "0 <= 1-W_sigma^-1 <= 6/u^3; hence 0 <= 2-V <= 12/u^3",
    "scoped_claims": {
        "normalized_derivative_identity_verified": True,
        "odd_valuation_identity_verified": True,
        "ordinary_abc_height_theorem_computationally_verified": False,
        "prime_existence_computationally_proved": False,
        "global_intrinsic_pole_theorem_computationally_proved": False,
    },
}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,default=HERE/'completeness_certificate.json')
parser.parse_args().output.write_text(json.dumps(certificate,indent=2)+'\n')
print(json.dumps(certificate, indent=2))
