#!/usr/bin/env python3
from fractions import Fraction as F
from math import isqrt
def val(q,p):
    q=F(q)
    if q==0:return float('inf')
    a,b=abs(q.numerator),q.denominator
    v=0
    while a%p==0:a//=p;v+=1
    while b%p==0:b//=p;v-=1
    return v
def r(y):return y*(y-1)*(y-2401)*(32*y+343)
c0=2504;P=r(c0)
assert P==51948354689656 and P%149==75 and val(P,2)==3
assert 1<=r(F(4*c0+1,4))/P<2
for y in [F(0),F(1),F(-2),F(13,17),F(2504),F(10017,4)]:
    z=y*y-F(76521,64)*y
    assert r(y)==32*z*z-F(5951086353,128)*z-F(455376332353657,8192)*y
def step(s,x):
    w=s*x*x;d=1+w
    y=c0+w/(d*d)
    assert isqrt(y.denominator)**2==y.denominator
    return s*r(y)/P,y
def unitmod8(q):
    v=val(q,2);u=F(q)/F(2)**v
    return (u.numerator*pow(u.denominator,-1,8))%8
count=0;new=0
for p in (19,23,43,67,149,157,211,251):
    assert P%p
    for e in range(-5,6):
        s=F(p)**e
        for x in [F(0),F(1),F(2),F(1,p),F(p),F(3,p*p),F(p*p,7),F(2,3)]:
            ss,y=step(s,x)
            if e%2:assert val(ss,p)==e
            if val(r(y),p)>0 and val(r(y),p)%2:
                new+=1
                assert e%2==0 and val(ss,p)%2==1
            count+=1
for p in (19,23,43,67,149,157,211):
    for a in range(1,20):
        s=F(a)
        if val(s,p)%2:continue
        for b in range(1,20):
            ss,y=step(s,F(b))
            if val(r(y),p)>0 and val(r(y),p)%2:
                assert val(ss,p)%2
                for x in (F(0),F(1,p),F(p),F(2,3)):
                    sss,_=step(ss,x)
                    assert val(sss,p)==val(ss,p)
                new+=1
for N in (1,2):
    for xs in [(0,1,2),(1,0,-3),(F(1,149),F(1,149**3),F(2,3))]:
        s=F(5*2**20*149**(2*N+1))
        for x in xs:
            s,y=step(s,F(x));assert val(s,149)==2*N+1
        R=(2**32*149**(N+1))**2*s/(1+s)**2
        assert R>100 and val(R,149)==4*N+3
        if all(F(x).denominator==1 for x in xs):
            assert val(s,2)==20 and unitmod8(s)==1
            assert val(R,2)==84 and unitmod8(R)==1
            assert val(R*(R+9792),2)==90 and unitmod8(R*(R+9792))==1
print({'valuation_fixtures':count,'new_contact_fixtures':new,'anchor_and_dyadic_fixtures':6})
