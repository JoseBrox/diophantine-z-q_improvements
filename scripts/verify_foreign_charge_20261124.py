#!/usr/bin/env python3
"""Exact local and rational-elliptic fixtures for the foreign charge notes.
The finite checks do not prove the retained abc or BB inputs.
"""
from fractions import Fraction as Q
from math import isqrt
from itertools import product

INF=float('inf')
def vp(x,p):
    x=Q(x)
    if not x:return INF
    a,b=abs(x.numerator),x.denominator;v=0
    while a%p==0:a//=p;v+=1
    while b%p==0:b//=p;v-=1
    return v

def add(A,B):
    if A is None:return B
    if B is None:return A
    x,y=A;u,v=B
    if x==u:
        if y==-v:return None
        w=(3*x*x-2)/(2*y)
    else:w=(v-y)/(u-x)
    xx=w*w-x-u
    return xx,w*(x-xx)-y

def mul(n,A):
    if n<0:return mul(-n,(A[0],-A[1]))
    B=None
    while n:
        if n&1:B=add(B,A)
        n//=2
        if n:A=add(A,A)
    return B

def g(A):
    x,y=A
    return (x*x+2)/(2*y)
R0=(Q(2),Q(2)); P=mul(2,R0)
assert P==(Q(9,4),Q(-21,8))
points={n:mul(n,P) for n in range(1,17)}
roots={n:g(mul(n,R0)) for n in points}
assert all(roots[n]**2==A[0] for n,A in points.items())

# BB charge: at odd foreign depth a, v(T)>3a/2 iff v(s)>9a/4.
profiles=0
for a in range(1,100,2):
    for vx,vs in product(range(0,12,2),range(-20,5*a+2)):
        assert -6*a-4*vx<0
        assert 3*a!=2*vs
        vT=2*vs-min(3*a,2*vs)
        assert (2*vT>3*a)==(4*vs>9*a)
        assert (9*a)//4+1<=3*a
        profiles+=1
# At odd common depth a outside m, no additional s condition.
for a in range(1,100,2):
    assert -6*a+8*a==2*a and -3*a+4*a==a
# At 2, a deep H and dyadic denominator of s suffice even if m is even.
for k in range(0,30):
    for a in range(15*k+3,15*k+15):
        assert 2*a-6*k>0
        assert -3*(a+k)+2*(2*a-6*k)==a-15*k>=3

# Conic exact rational tests and local necessary inequalities.
conic_profiles=0
for a,b,vs in product(range(1,40,2),range(0,20),range(-20,60)):
    vL=-a-2*b
    assert vL%2 and vL+2*vs!=0
    assert (vL+2*vs>0)==(2*vs>a+2*b)
    conic_profiles+=1
# Divisor degree census: [m] preimages of 2-torsion and zeros of f.
# Work with the abstract torsion grid (Z/(4|m|))^2 and a chosen T=(1/2,0).
for m in range(1,25):
    d=4*m
    def two(A):return ((2*A[0])%d,(2*A[1])%d)
    def mult(A):return ((m*A[0])%d,(m*A[1])%d)
    O=(0,0); TT=(d//2,0)
    def ord_f(A):
        if two(A)==O:return -1
        if two(A)==TT:return 1
        return 0
    Ldegree=Rdegree=0
    for A in product(range(d),repeat=2):
        of=ord_f(A); om=ord_f(mult(A))
        Ldegree+=max(0,2*of-om)
        Rdegree+=max(0,of-om)
    assert Ldegree==4*m*m+(4 if m%2==0 else 0)
    assert Rdegree==4*m*m-(4 if m%2 else 0)

ps=(3,5,11,13,17,19,23,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97)
def scalar(H,U,s):
    L=U[1]; Z=L*L/H[0]**4
    chi=1/(1+Z); T=L*s*s/(1+L*s*s)
    return 1+L*((1-chi)*T)**2
bb_fixtures=conic_fixtures=depth_fixtures=0
for h,j in product(range(1,7),range(1,17)):
    H,U=points[h],points[j]
    L=roots[j]/roots[h]**2
    t=Q(1) if L!=1 else Q(2)
    s=2*t/(1-L*t*t); r=(1+L*t*t)/(1-L*t*t)
    assert s and r*r==1+L*s*s
    R=roots[j]/roots[h]; c,d=3*R/5,4*R/5
    assert c and d and c*c+d*d==R*R
    for p in ps:
        if vp(H[0],p)<0 or vp(U[0],p)>=0:continue
        a=-vp(roots[j],p);b=vp(roots[h],p)
        assert a>0 and b>=0
        assert min(vp(c,p),vp(d,p))<=-a-b
        depth_fixtures+=1
        if a%2:
            assert 2*vp(s,p)>a+2*b
            conic_fixtures+=1
        if a==1:
            for e in range(0,5):
                bb=scalar(H,U,Q(p)**e)
                assert (vp(bb,p)<0)==(e<3)
                if e<3:assert vp(bb,p)%2
                else:assert vp(bb,p)==0
                bb_fixtures+=1
# Construct complete square-denominator BB arguments on exact arbitrary tuples.
# Choose s divisible by the cube of B_U and by enough fixed prime powers,
# then shrink its real value using a denominator supported at a new prime.
preparations=0
for h,j in [(1,2),(2,3),(3,7),(4,8),(5,9),(6,11),(4,12),(8,8)]:
    H,U=points[h],points[j]
    A=roots[j].denominator**3*(2*7*29)**40
    p=next(p for p in (5,11,13,17,19,23,31,37,41,43,47,53,59,61,67) if A%p)
    D=1
    while D<=A*100*(1+abs(U[1])):D*=p
    ss=Q(A,D); b=scalar(H,U,ss); e=Q(112,841)*b
    assert 0<e<1
    assert isqrt(e.denominator)**2==e.denominator
    assert vp(e,2)==4
    odd=e/16
    assert odd.numerator*pow(odd.denominator,-1,8)%8==7
    preparations+=1
print('PASS:',profiles,'BB profiles;',conic_profiles,'conic profiles;',bb_fixtures,'exact BB local fixtures;',conic_fixtures,'odd-depth and',depth_fixtures,'all-depth conic fixtures;',preparations,'complete prepared scalar fixtures; torsion degree census.')
