#!/usr/bin/env python3
"""Exact audit of the bounded outer lemma; exponential inputs remain external."""
from __future__ import annotations

import argparse
import hashlib
import json
from math import comb
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent


def valuation_two(n):
    assert n > 0
    return (n & -n).bit_length() - 1


def receipt():
    U, V, W, y, K, T, D, r1, r2, r3 = sp.symbols("U V W y K T D r1 r2 r3")
    coordinates = (U, V, W, y, K, T, D, r1, r2, r3)
    rows = (K - V * y, T - K * U + 4 * K, D - W + K * T,
            T * T - 4 * D * D - r1 * r1 - r2 * r2 - r3 * r3)
    assert all(sp.Poly(row, *coordinates).total_degree() == 2 for row in rows)
    A, M, DD, E2 = sp.symbols("A M DD E2", integer=True, nonnegative=True)
    E1 = (2 * A + 1) * DD + E2
    C = 2 * E1 + 4 * M + 4
    P, H = C * DD, C * (E1 - E2)
    assert sp.expand(H - P * (2 * A + 1)) == 0
    assert sp.expand(P - (4 * A + 6 + 4 * M)
                     - ((4 * A + 2) * (DD * DD - 1)
                        + (4 * M + 4) * (DD - 1) + 2 * E2 * DD)) == 0

    fixtures = []
    candidate_checks = 0
    for A0 in range(16):
        central = comb(2 * A0, A0)
        nu = valuation_two(central)
        for M0 in range(nu + 3):
            for extra in [0, 1]:
                P0 = 4 * A0 + 6 + 4 * M0 + extra
                U0, V0, W0 = 1 << P0, 1 << M0, 1 << (P0 * (2 * A0 + 1))
                Q = sum(comb(2 * j, j) * U0**(A0 - j) for j in range(A0 + 1))
                assert U0 > 32 * 4**A0 + 4
                assert U0 % V0 == 0 and Q % V0 == central % V0
                assert Q * Q * (U0 - 4) < W0
                assert 64 * W0 < (8 * Q + 1)**2 * (U0 - 4)
                candidates = {0}
                for delta in [-1, 0, 1, 2]:
                    value = Q // V0 + delta
                    candidates.add(value)
                    candidates.add(-value)
                successes = []
                for y0 in sorted(candidates):
                    K0 = V0 * y0
                    T0 = K0 * (U0 - 4)
                    D0 = W0 - K0 * T0
                    inequality = T0 * T0 >= 4 * D0 * D0
                    assert inequality == (abs(K0) == Q)
                    candidate_checks += 1
                    if inequality:
                        successes.append(y0)
                divides = central % V0 == 0
                assert bool(successes) == divides
                if divides:
                    y0, K0 = Q // V0, Q
                    T0 = K0 * (U0 - 4)
                    D0 = W0 - K0 * T0
                    S0 = T0 * T0 - 4 * D0 * D0
                    assert S0 > 0 and D0 > 0
                    assert valuation_two(Q) == nu
                    assert valuation_two(T0) == nu + 2
                    assert valuation_two(D0) == 2 * nu + 2
                    assert valuation_two(S0) == 2 * nu + 4
                    odd_part = S0 >> (2 * nu + 4)
                    assert odd_part % 8 == (5 if nu == 0 else 1)
                fixtures.append({"A": A0, "M": M0, "P": P0,
                                 "divisibility": divides,
                                 "three_square_criterion_checked": divides})

    explicit = {U: 64, V: 1, W: 64, y: 1, K: 1, T: 60, D: 4,
                r1: 0, r2: 40, r3: 44}
    assert all(row.subs(explicit) == 0 for row in rows)

    # Finite examples of the distinct-degree pattern, not a lower bound
    # on every possible existential polynomial source.
    z = sp.symbols("z")
    ranks = []
    for m in range(1, 9):
        p = (8 * (z + 1)**(m + 1) + 4) * (z * z + 3)
        exponents = [p] + [(2 * p + 2) * (z + 1)**k for k in range(1, m + 2)]
        degrees = [sp.degree(poly, z) for poly in exponents]
        assert degrees == list(range(degrees[0], degrees[0] + m + 2))
        ranks.append({"m": m, "independent_exponents_by_degree": m + 2})

    return {
        "status": "PASS",
        "quadratic_rows": 4,
        "external_input_symbols": ["U", "V", "W", "y"],
        "rational_auxiliaries_beyond_external_inputs": 6,
        "external_y_integrality_required": True,
        "external_power_graphs_required": True,
        "outer_fixtures": len(fixtures),
        "candidate_integer_y_checks": candidate_checks,
        "fixture_details": fixtures,
        "degree_rank_examples": ranks,
        "explicit_three_square_fixture": {str(key): value for key, value in explicit.items()},
        "full_polynomial_source_compiled": False,
        "rational_undecidability_witness_claim": False,
        "new_global_variable_bound_claim": False,
        "scope": "Exact outer lemma and finite arithmetic audit. The unary exponential source's lower circuits and all power graphs remain external; no full Diophantine transfer or global count is claimed.",
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
    print(json.dumps({k: v for k, v in result.items()
                      if k not in {"fixture_details", "degree_rank_examples"}}, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
