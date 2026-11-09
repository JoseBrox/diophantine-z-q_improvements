#!/usr/bin/env python3
"""Exact symbolic checks for the exceptional elliptic ratio surface.

Uses only the Python standard library.  Sparse Laurent polynomials certify
the morphism, both inverse identities after localization, the four entire
exceptional lines, and the nonzero boundary Jacobian minors.  The global
geometric and arithmetic theorems are proved in the accompanying paper;
this program does not substitute numerical tests for those proofs.
"""

from fractions import Fraction
from itertools import product
from pathlib import Path
import json


N = 4
ZERO = {}
ONE = {(0,) * N: Fraction(1)}


def constant(value):
    value = Fraction(value)
    return {(0,) * N: value} if value else {}


def variable(index):
    exponent = [0] * N
    exponent[index] = 1
    return {tuple(exponent): Fraction(1)}


def add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for exponent, coefficient in polynomial.items():
            result[exponent] = result.get(exponent, 0) + coefficient
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def scale(polynomial, coefficient):
    return add({exponent: coefficient * value for exponent, value in polynomial.items()})


def mul(left, right):
    result = {}
    for a, x in left.items():
        for b, y in right.items():
            exponent = tuple(a[i] + b[i] for i in range(N))
            result[exponent] = result.get(exponent, 0) + x * y
    return add(result)


def power(polynomial, exponent):
    if exponent < 0:
        assert len(polynomial) == 1
        monomial, coefficient = next(iter(polynomial.items()))
        return {tuple(exponent * e for e in monomial): coefficient ** exponent}
    result = ONE
    for _ in range(exponent):
        result = mul(result, polynomial)
    return result


def substitute(polynomial, images):
    assert len(images) == N
    result = ZERO
    for exponent, coefficient in polynomial.items():
        term = constant(coefficient)
        for image, degree in zip(images, exponent):
            term = mul(term, power(image, degree))
        result = add(result, term)
    return result


def derivative(polynomial, index):
    result = {}
    for exponent, coefficient in polynomial.items():
        degree = exponent[index]
        if degree:
            new_exponent = list(exponent)
            new_exponent[index] -= 1
            result[tuple(new_exponent)] = coefficient * degree
    return add(result)


def encode(polynomial):
    return [{"exponents": list(e), "coefficient": str(c)} for e, c in sorted(polynomial.items())]


# Source coordinate order is (t, s, y, z).
t, s, y, z = (variable(i) for i in range(N))
F1 = add(power(y, 2), scale(mul(power(t, 3), power(s, 3)), -1), constant(-9))
F2 = add(power(z, 2), scale(power(s, 3), -1), constant(-9))

# Target coordinate order is (x1, y1, x2, y2).
x1, y1, x2, y2 = (variable(i) for i in range(N))
E1 = add(power(y1, 2), scale(power(x1, 3), -1), constant(-9))
E2 = add(power(y2, 2), scale(power(x2, 3), -1), constant(-9))
pi = [mul(t, s), y, s, z]
inverse = [mul(x1, power(x2, -1)), x2, y1, y2]

assert substitute(E1, pi) == F1
assert substitute(E2, pi) == F2
assert substitute(F1, inverse) == E1
assert substitute(F2, inverse) == E2
assert [substitute(f, pi) for f in inverse] == [t, s, y, z]
assert [substitute(f, inverse) for f in pi] == [x1, y1, x2, y2]

minor = add(mul(derivative(F1, 2), derivative(F2, 3)),
            scale(mul(derivative(F1, 3), derivative(F2, 2)), -1))
assert minor == scale(mul(y, z), 4)
lines = []
for y_sign, z_sign in product((-1, 1), repeat=2):
    line = [t, ZERO, constant(3*y_sign), constant(3*z_sign)]
    assert substitute(F1, line) == ZERO
    assert substitute(F2, line) == ZERO
    image = [substitute(f, line) for f in pi]
    assert image == [ZERO, constant(3*y_sign), ZERO, constant(3*z_sign)]
    minor_on_line = substitute(minor, line)
    assert minor_on_line == constant(36*y_sign*z_sign)
    assert substitute(t, line) == t
    lines.append({
        "s": 0, "y": 3*y_sign, "z": 3*z_sign,
        "image_abscissas": [0, 0],
        "jacobian_minor": 36*y_sign*z_sign,
        "output_is_free_parameter": True,
    })

# The original ratio relation has both coefficients zero at each base point.
ratio_relation = add(x1, scale(mul(variable(3), x2), -1))
assert substitute(ratio_relation, [ZERO, y1, ZERO, variable(3)]) == ZERO

certificate = {
    "status": "PASS",
    "coefficient_ring": "Q[t,s,y,z], localized at s for the inverse identities",
    "surface_equations": [encode(F1), encode(F2)],
    "target_curve": "E: y^2 = x^3 + 9",
    "morphism": ["t*s", "y", "s", "z"],
    "inverse_when_x2_is_nonzero": ["x1/x2", "x2", "y1", "y2"],
    "curve_pullbacks_and_inverse_pullbacks_exact": True,
    "both_inverse_identities_exact": True,
    "exceptional_lines": lines,
    "boundary_jacobian_minor": "4*y*z",
    "surjective_section_of_output": ["t", 0, 3, 3],
    "ratio_coefficient_common_zero_locus": "x1=x2=0",
    "scope": "Symbolic verification of the explicit exceptional surface only. Smoothness, geometric irreducibility, and the general arithmetic obstruction are proved in the accompanying TeX paper.",
}
destination = Path(__file__).with_name("exceptional-correspondence-certificate.json")
destination.write_text(json.dumps(certificate, indent=2) + "\n")
print(json.dumps({"status": "PASS", "exceptional_lines": 4,
                  "boundary_minor_values": [-36, 36],
                  "certificate": str(destination)}, indent=2))
