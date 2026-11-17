#!/usr/bin/env python3
"""Exact arithmetic audit of the constants and elliptic fixtures in the proof.

The asymptotic theorem follows from weak abc and canonical height, not from
these finite fixtures.  This checker uses only the Python standard library.
"""
from fractions import Fraction as F
from math import gcd, isqrt
from pathlib import Path
import hashlib
import json
import argparse

HERE = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[3]
_parser = argparse.ArgumentParser(description=__doc__)
_parser.add_argument("--output", type=Path, default=HERE/"certificate.json")
OUTPUT = _parser.parse_args().output



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
        lam = (3*x*x-d*d)/(2*y)
    else:
        lam = (Y-y)/(X-x)
    x3 = lam*lam-x-X
    return x3, lam*(x-x3)-y


def add_mod(P, Q, p, d=5):
    if P is None:
        return Q
    if Q is None:
        return P
    x, y = P
    X, Y = Q
    if x == X:
        if (y+Y) % p == 0:
            return None
        lam = (3*x*x-d*d)*pow(2*y, -1, p) % p
    else:
        lam = (Y-y)*pow(X-x, -1, p) % p
    x3 = (lam*lam-x-X) % p
    return x3, (lam*(x-x3)-y) % p


def val(n, p):
    n = abs(n)
    assert n
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def primes_upto(B):
    return [p for p in range(2, B+1)
            if all(p % q for q in range(2, isqrt(p)+1))]


def reduce_point(P, p):
    if P[0].denominator % p == 0:
        return None
    assert P[1].denominator % p
    return tuple(v.numerator * pow(v.denominator, -1, p) % p for v in P)


def main():
    kappa = F(4, 3)
    old_support = F(1, 4)+F(1, 9)+F(1, 25)+F(1, 49)+F(1, 14)
    assert 2/kappa-1 == F(1, 2)
    assert old_support == F(21739, 44100)
    assert F(1, 2)-old_support == F(311, 44100)

    assert 2/(1+old_support) == F(88200, 65839)
    assert 2/F(121, 100)-1 == F(79, 121)
    coprime_index_rows = []
    for exponent in (F(16, 15), F(121, 100), F(4, 3), F(3, 2), F(19, 10), F(199, 100), F(1999, 1000)):
        coefficient = 2/exponent-1
        reciprocal = 1/coefficient
        R = reciprocal.numerator//reciprocal.denominator+1
        assert F(1, R) < coefficient
        prime_factors = primes_upto(R)
        coprime_index_rows.append({"kappa": str(exponent),
                                   "coefficient": str(coefficient),
                                   "R": R,
                                   "excluded_prime_count": len(prime_factors),
                                   "strict_gap": str(coefficient-F(1, R))})

    # A standard nonintegral rational point on E_5. Q=2R and P=4R.
    R = (F(25, 4), F(75, 8))
    assert R[1]**2 == R[0]**3-25*R[0]
    Q = add(R, R)
    assert Q == (F(1681, 144), F(-62279, 1728))
    P = add(Q, Q)
    fixtures = []
    points = []
    nQ = None
    nP = None
    for n in range(1, 13):
        nQ = add(nQ, Q)
        nP = add(nP, P)
        assert nP == add(nQ, nQ)
        points.append(nP)
        x, y = nQ
        assert y*y == x*x*x-25*x
        A, B = isqrt(x.numerator), isqrt(x.denominator)
        assert A*A == x.numerator and B*B == x.denominator
        assert gcd(A, B) == 1
        C = y*B**3/A
        assert C.denominator == 1
        C = C.numerator
        assert C*C == A**4-25*B**4 > 0
        assert A >= B
        g = gcd(A**4, 25*B**4)
        assert g == gcd(A**4, 25) and g <= 25
        assert gcd(C*C//g, 25*B**4//g) == 1
        assert C*C//g+25*B**4//g == A**4//g
        numerator = A**4+25*B**4
        denominator = 2*abs(A*B*C)
        root_double = F(numerator, denominator)
        assert root_double**2 == nP[0]
        common = gcd(numerator, denominator)
        rem = common
        for p in (2, 5):
            while rem % p == 0:
                rem //= p
        assert rem == 1
        for D1, D2 in ((A, B), (A, C), (B, C)):
            rem = gcd(D1, D2)
            for p in (2, 5):
                while rem % p == 0:
                    rem //= p
            assert rem == 1
        fixtures.append({"n": n, "A_Q": str(A), "B_Q": str(B),
                         "C_Q": str(C), "g": g,
                         "A": str(root_double.numerator),
                         "B": str(root_double.denominator),
                         "duplication_gcd": str(common)})

    # An independently computed finite-field order for each good small prime
    # tests the reduction-order equivalence, not just the recurrence itself.
    good_primes = [p for p in primes_upto(997) if p not in (2, 5)]
    reduction_checks = 0
    primitive_fixtures = []
    for p in good_primes:
        pbar = reduce_point(P, p)
        if pbar is None:
            order = 1
        else:
            qbar = None
            for order in range(1, 2*p+2):
                qbar = add_mod(qbar, pbar, p)
                if qbar is None:
                    break
            else:
                raise AssertionError((p, "order not found"))
        for f, point in zip(fixtures, points):
            n, B = f["n"], int(f["B"])
            assert (B % p == 0) == (n % order == 0)
            assert (reduce_point(point, p) is None) == (n % order == 0)
            if B % p == 0:
                product = int(f["A_Q"])*int(f["B_Q"])*int(f["C_Q"])
                assert val(B, p) == val(product, p)
            reduction_checks += 1
            if B % p == 0 and order < n:
                assert any(int(fixtures[n//ell-1]["B"]) % p == 0
                           for ell in primes_upto(n) if n % ell == 0)
            if n == order and B % p == 0:
                v = val(B, p)
                assert all(int(old["B"]) % p for old in fixtures[:n-1])
                primitive_fixtures.append({"n": n, "p": p, "valuation": v})

    result = {
        "status": "PASS",
        "scope": "Exact constants and finite elliptic arithmetic fixtures; the asymptotic theorem is conditional on weak abc and proved in the manuscript.",
        "kappa": str(kappa),
        "simple_support_coefficient": str(2/kappa-1),
        "general_kappa_upper_endpoint": str(2/(1+old_support)),
        "coefficient_at_121_over_100": str(2/F(121, 100)-1),
        "coprime_index_examples": coprime_index_rows,
        "old_support_upper_bound": str(old_support),
        "strict_gap": str(F(1, 2)-old_support),
        "curve": "y^2=x^3-25x",
        "point_P": [str(v) for v in P],
        "point_Q": [str(v) for v in Q],
        "good_primes_checked": len(good_primes),
        "reduction_order_checks": reduction_checks,
        "primitive_prime_fixtures": primitive_fixtures,
        "quartic_fixtures": fixtures,
        "manuscript_sha256": hashlib.sha256((REPO/"papers/elliptic_divisibility/simple_primitive_denominators_20261117_v60.tex").read_bytes()).hexdigest(),
    }
    out = OUTPUT
    out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k: result[k] for k in ("status", "strict_gap", "good_primes_checked", "reduction_order_checks")}))


if __name__ == "__main__":
    main()
