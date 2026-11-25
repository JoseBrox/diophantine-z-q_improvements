#!/usr/bin/env python3
"""Exact rational checks for the mixed-shift shared-pole construction."""
from fractions import Fraction as Q
from math import gcd, isqrt

def val(x,p):
    x=Q(x)
    assert x != 0
    n,d=abs(x.numerator),x.denominator
    v=0
    while n%p==0:
        n//=p; v+=1
    while d%p==0:
        d//=p; v-=1
    return v

def point(N,x,y):
    assert y*y == x*(x-N)*(x+N)
    assert y!=0

def square(x):
    x=Q(x)
    return x>0 and isqrt(x.numerator)**2==x.numerator and isqrt(x.denominator)**2==x.denominator

def factors(n):
    f=[]
    p=2
    while p*p<=n:
        while n%p==0:
            f.append(p);n//=p
        p+=1
    if n>1:f.append(n)
    return f

def legendre(a,p):
    assert a%p
    z=pow(a%p,(p-1)//2,p)
    assert z in (1,p-1)
    return 1 if z==1 else -1

def conic_test(j1,j2):
    assert j1%8==j2%8==7
    primes=set(factors(j1*j2))
    for p in primes:
        a,b=j1%p==0,j2%p==0
        if a and b: z=legendre((j1//p)*(j2//p),p)
        elif a: z=legendre(-j2,p)
        else: z=legendre(j1,p)
        if z==-1:return False
    return True

e1,e2=Q(11200,4695889),Q(1984,199809)
j1,j2=7,31
k1,k2=520521,7913
for e,j,k in [(e1,j1,k1),(e2,j2,k2)]:
    assert 0<e<1 and isqrt(e.denominator)**2==e.denominator
    assert val(e,2)==6 and j%8==7
    assert square(e/j) and square((1-e)/k)
    assert not square(k) and len(factors(k))==len(set(factors(k)))
assert j1!=j2 and conic_test(j1,j2)
assert not conic_test(7,23)
for e in (Q(112,101**2),Q(368,101**2)):
    assert 0<e<1 and val(e,2)==4 and isqrt(e.denominator)**2==e.denominator
N=41881
P0=(Q(260743),Q(131414472))
P1=(Q(5887,9),Q(164836,27))
P2=(Q(2553439,225),Q(2533011488,3375))
point(N,*P0)
point(609,*P1)
point(8897,*P2)
assert square(P0[0]/e1) and square((P0[0]-N)/(2*N*e2))
assert square(N*(1-e1)/609) and square(N*(1-e2)/8897)
assert square(P1[0]/e1) and square((P2[0]-8897)/(2*8897*e2))

r,a,b,s=Q(4023,248),Q(899,2167),Q(149,40),Q(8960,968649)
t=1+2*e2*r*r
D=e1/t
assert D==Q(347200,906306577)
assert s*s==e1*e2*(1+e2*r*r)
point(D,e1,2*e1*r*s/t)
D1,D2=D*(1-e1),D*(1-e2)
x1=e1*a*a
x2=D2*(1+2*e2*b*b)
Y1=Q(314280273664000,103550802255048880369)
Y2=Q(162112735232000,24539350711564713123)
point(D1,x1,Y1)
point(D2,x2,Y2)
assert x2-D2==2*D2*e2*b*b
print("Exact mixed-shift fixture, dyadic classes, and norm-obstruction checks passed.")
