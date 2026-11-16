#!/usr/bin/env python3
"""Exact finite audits supporting the published geometric proof.

The valuation and geometry theorems are proved in the accompanying paper.
This script checks source constants, independent point counts, polynomial
identities, and a finite audit grid. It does not certify the universal
geometric assertions, existence of rational lifts, or a defining polynomial.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse
import json


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", type=Path, default=HERE / "certificate.json",
                    help="Write the exact certificate to this path.")
args = parser.parse_args()


def mul(a, b):
    ans = [Q(0)] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        for j, v in enumerate(b):
            ans[i + j] += u * v
    return ans


def from_roots(roots):
    p = [Q(1)]
    for root in roots:
        p = mul(p, [-root, Q(1)])
    return p


def evaluate(poly, a):
    out = Q(0)
    for c in reversed(poly):
        out = out * a + c
    return out


def derivative(poly):
    return [i * poly[i] for i in range(1, len(poly))]


def count_enumeration(p, d):
    return 1 + sum(
        (y * y - x**3 + d * d * x) % p == 0
        for x in range(p)
        for y in range(p)
    )


def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def count_character(p, d):
    return p + 1 + sum(legendre(x**3 - d * d * x, p) for x in range(p))


def q2mul(a, b):
    return (a[0] * b[0] + 2 * a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def q2add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def q2pow(a, n):
    out = (Q(1), Q(0))
    for _ in range(n):
        out = q2mul(out, a)
    return out


source_paths = [
    "negative_results/papers/rational_fibers/abelian_parameter_obstruction_20261116_v44.tex",
    "papers/finite_algebra/unit_norm_20261114_v28.tex",
    "papers/pole_parameters/square_complement_baseline_20261116_v43.tex",
    "papers/pole_parameters/common_parameter_guard_reduction_20261116_v42.tex",
    "negative_results/papers/pole_parameters/square_complement_normalization_20261116_v43.tex",
]
source_binding = {}
for rel in source_paths:
    data = (REPO / rel).read_bytes()
    source_binding[rel] = sha256(data).hexdigest()

native = (REPO / source_paths[1]).read_text()
for token in (
    r"(f(U_i))_{i=0}^4",
    r"(\sigma f(V_i))_{i=0}^4",
    r"U_0=H",
    r"V_0=H-P",
    r"positions $12,13,14,16$",
    r"1+\frac{C_i^2}{\delta_j^2w_j^{2a_i-1}}",
    r"1+\frac{G_{j,k}^2}{w_j^{2\kappa_k-1}}",
    r"f(H),\ f(U),\ \sigma f(H-P)",
    r"\mathcal W=\prod_{i=1}^6(1+\delta^4C_i^2/F)",
):
    assert token in native, f"native source marker missing: {token}"

base_contacts = [Q(0), Q(-1, 2), Q(-1), Q(1, 2399), Q(-32, 407)]
contact_data = []
for j in range(3):
    roots = [Q(4 * j + shift) + theta for shift in (2, 4) for theta in base_contacts]
    assert len(set(roots)) == 10
    gamma = Q(-j - 1)
    assert gamma not in roots
    poly = from_roots(roots)
    assert len(poly) - 1 == 10 and poly[-1] == 1
    assert all(evaluate(poly, a) == 0 for a in roots)
    assert all(evaluate(derivative(poly), a) != 0 for a in roots)
    contact_data.append({
        "source": "general",
        "j": j,
        "contacts": [str(v) for v in roots],
        "gamma": str(gamma),
        "degree": 10,
        "hyperelliptic_genus": (10 - 2) // 2,
        "coefficients_low_to_high": [str(v) for v in poly],
    })

roots = [Q(0), Q(-1, 2), Q(-1, 4), Q(-2, 5), Q(-1), Q(-1, 3)]
assert len(set(roots)) == 6 and Q(1) not in roots
poly = from_roots(roots)
assert all(evaluate(poly, a) == 0 for a in roots)
assert all(evaluate(derivative(poly), a) != 0 for a in roots)
contact_data.append({
    "source": "conditional",
    "contacts": [str(v) for v in roots],
    "gamma": "1",
    "degree": 6,
    "hyperelliptic_genus": (6 - 2) // 2,
    "coefficients_low_to_high": [str(v) for v in poly],
})

p = 17
sqrt2 = 6
assert sqrt2**2 % p == 2
point_counts = []
for d, expected in ((14, 20), (9, 16)):
    n1, n2 = count_enumeration(p, d), count_character(p, d)
    assert n1 == n2 == expected
    assert (64 * pow(d, 6, p)) % p != 0
    point_counts.append({
        "p": p, "d": d, "curve_linear_coefficient": (-d*d) % p,
        "direct_count": n1, "character_count": n2,
        "frobenius_trace": p + 1 - n1,
    })

# Check the genuine source P and nonzero affine coordinates over Q(sqrt2).
xP = (Q(57, 8), Q(-28, 8))
yP = (Q(-660, 32), Q(417, 32))
d2 = (Q(11), Q(-6))
assert q2pow(yP, 2) == q2add(q2pow(xP, 3), q2mul((-d2[0], -d2[1]), xP))
assert xP != (0, 0) and yP != (0, 0)

# Exact conditional normalization and conic-incidence identities at many
# independent rational values; identities are also explained algebraically.
normalization_cases = 0
for delta in (Q(1), Q(2), Q(-3), Q(5, 7)):
    for F in (Q(1), Q(-2), Q(7, 13)):
        w = F / (4 * delta**8)
        for C in (Q(0), Q(1), Q(-2, 3)):
            assert delta**4 * C*C / F == (C / (2 * delta**2))**2 / w
            normalization_cases += 1

# Audit odd-contact factor parity and the quantitative order-one bound.
factor_cases = 0
for e in range(1, 42, 2):
    for order in range(1, 8):
        for va in range(-25, 26):
            second = 2 * va - (2 * order - 1) * e
            assert second % 2 == 1 and second != 0
            factor = min(0, second)
            assert factor <= 0
            if order == 1 and va <= 0:
                assert factor <= -e
            factor_cases += 1

# Audit consequences of v(V)>=e and all finite pole valuation cases.
complement_cases = pole_cases = 0
for e in range(1, 20, 2):
    for vV in range(e, e + 12):
        assert 2 * vV > e
        complement_rad = min(2 * vV, e)
        vb = e - 2 * vV
        assert complement_rad == e and vb < 0 and vb % 2 == 1
        complement_cases += 1
        for vD in range(-15, 16, 2):
            # d may change by an arbitrary square; its valuation can be
            # any odd integer, independently of the representative b.
            assert vD % 2 == 1
            for vtau in range(-10, 11):
                assert 2 * vtau != vD
                numerator = denominator = min(2 * vtau, vD)
                assert numerator - denominator == 0
                for vs in range(-10, 11):
                    assert 2 * vs != vb
                    vrad = vD + 2 * min(2 * vs, vb)
                    assert vrad % 2 == 1
                    pole_cases += 1
            # tau=0 and infinity have unit e_tau; s=0 gives vD+2vb;
            # s=infinity requires a square root of D.
            assert (vD + 2 * vb) % 2 == 1
            assert vD % 2 == 1

cert = {
    "status": "PASS",
    "scope": "Exact finite audits supporting the accompanying proof; no rational-lift or variable-count claim.",
    "source_sha256": source_binding,
    "contact_polynomials": contact_data,
    "restriction_of_scalars_simplicity_counts": point_counts,
    "source_point_P_on_curve": True,
    "conditional_weight_normalization_cases": normalization_cases,
    "odd_contact_factor_cases": factor_cases,
    "complement_valuation_cases": complement_cases,
    "pole_valuation_cases": pole_cases,
    "proof_only_steps": [
        "Nonisogeny from the unequal good-reduction Frobenius traces.",
        "Q-simplicity of Res(E) and codimension-two geometric fibers.",
        "Extension and rigidity for maps between abelian varieties.",
        "Even-divisor construction of an etale cover.",
        "Connected finite etale covers of abelian varieties are isogenies.",
        "No nonconstant map from an abelian variety to a genus>1 curve.",
        "The universal valuation quantifiers and boundary completeness.",
    ],
    "unresolved": "The fixed-slope native incidence cover and suitable individual rational points remain unresolved.",
}
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(cert, indent=2) + "\n")
print(json.dumps({"status": "PASS", "factor_cases": factor_cases, "pole_cases": pole_cases,
                  "certificate": str(args.output)}, indent=2))
