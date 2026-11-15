#!/usr/bin/env python3
"""Exact finite checks supporting pole_obstructions.md, not a global audit."""
from fractions import Fraction as F
from math import isqrt
import json

def valuation(a,p):
    a=F(a); n,d=a.numerator,a.denominator
    assert n
    v=0
    while n%p==0:n//=p;v+=1
    while d%p==0:d//=p;v-=1
    return v,F(n,d)

def residue(a,p):
    a=F(a)
    return a.numerator*pow(a.denominator,-1,p)%p

def prime(p):
    return p>=2 and all(p%d for d in range(2,isqrt(p)+1))

def prepared(b):
    assert 0<b<1 and isqrt(b.denominator)**2==b.denominator
    ans={}
    for p,depth in [(2,4),(3,2),(17,2)]:
        v,u=valuation(b,p);assert v>=depth and v%2==0
        rr=residue(u,8 if p==2 else p)
        assert rr==1 if p==2 else pow(rr,(p-1)//2,p)==1
        ans[str(p)]={'valuation':v,'unitResidue':rr}
    return ans

b=F(409*204**2,5011**2)
first=prepared(b)
assert prime(409) and prime(11) and 11%4==3
assert valuation(2-b,11)[0]==1
b2=F(409*204**2,1013**4)
second=prepared(b2)
assert prime(1013) and 1013%4==1
assert pow(409,506,1013)==1012
assert pow(-409,506,1013)==1012
assert valuation(b2,1013)[0]==-4
report={'status':'PASS','uEqualsE':{'b':str(b),'prepared':first,'twoMinusB':str(2-b),'valuationAt11':1},'uEqualsOne':{'b':str(b2),'prepared':second,'valuationAt1013':-4,'euler409':1012,'eulerMinus409':1012},'scope':'Exact rational preparation and local-obstruction data. Universal valuation proofs are in pole_obstructions.md. No lower bound or improved quartic is asserted.'}
print(json.dumps(report,indent=2))
