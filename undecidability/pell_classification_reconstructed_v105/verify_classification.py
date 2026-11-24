#!/usr/bin/env python3
"""Exact independent finite audit; the quantified proof is the manuscript."""
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
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    if numerator**2 != value.numerator or denominator**2 != value.denominator:
        return None
    return Q(numerator, denominator)


def enumerate_interval(a):
    """Exhaust all reduced denominators allowed by the proved divisor bound."""
    delta, modulus = a * a - 1, abs(4 * a - 5)
    answer = set()
    candidates = 0
    for v in range(1, modulus + 1):
        if modulus % v:
            continue
        for u in range(v):
            if gcd(u, v) != 1:
                continue
            candidates += 1
            c = Q(u, v)
            d = rational_sqrt(1 + delta * c * c)
            if d is None:
                continue
            trace = d - (a - 2) * c
            if trace.denominator == 1:
                answer.add((c, d))
    return answer, candidates


def formula_seeds(a):
    if a >= 2:
        D = 4 * a - 5
        return {(Q(0), Q(1)),
                (Q(2 * (a - 2), D), Q(2 * a * a - 4 * a + 3, D))}
    A, K, delta = -a, -4 * a + 5, a * a - 1
    answer = set()
    for t in range(1, 2 * A + 2):
        v2 = delta * t * t + K
        v = isqrt(v2)
        if v * v == v2:
            answer.add((Q((A + 2) * t - v, K),
                        Q((A + 2) * v - delta * t, K)))
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


def normalize(a, pair):
    """Recover the seed and exponent using only exact rational comparisons."""
    c, d = pair
    sign = 1 if d > 0 else -1
    c, d = sign * c, sign * d
    exponent = 0
    while c < 0:
        c, d = translate(a, (c, d), 1)
        exponent -= 1
    while c >= 1:
        c, d = translate(a, (c, d), -1)
        exponent += 1
    assert d > 0 and 0 <= c < 1
    return sign, (c, d), exponent


def reflection(a, pair):
    c, d = pair
    delta, D = a * a - 1, 4 * a - 5
    trace = d - (a - 2) * c
    return 2 * (a - 2) * trace / D - c, 2 * delta * trace / D - d


def symbolic_checks():
    a, c, T, A = sp.symbols("a c T A")
    delta, D, slope = a * a - 1, 4 * a - 5, a - 2
    d = T + slope * c
    norm = d * d - delta * c * c - 1
    quadratic = D * c * c - 2 * slope * T * c - (T * T - 1)
    assert sp.expand(norm + quadratic) == 0
    v = D * c - slope * T
    assert sp.expand(v * v - delta * T * T + D - D * quadratic) == 0
    assert sp.expand(A * d + delta * c - slope * (d + A * c)
                     - (A - a + 2) * T - D * c) == 0
    assert sp.expand(A * d - delta * c - slope * (-d + A * c)
                     - (A + a - 2) * T + D * c) == 0
    cr = 2 * slope * T / D - c
    dr = 2 * delta * T / D - d
    assert sp.cancel(dr - slope * cr - T) == 0
    assert sp.cancel(dr * dr - delta * cr * cr - 1 - norm) == 0
    assert sp.cancel(2 * slope * T / D - cr - c) == 0
    assert sp.cancel(2 * delta * T / D - dr - d) == 0
    return 8


def receipt():
    identities = symbolic_checks()
    intervals, candidates, translated, reflected = [], 0, 0, 0
    parameters = list(range(-30, -1)) + list(range(2, 41))
    for a in parameters:
        actual, count = enumerate_interval(a)
        expected = formula_seeds(a)
        assert actual == expected, (a, actual, expected)
        candidates += count
        delta = a * a - 1
        for seed in actual:
            c0, d0 = seed
            assert d0 * d0 - delta * c0 * c0 == 1
            assert (d0 - (a - 2) * c0).denominator == 1
            for n in range(-8, 9):
                point = translate(a, seed, n)
                c, d = point
                assert d * d - delta * c * c == 1
                assert (d - (a - 2) * c).denominator == 1
                assert c.denominator == c0.denominator
                for sign in [-1, 1]:
                    signed = sign * c, sign * d
                    assert normalize(a, signed) == (sign, seed, n)
                    assert translate(a, signed, -n) == (sign * c0, sign * d0)
                    translated += 1
        if a >= 2:
            rho = (Q(2 * (a - 2), 4 * a - 5),
                   Q(2 * a * a - 4 * a + 3, 4 * a - 5))
            for n in range(-8, 9):
                integral = translate(a, (Q(0), Q(1)), n)
                image = reflection(a, integral)
                assert image == translate(a, rho, -n)
                assert reflection(a, image) == integral
                assert image[1] - (a - 2) * image[0] == integral[1] - (a - 2) * integral[0]
                assert image[0].denominator == (4 * a - 5) // gcd(4 * a - 5, 3)
                if a >= 3:
                    assert image[0].denominator > 1
                reflected += 1
        intervals.append({"a": a, "seeds": [
            {"c": str(c), "d": str(d), "T": str(d - (a - 2) * c),
             "c_denominator": c.denominator}
            for c, d in sorted(actual)]})

    assert formula_seeds(-5) == {(Q(0), Q(1)), (Q(3, 25), Q(29, 25)),
                                  (Q(2, 5), Q(11, 5))}
    assert normalize(5, (Q(1, 5), Q(-7, 5))) == (-1, (Q(2, 5), Q(11, 5)), -1)
    zero = set()
    for t in range(-2, 3):
        root = rational_sqrt(5 - t * t)
        if root is None:
            continue
        for sign in [-1, 1]:
            c = (2 * t + sign * root) / 5
            d = t - 2 * c
            assert c * c + d * d == 1
            zero.add((c, d))
    expected_zero = {(Q(0), Q(1)), (Q(0), Q(-1)),
                     (Q(1), Q(0)), (Q(-1), Q(0)),
                     (Q(4, 5), Q(-3, 5)), (Q(-4, 5), Q(3, 5)),
                     (Q(3, 5), Q(4, 5)), (Q(-3, 5), Q(-4, 5))}
    assert zero == expected_zero
    assert all(not c or abs(c) >= Q(3, 5) for c, d in zero)

    return {
        "status": "PASS",
        "provenance": "newly reconstructed; the unlocated prior-conversation artifact is not claimed recovered",
        "symbolic_identities": identities,
        "parameter_values": len(parameters),
        "rational_interval_candidates": candidates,
        "signed_orbit_fixtures": translated,
        "reflection_fixtures": reflected,
        "zero_parameter_rational_points": len(zero),
        "fundamental_interval_fixtures": intervals,
        "integer_predicate_removed": False,
        "numerical_variable_saving": 0,
        "full_source_nonintegral_orbit_exclusion_proved": False,
        "positive_two_orbit_claim_applies_to_negative_a": False,
        "scope": "Exact symbolic and finite rational audits. The quantified positive and negative classifications are proved in pell_classification.tex; the full-source integrality problem remains open here.",
        "proof_sha256": hashlib.sha256((HERE / "pell_classification.tex").read_bytes()).hexdigest(),
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
    visible = {key: value for key, value in result.items()
               if key != "fundamental_interval_fixtures"}
    print(json.dumps(visible, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
