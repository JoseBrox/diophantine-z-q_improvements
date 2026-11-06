#!/usr/bin/env python3
"""Independent exact check of the point-depth datum used in geometric density.

Uses the closed duplication formula for z=-x/y, rather than the other
checker's tangent-slope implementation.  Only the standard library is used.
"""
from fractions import Fraction as Q
import json


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def mul(a, b):
    return a[0] * b[0] + 2 * a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def inv(a):
    norm = a[0] * a[0] - 2 * a[1] * a[1]
    assert norm != 0
    return a[0] / norm, -a[1] / norm


def main():
    x, y = (Q(57, 8), Q(-7, 2)), (Q(-165, 8), Q(417, 32))
    D = (Q(11), Q(-6))
    x_squared = mul(x, x)
    # z(2P)=-2*y*(x^2+D)/(x^4-6*D*x^2+D^2).
    numerator = mul((-2 * y[0], -2 * y[1]), add(x_squared, D))
    denominator = add(add(mul(x_squared, x_squared),
                          mul((Q(-6), Q(0)), mul(D, x_squared))), mul(D, D))
    z = mul(numerator, inv(denominator))
    assert z == (Q(3396356159088, 3287811625151), Q(-4135204317756, 3287811625151))
    for c in z:
        assert c.numerator % 3 == 0 and c.numerator % 9 != 0 and c.denominator % 3 != 0
    # The residue classes of 1 and sqrt(2) are independent over F_3.
    assert all(t * t % 3 != 2 for t in range(3))
    print(json.dumps({"status": "PASS", "z_2P": [str(c) for c in z],
                      "formal_depth_at_3": 1,
                      "scope": "Exact duplication identity and depth datum; geometric density and formal-group torsion exclusion are proved separately."}, indent=2))


if __name__ == "__main__":
    main()
