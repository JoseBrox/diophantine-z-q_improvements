#!/usr/bin/env python3
"""Exact contact certificate for the affine slope--scale argument.

The manuscript proves the quotient, good-reduction, vertical-valuation and
geometric statements. This checker certifies every possible collision of
its eighteen rational a-contacts at fixed slope, and symbolically verifies
the restricted logarithmic derivative for every rational affine relation.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

import sympy as sp


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manuscript", type=Path,
                        default=here / "vertical_and_fixed_slope_20261117_v70.tex")
    parser.add_argument("--output", type=Path, default=here / "certificate.json")
    args = parser.parse_args()
    shifts = (-10, -8, -5, 1, 2, 3, 4, 6, 7)
    # The two root sets intersect precisely when 2z=c-d.
    exceptional_slopes = sorted({Fraction(c-d, 2) for c in shifts for d in shifts})
    a, t, g0, g1 = sp.symbols("a t g0 g1", nonzero=True)
    local_checks = []
    for multiplicity in (1, 2):
        f_local = t**multiplicity * (g0 + g1*t)
        u_local = sp.cancel(-18*f_local/sp.diff(f_local, t))
        value = sp.cancel(sp.diff(u_local, t).subs(t, 0))
        assert value == -sp.Rational(18, multiplicity)
        local_checks.append({"multiplicity": multiplicity,
                             "u_derivative_at_root": str(value)})
    m, regular = sp.symbols("m regular")
    affine_checks = []
    for label, pole, expected in [
        ("first_contact_only", 1/((1-m)*t), -18*(1-m)),
        ("second_contact_only", 1/((1+m)*t), -18*(1+m)),
        ("collision", 1/((1-m)*t)+1/((1+m)*t), -9*(1-m*m)),
        ("parallel_guarded_line", 1/(2*t), -36),
    ]:
        restricted_u = sp.cancel(-18/(pole+regular))
        value = sp.cancel(sp.diff(restricted_u, t).subs(t, 0))
        assert sp.cancel(value-expected) == 0
        affine_checks.append({"contact_type": label,
                              "u_derivative_at_root": str(value)})
    cases = []
    for slope in exceptional_slopes:
        roots = Counter([slope-c for c in shifts] + [-slope-c for c in shifts])
        assert 9 <= len(roots) <= 18 and set(roots.values()) <= {1, 2}
        f = sp.Poly(1, a, domain=sp.QQ)
        for root, multiplicity in roots.items():
            f *= sp.Poly(a-sp.Rational(root.numerator, root.denominator), a)**multiplicity
        derivative = f.diff()
        common = sp.gcd(f, derivative)
        numerator, denominator = f.exquo(common), derivative.exquo(common)
        derivative_numerator = numerator.diff()
        checked = []
        for root, multiplicity in sorted(roots.items()):
            root_q = sp.Rational(root.numerator, root.denominator)
            assert numerator.eval(root_q) == 0
            assert denominator.eval(root_q) != 0
            value = sp.cancel(-18*derivative_numerator.eval(root_q)/denominator.eval(root_q))
            assert value == -sp.Rational(18, multiplicity)
            checked.append({"a": str(root), "multiplicity": multiplicity,
                            "u_derivative": str(value)})
        genus = (len(roots)-1)//2
        assert genus >= 4 and 4*len(roots) % 2 == 0
        cases.append({"z": str(slope), "distinct_roots": len(roots),
                      "hyperelliptic_genus": genus, "roots": checked})
    result = {
        "status": "PASS",
        "scope": "Exact contact algebra only; the geometric and arithmetic proofs are in the manuscript.",
        "source_sha256": sha256(args.manuscript.read_bytes()).hexdigest(),
        "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "sympy_version": sp.__version__,
        "shifts": shifts,
        "collision_criterion": "2*z=c-d with c,d in the shift set",
        "collision_slopes": len(exceptional_slopes),
        "generic_distinct_roots": 18,
        "generic_hyperelliptic_genus": 8,
        "root_count_distribution": dict(sorted(Counter(case["distinct_roots"] for case in cases).items())),
        "minimum_distinct_roots": min(case["distinct_roots"] for case in cases),
        "formal_local_derivative_checks": local_checks,
        "affine_contact_derivatives": affine_checks,
        "affine_scope": "First three cases have m != +/-1; parallel case has m=+/-1 and the identically-zero contact lines are excluded by the guards.",
        "cases": cases,
        "limitations": "This does not test good reduction, descent, rational witnesses, or any variable-count reduction."
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({key: result[key] for key in ["status", "source_sha256", "checker_sha256", "collision_slopes", "root_count_distribution", "minimum_distinct_roots"]}, indent=2))


if __name__ == "__main__":
    main()
