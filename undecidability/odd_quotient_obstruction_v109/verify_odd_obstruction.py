#!/usr/bin/env python3
"""Exact certificate for the odd-i rational norm-subsystem counterfamily."""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args()
    N, L = 3915331224839183366, 14018146210311261
    J0 = 400518463151751
    D = 78011
    u, v = 11428909442110, 40919175003
    seed_x, seed_y = 171647, 612
    assert u * u - D * v * v == 1
    assert seed_x * seed_x - D * seed_y * seed_y == 125 ** 4
    assert (N, L) == (u * seed_x + D * v * seed_y, v * seed_x + u * seed_y)
    assert N * N - D * L * L == 125 ** 4
    assert 35 * J0 == L + 24
    a, c, d = 5, Q(1, 5), Q(-7, 5)
    b, w, gamma, i, i_half = 2, 14, -2, 5, 2
    F, G, H, I = Q(7, 5), Q(-306, 125), Q(L, 125), Q(N, 15625)
    Delta = a * a - 1
    assert c.denominator == 5
    assert i == 2 * i_half + 1 and i_half > 0
    assert d == b * w + (a - 2) * c + (4 * a - 5) * gamma
    assert d * d - Delta * c * c == 1
    assert F * F - Delta * i * i * c ** 4 == 1
    assert G == a + F * F * (c + 1 - a)
    # Both coefficients of the bridge identity as an affine polynomial in B.
    assert F * F - 7 * c * F == 0
    assert c * (1 - F * F) + c * F * J0 == H
    assert G * G - 1 == Q(D, 125 ** 2)
    assert I * I - (G * G - 1) * H * H == 1
    assert a % 3 != 0
    assert 2 * (a * d + Delta * c + 1) == Q(-12, 5)
    fixture_count = 0
    for B in range(3, 67, 2):
        J = J0 - 7 * B
        assert H == c + F * F * (B - c) + c * F * J
        assert c < B and J > 0
        fixture_count += 1
    assert fixture_count == 32
    result = {
        "status": "PASS", "positive_odd_source_quotient": i,
        "certified_half_quotient": i_half, "nonintegral_c": str(c),
        "exact_odd_B_fixtures": fixture_count,
        "universal_B_identity_checked": "Both affine coefficients vanish exactly.",
        "pell_norm_certificate": {"discriminant": D, "N": N, "L": L,
                                  "unit": [u, v], "seed": [seed_x, seed_y], "norm": 125 ** 4},
        "source_modulo_three_hypothesis_satisfied": False,
        "halftrace_square_exists": False,
        "full_source_counterexample_claim": False,
        "variable_saving_claim": 0,
        "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256": sha256((HERE / "README.md").read_bytes()).hexdigest(),
        "scope": "First linear equation, three Pell norms and bridge with odd integral i and integral gamma,J; neither the complete source nor its 3|a, half-trace or closeness hypotheses is satisfied.",
    }
    if args.write_certificate:
        (HERE / "certificate.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    else:
        assert result == json.loads((HERE / "certificate.json").read_text())
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
