#!/usr/bin/env python3
"""Exact checks for ico coefficient elimination, local S-unit necessity and budgets."""
from fractions import Fraction as Q
from itertools import combinations, product
from math import gcd, lcm, prod


def chart(w, t):
    a = [(t-1)*(w*t+w-1), -(w-1)*((w+1)*t-1),
         -w*(t*t+w-1), -(t-w)*(t+w-1)]
    A = -t*(t+w*w-1)
    assert sum(a) == A
    if not A*prod(a)*(a[0]+a[2]):
        return None
    z = [-A*prod(a[j] for j in range(4) if j != i) for i in range(4)] + [prod(a)]
    den = lcm(*(Q(x).denominator for x in z))
    zz = [int(den*x) for x in z]
    g = gcd(*zz)
    return tuple(x//g for x in zz)


def egcd(a,b):
    r0,r1=a,b; s0,s1=1,0; t0,t1=0,1
    while r1:
        k,r=divmod(r0,r1)
        r0,r1=r1,r; s0,s1=s1,s0-k*s1; t0,t1=t1,t0-k*t1
    sign=1 if r0>0 else -1
    return sign*r0,sign*s0,sign*t0


def strip(n,d):
    while (g:=gcd(n,d))>1:
        n//=g
    return n


def Rproxy(w):
    w=Q(w)
    return abs(w.numerator*w.denominator*(w.numerator-w.denominator))


def Bproxy(z):
    return gcd(*(a*b for a,b in combinations(z,2)))


vals=sorted({Q(a,b) for a in range(-6,9) for b in range(1,6)}-{Q(0),Q(1)})
count=0
for w,t in product(vals,repeat=2):
    z=chart(w,t)
    if z is None: continue
    assert gcd(*z)==1
    assert sum(prod(v) for v in combinations(z,2))==0
    assert sum(prod(v) for v in combinations(z,4))==0
    A=sum(prod(v) for v in combinations(z,3))**5
    C=prod(z)**3; D=sum(z)**15
    assert C
    G,u,v=egcd(A,C)
    assert G>0 and gcd(G,D)==1 and u*A+v*C==G
    a=Q(-u*D,G); b=Q(-v*D,G)
    assert b==-(D+a*A)/C
    den=lcm(a.denominator,b.denominator)
    assert den==G
    assert den<=max(abs(a.numerator),a.denominator)*max(abs(b.numerator),b.denominator)
    B=Bproxy(z)
    assert B>0 and strip(B,G)==strip(G,B)==1
    zs=chart(t,w)
    assert zs is not None and Bproxy(zs)==B
    rw,rt=Rproxy(w),Rproxy(t)
    assert strip(rt,B*rw)==strip(rw,B*rt)==1
    count+=1


def vp(x,p):
    x=Q(x)
    if x==0: return float('inf')
    a,b=abs(x.numerator),x.denominator; v=0
    while a%p==0: a//=p;v+=1
    while b%p==0: b//=p;v-=1
    return v


local=0
for p in (3,5,7,11,13,17,19,23,29,31,37,41):
    for r in range(2,p):
        w=Q(r)
        for k in (1,2,4):
            for c in range(1,p):
                for t in (Q(c,p**k),Q(c*p**k),1+Q(c*p**k)):
                    z=chart(w,t)
                    if z is None: continue
                    assert vp(w,p)==vp(1-w,p)==0
                    assert sum(x%p!=0 for x in z)==1
                    local+=1


def f(t): return prod(t-i for i in range(1,11))
def phi(w): return w/(1+w)**2
f100=f(100)
anchor=0
for xs in product((Q(0),Q(1),Q(-1,2),Q(2,3),Q(-4,5)),repeat=3):
    s=Q(1); odd=set()
    for x in xs:
        w=s*x*x; t=100+phi(w); ss=s*f(t)/f100
        assert 100<=t<=Q(401,4)
        assert 1<=ss/s<2
        for p in (101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199):
            assert f100%p
            if p in odd: assert vp(ss,p)==vp(s,p) and vp(ss,p)%2
            if (n:=vp(f(t),p))>0 and n%2:
                odd.add(p)
                assert vp(ss,p)%2
        s=ss
    u=phi(s)
    assert 4<=1/u<=11
    for p in odd: assert vp(u,p)>0 and vp(u,p)%2
    anchor+=1
assert Q(40*3)+Q(3,4)+Q(5*3*2,2)==Q(543,4)
assert Q(543,4)/(Q(299,50)*16000)==Q(543,382720)<Q(1,100)
assert Q(9,10)*3-Q(1,100)==Q(269,100)>Q(3,25)
# Thomae determinant products: every point appears twice, six determinants.
partitions=0
for I in combinations(range(6),3):
    J=tuple(i for i in range(6) if i not in I)
    if I>J: continue
    edges=list(combinations(I,2))+list(combinations(J,2))
    assert len(edges)==6
    assert [sum(i in e for e in edges) for i in range(6)]==[2]*6
    partitions+=1
assert partitions==10
print(f'PASS: {count} rational interpolation and symmetry fixtures; {local} local contact fixtures; {anchor} three-argument anchor fixtures; exact height margins and {partitions} Thomae multidegrees.')
