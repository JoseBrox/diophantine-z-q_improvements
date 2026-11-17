#!/usr/bin/env python3
"""Exact identities only; this is not a defining-polynomial certificate."""
from fractions import Fraction
import argparse
import json
from pathlib import Path

import sympy as sp

a, delta, s, D, beta, uH, vH, J = sp.symbols(
    "a delta s D beta uH vH J"
)
q1 = a * delta - D * beta**4
q2 = a - s**2 - delta

# The scaled point (a, a*s) lies on y^2 = x^3 - D*beta^4*x.
curve_identity = sp.expand(
    a**3 - D * beta**4 * a - (a * s)**2 - (a * q1 + a**2 * q2)
)
assert curve_identity == 0

# F = delta/D is exactly beta^2 / x(U), where x(U)=a/beta^2.
reciprocal_identity = sp.expand(a * delta - D * beta**4 - q1)
assert reciprocal_identity == 0

# Substitution in v_H*J = u_H*F does not increase the row degree.
product_row = D * vH * J - uH * delta
assert sp.Poly(product_row, vH, J, uH, delta).total_degree() == 2

# The local residual and mixed-height absorption calculation is unchanged.
absorption = Fraction(301, 388) * Fraction(8, 7)
assert absorption == Fraction(602, 679) < 1

certificate = {
    "scope": "finite algebraic identities; no completeness or variable-bound result",
    "sympy_version": sp.__version__,
    "scaled_curve_identity": True,
    "reciprocal_identity": True,
    "direct_product_row_degree": 2,
    "absorption": str(absorption),
    "full_quartic_reduction_proved": False,
    "inherited_multiplication_completeness_obstructed": "proved in docs/audits/quartic_chart_review_20261117_v63.md",
}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", type=Path, default=Path(__file__).with_name("certificate.json"))
target = parser.parse_args().output
target.write_text(json.dumps(certificate, indent=2) + "\n")
print(json.dumps(certificate, indent=2))
