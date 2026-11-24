#!/usr/bin/env python3
"""Exact checks for the modular-contact auxiliary carrier."""
from fractions import Fraction as Q
from itertools import combinations
from math import gcd
import sympy as s

x,t=s.symbols('x t')
f=2*(1-x)*(1-2401*x)*(32+343*x)
A=s.Poly(f,x).LC()
assert A==1647086==49*33614==343*4802
G=(x-33614)*(x-14)*(x+3136)
assert s.expand(4802**2*f.subs(x,Q(49,int(A))*x)-G)==0
assert s.expand(G)==x**3-30492*x**2-104986812*x+1475789056
assert G.subs(x,0)==38416**2
assert set(s.factorint(int(s.discriminant(G,x))))=={2,3,5,7}
slope=Q(-104986812,2*38416)
xx=slope*slope+30492; yy=-38416-slope*xx
assert xx==Q(5951086353,3136) and yy==Q(455376332353657,175616)
assert G.subs(x,xx)==yy*yy
assert xx.numerator%2 and xx.denominator%64==0 and xx.denominator%128!=0
pts=[None,Q(0),Q(1),Q(2401),Q(-343,32)]
def det(a,b):
    x,y=(1,0) if a is None else (a,1)
    u,v=(1,0) if b is None else (b,1)
    return x*v-u*y
expected=[Q(191342053882402567201,129708022500),Q(2179252305146449,66177562500),Q(128031684631201,9922500),Q(1169975873419524361,108425318400),Q(1439069689,44100)]
for i,(a,b,c,d) in enumerate(combinations(pts,4)):
    lam=det(a,c)*det(b,d)/(det(a,d)*det(b,c))
    j=256*(1-lam+lam*lam)**3/(lam*lam*(1-lam)**2)
    assert j==expected[i] and j.denominator>1
c,b=1,0
fixtures=0
for k in range(1,25):
    c,b=3*c+4*b,2*c+3*b
    assert c*c-2*b*b==1 and gcd(c-1,c+1)==2
    for n in (c-1,c+1):
        while n%2==0:n//=2
        assert s.integer_nthroot(n,2)[1]
        fixtures+=1
for p in list(s.primerange(76177,76320)):
    count=1+sum(1 if (y:=(x-33614)*(x-14)*(x+3136)%p)==0 else 2 if pow(y,(p-1)//2,p)==1 else 0 for x in range(p))
    assert count%4==0 and count%p!=0
print('PASS: exact auxiliary model, doubled point, five j-invariants,',fixtures,'Pell odd-part fixtures and reduction-order checks.')
