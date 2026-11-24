#!/usr/bin/env python3
"""Exact verification of ico interpolation and local boundary redirection."""
from fractions import Fraction as Q
from itertools import combinations, product
from math import gcd, lcm, prod
import sympy as S

pairs = tuple(combinations(range(5), 2))
triples = tuple(combinations(range(5), 3))
quads = tuple(combinations(range(5), 4))

def elementary(z, I):
    return sum(prod(z[i] for i in ind) for ind in I)

def chart(w,t):
    a = [(t-1)*(w*t+w-1), -(w-1)*((w+1)*t-1),
         -w*(t*t+w-1), -(t-w)*(t+w-1)]
    A = sum(a)
    return a,A

def projective(w,t):
    a,A=chart(w,t)
    if not A*prod(a)*(a[0]+a[2]): return None
    z=[-A*prod(a[j] for j in range(4) if j!=i) for i in range(4)]+[prod(a)]
    den=lcm(*(Q(x).denominator for x in z))
    v=[int(den*x) for x in z]; g=gcd(*v)
    return [x//g for x in v]

w,t=S.symbols('w t'); a,A=chart(w,t); Qw=w*w+w-1
assert S.expand(A+t*(t+w*w-1))==0
assert S.expand(a[0]+a[2]+t+w*w-1)==0
expected=[w*(w-1)**2*Qw,w**3*(w-1)*Qw,w*(w-1)**3*Qw,w**2*(w-1)**2*Qw,
          w**2*(w-1)**2*Qw,w**2*(w-1)**2*Qw,w*(w-1)**2*Qw,
          w**3*(w-1)*Qw,w**3*(w-1)**2*Qw,w**2*(w-1)**2*Qw]
for (x,y),e in zip(combinations(a+[A],2),expected):
    r=S.resultant(x,y,t)
    assert S.expand(r-e)==0 or S.expand(r+e)==0
forms=[(2-w)*(w+1)/w,-(w-1)*(w+2)/w,-(w**3-w*w+4)/w,
       (w*w-2)*(w*w-w+2)/w**2,-2*(w**3-w+2)/w**2]
for x,y in zip(a+[A],forms):assert S.cancel(x.subs(t,2/w)-y)==0

# Check the characteristic-polynomial criterion on complete small projective spaces.
finite=surface=0
for p in (2,3,5,7,11,13,17,19):
    for k in range(5):
        for tail in product(range(p),repeat=4-k):
            z=(0,)*k+(1,)+tail;finite+=1
            if elementary(z,pairs)%p or elementary(z,quads)%p:continue
            surface+=1
            boundary=sum(x!=0 for x in z)==1
            assert ((elementary(z,triples)%p==0 and prod(z)%p==0)==boundary)
            assert sum(x!=0 for x in z) in (1,3,5)

def vp(x,p):
    x=Q(x)
    if x==0:return float('inf')
    a,b=abs(x.numerator),x.denominator;v=0
    while a%p==0:a//=p;v+=1
    while b%p==0:b//=p;v-=1
    return v

def unit(x,p):return vp(x,p)==0

def good_z(z,p):return z is not None and sum(x%p!=0 for x in z)>1

# Local lift in every possible valuation regime, including w near 0 and 1.
local=0
for p in (13,17,19,23,29,31,37,41,43,47):
    for k in (1,2,5):
        for c in range(1,p):
            for wr,tr in [(Q(c,p**k),Q(2*p**k,c)),
                          (Q(c*p**k),Q(2*c*p**k)),
                          (1+Q(c*p**k),1+Q(2*c*p**k))]:
                vals,AA=chart(wr,tr)
                vv=[vp(x,p) for x in vals+[AA]]
                if vp(wr,p)<0: assert vv==[-k,-k,-2*k,-2*k,-k]
                elif vp(wr,p)>0: assert vv==[0,0,k,k,k]
                else: assert vv==[k,k,0,k,0]
                assert good_z(projective(wr,tr),p)
                local+=1
    for residue in range(2,p):
        wr=Q(residue)
        tr=next(Q(i) for i in range(p) if all(unit(x,p) for x in chart(wr,Q(i))[0]+[chart(wr,Q(i))[1]]))
        assert good_z(projective(wr,tr),p)
        local+=1

# Extended Euclid in the two mixed coefficients.
def egcd(a,b):
    r0,r1=a,b; u0,u1=1,0; v0,v1=0,1
    while r1:
        q,r=divmod(r0,r1);r0,r1=r1,r
        u0,u1=u1,u0-q*u1;v0,v1=v1,v0-q*v1
    sign=1 if r0>=0 else -1
    return sign*r0,sign*u0,sign*v0

def check(z):
    assert gcd(*z)==1 and elementary(z,pairs)==elementary(z,quads)==0
    A=elementary(z,triples)**5; C=prod(z)**3; D=sum(z)**15
    G,u,v=egcd(A,C)
    assert G>0 and gcd(G,D)==1
    assert G*D-u*D*A-v*D*C==0
    # Exact prime-support equivalence to the gcd of all mixed quadrics.
    B0=gcd(*(z[i]*z[j] for i,j in pairs))
    assert B0>0
    # Remove all common prime factors iteratively, without integer factorization.
    def strip(n,b):
        while (g:=gcd(n,b))>1:n//=g
        return n
    assert strip(G,B0)==strip(B0,G)==1

checks=0
for wr,tr in product([Q(a,b) for a in range(-4,7) for b in range(1,5)],repeat=2):
    z=projective(wr,tr)
    if z is None:continue
    check(z);checks+=1

# Actual elliptic square-abscissa fixtures; these are not prepared BB witnesses.
def add(P,R):
    if P is None:return R
    if R is None:return P
    x,y=P; a,b=R
    if x==a:
        if y==-b:return None
        l=(3*x*x-2)/(2*y)
    else:l=(b-y)/(a-x)
    X=l*l-x-a;return X,l*(x-X)-y
R0=(Q(2),Q(2));P=None;ell=0
for j in range(1,9):
    P=add(P,R0);x,y=P;g=(x*x+2)/(2*y)
    assert g*g==add(P,P)[0]
    for tr in (Q(2),Q(2)/g,Q(2)*g,Q(2)*g-1):
        z=projective(g,tr)
        if z is None:continue
        check(z);ell+=1
print(f'PASS: {finite} projective finite-field points ({surface} on ico); {local} local lifts; {checks} rational and {ell} elliptic interpolation fixtures; exact resultants.')
