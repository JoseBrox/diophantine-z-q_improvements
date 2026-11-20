#!/usr/bin/env python3
"""Exact checks for the eta=241 obstruction family on the new scalar locus.

The rational rank bounds use PARI algebraic descent, with a consistency check
on a two-isogenous curve. Kummer classes use separate rational group additions.
The universal approximation argument is in the accompanying proof note.
"""
from fractions import Fraction as Q
from hashlib import sha256
import json
from sympy import symbols, expand, factorint, together
from sage.libs.pari import pari


def val(q,p):
    q=Q(q)
    assert q
    a,b=abs(q.numerator),q.denominator
    v=0
    while a%p==0:a//=p;v+=1
    while b%p==0:b//=p;v-=1
    return v


def sc(q):
    q=Q(q);assert q
    n=q.numerator*q.denominator
    ans=-1 if n<0 else 1
    for p,e in factorint(abs(n)).items():
        if e%2:ans*=int(p)
    return ans


def add(P,R,a2,a4):
    if P is None:return R
    if R is None:return P
    x,y=P;u,v=R
    if x==u and y==-v:return None
    m=(3*x*x+2*a2*x+a4)/(2*y) if P==R else (v-y)/(u-x)
    z=m*m-a2-x-u
    return z,-y+m*(x-z)


def mul(P,n,a2,a4):
    R=None
    while n:
        if n&1:R=add(R,P,a2,a4)
        P=add(P,P,a2,a4);n//=2
    return R


def on(P,a2,a4):
    return P is None or P[1]**2==P[0]**3+a2*P[0]**2+a4*P[0]


# The raw scalar has two exact square identities.
t,m=symbols('t m')
L=t*t-14*t+77;F=t*(t-7)*(t-11)
assert expand((t*t-77)**2-L**2-28*F)==0
assert expand(49*(t*t-22*t+77)**2-49*L**2+784*F)==0
# Rational parametrization of q^2+15=241 c^2.
qn=-1-241*m*m+482*m
cn=1+241*m*m-2*m
qd=4*(1-241*m*m)
assert expand(qn*qn+15*qd*qd-241*cn*cn)==0

# Scalar-curve point and elementary non-torsion certificate.
a2,a4=-1890,848925
P=(Q(5145,4),Q(77175,8))
assert on(P,a2,a4)
reductions=[]
for p in [13,17]:
    assert len({0,735%p,1155%p})==3
    count=1+sum((b*b-(a**3+a2*a*a+a4*a))%p==0
                for a in range(p) for b in range(p))
    PP=(5145*pow(4,-1,p)%p,77175*pow(8,-1,p)%p)
    def addp(A,B):
        if A is None:return B
        if B is None:return A
        x,y=A;u,v=B
        if x==u and (y+v)%p==0:return None
        slope=((3*x*x+2*a2*x+a4)*pow(2*y,-1,p))%p if A==B else ((v-y)*pow(u-x,-1,p))%p
        z=(slope*slope-a2-x-u)%p
        return z,(-y+slope*(x-z))%p
    RR=None;order=None
    for n in range(1,count+1):
        RR=addp(RR,PP)
        if RR is None:order=n;break
    reductions.append({'prime':p,'curve_order':count,'point_order':order})
assert reductions==[{'prime':13,'curve_order':12,'point_order':6},
                    {'prime':17,'curve_order':16,'point_order':8}]
# The exact duplication identity used in the universal valuation argument.
x,A,B=symbols('x A B')
# Eliminating y^2=x(x^2+A*x+B) from the tangent formula.
assert expand((3*x*x+2*A*x+B)**2
              -4*x*(x*x+A*x+B)*(A+2*x)-(x*x-B)**2)==0
valuation_fixtures=[]
for k in range(1,6):
    PP=mul(P,2**(k-1),a2,a4)
    xx,yy=PP;tt=xx/105;LL=tt*tt-14*tt+77;rr=2*yy/(1575*LL)
    assert (val(tt,2),val(rr,2))==(-2*k,k+1)
    valuation_fixtures.append({'k':k,'v2_t':-2*k,'v2_r':k+1})

# Target curve: rank upper/lower bounds and full mod-two Kummer image.
N=3615
EE=pari.ellinit([0,0,0,-N*N,0])
EE2=pari.ellinit([0,0,0,4*N*N,0])
rankdata=[pari.ellrank(E) for E in [EE,EE2]]
assert all(int(v[0])==int(v[1])==1 for v in rankdata)
torsion=pari.elltors(EE)
assert int(torsion[0])==4 and list(map(int,torsion[1]))==[2,2]
R=(Q(-441),Q(75348))
Ts=[None,(Q(0),Q(0)),(Q(N),Q(0)),(Q(-N),Q(0))]
assert on(R,0,-N*N)
points=Ts+[add(R,T,0,-N*N) for T in Ts]
def delta(P0):
    if P0 is None:return (1,1)
    x,y=P0
    return (sc(x) if x else -1,sc(x-N) if x!=N else 2)
classes=[delta(P0) for P0 in points]
assert all(on(P0,0,-N*N) for P0 in points)
assert len(set(classes))==8
assert set(a for a,b in classes)=={1,-1,N,-N}
assert 15 not in set(a for a,b in classes)
assert delta(R)==(-1,-6)
for T0,RT in zip(Ts,points[4:]):
    dT=delta(T0)
    assert delta(RT)==tuple(sc(Q(a*b)) for a,b in zip(delta(R),dT))

# An exact prepared k=2 fixture without printing its large elliptic coordinates.
Q18=mul(P,18,a2,a4);xx,yy=Q18
t0=xx/105;L0=t0*t0-14*t0+77
r0=2*yy/(1575*L0)
d0=28*t0*(t0-7)*(t0-11)/(L0*L0)
q0=Q(-52729,6548);c0=Q(3769,6548)
assert q0*q0+15==241*c0*c0
assert q0==Q(qn.subs(m,Q(-2,51)),qd.subs(m,Q(-2,51)))
assert c0==Q(cn.subs(m,Q(-2,51)),qd.subs(m,Q(-2,51)))
V0=q0*r0;e0=4*d0/(V0*V0);H0=V0*V0+d0
assert d0==15*r0*r0 and t0>11
assert 0<d0<1 and 0<V0<2 and 0<e0<1
assert 1+d0==((t0*t0-77)/L0)**2
assert d0*H0==N*(r0*r0*c0)**2
assert (val(t0,2),val(r0,2),val(d0,2),val(q0,2),val(V0,2),val(e0,2))==(-4,3,6,-2,1,6)
from math import isqrt
assert isqrt(d0.denominator)**2==d0.denominator
assert isqrt(e0.denominator)**2==e0.denominator
assert d0/15==r0*r0 and e0/15==(2/q0)**2
fixture={name:str(value) for name,value in [('x',xx),('y',yy),('t',t0),('r',r0),('d',d0),('q',q0),('c',c0),('V',V0),('e',e0),('H',H0)]}
fixture_bytes=(json.dumps(fixture,sort_keys=True,separators=(',',':'))+'\n').encode()

# The universal curve map after removing the rational square in the level.
r,c,s,Y=symbols('r c s Y',nonzero=True)
d=15*r*r;H=241*r*r*c*c
X=15*s*s/(r*r*c*c);YY=15*s*Y/(r**4*c**3)
assert expand(together(YY**2-X**3+N*N*X
 -225*s*s/(r**8*c**6)*(Y*Y-d*(s**4-H*H))))==0

print(json.dumps({
 'status':'PASS','schema':'deep-new-scalar-obstruction-v1',
 'symbolic_scalar_conic_duplication_and_curve_map_identities':True,
 'scalar_point_reductions':reductions,'valuation_fixtures':valuation_fixtures,
 'target_level':N,'target_rank_bounds':[[int(z[0]),int(z[1])] for z in rankdata],
 'target_torsion_order':4,'target_torsion_invariants':[2,2],
 'kummer_classes':[list(z) for z in classes],
 'complete_abscissa_classes':[-N,-1,1,N],
 'excluded_abscissa_class':15,
 'prepared_fixture':{'scalar_point_multiple':18,'conic_parameter':'-2/51',
    'q':str(q0),'c':str(c0),'e':str(e0),
    'two_adic_valuations':{'t':-4,'r':3,'d':6,'q':-2,'V':1,'e':6},
    'full_exact_fixture_sha256':sha256(fixture_bytes).hexdigest(),
    'full_exact_fixture_canonical_json_bytes':len(fixture_bytes)},
 'family_k_minimum':2,
 'actual_detector_trace_realization_claimed':False,
 'limitations':['Both rank intervals use PARI algebraic descent, not independent algorithms.',
                'The universal real and 2-adic approximation arguments are proved in the note.',
                'No actual detector tuple and no smaller defining-variable count is established.']
},indent=2))
