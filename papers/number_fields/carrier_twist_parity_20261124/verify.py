#!/usr/bin/env python3
"""Exact 2-isogeny upper bounds and local ratio for the original carrier.
Only integer arithmetic; no analytic rank, Sha finiteness, or PARI needed.
See README for the mathematical descent and conditional parity implication.
"""
from itertools import product
from math import gcd
from functools import lru_cache
O=(1,0); neg=(-1,0); eps=(1,1); pi=(0,1); d=(3,-1); db=(3,1)
def mul(x,y):
    a,b=x;c,e=y
    return a*c+2*b*e,a*e+b*c
def add(x,y):return x[0]+y[0],x[1]+y[1]
def norm(x):return x[0]**2-2*x[1]**2
def div(x,y):
    t=mul(x,(y[0],-y[1]));n=norm(y)
    if n and t[0]%n==0 and t[1]%n==0:return t[0]//n,t[1]//n
    return None
def red(x,m):return x[0]%m,x[1]%m
def inv(x,m):return red(mul((x[0],-x[1]),(pow(norm(x),-1,m),0)),m)
def sign(x,slot):
    a,b=x;b*=slot
    if a>=0 and b>=0:return 1
    if a<=0 and b<=0:return -1
    return (1 if a>0 else -1) if a*a>2*b*b else (1 if b>0 else -1)
def vu(x,g):
    v=0
    while (q:=div(x,g)) is not None:x=q;v+=1
    return v,x
def squareunit(x,g):
    q=abs(norm(g))
    if g[1]==0: # inert
        p=abs(g[0]);assert q==p*p
        n=(q-1)//2;u=O;v=red(x,p)
        while n:
            if n&1:u=red(mul(u,v),p)
            v=red(mul(v,v),p);n//=2
        return u==O
    p=q;r=-g[0]*pow(g[1],-1,p)%p
    u=(x[0]+r*x[1])%p;assert u
    return pow(u,(p-1)//2,p)==1
def lsquare(x,g):
    v,u=vu(x,g);return v%2==0 and squareunit(u,g)
def odd_filter(b,n,g,dual):
    v,_=vu(n,g);w,_=vu(b,g)
    if v%2==0:return w%2==0
    if abs(norm(g))%4==3:return lsquare(b,g) if dual else True
    return lsquare(b,g) or lsquare(mul(b,n),g)
@lru_cache(None)
def residues(m):
    squares={red(mul(t,t),m) for t in product(range(m),repeat=2)}
    return squares,{red(mul(t,t),m) for t in squares}
def dyadic_mod(b,c,m=32):
    squares,fourths=residues(m)
    return any(red(add(mul(b,t),c),m) in squares or red(add(mul(c,t),b),m) in squares for t in fourths)
# All unit classes over Q_2(sqrt2), from the quotient modulo 8.
units={(a,b) for a,b in product(range(8),repeat=2) if a%2}
unit_squares={red(mul(t,t),8) for t in units}
assert unit_squares=={(1,0),(1,4),(3,2),(3,6)}
reps=[]
while units:
    t=min(units);reps.append(t);units-={red(mul(t,s),8) for s in unit_squares}
assert reps==[(1,0),(1,1),(1,2),(1,3),(3,1),(3,3),(5,0),(5,2)]
for a in (1,5):
    n=mul((a,0),d)
    sizes=[]
    for dual in (False,True):
        B=mul((4 if dual else -1,0),mul(n,n));surv=[]
        for b in reps:
            for par in range(2 if dual else 1):
                c=mul(b,pi) if par else b
                B0=div(B,pi) if par else B
                assert B0 is not None
                q=red(mul(B0,inv(b,32)),32)
                if dyadic_mod(c,q):surv.append((b,par))
        if dual:assert surv==[((1,0),0),((5,0),0)]
        else:assert len(surv)==8
        sizes.append(len(surv))
    assert sizes==[8,2] # product 16 proves exactness by local [2] index
# Explicit globally squarefree divisor supports. 3,5 inert; 7 and 17 split.
gens={3:[(3,0)],5:[(5,0)],7:[d,db],17:[(5,2),(5,-2)]}
for p,g in gens.items():
    if len(g)==1:assert all(r*r%p!=2 for r in range(p))
    else:
        assert all(abs(norm(t))==p for t in g)
        assert mul(*g)==(p,0) or mul(*g)==(-p,0)
points={
    1:((23,-17),(160,-114),1),
    3:((35,-21),(252,-182),1),
    5:((1,5),(24,-20),1),
    7:((70,-56),(882,-637),1),
    15:((-18,-12),(396,90),2),
    17:((81,-63),(1032,-678),1),
    21:((-45,27),(144,-162),1),
    35:((71,-61),(80,-204),1),
}
def global_candidates(a,dual):
    n=mul((a,0),d);B=mul((4 if dual else -1,0),mul(n,n))
    support=[d]
    for p,gs in gens.items():
        if a%p==0:
            for g in gs:
                if g not in support:support.append(g)
    G=[neg,eps]+support+([pi] if dual else [])
    result=[]
    for bits in product(range(2),repeat=len(G)):
        b=O
        for t,bit in zip(G,bits):
            if bit:b=mul(b,t)
        if dual and min(sign(b,1),sign(b,-1))<0:continue
        if not all(odd_filter(b,n,g,dual) for g in support):continue
        c=div(B,b);assert c is not None
        if dyadic_mod(b,c):result.append(b)
    return result
def count_split(a,p,g):
    r=-g[0]*pow(g[1],-1,p)%p;n=(a*(3-r))%p;assert n
    return 1+sum(1 if v==0 else 2 if pow(v,(p-1)//2,p)==1 else 0 for x in range(p) for v in [(x**3-n*n*x)%p])
def count_inert(a,p):
    assert all(r*r%p!=2 for r in range(p));n=red(mul((a,0),d),p);n2=red(mul(n,n),p)
    ts=list(product(range(p),repeat=2));sq={}
    for t in ts:
        s=red(mul(t,t),p);sq[s]=sq.get(s,0)+1
    return 1+sum(sq.get(red(mul(t,add(mul(t,t),(-n2[0],-n2[1]))),p),0) for t in ts)
for a,(x,y,q) in points.items():
    n=mul((a,0),d);n2=mul(n,n);assert y!=(0,0)
    assert mul(y,y)==mul(x,add(mul(x,x),mul(n2,(-q**4,0))))
    A=global_candidates(a,False);Ap=global_candidates(a,True)
    assert len(A)==8 and Ap==[O],(a,A,Ap)
    if a!=17:
        ct=[count_split(a,17,g) for g in gens[17]]
        assert sorted(ct)==[16,20] and count_inert(a,11)%17!=0
    else:
        assert count_inert(a,3)==16 and count_inert(a,5)==20
    print(a,'rank exactly 1; local upper images',len(A),len(Ap),'point',x,y,q)
print('PASS: dyadic image cardinalities, all eight global rank certificates')
