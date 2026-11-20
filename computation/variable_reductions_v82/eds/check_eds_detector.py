#!/usr/bin/env python3
"""Exact finite audit of the prepared EDS divisibility detector.

Default execution is read-only. --report PATH writes a deterministic JSON
receipt. --pari additionally checks exact rank bounds and torsion with cypari2;
the standard checks use only the Python standard library.

No finite check proves abc or an odd-primitive-divisor theorem. No defining
polynomial for Z is asserted by this audit.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction as F
import hashlib
import json
from math import isqrt
from pathlib import Path
import sys

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


class Poly:
    """Exact sparse Laurent polynomials, for the universal clearing only."""

    def __init__(self, n, terms=None):
        self.n = n
        self.terms = {tuple(e): F(c) for e, c in (terms or {}).items() if c}

    @classmethod
    def constant(cls, n, c):
        return cls(n, {(0,) * n: c})

    @classmethod
    def var(cls, n, k):
        e = [0] * n
        e[k] = 1
        return cls(n, {tuple(e): 1})

    def coerce(self, x):
        return x if isinstance(x, Poly) else Poly.constant(self.n, x)

    def __add__(self, x):
        x = self.coerce(x)
        d = defaultdict(F, self.terms)
        for e, c in x.terms.items():
            d[e] += c
        return Poly(self.n, d)

    __radd__ = __add__

    def __neg__(self):
        return Poly(self.n, {e: -c for e, c in self.terms.items()})

    def __sub__(self, x):
        return self + (-self.coerce(x))

    def __rsub__(self, x):
        return self.coerce(x) - self

    def __mul__(self, x):
        x = self.coerce(x)
        d = defaultdict(F)
        for e, c in self.terms.items():
            for f, b in x.terms.items():
                d[tuple(a + z for a, z in zip(e, f))] += c * b
        return Poly(self.n, d)

    __rmul__ = __mul__

    def __pow__(self, k):
        if k < 0:
            assert len(self.terms) == 1
            e, c = next(iter(self.terms.items()))
            return Poly(self.n, {tuple(k * a for a in e): c**k})
        answer = Poly.constant(self.n, 1)
        power = self
        while k:
            if k & 1:
                answer *= power
            power *= power
            k >>= 1
        return answer

    def __eq__(self, x):
        x = self.coerce(x)
        return self.n == x.n and self.terms == x.terms


def add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P
    x, y = P
    z, w = Q
    if x == z and y == -w:
        return None
    slope = (3 * x*x - 2) / (2*y) if P == Q else (w-y)/(z-x)
    u = slope*slope-x-z
    return u, slope*(x-u)-y


def mul(n, P):
    if n < 0:
        return mul(-n, (P[0], -P[1]))
    Q = None
    while n:
        if n & 1:
            Q = add(Q, P)
        P = add(P, P)
        n >>= 1
    return Q


def on_curve(P):
    return P is None or P[1]**2 == P[0]**3 - 2*P[0]


def vp(q, p):
    q = F(q)
    if not q:
        return None
    a, b = abs(q.numerator), q.denominator
    result = 0
    while a % p == 0:
        a //= p
        result += 1
    while b % p == 0:
        b //= p
        result -= 1
    return result


def square_outside(n, primes):
    for p in primes:
        while n % p == 0:
            n //= p
    return isqrt(n)**2 == n


def b_value(H, U):
    q = U[0]
    g = 1 + q*q
    return (H[1] + q*q*g)/(g*g)


def mod_add(P, Q, p):
    if P is None:
        return Q
    if Q is None:
        return P
    x, y = P
    z, w = Q
    if x == z and (y+w) % p == 0:
        return None
    num, den = (3*x*x-2, 2*y) if P == Q else (w-y, z-x)
    slope = num * pow(den, -1, p) % p
    u = (slope*slope-x-z) % p
    return u, (slope*(x-u)-y) % p


def mod_order(P, p):
    Q = None
    for n in range(1, p+2+2*isqrt(p)+3):
        Q = mod_add(Q, P, p)
        if Q is None:
            return n
    raise AssertionError("Hasse range exceeded")


def digest_fractions(values):
    text = "\n".join(f"{v.numerator}/{v.denominator}" for v in values)
    return hashlib.sha256(text.encode()).hexdigest()


def check(pari=False):
    primitive_margin = 1-F(2,3)-F(8,101)
    assert primitive_margin == F(77,303) and primitive_margin > F(1,5)
    A, G, v, s = [Poly.var(4, i) for i in range(4)]
    d = A * G**(-2)
    native = d*(d+v*v)**2*s**4-d*(d-v*v)**2*(1-d)**2
    cleared = A*G**4*(A+G*G*v*v)**2*s**4 - A*(A-G*G*v*v)**2*(G*G-A)**2
    assert G**10*native == cleared
    assert G**8*native != cleared

    y, q = [Poly.var(2, i) for i in range(2)]
    g = 1+q*q
    numerator = y+q*q*g
    assert numerator-g*g == y-1-q*q

    r, t, v, s, eta = [Poly.var(5, i) for i in range(5)]
    A = 112*(r*eta+t**4+t**8)
    G = 29*(1+t**4)
    R = A*G**4*(A+G*G*v*v)**2*s**4 - A*(A-G*G*v*v)**2*(G*G-A)**2
    total_degree = max(sum(e) for e in R.terms)
    weighted_degree = max(sum(e[:4])+2*e[4] for e in R.terms)
    assert total_degree == weighted_degree == 48
    coefficients = [[list(e), int(c)] for e, c in sorted(R.terms.items())]
    assert all(c.denominator == 1 for c in R.terms.values())
    coefficient_hash = hashlib.sha256(json.dumps(coefficients, separators=(",", ":")).encode()).hexdigest()

    P0 = F(2), F(2)
    assert add((F(-1), F(1)), (F(0), F(0))) == P0
    P = mul(2, P0)
    assert P == (F(9,4), F(-21,8))
    assert on_curve(P)
    torsion_counts = {}
    for p in (5, 7):
        torsion_counts[str(p)] = 1 + sum(1 for x in range(p) for y in range(p) if (y*y-x*x*x+2*x) % p == 0)
    assert torsion_counts == {"5": 10, "7": 8}

    values = []
    count = 0
    for h in range(-12, 13):
        if h == 0:
            continue
        H = mul(h, P0)
        assert on_curve(H)
        for m in range(-6, 7):
            if m == 0:
                continue
            U = mul(m, H)
            assert on_curve(U)
            b = b_value(H, U)
            assert square_outside(b.denominator, (2,3)), (h, m)
            values.append(b)
            count += 1

    # Exact primitive-odd fixtures. Primality and reduction order are checked
    # independently of the characteristic-zero multiplication routine.
    primitive_fixtures = []
    for p in (5,7,11,13,17,19,23,31,41,43):
        assert all(p % d for d in range(2,isqrt(p)+1))
        h = mod_order((2 % p,2 % p), p)
        H = mul(h, P0)
        depth = -vp(H[0], p)//2
        assert depth > 0
        if depth % 2 == 0:
            continue
        U = P0
        b = b_value(H, U)
        predicted = -3*depth - 2*vp(1+U[0]**2,p)
        assert vp(b,p) == predicted < 0 and predicted % 2
        primitive_fixtures.append({"p":p,"rank_of_apparition":h,"formal_depth":depth,"v_b":predicted})
    assert primitive_fixtures

    # H=68P0 is formal at 2,3,7,29. Its ordinate is between 0 and 8;
    # every U=mH has x(U)>sqrt(2), so these actual values satisfy d<1.
    H = mul(68, P0)
    assert 0 < H[1] < 8
    prepared = []
    for m in (1,2,3,-1,-2,-3):
        U = mul(m,H)
        b = b_value(H,U)
        d = F(112,841)*b
        assert 0 < d < 1
        assert isqrt(d.denominator)**2 == d.denominator
        local = {}
        for p in (2,3,7,29):
            eH = -vp(H[0],p)//2
            eU = -vp(U[0],p)//2
            assert eU >= eH >= 1
            assert vp(b-1,p) == 4*eU
            local[str(p)] = {"e_H":eH,"e_U":eU,"v_b_minus_1":4*eU,"v_d":vp(d,p)}
        assert vp(d,2) == 4
        unit = d / (7*F(2)**4)
        assert unit.numerator * pow(unit.denominator,-1,8) % 8 == 1
        prepared.append({"m":m,"local":local,"d_sha256":digest_fractions([d])})

    # Valuation inequalities underlying the formal case, for an exact finite
    # range; the written argument establishes them for all positive depths.
    for eH in range(1,33):
        for eU in range(eH,65):
            assert -8*eU < -3*eH
            assert min(-3*eH,0,-4*eU)+8*eU == 4*eU

    result = {
        "status":"PASS",
        "scope":"finite algebra and rational fixtures for prepared EDS divisibility; no Z variable reduction",
        "curve":[0,0,0,-2,0],
        "universal_clearing":"G^10 P_(A/G^2)(v,s)",
        "terminal_degree":total_degree,
        "terminal_weighted_degree":weighted_degree,
        "terminal_monomials":len(R.terms),
        "terminal_max_coefficient":str(max(abs(c.numerator) for c in R.terms.values())),
        "terminal_coefficients_sha256":coefficient_hash,
        "true_multiple_fixtures":count,
        "true_multiple_values_sha256":digest_fractions(values),
        "primitive_rejection_fixtures":primitive_fixtures,
        "prepared_fixtures":prepared,
        "torsion_reduction_counts":torsion_counts,
        "finite_algebra_rank":8,
        "separator_menu_size":2*(8*7//2)+1,
        "primitive_mass_margin":str(primitive_margin),
        "arithmetic_inputs_not_computationally_proved":[
            "ordinary rational abc",
            "Cornelissen-Zahidi Proposition 3.10(iii) / Silverman Lemma13 odd primitive divisors",
            "published class-seven intrinsic-pole realization and density",
            "database assertion that (2,2) generates the free part of E(Q)"
        ],
        "unresolved":"identifying an external rational X with the integer multiplier j/h"
    }
    if pari:
        from cypari2 import Pari
        gp = Pari()
        E = gp.ellinit([0,0,0,-2,0])
        rank = gp.ellrank(E)
        tors = gp.elltors(E)
        assert int(rank[0]) == int(rank[1]) == 1
        assert int(tors[0]) == 2
        result["pari_exact"] = {"version":str(gp.version()),"rank_bounds":[int(rank[0]),int(rank[1])],"torsion_order":int(tors[0]),"rank_point_output":str(rank[3]),"conductor":int(gp.ellglobalred(E)[0])}
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report",type=Path)
    parser.add_argument("--pari",action="store_true")
    args = parser.parse_args()
    result = check(args.pari)
    if args.report:
        args.report.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    else:
        baseline = Path(__file__).with_name("eds_detector_certificate.json")
        if baseline.exists():
            expected = json.loads(baseline.read_text())
            core = {k:v for k,v in result.items() if k != "pari_exact"}
            assert core == expected, "detector receipt differs from independent recomputation"
    print(json.dumps({k:result[k] for k in ("status","terminal_degree","terminal_monomials","true_multiple_fixtures","finite_algebra_rank","separator_menu_size")},sort_keys=True))
    if args.pari:
        print(json.dumps({"pari_exact":result["pari_exact"]},sort_keys=True))


if __name__ == "__main__":
    main()
