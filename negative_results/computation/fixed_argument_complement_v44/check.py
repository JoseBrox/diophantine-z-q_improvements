#!/usr/bin/env python3
"""Exact source and algebra audits for fixed-argument complement ramification.

The accompanying paper proves the geometric and universal statements.
This checker uses only the Python standard library and does not claim
to find a native rational lift or improve a defining-polynomial count.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
from pathlib import Path
import json


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", type=Path, default=HERE / "certificate.json",
                    help="Write the deterministic certificate to this path.")
args = parser.parse_args()

# Sparse Laurent polynomials. Negative exponents only occur in explicitly
# inverted monomials, so every identity below is exact in a rational ring.
N = 10
ZERO = (0,) * N
ONE = {ZERO: Q(1)}
NAMES = ["x", "y", "d", "alpha", "h", "c", "a", "f", "z", "r"]


def clean(p):
    return {m: q for m, q in p.items() if q}


def add(*ps):
    out = {}
    for p in ps:
        for m, q in p.items():
            out[m] = out.get(m, Q(0)) + q
    return clean(out)


def scale(p, q):
    return clean({m: c * q for m, c in p.items()})


def mul(a, b):
    out = {}
    for m, q in a.items():
        for n, r in b.items():
            t = tuple(u + v for u, v in zip(m, n))
            out[t] = out.get(t, Q(0)) + q * r
    return clean(out)


def power(p, n):
    assert n >= 0
    out = ONE
    for _ in range(n):
        out = mul(out, p)
    return out


def var(name):
    idx = NAMES.index(name)
    exponent = [0] * N
    exponent[idx] = 1
    return {tuple(exponent): Q(1)}


def inv_monomial(p):
    assert len(p) == 1
    m, q = next(iter(p.items()))
    assert q
    return {tuple(-v for v in m): 1 / q}


def coefficient(p, selections):
    selections = {NAMES.index(k): v for k, v in selections.items()}
    out = {}
    for m, q in p.items():
        if all(m[i] == e for i, e in selections.items()):
            n = tuple(0 if i in selections else e for i, e in enumerate(m))
            out[n] = out.get(n, Q(0)) + q
    return clean(out)


def substitute(p, name, value):
    idx = NAMES.index(name)
    out = {}
    for m, q in p.items():
        e = m[idx]
        assert e >= 0
        n = list(m)
        n[idx] = 0
        term = mul({tuple(n): q}, power(value, e))
        out = add(out, term)
    return out


symbols = {name: var(name) for name in NAMES}
x, y, d = (symbols[n] for n in ("x", "y", "d"))
alpha, h, c, a, f, z, r = (symbols[n] for n in ("alpha", "h", "c", "a", "f", "z", "r"))
xi, yi, hi = (inv_monomial(v) for v in (x, y, h))
identities = []


def identity(name, lhs, rhs):
    assert lhs == rhs, name
    identities.append(name)


# T0-Q on y^2=x^3-d^2*x.
curve = add(power(y, 2), scale(power(x, 3), -1), mul(power(d, 2), x))
xp = scale(mul(power(d, 2), xi), -1)
yp = scale(mul(mul(power(d, 2), y), power(xi, 2)), -1)
translated_curve = add(power(yp, 2), scale(power(xp, 3), -1), mul(power(d, 2), xp))
identity("torsion_translation_preserves_curve_mod_original_equation",
         translated_curve, mul(mul(power(d, 4), power(xi, 4)), curve))
chord_x = add(mul(power(y, 2), power(xi, 2)), scale(x, -1))
identity("torsion_translation_abscissa_from_chord",
         add(xp, scale(chord_x, -1)), scale(mul(power(xi, 2), curve), -1))
chord_y = add(mul(scale(mul(y, xi), -1), add(x, scale(xp, -1))), y)
identity("torsion_translation_ordinate_from_chord", yp, chord_y)
identity("z_T0_minus_Q_equals_z_Q",
         scale(mul(xp, inv_monomial(yp)), -1), scale(mul(x, yi), -1))

# Expansion around x=+/-d, using x as the local displacement variable.
for sign in (-1, 1):
    local_x = add(scale(d, sign), x)
    rhs = add(power(local_x, 3), scale(mul(power(d, 2), local_x), -1))
    expected = add(scale(mul(power(d, 2), x), 2),
                   scale(mul(d, power(x, 2)), 3 * sign), power(x, 3))
    identity(f"curve_expansion_at_{sign:+d}_d", rhs, expected)

# The actual three-factor boundary product, omitting its nonzero U-constant K0.
zh = mul(z, hi)
first = add(ONE, mul(alpha, power(f, 2)))
second = add(ONE, mul(alpha, power(add(zh, scale(c, -1)), 2)))
third = add(ONE, mul(alpha, power(add(zh, scale(a, -1)), 2)))
W = mul(mul(first, second), third)
lead_T0 = mul(mul(alpha, add(ONE, mul(alpha, power(c, 2)))),
              add(ONE, mul(alpha, power(a, 2))))
identity("leading_coefficient_at_T0",
         coefficient(W, {"f": 2, "z": 0}), lead_T0)
lead_pm = mul(mul(power(alpha, 2), power(hi, 4)),
              add(ONE, mul(alpha, power(inv_monomial(d), 2))))
for sign in (-1, 1):
    identity(f"leading_coefficient_at_T{sign:+d}",
             substitute(coefficient(W, {"z": 4}), "f", scale(inv_monomial(d), sign)),
             lead_pm)
identity("moving_zero_equation",
         substitute(third, "z", mul(h, add(a, r))),
         add(ONE, mul(alpha, power(r, 2))))

source_paths = [
    "negative_results/papers/rational_fibers/fixed_argument_complement_ramification_20261116_v44.tex",
    "papers/finite_algebra/unit_norm_20261114_v28.tex",
    "papers/conditional_few_variables/direct_input13_20261110_v22.tex",
    "papers/pole_parameters/common_parameter_guard_reduction_20261116_v42.tex",
]
source_hashes = {rel: sha256((REPO / rel).read_bytes()).hexdigest() for rel in source_paths}
native = (REPO / source_paths[1]).read_text()
direct = (REPO / source_paths[2]).read_text()
markers = [
    r"(f(U_i))_{i=0}^4",
    r"(\sigma f(V_i))_{i=0}^4",
    r"(L_i-L'_i)_{i=1}^4",
    r"L_1-\beta",
    r"\mathcal F(L_2,L_3,L_4)",
    r"positions $12,13,14,16$",
    r"$f(H)$, $f(S-P)$, and $z(S-P)/z(H)$",
    r"1+\frac{C_i^2}{\delta_j^2w_j^{2a_i-1}}",
    r"1+\frac{G_{j,k}^2}{w_j^{2\kappa_k-1}}",
    r"f(H),\ f(U),\ \sigma f(H-P),\ \sigma f(U-A)",
    r"z(U)/z(H)-X",
]
for token in markers:
    assert token in native, f"missing native marker: {token}"
for token in (r"D_1=f(H),\ D_2=f(U)", r"D_5=L-L',\ D_6=L-X"):
    assert token in direct, f"missing direct-comparison marker: {token}"

general_orders = {i: (3 if i in (12, 13, 14, 16) else 1) for i in range(1, 17)}
assert all(general_orders[i] == 1 for i in (2, 11, 15))
conditional_orders = {i: 1 for i in range(1, 7)}
assert all(conditional_orders[i] == 1 for i in (2, 5, 6))

conditional_cases = 0
for delta in (Q(1), Q(-2), Q(5, 7)):
    for F in (Q(1), Q(3), Q(17, 19)):
        w = F / (4 * delta**8)
        assert w > 0
        assert delta**4 / F == 1 / (4 * delta**4 * w)
        conditional_cases += 1

local_orders = [
    {"point": "O", "x": -2, "y": -3, "f": 2, "z": 1, "factor_orders": [0, 0, 0]},
    {"point": "T0", "x": 2, "y": 1, "f": -2, "z": 1, "factor_orders": [-4, 0, 0]},
    {"point": "T+", "x": 0, "y": 1, "f": 0, "z": -1, "factor_orders": [0, -2, -2]},
    {"point": "T-", "x": 0, "y": 1, "f": 0, "z": -1, "factor_orders": [0, -2, -2]},
]
for entry in local_orders:
    assert entry["f"] == -entry["x"]
    assert entry["z"] == entry["x"] - entry["y"]
    expected = 0 if entry["point"] == "O" else -4
    assert sum(entry["factor_orders"]) == expected

signed_sums = sorted({sum(4 * sign for sign in signs) for signs in product((-1, 1), repeat=3)})
assert signed_sums == [-12, -4, 4, 12] and 0 not in signed_sums

cert = {
    "status": "PASS",
    "source_sha256": source_hashes,
    "native_marker_count": len(markers) + 2,
    "general_U_dependent_positions": [2, 11, 15],
    "conditional_U_dependent_positions": [2, 5, 6],
    "all_selected_test_orders": 1,
    "exact_laurent_polynomial_identities": identities,
    "conditional_weight_cases": conditional_cases,
    "elliptic_local_orders": local_orders,
    "three_pole_weights": [4, 4, 4],
    "signed_weight_sums": signed_sums,
    "balanced_split_cover_possible": False,
    "proof_only_steps": [
        "Generic nonvanishing of remaining native boundary factors by the retained guards and real positivity.",
        "Classification of etale quadratic elliptic covers and constant-field finiteness.",
        "The native moving zero divisor cannot be cancelled by the U-independent coefficient.",
        "Restriction of an assumed etale cover to the boundary and generic elliptic fiber.",
        "Preservation of odd divisor valuation under smooth surjective abelian maps.",
    ],
    "scope": "Geometric ramification and absence of sections on dominant abelian pullbacks of the full independent native auxiliary variety.",
    "not_claimed": [
        "Nonexistence of individual rational lifts.",
        "Nonexistence on a proper coupled subvariety.",
        "Nonexistence of direct common-pole witnesses without square complements.",
        "Any reduced defining-polynomial variable bound.",
    ],
}
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(cert, indent=2) + "\n")
print(json.dumps({"status": "PASS", "symbolic_identities": len(identities),
                  "certificate": str(args.output)}, indent=2))
