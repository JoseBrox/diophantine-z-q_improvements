#!/usr/bin/env python3
"""Exact finite checks supplementing the Lucas congruence proofs."""
from fractions import Fraction
from math import comb,gcd
from pathlib import Path
import json


def u_mod(A,n,m):
    a,b=0,1
    for _ in range(n):a,b=b,(A*b-a)%m
    return a


def check():
    congruences=0;rank_examples=[];sharp=[]
    for a in list(range(-100,-2))+list(range(3,101)):
        A=abs(a);d=abs(a-2);m=d*d
        u0,u1=0,1
        for j in range(1,301):
            actual=u1%m
            if a>0:expected=(j+d*comb(j+1,3))%m
            else:expected=(-1)**(j-1)*(j-d*comb(j+1,3))%m
            assert actual==expected
            if actual==0:
                assert j%d==0 and (6*j)%(d*d)==0
                assert j>=d*d//gcd(d,6)
            u0,u1=u1,(A*u1-u0)%m
            congruences+=1
        found=None
        for j in range(1,6*d*d+1):
            # A new simple recurrence independently checks the first index.
            if j==1:v0,v1=0,1
            if v1%m==0:found=j;break
            v0,v1=v1,(A*v1-v0)%m
        assert found is not None and found>=d*d//gcd(d,6)
        rank_examples.append({'a':a,'d':d,'first_divisible_index':found})
    for m in range(1,62,6):
        d=6*m;j=d*d//6
        assert u_mod(d+2,j,d*d)==0
        sharp.append({'d':d,'index':j})
    for a in range(7,128,6):
        d=a-2;j=d*d
        assert u_mod(a,j,d*d)==0
        assert u_mod(a,j,2)==u_mod(a,j+1,2)==1
    perturbations=0
    a,t,C0,M,r=7,48,7,30,3
    assert C0*C0-a*t*C0+t*t-1==0
    for q in range(2,501):
        if gcd(q,M)>1:continue
        C=Fraction(C0)+Fraction(M**r,q)
        G=C*C-a*t*C+t*t-1
        assert C.denominator==q and G.denominator==q*q
        assert G==Fraction(M**r*(2*C0-a*t)*q+M**(2*r),q*q)
        perturbations+=1
    return {'status':'PASS','congruences_checked':congruences,
            'first_divisibility_examples':rank_examples,
            'sharp_constant_examples':sharp,
            'rational_perturbation_examples':perturbations,
            'scope':'Exact finite checks; the universal congruence, growth and integrality assertions are proved in the accompanying TeX note. No polynomial variable reduction is certified.'}


if __name__=='__main__':
    report=check();p=Path(__file__).with_name('lucas-congruence-certificate.json')
    p.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','congruences_checked','rational_perturbation_examples')}))
