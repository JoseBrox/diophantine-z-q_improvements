#!/usr/bin/env python3
"""Independent arithmetic audit; this file does not compile full source tables."""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import json
from math import gcd, isqrt
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent


def rational_sqrt(value):
    value = Q(value)
    if value < 0:
        return None
    u, v = isqrt(value.numerator), isqrt(value.denominator)
    return Q(u, v) if u * u == value.numerator and v * v == value.denominator else None


def square_test_seeds(A):
    K, delta = 4 * A + 5, A * A - 1
    answer = set()
    for t in range(1, 2 * A + 2):
        v2 = delta * t * t + K
        v = isqrt(v2)
        if v * v == v2:
            answer.add((Q((A + 2) * t - v, K),
                        Q((A + 2) * v - delta * t, K)))
    return answer


def short_seeds(A):
    K = 4 * A + 5
    answer = {(Q(0), Q(1)), (Q(3, K), Q(5 * A + 4, K))}
    h = isqrt(K)
    if h * h == K:
        answer.add((Q(2, h), Q(2 * A + 1, h)))
    return answer


def translate(a, pair, exponent):
    c, d = pair
    A, delta = abs(a), a * a - 1
    for _ in range(abs(exponent)):
        if exponent >= 0:
            c, d = d + A * c, A * d + delta * c
        else:
            c, d = -d + A * c, A * d - delta * c
    return c, d


def pell(a, n):
    x0, x1, y0, y1 = 1, a, 0, 1
    if n == 0:
        return x0, y0
    for _ in range(1, n):
        x0, x1 = x1, 2 * a * x1 - x0
        y0, y1 = y1, 2 * a * y1 - y0
    return x1, y1


def receipt():
    a, c, trace, q, S, T0, w, s = sp.symbols("a c trace q S T0 w s")
    delta, D, La = a * a - 1, 4 * a - 5, 2 * a * a - 2 * a - 1
    d = (a - 2) * c + trace
    assert sp.expand(8 * La + 3 - D * (4 * a + 1)) == 0
    assert sp.expand(2 * (a * d + delta * c + 1)
                     - (2 * La * c + 2 * a * trace + 2)) == 0
    norm = d * d - delta * c * c - 1
    quadratic = D * c * c - 2 * (a - 2) * trace * c - trace * trace + 1
    assert sp.expand(norm + quadratic) == 0
    assert sp.expand((D * c - (a - 2) * trace)**2 - delta * trace**2
                     + D - D * quadratic) == 0
    modulus = sp.Poly(q**3 - q, q, modulus=3)
    assert sp.rem(sp.Poly(q**64 - q**48, q, modulus=3), modulus).is_zero
    assert sp.rem(sp.Poly(q**64 - q**32, q, modulus=3), modulus).is_zero

    extra_seeds = []
    for A in range(2, 1001):
        actual, predicted = square_test_seeds(A), short_seeds(A)
        assert actual == predicted, A
        if len(actual) == 3:
            extra_seeds.append({"A": A, "sqrt_4A_plus_5": isqrt(4 * A + 5)})
        if A % 3 == 0:
            assert len(actual) == 2
            assert (4 * A + 5) % 3 == 2
            for c0, d0 in actual:
                if c0:
                    assert c0.denominator == 4 * A + 5
                    assert isqrt(c0.denominator)**2 != c0.denominator

    orbit_count = 0
    surviving_halftraces = 0
    for a0 in list(range(-60, 0, 3)) + list(range(3, 61, 3)):
        if a0 > 0:
            divisor = 4 * a0 - 5
            seeds = {(Q(0), Q(1)),
                     (Q(2 * (a0 - 2), divisor),
                      Q(2 * a0 * a0 - 4 * a0 + 3, divisor))}
        else:
            seeds = short_seeds(-a0)
        for seed in seeds:
            for n in range(-5, 6):
                c0, d0 = translate(a0, seed, n)
                assert c0.denominator == seed[0].denominator
                for sign in [-1, 1]:
                    cc, dd = sign * c0, sign * d0
                    delta0 = a0 * a0 - 1
                    trace0 = dd - (a0 - 2) * cc
                    value = 2 * (a0 * dd + delta0 * cc + 1)
                    assert dd * dd - delta0 * cc * cc == 1
                    assert trace0.denominator == 1
                    assert gcd(2 * (2 * a0 * a0 - 2 * a0 - 1), abs(4 * a0 - 5)) == 1
                    assert value.denominator == cc.denominator
                    root = rational_sqrt(value)
                    if root is not None:
                        assert cc.denominator == dd.denominator == 1
                        surviving_halftraces += 1
                    orbit_count += 1

    zero_values = [(Q(0), Q(1)), (Q(0), Q(-1)), (Q(1), Q(0)), (Q(-1), Q(0)),
                   (Q(3, 5), Q(4, 5)), (Q(-3, 5), Q(-4, 5)),
                   (Q(4, 5), Q(-3, 5)), (Q(-4, 5), Q(3, 5))]
    for cc, dd in zero_values:
        assert cc * cc + dd * dd == 1
        assert (dd + 2 * cc).denominator == 1
        value = 2 * (1 - cc)
        assert value.denominator == cc.denominator
        if rational_sqrt(value) is not None:
            assert cc.denominator == dd.denominator == 1
            assert cc in [-1, 1]

    prefix_count = 0
    for q0 in range(-12, 13):
        n0, M0 = q0**16, q0**32
        for S0 in range(-2, 3):
            for T00 in range(-2, 3):
                r0 = S0 * (M0 - n0) + T00 * (M0 - 1)
                assert M0 * r0 % 3 == 0
                for w0 in [-1, 0, 1]:
                    for s0 in [-1, 0, 1]:
                        a0 = (w0 * M0 + 1) * r0 * s0 * M0
                        assert a0 % 3 == 0
                        prefix_count += 1

    completions = 0
    for a0 in range(2, 16):
        for r0 in range(1, 10):
            dd, cc = pell(a0, 2 * r0 + 1)
            root = 2 * pell(a0, r0 + 1)[0]
            assert root * root == 2 * (a0 * dd + (a0 * a0 - 1) * cc + 1)
            assert dd * dd - (a0 * a0 - 1) * cc * cc == 1
            completions += 1

    # The hypothesis 3|a cannot simply be omitted from the signed theorem.
    a0, cc, dd, zeta = -5, Q(-3, 25), Q(-29, 25), Q(14, 5)
    assert dd * dd - (a0 * a0 - 1) * cc * cc == 1
    assert dd - (a0 - 2) * cc == -2
    assert zeta * zeta == 2 * (a0 * dd + (a0 * a0 - 1) * cc + 1)
    assert cc.denominator > 1 and a0 % 3 != 0

    return {
        "status": "PASS",
        "symbolic_identities_and_finite_field_reductions": 6,
        "negative_parameters_classified": 999,
        "negative_parameters_with_third_seed": extra_seeds,
        "signed_orbit_fixtures": orbit_count,
        "surviving_integral_halftrace_fixtures": surviving_halftraces,
        "zero_edge_fixtures": len(zero_values),
        "exact_prefix_fixtures": prefix_count,
        "canonical_positive_halftrace_completions": completions,
        "counterexample_if_three_divisibility_is_omitted": {
            "a": a0, "c": str(cc), "d": str(dd), "zeta": str(zeta), "shifted_trace": -2},
        "arithmetic_c_integrality_replacement_proved": True,
        "new_unconditional_rational_undecidability_claim": False,
        "complete_table_count_claim_in_this_checkpoint": False,
        "scope": "Quantified arithmetic proofs are in pell_integrality_replacement.tex. This audit verifies identities and finite fixtures; full coefficient-table compilation and coordinate counts are separate.",
        "proof_sha256": hashlib.sha256((HERE / "pell_integrality_replacement.tex").read_bytes()).hexdigest(),
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
                      if k != "negative_parameters_with_third_seed"}, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
