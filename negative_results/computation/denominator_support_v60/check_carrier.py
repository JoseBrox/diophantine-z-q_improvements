#!/usr/bin/env python3
"""Exact fixtures for the specialization guard and rational-root height bound.

No finite computation is used to infer the geometric Siegel argument.
"""
from fractions import Fraction as F
from functools import reduce
from math import gcd, lcm
from pathlib import Path
import hashlib
import json
import argparse
import random

HERE = Path(__file__).resolve().parent
REPO=Path(__file__).resolve().parents[3]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output",type=Path,default=HERE/"carrier_certificate.json")
OUTPUT=parser.parse_args().output


def trim(a):
    a = list(map(F, a))
    while len(a) > 1 and not a[-1]:
        a.pop()
    return a or [F(0)]


def padd(a, b):
    n = max(len(a), len(b))
    return trim([(a[i] if i < len(a) else 0)+(b[i] if i < len(b) else 0)
                 for i in range(n)])


def pscale(a, s):
    return trim([s*x for x in a])


def pmul(a, b):
    r = [F(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i+j] += x*y
    return trim(r)


def peval(a, x):
    r = F(0)
    for c in reversed(a):
        r = r*x+c
    return r


def H(q):
    q = F(q)
    return max(abs(q.numerator), q.denominator)


def projective_H(qs):
    qs = list(map(F, qs))
    assert any(qs)
    den = lcm(*(q.denominator for q in qs))
    v = [q.numerator*(den//q.denominator) for q in qs]
    common = abs(reduce(gcd, v))
    return max(map(abs, v))//common


def add(P, Q, d=5):
    if P is None:
        return Q
    if Q is None:
        return P
    x, y = P
    X, Y = Q
    if x == X:
        if y == -Y:
            return None
        m = (3*x*x-d*d)/(2*y)
    else:
        m = (Y-y)/(X-x)
    x3 = m*m-x-X
    return x3, m*(x-x3)-y


def check(A, B, C, D, U, d=5):
    N = max(len(a) for a in (A, B, C, D))-1
    arrays = [list(map(F, a))+[F(0)]*(N+1-len(a)) for a in (A, B, C, D)]
    A, B, C, D = arrays
    p, q = A+B, C+D
    gamma = sum((p[i]*q[j]-p[j]*q[i])**2
                for i in range(len(p)) for j in range(i+1, len(p)))
    x, y = U
    den = peval(C, x)+peval(D, x)*y
    if not den:
        return "denominator_guard"
    r = (peval(A, x)+peval(B, x)*y)/den
    a = padd(A, pscale(C, -r))
    b = padd(B, pscale(D, -r))
    norm = padd(pmul(a, a), pscale(pmul([0, -d*d, 0, 1], pmul(b, b)), -1))
    assert peval(norm, x) == 0
    if not gamma:
        assert not any(norm)
        return "constant_specialization"
    assert any(norm)
    HC = projective_H(p+q)
    HE = projective_H(norm)
    constant = 4*(N+1)*(d*d+2)
    assert H(x) <= HE
    assert HE <= constant*HC**2*H(r)**2
    assert H(x) <= constant*HC**2*H(r)**2
    return "nonconstant_verified"


def main():
    generator = (F(25, 4), F(75, 8))
    P = add(generator, generator)
    points = []
    p = None
    for _ in range(4):
        p = add(p, P)
        points.append(p)

    families = [
        ([0, 1], [0], [1], [0]),
        ([0], [1], [1], [0]),
        ([1, 0, 1], [0], [0, 1], [0]),
        ([-6, 1, 1], [0], [-2, 1], [0]),  # common polynomial factor
        ([0, 2], [2], [0, 1], [1]),       # constant2 after cancellation
        ([1], [0], [0], [0]),             # invalid denominator
    ]
    rng = random.Random(5959060)
    for N in range(4):
        for _ in range(80):
            families.append(tuple([F(rng.randint(-5, 5), rng.randint(1, 5))
                                   for _ in range(N+1)] for _ in range(4)))

    counts = {"nonconstant_verified": 0, "constant_specialization": 0,
              "denominator_guard": 0}
    for U in points:
        for family in families:
            counts[check(*family, U)] += 1
        counts[check([-U[0], 1], [0], [1], [0], U)] += 1  # zero value, nonconstant map
        counts[check([1], [0], [-U[0], 1], [0], U)] += 1  # pole at the chosen point

    parameter_fixtures = 0
    for H_point in points:
        xh, yh = H_point
        for external in (F(0), F(1), F(-2), F(1, 3), F(17, 5), xh):
            # R=((X+yH)z²+(X²-xH)y)/((1+xH)z+Xy+1).
            arrays = ([0, 0, external+yh], [external**2-xh], [1, 1+xh], [external])
            N = 2
            padded = [list(map(F, a))+[F(0)]*(N+1-len(a)) for a in arrays]
            HC = projective_H([1]+sum(padded, []))
            assert HC <= 2*H(external)**2*H(xh)*H(yh)
            for U in points:
                counts[check(*arrays, U)] += 1
                parameter_fixtures += 1
            # Exact degeneration locus for R=(X-xH)z+yH.
            degenerate = ([yh, external-xh], [0], [1], [0])
            status = check(*degenerate, points[0])
            assert (status == "constant_specialization") == (external == xh)
            counts[status] += 1

    cert = {
        "status": "PASS",
        "scope": "Exact specialization guards, nonzero norm polynomials, rational-root heights, and fixed coefficient-height bounds. The geometric finiteness result uses the proved argument and Siegel's theorem.",
        "counts": counts,
        "parameter_height_fixtures": parameter_fixtures,
        "curve": "y^2=x^3-25x",
        "constant_bound": "4(N+1)(d^2+2)",
        "lemma_sha256": hashlib.sha256((REPO/"negative_results/papers/pole_parameters/denominator_support_height_obstruction_20261117_v60.tex").read_bytes()).hexdigest(),
        "architecture_sha256": hashlib.sha256((REPO/"negative_results/papers/pole_parameters/denominator_support_height_obstruction_20261117_v60.tex").read_bytes()).hexdigest(),
    }
    OUTPUT.write_text(json.dumps(cert, indent=2)+"\n")
    print(json.dumps({"status": cert["status"], "counts": counts,
                      "parameter_height_fixtures": parameter_fixtures}))


if __name__ == "__main__":
    main()
