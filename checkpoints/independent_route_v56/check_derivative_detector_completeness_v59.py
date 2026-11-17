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
for m in (1, 2, 4, 8):
    k = 2*m
    G = {(0, 0): 1}
    for j in range(1, m+1):
        factor = {(2, 0): 1, (0, 2): 1, (1, 1): -2,
                  (1, 0): -2*j*j, (0, 1): -2*j*j, (0, 0): j**4}
        G = mul(G, factor)
    GA = derivative_a(G)
    assert G[(0, k)] == 1
    assert GA[(0, k-1)] == -k
    assert max(i+j for i, j in G) == k
    assert max(i+j for i, j in GA) == k-1
    # Directly differentiate F(a,z)=G(a^2,z^2) and compare 2a*G_A.
    F = {(2*i, 2*j): c for (i, j), c in G.items()}
    Fa = derivative_a(F)
    expected = {(2*i+1, 2*j): 2*c for (i, j), c in GA.items()}
    assert Fa == expected
    content = 0
    for c in GA.values():
        content = gcd(content, abs(c))
    assert k % content == 0
    a, z = Q(m+2), Q(3*m+7)
    f, fa = evaluate(F, a, z), evaluate(Fa, a, z)
    assert f > 0 and fa < 0
    u = -2*k*a*f/fa
    assert u == -k*evaluate(G, a*a, z*z)/evaluate(GA, a*a, z*z)
    assert u > 0
    polynomial_rows.append({"number_of_symmetric_shifts": k,
                            "G_monomials": len(G), "G_A_monomials": len(GA),
                            "G_A_content": content,
                            "reduced_numerator_multiplier": k//content,
                            "leading_G": 1, "leading_G_A": -k,
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
(HERE/'derivative_detector_completeness_v59_certificate.json').write_text(
    json.dumps(certificate, indent=2)+'\n')
print(json.dumps(certificate, indent=2))
