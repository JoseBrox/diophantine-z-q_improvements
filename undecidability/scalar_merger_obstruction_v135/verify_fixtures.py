#!/usr/bin/env python3
"""Independent exact arithmetic checks; no external dependencies."""
def P(x):
    b=51*x*x+2504
    return b*(b-1)*(b-2401)*(32*b+343)
p=43
assert P(3)%(p*p)==1677
assert 1677==39*p
for N in range(1,43):
    good=[]
    for x in (0,1):
        r=P(x)%p
        den=(1+149**2*r)%p
        if not (r and den): continue
        R=149*pow(149,2*N,p)*r*pow(den,-1,p)%p
        if R and (R+9792)%p: good.append(x)
    assert good, N
b,s,L=2,1,5**60
T=b**5-1
A=(b**9+8*b**5+b-8)//2+5*T*s
m=2*b*A-b*b-1
C,D=2*A,2*A*A-1
q=D-(A-b)*C
assert (A,m,C,D,q)==(536,2139,1072,574591,2143)
assert D*D-(A*A-1)*C*C==1
assert q>b**5 and (C-L)%(A-1)!=0
assert (q**4-1)%T==7
assert L%5==0 and (33**4-1)%T==15
print("43-adic scalar fixture and short-power index-two fixture verified")
