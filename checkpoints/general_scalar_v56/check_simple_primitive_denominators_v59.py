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

HERE = Path(__file__).resolve().parent


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
    kappa = F(16, 15)
    old_support = F(1, 4)+F(1, 9)+F(1, 25)+F(1, 49)+F(1, 14)
    assert 8/kappa-7 == F(1, 2)
    assert old_support == F(21739, 44100)
    assert F(1, 2)-old_support == F(311, 44100)

    # A standard nonintegral rational point on E_5; P is its double.
    R = (F(25, 4), F(75, 8))
    assert R[1]**2 == R[0]**3-25*R[0]
    P = add(R, R)
    assert P == (F(1681, 144), F(-62279, 1728))
    fixtures = []
    points = []
    Q = None
    for n in range(1, 13):
        Q = add(Q, P)
        points.append(Q)
        x, y = Q
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
        fixtures.append({"n": n, "A": str(A), "B": str(B), "C": str(C), "g": g})

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
        "simple_support_coefficient": str(8/kappa-7),
        "old_support_upper_bound": str(old_support),
        "strict_gap": str(F(1, 2)-old_support),
        "curve": "y^2=x^3-25x",
        "point_P": [str(v) for v in P],
        "good_primes_checked": len(good_primes),
        "reduction_order_checks": reduction_checks,
        "primitive_prime_fixtures": primitive_fixtures,
        "quartic_fixtures": fixtures,
        "manuscript_sha256": hashlib.sha256((HERE/"simple_primitive_denominators_v59.tex").read_bytes()).hexdigest(),
    }
    out = HERE/"simple_primitive_denominators_v59_certificate.json"
    out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k: result[k] for k in ("status", "strict_gap", "good_primes_checked", "reduction_order_checks")}))


if __name__ == "__main__":
    main()
