#!/usr/bin/env python3
"""Exact proper-subsystem obstruction; no full-source counterexample claim."""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def pell(base, n):
    X, Y = 1, 0
    for _ in range(n):
        X, Y = base * X + (base * base - 1) * Y, X + base * Y
    return X, Y


def receipt():
    a, c, d, b, w, gamma = 6, 143, 846, 2, 4, 14
    B, r, F, E = 71, 35, 6, 1
    i, i_half = Q(1, 20449), Q(-10224, 20449)
    G, H, I, J = 4974, 98962703, 492240474774, 115344
    delta = a * a - 1
    assert B == 2 * r + 1
    assert d == b * w + (a - 2) * c + (4 * a - 5) * gamma
    assert d * d - delta * c * c == 1
    assert E == i * c * c
    assert F * F - delta * E * E == 1
    assert G == a + F * F * (c + 1 - a)
    assert H == c + F * F * (B - c) + c * F * J
    assert I * I - (G * G - 1) * H * H == 1
    assert 142**2 == 2 * (a * d + delta * c + 1)
    assert 12**2 == 2 * (a * F + delta * E + 1)
    assert (d, c) == pell(a, 3)
    assert (I, H) == pell(G, 3)
    assert H == 4 * G * G - 1 and I == 4 * G**3 - 3 * G
    assert H + 2449 == 858 * J
    assert a % 3 == 0 and c > B and B % 2 == 1
    assert i > 0 and i.denominator > 1
    assert i == 2 * i_half + 1 and i_half.denominator > 1
    lower_bound = (w * 16 + 1) * r * 16
    assert lower_bound == 36400 and lower_bound > abs(a)
    return {
        "status": "PASS",
        "coordinates": {"a": a, "c": c, "d": d, "b": b, "w": w,
                        "gamma": gamma, "B": B, "r": r, "F": F, "E": E,
                        "i": str(i), "i_half": str(i_half), "G": G, "H": H,
                        "I": I, "J": J, "first_halftrace_root": 142,
                        "second_halftrace_root": 12},
        "a_multiple_of_three": True,
        "integral_second_pell_coordinates": True,
        "both_halftrace_squares": True,
        "c_greater_than_B": True,
        "nonintegral_i": True,
        "full_source_counterexample_claim": False,
        "minimum_source_a_magnitude_at_M16": lower_bound,
        "integer_predicate_removed": False,
        "scope": "Exact norm/linear/bridge/one-quotient/half-trace subsystem only. The source identity a=(wM+1)rsM is excluded for M>=16 and nonzero integer s; no full-source or closeness claim.",
        "proof_sha256": hashlib.sha256((HERE / "README.md").read_bytes()).hexdigest(),
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args()
    result = receipt()
    path = HERE / "certificate.json"
    if args.write_certificate:
        path.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    else:
        assert json.loads(path.read_text()) == result
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
