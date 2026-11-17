#!/usr/bin/env python3
"""Exact rational fixtures for the centered-quartic contact obstruction."""
from fractions import Fraction as Q
from pathlib import Path
import json


def valuation(x, p):
    x = Q(x)
    assert x
    n, d = abs(x.numerator), x.denominator
    result = 0
    while n % p == 0:
        n //= p
        result += 1
    while d % p == 0:
        d //= p
        result -= 1
    return result


def values(w, V):
    U = V-w/2
    D = w*(2-w/4)
    C = V*V+w*(2-V)
    delta = (U*U-D)/w
    assert C == U*U+D
    assert delta*C == (U**4-D*D)/w
    assert delta*C*C/w == (C/w)**2*(U*U-D)
    return U, D, C, delta


p = 100129
assert p > 76176 and p % 24 == 1
assert all(p % d for d in range(2, int(p**0.5)+1))
rows = []
for nu in (1, 3, 5, 7):
    u = Q(p**nu)
    w = u/(1+u)**2
    assert 0 < w <= Q(1, 4) and valuation(w, p) == nu
    for V in (Q(1), Q(2), Q(1+p), Q(2+p)):
        U, D, C, delta = values(w, V)
        assert valuation(C, p) == 0
        assert valuation(U*U-D, p) == 0
        assert valuation(delta*C, p) == -nu
        rows.append({"nu": nu, "trace": str(V),
                     "radicand_valuation": -nu})
    for m in range((nu+1)//2, nu+3):
        V = Q(p**m, p**m+1)
        U, D, C, delta = values(w, V)
        assert valuation(V, p) == m
        assert valuation(C, p) == nu
        assert valuation(U*U-D, p) == nu
        assert valuation(delta, p) == 0
        assert valuation(delta*C, p) == nu

U, D, C, delta = values(Q(1, 4), Q(2))
assert U*U-D == Q(97, 32)
assert valuation(U*U-D, 2) == -5
U, D, C, delta = values(Q(1, 4), Q(1, 8))
assert U*U-D == -Q(31, 64)

report = {"status": "PASS", "prime": p,
          "fresh_contact_rows": rows,
          "bad_pole_valuation_checks": True,
          "minus_conic_reference_value": "97/32",
          "minus_conic_negative_rectangle_value": "-31/64",
          "scope": "Displayed centered quartic and correction by squares only"}
out = Path(__file__).with_name("j1728_trace_multiplier_v58_certificate.json")
out.write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({"status": "PASS", "fresh_contact_fixtures": len(rows)}))
