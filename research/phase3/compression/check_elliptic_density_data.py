#!/usr/bin/env python3
"""Exact rational arithmetic for the data in geometric_compression.tex."""
from fractions import Fraction as Q
import json


def k(a,b=0):return (Q(a),Q(b))
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def neg(a):return (-a[0],-a[1])
def sub(a,b):return add(a,neg(b))
def mul(a,b):return (a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def square(a):return mul(a,a)
def norm(a):return a[0]*a[0]-2*a[1]*a[1]
def inv(a):
    n=norm(a)
    assert n
    return (a[0]/n,-a[1]/n)
def div(a,b):return mul(a,inv(b))
def conj(a):return (a[0],-a[1])


def vp(a,p):
    assert a
    a=Q(a);n=abs(a.numerator);d=a.denominator;e=0
    while n%p==0:n//=p;e+=1
    while d%p==0:d//=p;e-=1
    return e


def main():
    d=k(3,-1);D=square(d)
    x=k(Q(57,8),Q(-7,2));y=k(Q(-165,8),Q(417,32))
    assert norm(d)==7 and D==k(11,-6)
    assert square(y)==sub(mul(square(x),x),mul(D,x))
    slope=div(sub(mul(k(3),square(x)),D),mul(k(2),y))
    x2=sub(square(slope),mul(k(2),x))
    y2=sub(mul(slope,sub(x,x2)),y)
    z2=div(neg(x2),y2)
    expected=k(Q(3396356159088,3287811625151),
               Q(-4135204317756,3287811625151))
    assert z2==expected
    assert [vp(a,3) for a in z2]==[1,1]
    assert min(vp(a,3) for a in x2 if a)==-2
    assert min(vp(a,3) for a in y2 if a)==-3
    assert mul(square(div(D,k(7))),square(conj(d)))==D
    result={'status':'PASS','checks':{
        'point_on_curve':True,'norm_d_equals_7':True,
        'double_parameter_exact':True,'double_formal_depth_3_equals_1':True,
        'conjugate_twist_isomorphism_coefficient':True},
        'z_2P':[str(a) for a in z2],
        'scope':'Exact fixed data only; geometric density is proved in the TeX.'}
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
