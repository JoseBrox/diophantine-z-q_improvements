#!/usr/bin/env python3
"""Exact certificates accompanying effective_elliptic_sums_20261108_v10.tex.

Only Python's standard library is used. The all-place height inequality is
proved in the paper, not inferred from these finite identity checks.
"""
from __future__ import annotations

from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import hashlib
import json


class Q2:
    """An exact element a+b*sqrt(2)."""

    def __init__(self, a=0, b=0):
        self.a, self.b = F(a), F(b)

    def __add__(self, other):
        other = other if isinstance(other, Q2) else Q2(other)
        return Q2(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Q2(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-other if isinstance(other, Q2) else -Q2(other))

    def __mul__(self, other):
        other = other if isinstance(other, Q2) else Q2(other)
        return Q2(self.a * other.a + 2 * self.b * other.b,
                  self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = other if isinstance(other, Q2) else Q2(other)
        norm = other.a**2 - 2 * other.b**2
        assert norm != 0
        return self * Q2(other.a / norm, -other.b / norm)

    def __pow__(self, power):
        assert power >= 0
        answer, base = Q2(1), self
        while power:
            if power % 2:
                answer = answer * base
            base = base * base
            power //= 2
        return answer

    def __eq__(self, other):
        other = other if isinstance(other, Q2) else Q2(other)
        return self.a == other.a and self.b == other.b

    def data(self):
        return [str(self.a), str(self.b)]


def v2_int(n):
    assert n != 0
    n = abs(n)
    answer = 0
    while n % 2 == 0:
        answer += 1
        n //= 2
    return answer


def v2_fraction(q):
    return v2_int(q.numerator) - v2_int(q.denominator)


def v_sqrt2(z):
    # The two rational components have opposite valuation parity, so
    # their finite valuations cannot coincide or cancel.
    vals = []
    if z.a:
        vals.append(2 * v2_fraction(z.a))
    if z.b:
        vals.append(1 + 2 * v2_fraction(z.b))
    assert vals
    return min(vals)


def series_add(a, b, order):
    return [(a[k] if k < len(a) else F(0)) +
            (b[k] if k < len(b) else F(0)) for k in range(order)]


def series_mul(a, b, order):
    return [sum((a[i] * b[k-i]
                 for i in range(k+1) if i < len(a) and k-i < len(b)), F(0))
            for k in range(order)]


def series_inverse(a, order):
    assert a[0]
    result = [1 / a[0]]
    for k in range(1, order):
        result.append(-sum((a[i] * result[k-i]
                           for i in range(1, min(k+1, len(a)))), F(0)) / a[0])
    return result


def exp_lower(q, terms):
    return sum((q**k / factorial(k) for k in range(terms+1)), F(0))


def main():
    D = Q2(11, -6)
    x0, y0 = Q2(1, 1), Q2(0, 2)
    assert y0**2 == x0**3 - D*x0
    slope = (3*x0**2 - D)/(2*y0)
    xp = slope**2 - 2*x0
    yp = slope*(x0-xp) - y0
    assert xp == Q2(F(57, 8), F(-7, 2))
    assert yp == Q2(F(-165, 8), F(417, 32))
    assert yp**2 == xp**3 - D*xp
    assert xp == ((x0**2 + D)/(2*y0))**2
    valuations = [v_sqrt2(xp), v_sqrt2(yp), v_sqrt2(-xp/yp)]
    assert valuations == [-6, -9, 3]

    # Write x=t^-2 F(s), s=D*t^4. Check F^2-F-s=0 and
    # 1-2sF'/F=(1+4s)^(-1/2) through s^12, all exactly.
    order = 13
    fx = [F(1)] + [F((-1)**(k-1)*comb(2*k-2, k-1), k)
                   for k in range(1, order)]
    quadratic = series_add(series_mul(fx, fx, order), [-a for a in fx], order)
    quadratic[1] -= 1
    assert all(a == 0 for a in quadratic)
    sfx_prime = [F(k)*fx[k] for k in range(order)]
    differential = series_mul(sfx_prime, series_inverse(fx, order), order)
    differential = [-2*a for a in differential]
    differential[0] += 1
    expected = [F((-1)**k*comb(2*k, k)) for k in range(order)]
    assert differential == expected
    log_coefficients = [F((-1)**k*comb(2*k, k), 4*k+1)
                        for k in range(order)]
    assert all(c.denominator % 2 == 1 for c in log_coefficients)

    r = 4
    target_log_coefficient = 2*sum(comb(r-1, k-1)*(k-1) for k in range(1, r+1))
    target_integer_constant = 1
    vector_integer_constant = 1
    for k in range(1, r+1):
        target_integer_constant *= k**comb(r-1, k-1)
        vector_integer_constant *= k**comb(r, k)
    vector_log_coefficient = 2*r + 2*sum(comb(r, k)*(k-1) for k in range(1, r+1))
    assert target_log_coefficient == 24
    assert target_integer_constant == 864
    assert vector_log_coefficient == 42
    assert vector_integer_constant == 20736

    exp_13_4 = exp_lower(F(13, 4), 12)
    exp_7 = exp_lower(F(7), 12)
    assert exp_13_4 > 24
    assert exp_7 > 864
    # 12*log(24)-12 < 27; 6+log(864) < 13. Thus loss <40.
    assert 12*F(13, 4)-12 + 6 + 7 == 40

    path = Path(__file__).resolve()
    result = {
        "status": "PASS",
        "arithmetic": "exact rational arithmetic; Python standard library",
        "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "curve": {"field": "Q(sqrt(2))", "D": D.data(), "P": [xp.data(), yp.data()]},
        "point_and_doubling_identities": "PASS",
        "sqrt2_valuations_of_x_y_t": valuations,
        "formal_identity_check": {
            "variable": "s=D*t^4",
            "verified_modulus": "s^13",
            "identities": ["F^2-F-s=0", "1-2sF'/F=(1+4s)^(-1/2)"],
            "scope": "Finite exact checks support the symbolic derivation; the infinite identities and all-place bounds are proved in the paper.",
            "log_coefficients": [str(c) for c in log_coefficients],
        },
        "four_term_individual_height_loss": {"log_B_coefficient": 24, "log_constant_argument": 864},
        "four_term_joint_height_loss": {"log_B_coefficient": 42, "log_constant_argument": 20736},
        "numerical_corollary": {
            "retained_premise": "h(x([n]P)) >= n^2 - 6 for every nonzero integer n",
            "bound": "B^2 <= 2*h(Z)+80 <= 2*h(S0)+2*h(S1)+83",
            "parity_restriction": False,
        },
        "exponential_lower_bound_certificates": [
            {"x": "13/4", "terms_through": 12, "partial_sum": str(exp_13_4), "strictly_exceeds": 24},
            {"x": "7", "terms_through": 12, "partial_sum": str(exp_7), "strictly_exceeds": 864},
        ],
    }
    output = path.with_name("effective-elliptic-sums-certificate.json")
    output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": "PASS", "certificate": str(output),
                      "individual_height_loss": "24 log B + log 864",
                      "numerical_bound": "B^2 <= 2 h(S0)+2 h(S1)+83"}, indent=2))


if __name__ == "__main__":
    main()
