#!/usr/bin/env python3
"""Finite arithmetic checks for duplication mass and sharp quotient precision.
The conjectural height inputs and geometric theorem are not computational claims.
"""
from fractions import Fraction as Q
from itertools import product
from math import gcd

# Exact Belyi parameter/contact exponents, surplus inequalities.
assert Q(147,242)-Q(4,7)==Q(61,1694)>Q(1,30)
assert Q(2,1)/Q(8,5)-1==Q(1,4)
assert Q(3,1)/Q(3,2)-2==0
profiles=0
for k in range(1,7):
    for es in product(range(5), repeat=k):
        rad=sum(e>0 for e in es)
        simple=sum(e==1 for e in es)
        full=sum(es)
        surplus=full-rad
        assert simple>=2*rad-full
        if max(es)>=2: assert full<=(k+1)*surplus
        profiles+=1
# Weak abc family: explicit fixed d,K0 with positive margin.
for kappa in (Q(7,5),Q(3,2),Q(8,5),Q(19,10),Q(199,100),Q(1999,1000)):
    sigma=2/kappa-1
    d=2//sigma+1
    gamma=d*sigma-2
    assert gamma>0
    K=4*(d+1)//(sigma*gamma)+1
    delta=sigma-Q(2*(d+1),K)/gamma
    assert delta>sigma/2
    assert -2*(4*K+1)+8*(K-1)<0
    # gcd bound uses only positive mass; no primitive divisor assumption
    assert 2*(d+1)/(K*gamma) < sigma
    print('weak exponent',kappa,'d',d,'depth',K,'positive mass',delta)
# Exact local Boolean and discrepancy valuations for finite valuation profiles.
checks=0
for N in range(1,13):
    for a in range(1,100,2):
        # v(T)>3a/2 iff v(F)>9a/4.
        # At negative odd L no cancellation is possible in its defining sum.
        for vF in range(-a,5*a+3):
            assert 2*vF != 3*a
            vT=2*vF-min(3*a,2*vF)
            assert (2*vT>3*a)==(4*vF>9*a)
            checks+=1
        k=((4*N+9)*a)//4+1
        assert k <= (N+3)*a
        assert (N+4)*a > Q(4*N+9,4)*a
        if a==1: assert k==N+3
        # If either comparison point has equal/greater formal depth, both
        # chi errors have depth >=2a, so the above criterion is exact.
        for e in range(a,a+4):
            assert -6*a+8*e>=2*a>Q(3*a,2)
# Fixed scaling constants and original uniform mass margin.
assert Q(1,1)-Q(10,299)>Q(96,100)
assert Q(1,1196)<Q(1,1000)
for N in range(1,50):
    assert (N+3)*(1-Q(10,299))-Q(1,1196)>Q(N+2,2)-Q(1,1196)
# Local two-pole weight: at a split prime with one simple and one deeper slot,
# norm/trace y has valuation exactly -3, for every other depth.
for b in range(2,101):
    assert (-3-3*b)-min(-3,-3*b)==-3
    for vF in range(-30,31):
        assert (2*vF>3)==(vF>=2)
for n in range(1,30):
    for j in range(1,40):
        g=gcd(n,j)
        if g<n: assert g<=n//2
print('PASS',profiles,'denominator profiles;',checks,'sharp local precision profiles; weak mass, gcd, and two-pole margins')
