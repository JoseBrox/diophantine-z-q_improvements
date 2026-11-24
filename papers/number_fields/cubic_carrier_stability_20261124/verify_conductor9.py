#!/usr/bin/env python3
"""Complete integer/rational rank-upper-bound certificate over Q(sqrt2,zeta9+zeta9^-1)."""
from itertools import product
from fractions import Fraction as Q
from math import factorial

zero=(0,0,0); one=(1,0,0); z=(0,1,0)
def cmul(a,b):
    a0,a1,a2=a;b0,b1,b2=b
    w=a1*b2+a2*b1;t=a2*b2
    return (a0*b0-w,a0*b1+a1*b0+3*w-t,a0*b2+a1*b1+a2*b0+3*t)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(k,a):return tuple(k*x for x in a)
def mul(a,b):
    x,y=a[:3],a[3:];u,v=b[:3],b[3:]
    return add(cmul(x,u),scale(2,cmul(y,v)))+add(cmul(x,v),cmul(y,u))
def cnorm(a):
    A,B,C=cmul(a,one),cmul(a,z),cmul(a,(0,0,1))
    return A[0]*(B[1]*C[2]-B[2]*C[1])-B[0]*(A[1]*C[2]-A[2]*C[1])+C[0]*(A[1]*B[2]-A[2]*B[1])
def norm(a):return cnorm(add(cmul(a[:3],a[:3]),scale(-2,cmul(a[3:],a[3:]))))
O=one+zero; pi=zero+one; d=(3,0,0,-1,0,0); B=mul(d,d)
# Exact interval arithmetic certifies signatures in all six embeddings.
def ia(x,y):return x[0]+y[0],x[1]+y[1]
def im(x,y):
    v=[a*b for a in x for b in y];return min(v),max(v)
def f(x):return x**3-3*x+1
roots=[(Q(-18794,10000),Q(-18793,10000)),(Q(3472,10000),Q(3473,10000)),(Q(15320,10000),Q(15321,10000))]
assert all(f(a)*f(b)<0 for a,b in roots)
r2=(Q(1414,1000),Q(1415,1000));assert r2[0]**2<2<r2[1]**2
def sig(a):
    mask=0
    for j,(r,t) in enumerate(product(roots,[(-r2[1],-r2[0]),r2])):
        acc=(Q(0),Q(0))
        for i in (2,1,0):
            acc=ia(im(acc,r),ia((a[i],a[i]),im((a[i+3],a[i+3]),t)))
        assert acc[0]>0 or acc[1]<0,(a,j,acc)
        if acc[1]<0:mask|=1<<j
    return mask
units=[(-1,-1,-1,0,-1,0),(-1,-1,-1,0,1,0),(-1,-1,0,-1,0,0),(-1,-1,0,-1,1,1),(-1,-1,0,1,-1,-1),(-1,-1,0,1,0,0)]
g=d
assert all(abs(norm(u))==1 for u in units)
ms=[sig(u) for u in units];assert ms==[61,62,58,29,46,53]
S={0}
for u in ms:S|={v^u for v in S}
assert len(S)==64
# Field/class group certificate. Discriminants 8 and 81 are coprime.
assert factorial(6)**2*8**3*81**2 < 29**2*6**12
assert abs(norm(pi))==8 and abs(norm((1,1,0,0,0,0)))==9
assert norm((-1,-1,-1,-1,0,-1))==17
assert all(f(r)%2 for r in range(2))
assert [(p,all(r*r%p!=2 for r in range(p)),all(f(r)%p for r in range(p))) for p in (5,7,11,13,17,19,23)]==[(5,True,True),(7,False,True),(11,True,True),(13,True,True),(17,False,False),(19,True,False),(23,False,True)]
assert all(f(r)%3==(r+1)**3%3 for r in range(3))
assert sum(f(r)%17==0 for r in range(17))==3
assert norm(d)==7**3
def div(a,b):
    cols=[mul(tuple(int(i==j) for i in range(6)),b) for j in range(6)]
    M=[[Q(cols[j][i]) for j in range(6)]+[Q(a[i])] for i in range(6)]
    for j in range(6):
        i=next(i for i in range(j,6) if M[i][j]);M[i],M[j]=M[j],M[i]
        u=M[j][j];M[j]=[v/u for v in M[j]]
        for i in range(6):
            if i!=j:
                u=M[i][j];M[i]=[x-u*y for x,y in zip(M[i],M[j])]
    a=tuple(row[-1] for row in M);assert all(x.denominator==1 for x in a)
    return tuple(map(int,a))
def red(a,m):return tuple(t%m for t in a)
# Every square modulo 8 depends only on the argument modulo 4;
# every fourth power modulo 8 depends only on the argument modulo 2.
squares={red(mul(t,t),8) for t in product(range(4),repeat=6)}
fourths={red(mul(q,q),8) for t in product(range(2),repeat=6) for q in [mul(t,t)]}
assert (len(squares),len(fourths))==(1856,64)
def dyadic(a,b):
    return any(red(add(a,mul(b,t)),8) in squares or red(add(b,mul(a,t)),8) in squares for t in fourths)
for dual in (False,True):
    coef=scale(4 if dual else -1,B)
    G=units+[g]+([pi] if dual else [])
    cand=[]
    for bits in product((0,1),repeat=len(G)):
        b=O
        for u,bit in zip(G,bits):
            if bit:b=mul(b,u)
        if dual:
            mask=0
            for u,bit in zip(ms,bits):
                if bit:mask^=u
            if bits[-1]:mask^=21 # sqrt2 negative in embeddings 0,2,4
            if bits[6] or mask:continue # dual square at g, total positivity
            val=tuple((b[i]+3*b[i+3])%7 for i in range(3))
            power=one
            for _ in range(171):power=red(cmul(power,val),7)
            if power!=one:continue
        c=div(coef,b);assert mul(b,c)==coef
        if dyadic(b,c):cand.append(bits)
    if dual:assert cand==[(0,)*8]
    else:assert cand==[(0,0,0,0,0,0,0),(0,0,0,0,0,0,1),(0,1,1,0,1,0,0),(0,1,1,0,1,0,1),(1,0,0,1,0,1,0),(1,0,0,1,0,1,1),(1,1,1,1,1,1,0),(1,1,1,1,1,1,1)]
    print('dual' if dual else 'original','upper image size',len(cand),'bit vectors',cand)
print('PASS: rank upper bound 1 over the cubic compositum')
