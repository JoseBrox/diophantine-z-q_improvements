#!/usr/bin/env python3
"""Exact rational smoke tests for the monic and selected-character lemmas."""
from fractions import Fraction as F
from math import comb

def rank(a):
    a=[list(map(F,row)) for row in a]
    h=0
    for j in range(len(a[0])):
        k=next((k for k in range(h,len(a)) if a[k][j]),None)
        if k is None: continue
        a[h],a[k]=a[k],a[h]
        v=a[h][j]
        a[h]=[x/v for x in a[h]]
        for k in range(h+1,len(a)):
            v=a[k][j]
            a[k]=[x-v*y for x,y in zip(a[k],a[h])]
        h+=1
        if h==len(a): break
    return h

tests=0
for coeff in ((1,2,3),(0,-2,1),(3,-6,3),(-4,0,0,2),(0,0,0,7),(0,1)):
    j=len(coeff)-1
    a=coeff[-1]
    for w in (F(0),F(-2),F(3,5),F(7,3)):
        W=a*w
        transformed=W**j+sum(coeff[i]*a**(j-1-i)*W**i for i in range(j))
        assert transformed==a**(j-1)*sum(c*w**i for i,c in enumerate(coeff))
        tests+=1

# Geometric values, multiplicities, including a dummy zero eigenvalue.
# Distinct guarded vectors and duplicate copies from nonreduced factors.
for vectors in (
    [(2,3),(2,3),(1,-1),(0,0)],
    [(1,1,-1),(1,-1,1),(2,-2,0),(0,0,0)],
    [(1,0),(1,0),(1,-1),(0,0),(0,0)],
    [(0,0),(0,0)],
    [(1,0),(2,0),(-1,1)],
):
    m=len(vectors[0])-1
    r=len(vectors)
    target=len(set(vectors)-{(0,)*(m+1)})+1
    maxima=0
    for h in range(1,m*comb(r+1,2)+2):
        ev=[0]+[sum(c*h**i for i,c in enumerate(v)) for v in vectors]
        # 0^0=1 matches trace of identity.
        H=[[sum(e**(i+j) for e in ev) for j in range(r+1)] for i in range(r+1)]
        rr=rank(H)
        assert rr==len(set(ev))
        maxima=max(maxima,rr)
        tests+=1
    assert maxima==target

assert 7*11+2==79
for d in range(1,100):
    N=3*d+8
    assert N-1+2*N+2+4*N+1==7*N+2==21*d+58
assert 21*2+58==100
print("PASS:",tests,"exact monic/Hankel checks; census 79 / 100.")
