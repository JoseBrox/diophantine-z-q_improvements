#!/usr/bin/env python3
"""Small exact check of the fixed data and binary multiplication algorithm.

This verifies finitely many values.  The uniform height and operator-norm
bounds are proved in fixed_anchor_height.tex, not inferred from this run.
Only Python's standard library is used; no producer or compiler is imported.
"""

from fractions import Fraction
from hashlib import sha256
import json
from math import gcd, lcm
from pathlib import Path


def K(a=0, b=0):
    return (Fraction(a), Fraction(b))


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def neg(a):
    return (-a[0], -a[1])


def sub(a, b):
    return add(a, neg(b))


def mul(a, b):
    return (a[0] * b[0] + 2 * a[1] * b[1],
            a[0] * b[1] + a[1] * b[0])


def inv(a):
    norm = a[0] ** 2 - 2 * a[1] ** 2
    assert norm
    return (a[0] / norm, -a[1] / norm)


def div(a, b):
    return mul(a, inv(b))


def triple(a):
    c = lcm(a[0].denominator, a[1].denominator)
    x = a[0].numerator * (c // a[0].denominator)
    y = a[1].numerator * (c // a[1].denominator)
    g = gcd(gcd(abs(x), abs(y)), c)
    out = (x // g, y // g, c // g)
    assert out[2] > 0
    assert gcd(gcd(abs(out[0]), abs(out[1])), out[2]) == 1
    assert K(Fraction(out[0], out[2]), Fraction(out[1], out[2])) == a
    return out


def height(a):
    return (max(1, *map(abs, triple(a))) - 1).bit_length()


D = K(11, -6)
P = (K(Fraction(57, 8), Fraction(-28, 8)),
     K(Fraction(-660, 32), Fraction(417, 32)))
ZERO = K()


def on_curve(p):
    if p is None:
        return True
    x, y = p
    return mul(y, y) == sub(mul(mul(x, x), x), mul(D, x))


def point_add(p, q):
    if p is None:
        return q
    if q is None:
        return p
    x, y = p
    xx, yy = q
    if x == xx:
        if add(y, yy) == ZERO:
            return None
        assert y == yy and y != ZERO
        slope = div(sub(mul(K(3), mul(x, x)), D), mul(K(2), y))
    else:
        slope = div(sub(yy, y), sub(xx, x))
    rx = sub(sub(mul(slope, slope), x), xx)
    ry = sub(mul(slope, sub(x, rx)), y)
    return (rx, ry)


def binary_multiple(n):
    assert n >= 1
    r = P
    for bit in bin(n)[3:]:
        r = point_add(r, r)
        if bit == "1":
            r = point_add(r, P)
    return r


def point_height(p):
    return 0 if p is None else max(height(p[0]), height(p[1]))


def main():
    assert on_curve(P)
    assert (height(D), height(P[0]), height(P[1])) == (4, 6, 10)
    assert point_add(P, (P[0], neg(P[1]))) is None
    assert point_add(None, P) == P
    rows = []
    repeated = None
    for n in range(1, 25):
        repeated = point_add(repeated, P)
        binary = binary_multiple(n)
        assert repeated == binary
        assert on_curve(binary)
        h = point_height(binary)
        assert h <= 17 * n ** 8
        twice = point_add(binary, binary)
        shifted = point_add(binary, P)
        assert on_curve(twice) and on_curve(shifted)
        assert point_height(twice) <= 15 * h + 80
        assert point_height(shifted) <= 12 * h + 129
        if binary is not None:
            a, b, c = triple(binary[0])
            # Exact zero of the canonical factor at its intended abscissa.
            u = c * binary[0][0] - a
            v = c * binary[0][1] - b
            assert u * u - 2 * v * v == 0
            # Translating only the rational component by one cannot vanish.
            assert (u + c) ** 2 - 2 * v * v == c ** 2
        rows.append({"n": n, "point_height": h,
                     "abscissa_height": None if binary is None else height(binary[0])})
    here = Path(__file__).resolve().parent
    receipt = {
        "status": "passed",
        "scope": "Exact fixed-point membership, primitive triples, binary versus repeated addition for n=1..24, exceptional identity/opposite cases, and the stated finite height inequalities. Uniform bounds are proved in the companion TeX file.",
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256": sha256((here / "fixed_anchor_height.tex").read_bytes()).hexdigest(),
        "multiples": rows,
    }
    target = here / "fixed-anchor-height-verification.json"
    target.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": "passed", "checked_multiples": len(rows),
                      "maximum_point_height": max(r["point_height"] for r in rows),
                      "receipt": str(target)}))


if __name__ == "__main__":
    main()
