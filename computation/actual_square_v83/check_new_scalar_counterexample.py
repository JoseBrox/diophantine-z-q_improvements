#!/usr/bin/env python3
"""Exact prepared obstruction on the proposed raw-square scalar locus.

This checks scalar data, not an actual elliptic detector tuple. The rank upper
bounds are PARI algebraic descent results; both curves use the same library.
"""
from fractions import Fraction as Q
from math import isqrt
import json
from sage.libs.pari import pari
from sympy import symbols, expand

def val(q,p):
    q=Q(q)
    if not q: raise ValueError('zero')
    n,d=abs(q.numerator),q.denominator
    a=b=0
    while n%p==0: a+=1;n//=p
    while d%p==0: b+=1;d//=p
    return a-b

def square(q):
    q=Q(q)
    return q>=0 and isqrt(q.numerator)**2==q.numerator and isqrt(q.denominator)**2==q.denominator

T=symbols("T")
LT=T*T-14*T+77
PT=T*(T-7)*(T-11)
assert expand((T*T-77)**2-LT**2-28*PT)==0
assert expand(49*(T*T-22*T+77)**2-49*LT**2+784*PT)==0

t=Q(49,4)
L=t*t-14*t+77
r=Q(196,889)
d=28*t*(t-7)*(t-11)/L**2
V=Q(1666,889)
e=4*d/V**2
H=V*V+d
assert t>11 and val(t,2)==-2
assert L==Q(889,16)
assert d==Q(576240,790321)==15*r*r
assert 1+d==Q(1169,889)**2
assert 49-28*d==Q(4753,889)**2
assert V==Q(17,2)*r and 0<V<2
assert e==Q(240,289) and 0<e<1
assert square(Q(d.denominator)) and square(Q(e.denominator))
assert (val(d,2),val(V,2),val(e,2))==(4,1,4)
assert d/(2**4)==Q(36015,790321)
assert (36015*pow(790321,-1,8))%8==7
assert H==Q(349,4)*r*r
assert d*H==5235*(r*r/2)**2
assert (15*pow(289,-1,8))%8==7
N=5235
E=pari.ellinit([0,0,0,-N*N,0])
E2=pari.ellinit([0,0,0,4*N*N,0])
ranks=[pari.ellrank(curve) for curve in (E,E2)]
assert all(int(a[0])==int(a[1])==0 for a in ranks)
torsion=pari.elltors(E)
assert int(torsion[0])==4
assert not square(Q(N,15))
assert not square(Q(-N,15))
# Map x=60(s/r)^2, y=120 sY/r^4. Using the quartic relation,
# both sides equal 14400*s^2/r^8 * d*(s^4-H^2).
assert 60**3/r**6 == Q(14400)*d/r**8
assert Q(N*N*60)/r**2 == Q(14400)*d*H**2/r**8
print(json.dumps({
 'status':'PASS',
 't':str(t),'L':str(L),'d':str(d),'V':str(V),'e':str(e),'H':str(H),
 'raw_square_root':str(Q(1169,889)),
 'symbolic_scalar_square_identities':True,
 'level_square_factor':str(r*r/2),
 'second_square_root':str(Q(4753,889)),
 'two_adic_valuations':{'t':-2,'d':4,'V':1,'e':4},
 'rank_E':str(ranks[0]),'rank_isogenous_E':str(ranks[1]),
 'torsion':str(torsion),
 'target_abscissa_squareclass':15,
 'positive_torsion_abscissa':N,
 'quotient':str(Q(N,15)),
 'actual_elliptic_detector_tuple_claimed':False,
 'rank_verification':'PARI algebraic descent; the two isogenous curves use the same implementation',
},indent=2))
