#!/usr/bin/env python3
"""Exact finite checks for the 9m+2 transfer; not a proof of source premises."""
from fractions import Fraction
from math import isqrt
import json

def eta(nu, delta):
    return (15616 + 233856*delta + 233952*delta*(2*delta+1)**(nu+1)
            + 467712*delta*delta*(2*delta+1)**(nu+1))

expected = 1681043235226619916301182624511918527834137733707408448335539840
assert eta(58,4) == expected
assert eta(32,12) == 950817549694171759711025515571236610412597656252821888
routes = [dict(route='general25',m=25,degree=48318382080),
          dict(route='explicit27',m=27,degree=183368679424),
          dict(route='ordinary_abc11',m=11,degree=3261569)]
for row in routes:
    row['unknowns'] = 8 + 3 + 9*(row['m']-1)
    assert row['unknowns'] == 9*row['m']+2
    row['degree_bound'] = str(max(2*expected,4*row['degree']))
assert [r['unknowns'] for r in routes] == [227,245,101]

# Exact representation search is only an illustration/edge-case check.
# The general theorem in the manuscript uses Gauss--Legendre.
for n in range(1001):
    found = False
    for s in range(isqrt(n)+1):
        for u in range(isqrt(n)+1):
            rem = n-s*s-u*u-u
            if rem >= 0 and isqrt(rem)**2 == rem:
                found = True
                break
        if found: break
    assert found, n

for s in (Fraction(-3,2), Fraction(0), Fraction(2,3)):
    for t in (Fraction(-1,5), Fraction(0), Fraction(7,3)):
        for u in (Fraction(-1,2), Fraction(0), Fraction(3,7)):
            L=s*s+t*t+u*u+u
            assert L+Fraction(1,4) == s*s+t*t+(u+Fraction(1,2))**2
            assert L >= -Fraction(1,4)
            if L.denominator == 1: assert L >= 0

# A concrete failure of the proposed single sum-of-squares integrality test.
assert Fraction(3,5)**2+Fraction(4,5)**2 == 1
assert Fraction(3,5).denominator != 1
n=Fraction(773,9)
assert n == Fraction(17,3)**2+Fraction(22,3)**2
assert 9*n+1-9*(1+4**3+1+4+16) == 0
assert 1 % 3 != 0
print(json.dumps({'status':'exact finite checks passed',
 'eta_58_4':str(expected),'routes':routes,
 'wrapper_integer_examples_checked':'0 through 1000',
 'limitations':['Does not verify the defining-polynomial arithmetic premises.',
               'Does not rerun Sun or Isabelle proofs.',
               'The infinite transfer and obstruction are proved in the TeX.']},indent=2))
