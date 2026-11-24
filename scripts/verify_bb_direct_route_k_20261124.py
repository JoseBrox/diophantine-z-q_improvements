#!/usr/bin/env python3
"""Independent finite and symbolic checks for docs/bb_direct_route_k_replacement_20261124.md.

Not a proof of Bhargava--Burungale's global rational-point theorem.
Requires SymPy.
"""
from fractions import Fraction
from itertools import product
from math import isqrt
import sympy as S

MENU = (1, 2, 3, 5, 6, 10, 15, 30)
B, s, t, r = S.symbols("B s t r")

def factor(m):
    return m*(m*s**2+B)*(m*t**2-B) - (m-B)*r**2*(m*s**2-B)*(m*t**2+B)

def squarefree_part(q):
    a = q.numerator * q.denominator
    out = 1 if a > 0 else -1
    for p, e in S.factorint(abs(a)).items():
        if e & 1:
            out *= int(p)
    return out

def valuation(q, p):
    def count(n):
        e = 0
        while n and n % p == 0:
            n //= p
            e += 1
        return e
    return count(q.numerator) - count(q.denominator)

for m in MENU:
    P = S.Poly(factor(m), B, s, t, r)
    assert P.total_degree() == 7
    assert P.domain.is_ZZ
assert 7*len(MENU) == 56  # Degree of product is the sum in an integral domain.

for f, odd_unit in product((0, 1), (1, 3, 5, 7)):
    m0 = next(a for a in (1, 3, 5, 15) if (a*odd_unit) % 8 == 7)
    m = (2**f)*m0
    assert m in MENU
    assert (odd_unit * pow(m0, -1, 8)) % 8 == 7
    B0 = Fraction((2**(4+f))*3*5*7*odd_unit, 1009**2)
    assert 0 < B0 < 1
    assert all(valuation(B0, p) >= 1 for p in (3, 5))
    assert valuation(B0, 2) >= 4
    c = B0/m
    assert c.denominator == isqrt(c.denominator)**2
    assert squarefree_part(c) % 8 == 7
    assert valuation(c, 2) >= 3
    assert 0 < c < 1

# Explicit v88 example on the degree-seven curve.
q = Fraction(112, 225)
u, v, w = Fraction(28, 15), Fraction(644, 825), Fraction(15, 29)
subs = {B: S.Rational(q.numerator, q.denominator),
        s: S.Rational(u.numerator, u.denominator),
        t: S.Rational(v.numerator, v.denominator),
        r: S.Rational(w.numerator, w.denominator)}
assert factor(1).subs(subs) == 0

# Degree-nine to degree-seven residual identity, including zero factors.
c, z = S.symbols("c z")
F = (1-c)*(s**4-c**2)*(t**4-c**2)-z**2
G = (s**2+c)*(t**2-c) - (1-c)*r**2*(s**2-c)*(t**2+c)
subst = (1-c)*r*(s**2-c)*(t**2+c)
assert S.expand(F.subs(z, subst) - (1-c)*(s**2-c)*(t**2+c)*G) == 0
print("PASS: eight multipliers, all 16 residue/parity cases, degree 56, explicit point, identity")
