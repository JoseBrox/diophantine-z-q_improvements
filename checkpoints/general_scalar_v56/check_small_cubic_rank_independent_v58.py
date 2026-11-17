#!/usr/bin/env python3
"""Independent exact tangent/chord audit of the small trace cubic.

This checker does not use division-polynomial recurrences.  It computes
x([8]P), x([10]P), x([12]P) directly in Q(w), extracts the primitive square
root of each reduced denominator, and checks rational-root exclusions.
The independently generated roots are also compared with the other
agent's evaluated division-polynomial coefficient arrays.
"""
from fractions import Fraction
from hashlib import sha256
from math import gcd, isqrt, lcm
from pathlib import Path
import json

from sympy.polys.domains import QQ
from sympy.polys.fields import field


HERE = Path(__file__).resolve().parent
AUTHOR_DATA = (HERE.parent / "independent_route_v56" /
               "small_cubic_rank_v58_coefficients.json")
OUTPUT = HERE / "small_cubic_rank_independent_v58_certificate.json"
F, w = field("w", QQ)
A, B = -(w + 4), 4 * (w + 1)
P = (F(4), F(4))
points = {1: P}


def add_points(p, q):
    x1, y1 = p
    x2, y2 = q
    if p == q:
        slope = (3*x1*x1 + 2*A*x1 + B)/(2*y1)
    else:
        assert x1 != x2, "Unexpected generic vertical chord"
        slope = (y2-y1)/(x2-x1)
    x3 = slope*slope - A - x1 - x2
    y3 = -y1 + slope*(x1-x3)
    assert y3*y3 == x3*x3*x3 + A*x3*x3 + B*x3
    return x3, y3


def multiple(n):
    if n not in points:
        if n % 2 == 0:
            half = multiple(n//2)
            points[n] = add_points(half, half)
        else:
            points[n] = add_points(multiple(n-1), P)
    return points[n]


def primitive_integer_coefficients(poly):
    degree = poly.degree()
    coefficients = [Fraction(0) for _ in range(degree+1)]
    for (i,), c in poly.to_dict().items():
        coefficients[i] = Fraction(int(c.numerator), int(c.denominator))
    denominator = lcm(*(c.denominator for c in coefficients))
    values = [int(c*denominator) for c in coefficients]
    content = gcd(*values)
    if values[-1] < 0:
        content = -content
    return [v//content for v in values]


def square_root_polynomial(a):
    """Recover the positive-leading integer square root without factoring."""
    degree = len(a)-1
    assert degree % 2 == 0
    m = degree//2
    b = [0]*(m+1)
    b[m] = isqrt(a[-1])
    assert b[m] > 0 and b[m]*b[m] == a[-1]
    for k in range(m-1, -1, -1):
        known = sum(b[i]*b[j]
                    for i in range(k+1, m+1)
                    for j in range(k+1, m+1)
                    if i+j == m+k)
        remainder = a[m+k]-known
        assert remainder % (2*b[m]) == 0
        b[k] = remainder//(2*b[m])
    squared = [0]*(2*m+1)
    for i, bi in enumerate(b):
        for j, bj in enumerate(b):
            squared[i+j] += bi*bj
    assert squared == a
    assert gcd(*b) == 1
    return b


def evaluate(coefficients, value):
    result = 0
    for coefficient in reversed(coefficients):
        result = result*value + coefficient
    return result


assert P[1]**2 == P[0]**3+A*P[0]**2+B*P[0]
assert 16*B*B*(A*A-4*B) == 256*w*(w-8)*(w+1)**2
assert A*A-4*B == w*(w-8)
x2, y2 = multiple(2)
assert x2 == (w-3)**2/4
assert y2 == (w-3)*(w*w-8*w-1)/8

# Verify the change of variables by a separate two-variable calculation.
G, ww, V = field("w,V", QQ)
x = V+2
C = V*V+ww*(2-V)
assert (V+2)*C == x**3-(ww+4)*x*x+4*(ww+1)*x

author_data = json.loads(AUTHOR_DATA.read_text())
author_rows = {row["n"]: row for row in author_data["rows"]}
rows = []
for n, expected_degree, expected_lead in ((8, 15, 1), (10, 24, 5),
                                           (12, 35, 3)):
    xx, yy = multiple(n)
    assert xx.numer.gcd(xx.denom).degree() == 0
    denominator = primitive_integer_coefficients(xx.denom)
    root = square_root_polynomial(denominator)
    assert len(root)-1 == expected_degree and root[-1] == expected_lead
    assert root == author_rows[n]["primitive_coefficients_ascending"]
    candidates = []
    # Rational-root theorem: reduced denominator divides the leading
    # coefficient. Enumerate every positive reduced rational <= 1/4.
    for denominator_candidate in range(1, expected_lead+1):
        if expected_lead % denominator_candidate:
            continue
        for numerator_candidate in range(1, denominator_candidate//4+1):
            if gcd(numerator_candidate, denominator_candidate) == 1:
                value = Fraction(numerator_candidate, denominator_candidate)
                exact = evaluate(root, value)
                assert exact != 0
                residue = None
                if denominator_candidate % 3:
                    residue = evaluate(root, numerator_candidate *
                                       pow(denominator_candidate, -1, 3)) % 3
                    assert residue != 0
                candidates.append({"weight": str(value),
                                   "value": str(exact),
                                   "modulo_3": residue})
    assert candidates == ([] if n != 10 else [{
        "weight": "1/5",
        "value": "-55421818556438910529961984/11920928955078125",
        "modulo_3": 2}])
    rows.append({
        "n": n,
        "x_numerator_degree": xx.numer.degree(),
        "x_denominator_degree": xx.denom.degree(),
        "reduced_denominator_primitive_square": True,
        "denominator_square_root_degree": expected_degree,
        "denominator_square_root_leading_coefficient": expected_lead,
        "denominator_square_root_coefficients_ascending": root,
        "matches_independent_division_polynomial_array": True,
        "rational_root_candidates_in_range": candidates,
        "no_denominator_root_for_0_less_w_le_quarter": True,
    })

report = {
    "status": "PASS",
    "method": "Exact tangent/chord addition in Q(w); no division recurrence",
    "curve": "y^2=x^3-(w+4)*x^2+4*(w+1)*x",
    "point": [4, 4],
    "discriminant": "256*w*(w-8)*(w+1)^2",
    "change_of_variables": "x=V+2; y=Y",
    "coefficient_order": "ascending powers of w",
    "rows": rows,
    "generic_point_curve_membership_checked_after_every_addition": True,
    "author_coefficient_data_sha256": sha256(AUTHOR_DATA.read_bytes()).hexdigest(),
    "scope": {
        "reference_point_infinite_order_for_rational_0_less_w_le_quarter": True,
        "external_torsion_theorem_required": "Mazur 1977, Theorem (8)",
        "actual_prescribed_detector_trace_matching_proved": False,
        "new_diophantine_variable_bound_proved": False,
    },
}
OUTPUT.write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({"status": "PASS", "method": report["method"],
                  "orders": [r["n"] for r in rows],
                  "certificate": str(OUTPUT)}))
