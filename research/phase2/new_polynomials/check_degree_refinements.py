#!/usr/bin/env python3
"""Exact small polynomial identities for the last source refinements."""
import json


def add(a,b):
    c=dict(a)
    for m,v in b.items():
        c[m]=c.get(m,0)+v
        if not c[m]:del c[m]
    return c


def scale(a,k):
    return {m:k*v for m,v in a.items() if k*v}


def mul(a,b):
    c={}
    for m,u in a.items():
        for n,v in b.items():
            z=tuple(x+y for x,y in zip(m,n))
            c[z]=c.get(z,0)+u*v
    return {m:v for m,v in c.items() if v}


def power(a,n):
    c={(0,0,0):1}
    for _ in range(n):c=mul(c,a)
    return c


def main():
    one={(0,0,0):1}
    B={(1,0,0):1}; t={(0,1,0):1}; sigma={(0,0,1):1}
    D=add(power(t,2),scale(B,3))
    E=add(power(t,2),mul(add(scale(sigma,4),scale(one,-1)),B))
    P=scale(mul(mul(B,t),add(one,scale(sigma,-1))),-4)
    residual=add(power(P,2),scale(mul(B,mul(add(D,scale(E,-1)),
                                            add(D,scale(E,3)))),-1))
    expected=scale(mul(power(B,2),mul(D,add(power(sigma,2),scale(sigma,-1)))),16)
    assert residual==expected
    # For this independent identity use B=a, t=the curve constant D.
    numerator=add(power(add(scale(power(B,2),3),scale(t,-1)),2),
                  scale(mul(B,add(power(B,3),scale(mul(t,B),-1))),-8))
    assert numerator==power(add(power(B,2),t),2)
    assert 4**9*2**11==2**29
    assert 4**9*2**12==2**30
    print(json.dumps({'status':'PASS',
        'checks':{'conic_identity_mod_sigma_squared_minus_sigma':True,
                  'elliptic_duplication_square_identity':True,
                  'finite_rank_exponents_29_and_30':True},
        'scope':'Exact polynomial identities and rank arithmetic; height and '
                'completeness proofs are in degree_refinements.tex.'},indent=2))


if __name__=='__main__':main()
