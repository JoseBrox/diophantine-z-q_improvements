"""Independent finite checks for the H-normalized weak-abc construction.
For positive contact valuations (1,m), m runs through every kept case.
Branches with negative m are affine in m on the entire negative ray.
"""
from fractions import Fraction
from itertools import permutations
from math import prod
from pathlib import Path
import json

THETA = (0, -1, Fraction(-1,2), Fraction(-1,3), Fraction(-1,4), Fraction(-2,5))
assert len(set(THETA)) == 6 and all(t != 1 for t in THETA)


def denom_order(a,b,K):
    pairs = ((3*a,5*b),(a,K*b),(K*a,b))
    assert all(x != y for x,y in pairs)
    return sum(min(x,y) for x,y in pairs)


def audit(kappa,d,K):
    gamma = 8/kappa-6
    alpha = d/kappa-3
    margin = alpha*(gamma-Fraction(6,K))/2-Fraction(1,2)
    assert margin > 0
    for m in range(1,K):
        for a,b in ((1,m),(m,1)):
            base = 3*(a+b)-denom_order(a,b,K)
            assert base%2==1 and base>0
    # When the other argument has valuation s<0, its sextic has order 6*s,
    # and v(H)=s. The branch is affine down the entire ray for s<=-1.
    for a,b,want in ((1,-6,21),(-6,1,9)):
        for s in (-1,-2,-37):
            m=a if a==1 else -a*s
            n=b if b==1 else -b*s
            nu=6*K*s+3*(m+n)-denom_order(m,n,K)
            assert nu==(3-18*s if a==1 else 3-6*s)
    # All orders of potential equality in the two balanced sums are excluded
    # by the odd valuation of u, even when a comparison C is zero.
    for nu in range(1,90,2):
        for v in range(-14,15):
            y=max(4*v,-2*nu)-nu
            assert y%2==1
            if 2*y>Fraction(-nu,2):
                assert v>0
    return dict(kappa=str(kappa),d=d,K=K,gamma=str(gamma),alpha=str(alpha),
                margin_over_one_half=str(margin))


if __name__=='__main__':
    print(json.dumps([audit(Fraction(121,100),10,15),audit(Fraction(16,15),6,6)],indent=2))
