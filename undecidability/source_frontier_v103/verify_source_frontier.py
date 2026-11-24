#!/usr/bin/env python3
"""Independent exact checks for the v103 source-frontier checkpoint.

Finite examples supplement the quantified proofs in README.md. They do not
verify either a universal coding theorem or a rational integrality interface.
No builder or complete coefficient table is imported or modified.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
from math import comb, gcd, isqrt
import json
from pathlib import Path

import sympy as sp


def valuation_two(n: int) -> int:
    assert n > 0
    return (n & -n).bit_length() - 1


def audit() -> dict:
    a, c, T, d = sp.symbols("a c T d")
    delta = a**2 - 1
    norm = d**2 - delta*c**2 - 1
    monic = sp.expand(norm.subs(d, a*c+T))
    assert monic == c**2+2*a*T*c+T**2-1
    shifted = sp.expand(norm.subs(d, (a-2)*c+T))
    assert sp.expand(shifted-((5-4*a)*c**2+2*(a-2)*T*c+T**2-1)) == 0
    assert sp.expand((a*d-delta*c)**2-delta*(a*c-d)**2
                     -(d**2-delta*c**2)) == 0

    # Verify the actual modular-power recurrence and monic-row alternative.
    x0, y0, x1, y1 = sp.Integer(1), sp.Integer(0), a, sp.Integer(1)
    previous_y = sp.Integer(0)
    for j in range(1, 12):
        assert sp.expand(x1-a*y1+previous_y) == 0
        residue = sp.rem(sp.Poly(x1-(a-2)*y1-2**j, a), sp.Poly(4*a-5, a))
        assert residue.is_zero
        previous_y = y1
        x0, x1 = x1, sp.expand(2*a*x1-x0)
        y0, y1 = y1, sp.expand(2*a*y1-y0)

    norm_points = 0
    trace_points = 0
    nonintegral_points = 0
    for A in range(2, 101):
        Delta = A*A-1
        for denominator in range(1, 17):
            for numerator in range(1, 101):
                if gcd(numerator, denominator) != 1:
                    continue
                C = Fraction(numerator, denominator)
                rhs = 1+Delta*C*C
                if rhs.denominator != 1:
                    continue
                D = isqrt(rhs.numerator)
                if D*D != rhs.numerator:
                    continue
                norm_points += 1
                if denominator <= 3:
                    assert denominator == 1
                if denominator != 1:
                    nonintegral_points += 1
                if (D-(A-2)*C).denominator == 1:
                    trace_points += 1
                    assert denominator == 1
    assert Fraction(2)**2-(7**2-1)*Fraction(1,4)**2 == 1
    # This is the old kind of nonintegral example: its first trace is not integral.
    assert Fraction(-7,5)**2-(5**2-1)*Fraction(1,5)**2 == 1
    assert Fraction(-7,5)-(5-2)*Fraction(1,5) == -2

    binomial_checks = 0
    for n in range(0, 1001):
        assert valuation_two(comb(2*n,n)) == n.bit_count()
        binomial_checks += 1
    shift_checks = 0
    for n in range(1, 65):
        for h in range(0, 7):
            assert (n << h).bit_count() == n.bit_count()
            shift_checks += 1
    failed_general_bases = []
    for b in range(1, 65):
        at_one = valuation_two(comb(2*b,b)) == valuation_two(comb(2,1))
        assert at_one == (b & (b-1) == 0)
        if b % 2 == 0 and not at_one:
            failed_general_bases.append(b)

    return {
        "status": "proved local lemmas and research checkpoint; no numerical bound changed",
        "symbolic_norm_substitutions": 2,
        "pell_descent_identity": True,
        "pell_recurrence_examples": 11,
        "finite_rational_scan": {
            "A_range": [2, 100], "reduced_denominator_range": [1, 16],
            "positive_numerator_range": [1, 100],
            "integral_trace_norm_points": norm_points,
            "points_also_satisfying_integral_shifted_trace": trace_points,
            "nonintegral_c_norm_points": nonintegral_points,
        },
        "sharp_denominator_four_example": {"A":7,"d":2,"c":"1/4"},
        "direct_binomial_checks": binomial_checks,
        "binary_shift_checks": shift_checks,
        "even_bases_failing_shift_identity_at_n_one": failed_general_bases,
        "verification_scope": "Exact identities and stated finite scans only; universal local lemmas are proved in README.md. No coding or arithmetic-interface premise is discharged.",
        "first_trace_integrality_independently_available_in_current_source": False,
        "power_of_two_redundancy_in_full_source_settled": False,
        "new_polynomial_universal_source_compiled": False,
        "integer_predicates_removed": 0,
        "unconditional_rational_undecidability_claim": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args()
    report = audit()
    here = Path(__file__).resolve().parent
    report["readme_sha256"] = sha256((here/"README.md").read_bytes()).hexdigest()
    report["checker_sha256"] = sha256(Path(__file__).read_bytes()).hexdigest()
    encoded = json.dumps(report, indent=2, sort_keys=True)+"\n"
    certificate = here/"certificate.json"
    if args.write_certificate:
        certificate.write_text(encoded)
    else:
        assert certificate.read_text() == encoded, "certificate mismatch; inspect before regeneration"
    print(encoded, end="")


if __name__ == "__main__":
    main()
