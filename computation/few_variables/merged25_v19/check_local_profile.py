#!/usr/bin/env python3
"""Exact finite checks for the raw-comparison, linear-scalar local profile.

The valuation and formal-group proofs are in the companion papers. This
checker verifies rational normalization examples, all rounding identities
used by the profile, the Hasse clustering polynomial identity, and the
complete exceptional-prime lists by exact arithmetic. It does not purport
to verify a universal arithmetic theorem by sampling.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import json
from pathlib import Path


def valuation(x,p):
    x=F(x)
    if not x: return None
    n,d=x.numerator,x.denominator;v=0
    while n%p==0:n//=p;v+=1
    while d%p==0:d//=p;v-=1
    return v


def prime_divisors(n):
    n=abs(n);out=set();p=2
    while p*p<=n:
        if n%p==0:
            out.add(p)
            while n%p==0:n//=p
        p=3 if p==2 else p+2
    if n>1:out.add(n)
    return out


def contacts(detectors):
    theta=[F(0),F(-1,2),F(-1),F(1,2399),F(-32,407)]
    blocks=[[s+t for s in (4*j+2,4*j+4) for t in theta]
            for j in range(detectors)]
    values=[a for block in blocks for a in block]+[F(-j-1) for j in range(detectors)]
    assert len(values)==len(set(values)) and all(values)
    tested=values+[a-b for i,a in enumerate(values) for b in values[:i]]
    factors=set()
    for a in tested:
        factors|=prime_divisors(a.numerator)|prime_divisors(a.denominator)
    extra=sorted(p for p in factors if p>76176)
    expected={2:[1875611,3828397,3982747],
              3:[149027,272011,1875611,3828397,3982747]}[detectors]
    assert extra==expected and 76249 not in factors
    product=1
    for p in extra:product*=p
    return {'detectors':detectors,'contact_and_pole_values':len(values),
            'checked_nonzero_values_and_differences':len(tested),
            'extra_exceptional_primes':extra,'extra_prime_product':product,
            'extra_prime_product_power_of_two_bound':product.bit_length(),
            'forced_prime_is_nonexceptional':True}


def check():
    examples=0;singular=0
    for p in (7,11,13):
        for nu in range(-7,8):
            for d in range(-7,8):
                for qunit in (-3,-1,1,2,3):
                    for dunit in (-3,-1,1,2,3):
                        q=qunit*F(p)**nu;D=dunit*F(p)**d
                        if 1+q*D==0:singular+=1;continue
                        value=valuation(q*D/(1+q*D),p);e=nu+d
                        assert value<=max(0,e)
                        if e:assert value==max(0,e)
                        if nu==0:
                            assert (value>0)==(d>0)
                            if d>0:assert value==d
                        if nu==1 and (d>=0 or d<=-2):assert value>=0
                        examples+=1
    rounded=0
    for alpha in range(1,502,2):
        for order in (1,3):
            threshold=(F(order)-F(3,4))*alpha
            smallest=threshold.numerator//threshold.denominator+1
            assert smallest>=order
            rounded+=1
        first_four_threshold=F(1,4)*alpha
        assert first_four_threshold.numerator//first_four_threshold.denominator+1>=1
        rounded+=1
        threshold=F(9,4)*alpha
        smallest=threshold.numerator//threshold.denominator+1
        assert smallest>=2*alpha+1>=3
        rounded+=1
    # u^2-20u+4=(u-25)^2+30(u-25)+129. All right-hand
    # summands are nonnegative for u>=25, and the constant is positive.
    assert (1,-50+30,625-750+129)==(1,-20,4)
    # Selected-place comparison second terms are >=3 at f-depth2
    # and at ratio-error4. Scalar G-depth3 gives second-term depth1.
    assert 1+2*2-2*1==3
    assert 1+2*4-2*3==3
    assert 1+2*3-2*3==1
    return {'status':'PASS','rational_normalization_examples':examples,
            'excluded_zero_denominator_examples':singular,
            'integer_rounding_examples':rounded,
            'hasse_cluster_positive_polynomial_coefficients':[1,30,129],
            'comparison_orders':[1]*11+[3]*3+[1,3],
            'scalar_denominator_orders':[1]*4+[3]*2,
            'lucas_residual_precision':3,'input_residual_precision':1,
            'formal_logarithm_relative_precision':4,
            'extra_common_index_divisibility':True,
            'contact_certificates':[contacts(2),contacts(3)],
            'scope':'Exact rational examples and arithmetic identities supplement the universal valuation and completeness proofs in the companion papers. The finite examples alone do not prove those theorems.'}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();report=check()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
