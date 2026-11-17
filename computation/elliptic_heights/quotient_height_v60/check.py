#!/usr/bin/env python3
"""Exact group-law and height-inequality checks for the quotient coordinate.

The canonical-height estimate is proved in the manuscript;
the finite checks do not assert a defining-variable bound.
"""
from fractions import Fraction as F
from functools import reduce
from math import gcd, lcm
from pathlib import Path
import hashlib
import json
import argparse

from sympy import QQ
from sympy.polys.fields import field

HERE = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[3]
_parser = argparse.ArgumentParser(description=__doc__)
_parser.add_argument("--output", type=Path, default=HERE/"certificate.json")
OUTPUT = _parser.parse_args().output



def height(q):
    q = F(q)
    return max(abs(q.numerator), q.denominator)


def projective_height(qs):
    qs = [F(q) for q in qs]
    den = lcm(*(q.denominator for q in qs))
    nums = [q.numerator*(den//q.denominator) for q in qs]
    common = reduce(gcd, nums)
    return max(map(abs, nums))//abs(common)


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


def main():
    K, x = field("x", QQ)
    formal = []
    for d in (1, 2, 5, 7):
        f = x**3-d*d*x
        X, Y = x, K(1)
        # The generic point is (x,y), y²=f. Store [n]H as (X,Y*y).
        # This uses tangent/chord addition, not a formal logarithm.
        for n in range(1, 9):
            assert Y*Y*f == X**3-d*d*X
            correction = n*n*X-x
            expected = F(d*d*(n**4-1), 5)
            if n == 1:
                assert not correction
                row = {"d": d, "n": n, "identically_zero": True}
            else:
                assert correction.numer.degree()+1 == correction.denom.degree()
                lead = F(str(correction.numer.LC/correction.denom.LC))
                assert lead == expected
                row = {"d": d, "n": n,
                       "numerator_degree": correction.numer.degree(),
                       "denominator_degree": correction.denom.degree(),
                       "leading_at_infinity": str(lead)}
            formal.append(row)
            if n == 1:
                slope = (3*X*X-d*d)/(2*Y*f)
            else:
                slope = (Y-1)/(X-x)
            new_X = slope*slope*f-X-x
            Y = slope*(x-new_X)-1
            X = new_X

    P = add((F(25, 4), F(75, 8)), (F(25, 4), F(75, 8)))
    multiples = [None]
    for _ in range(12):
        multiples.append(add(multiples[-1], P))
    count = 0
    cancellation_count = 0
    for h in (1, 2, 3):
        H = multiples[h]
        for n in (1, 2, 3, 4):
            U = multiples[n*h]
            for external in (F(-3), F(-1), F(1, 2), F(5, 7), F(1), F(2), F(n)):
                for B in (1, 3, 81):
                    beta = external**2+B
                    value = external**2*U[0]-H[0]
                    HV = height(value)
                    HX = height(external)
                    assert HV*HX**2*height(H[0])*2 >= height(U[0])
                    assert height(beta) >= HX**2
                    HE = projective_height([1, beta, value])
                    assert HE >= HX**2
                    assert HE**2 >= HV*HX**2
                    assert HE >= B
                    if value == 0:
                        cancellation_count += 1
                    count += 1

    cert = {
        "status": "PASS",
        "scope": "Exact generic group-law coefficients and rational height inequalities. No defining-variable bound is claimed.",
        "generic_group_law_cases": len(formal),
        "generic_group_law_data": formal,
        "rational_height_fixtures": count,
        "zero_correction_fixtures": cancellation_count,
        "manuscript_sha256": hashlib.sha256((REPO/"papers/elliptic_heights/pole_cancelling_quotient_height_20261117_v60.tex").read_bytes()).hexdigest(),
    }
    OUTPUT.write_text(json.dumps(cert, indent=2)+"\n")
    print(json.dumps({k: cert[k] for k in ("status", "generic_group_law_cases", "rational_height_fixtures")}))


if __name__ == "__main__":
    main()
