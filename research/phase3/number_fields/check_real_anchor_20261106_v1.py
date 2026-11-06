#!/usr/bin/env python3
"""Exact arithmetic for the totally real quartic finite-anchor obstruction."""
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path


def k(*values):
    return tuple(map(F, values+(0,)*(4-len(values))))


def add(a, b): return tuple(x+y for x, y in zip(a, b))
def neg(a): return tuple(-x for x in a)
def sub(a, b): return add(a, neg(b))
def scale(a, c): return tuple(x*c for x in a)


def mul(a, b):
    values = [F(0)]*7
    for i, x in enumerate(a):
        for j, y in enumerate(b): values[i+j] += x*y
    for i in range(6, 3, -1):
        values[i-2] += 1696*values[i]
        values[i-4] -= 18432*values[i]
    return tuple(values[:4])


def inv(a):
    columns = [mul(a, k(*(0,)*i+(1,))) for i in range(4)]
    mat = [[columns[j][i] for j in range(4)]+[F(i == 0)] for i in range(4)]
    for j in range(4):
        pivot = next(i for i in range(j, 4) if mat[i][j])
        mat[j], mat[pivot] = mat[pivot], mat[j]
        c = mat[j][j]; mat[j] = [x/c for x in mat[j]]
        for i in range(4):
            if i != j:
                c = mat[i][j]; mat[i] = [x-c*y for x, y in zip(mat[i], mat[j])]
    answer = tuple(row[4] for row in mat)
    assert mul(a, answer) == k(1)
    return answer


def pair(a=(), b=()):
    return (a if isinstance(a, tuple) else k(a), b if isinstance(b, tuple) else k(b))


def fadd(a, b): return (add(a[0], b[0]), add(a[1], b[1]))
def fneg(a): return (neg(a[0]), neg(a[1]))
def fsub(a, b): return fadd(a, fneg(b))
def fmul(a, b):
    return (add(mul(a[0], b[0]), scale(mul(a[1], b[1]), 2)), add(mul(a[0], b[1]), mul(a[1], b[0])))


def finv(a):
    ni = inv(sub(mul(a[0], a[0]), scale(mul(a[1], a[1]), 2)))
    out = (mul(a[0], ni), neg(mul(a[1], ni)))
    assert fmul(a, out) == pair(k(1), k())
    return out


def fdiv(a, b): return fmul(a, finv(b))


def dump(a):
    return [[[c.numerator, c.denominator] for c in part] for part in a]


def main():
    zero, one = pair(k(), k()), pair(k(1), k())
    s = k(0, 1)
    D = pair(k(11), k(-6))
    x = pair(k(8), k())
    b = pair(scale(s, F(1, 2)), scale(inv(s), 48))
    expected_square = pair(k(424), k(48))
    assert fmul(b, b) == expected_square
    assert fmul(b, b) == fsub(fmul(fmul(x, x), x), fmul(D, x))
    slope = fdiv(fsub(fmul(pair(k(3), k()), fmul(x, x)), D), fmul(pair(k(2), k()), b))
    xx = fsub(fmul(slope, slope), fmul(pair(k(2), k()), x))
    yy = fsub(fmul(slope, fsub(x, xx)), b)
    assert fmul(yy, yy) == fsub(fmul(fmul(xx, xx), xx), fmul(D, xx))
    expected_x = fdiv(pair(k(5697), k(-900)), pair(k(1696), k(192)))
    assert xx == expected_x
    assert all(c == 0 for part in xx for c in part[1:])
    assert any(c != 0 for part in yy for c in part[1:])
    assert xx != zero and yy != zero
    assert 424**2-2*48**2 == 2**6*7*17*23
    assert 848**2-16**2*2737 == 18432 == 2*96**2
    assert 7*17*23 == 2737
    # Rational inequalities prove that both conjugates of s^2 are positive.
    assert 848 > 0 and 848**2 > 16**2*2737
    report = {
        "status": "passed", "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "base_field_polynomial": [18432, 0, -1696, 0, 1],
        "base_field_properties": "The companion proof establishes degree4, total reality, and sqrt(2) not in Q(s).",
        "halfpoint_x": dump(x), "halfpoint_y": dump(b),
        "double_x": dump(xx), "double_y": dump(yy),
        "double_x_is_in_Q_sqrt2": True, "double_y_is_not_in_Q_sqrt2": True,
        "norm_of_halfpoint_ordinate_square": 175168,
        "consequence": "The doubled point is not any integer multiple of the original fixed point P. Its abscissa differs from x(nP) for every integern, so every finite exclusion product is nonzero on this same fixed point.",
        "scope": "Exact quotient-ring and elliptic group-law identities; the field and all-n exclusion arguments are proved in base_change_20261106_v1.tex.",
    }
    target = Path(__file__).with_name("real-anchor-verification_20261106_v1.json")
    target.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": "passed", "receipt": str(target)}))


if __name__ == "__main__": main()
