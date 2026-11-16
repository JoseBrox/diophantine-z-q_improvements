#!/usr/bin/env python3
"""Exact finite certificates for actual-source duplication branches.

The affine producer and Jacobian verifier are separate retained routines.
The universal global progression and scope are proved in the companion note.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from math import gcd, isqrt, lcm
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


affine = module("affine_v42", REPO / "negative_results/computation/mixed_sign_v42/build.py")
jacobian = module("jacobian_v42", REPO / "negative_results/computation/mixed_sign_v42/check.py")


def prime(n):
    return n > 1 and all(n % d for d in range(2, isqrt(n) + 1))


def valuation(x, p):
    x = Fraction(x)
    if x == 0:
        return None
    a, b, v = abs(x.numerator), x.denominator, 0
    while a % p == 0:
        a //= p
        v += 1
    while b % p == 0:
        b //= p
        v -= 1
    return v


def reduction(p, rho, r_order, p_order):
    assert prime(p) and rho * rho % p == 2
    D = (11 - 6 * rho) % p
    assert D != 0
    R = [(1 + rho) % p, 2 * rho % p]
    P = [(57 - 28 * rho) * pow(8, -1, p) % p,
         (-660 + 417 * rho) * pow(32, -1, p) % p]
    J = jacobian.Jacobian(p, -D)

    def multiply(Q, n):
        a = affine.multiply(Q, n, D, p)
        b = J.multiply(Q, n)
        assert a == b
        return a

    assert multiply(R, 2) == P
    orders = []
    for name, Q, n in [("R0", R, r_order), ("P", P, p_order)]:
        assert (Q[1]**2 - Q[0]**3 + D * Q[0]) % p == 0
        assert multiply(Q, n) is None
        tests = []
        for q in affine.factors(n):
            assert prime(q)
            value = multiply(Q, n // q)
            assert value is not None
            tests.append({"prime_divisor": q, "multiple": n // q, "point": value})
        orders.append({"point_name": name, "order": n, "proper_prime_quotients": tests})
    return {"p": p, "rho": rho, "D": D, "R0": R, "P": P,
            "orders": orders}, multiply


def run():
    p = 76537
    first, mul1 = reduction(p, 26935, 6375, 6375)
    second, mul2 = reduction(p, 49602, 9572, 4786)
    R = mul2(second["R0"], 2393)
    assert R == [35686, 1608]
    assert mul2(R, 2) == [0, 0] and mul2(R, 4) is None
    # Membership in full 2E(F_p) is strictly weaker than membership in red(ZP).
    half = [24152, 13484]
    assert (half[1]**2 - half[0]**3 + second["D"] * half[0]) % p == 0
    assert mul2(half, 2) == R
    assert 4786 % 4 != 0
    m, period = 10435875, 61021500
    assert period == lcm(6375, 9572) and gcd(6375, 9572) == 1
    assert m % 6375 == 0 and (m - 2) % 9572 == 2393
    assert m % 2 == 1 and period % 2 == 0
    assert mul1(first["R0"], m) is None
    assert mul2(second["R0"], m - 2) == R
    assert mul1(first["R0"], 2 * m) is None
    assert mul2(second["R0"], 2 * (m - 2)) == [0, 0]
    assert (R[0]**2 + second["D"]) % p == 0 and R[0] and R[1]
    # Simple exact contact at the rational argument t=p.
    theta = [-5, -2, -1, 0, 2, 3, 4, 7]
    derivative, numerator = 1, 1
    for c in theta:
        numerator *= p - c
        if c:
            derivative *= -c
    assert derivative == 1680 and derivative % p != 0
    w = Fraction(numerator, (p - 1)**6)
    assert valuation(w, p) == 1 and p > 76176
    assert p % 7 == 6  # Not the norm of the stronger Gaussian ray class.
    small, _ = reduction(17, 6, 10, 5)
    assert 6375 % 3 == 0 and 5 % 3 != 0

    sources = [
        "papers/quartic_existence/quartic_abc79_20261114_v27.tex",
        "papers/quartic_existence/quartic_abc78_20261115_v34.tex",
        "papers/arithmetic_dependencies/arithmetic_dependencies_20261108_v8.tex",
        "papers/trace_heights/trace_on_all_points_20261113_v25.tex",
        "papers/elliptic_charts/three_coordinate_reference_20261115_v40.tex",
        "negative_results/papers/elliptic_charts/mixed_reference_signs_20261116_v42.tex",
        "negative_results/computation/mixed_sign_v42/build.py",
        "negative_results/computation/mixed_sign_v42/check.py",
    ]
    proof = "negative_results/papers/elliptic_charts/duplicated_reference_signs_20261116_v44.tex"
    return {
        "proof_note": proof, "proof_note_sha256": sha256((REPO / proof).read_bytes()).hexdigest(),
        "status": "PASS", "method": "affine and independent Jacobian arithmetic; exact order certificates; trial primality",
        "mixed_reference_prime": p, "embeddings": [first, second],
        "order_four_point": R, "finite_field_half": half,
        "index_progression": {"R0_coefficient": m, "period": period, "index_is_half_integral": True},
        "contact": {"argument": p, "weight_valuation": 1, "derivative": derivative},
        "non_torsion_control": small,
        "source_sha256": {s: sha256((REPO / s).read_bytes()).hexdigest() for s in sources},
        "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": "Actual global quartic reference progression with opposite signs after duplication; no complete detector tuple or defining-polynomial counterexample. Gaussian ray conditions are completeness-only.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE / "verification.json")
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "certificate": str(args.output),
                      "mixed_prime": result["mixed_reference_prime"]}))
