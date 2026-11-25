#!/usr/bin/env python3
"""Exact replay of the 52-variable contact replacement and expansion."""
from pathlib import Path
from collections import Counter, defaultdict
from fractions import Fraction as Q
from functools import reduce
from math import gcd
import hashlib, json

here=Path(__file__).resolve().parent
raw=(here.parent/'reciprocal_gate53_20261124/quadrics.json').read_bytes()
cert=json.loads((here/'certificate.json').read_text())
assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==cert['parent']
old=json.loads(raw)
new=json.loads((here/'quadrics.json').read_text())
def read(ts):
    d=defaultdict(int)
    for t in ts:d[t['parameterPower'],tuple(t['monomial'])]+=int(t['coefficient'])
    return {k:v for k,v in d.items() if v}
def add(*ds):
    d=defaultdict(int)
    for a in ds:
        for k,v in a.items():d[k]+=v
    return {k:v for k,v in d.items() if v}
def sc(a,s):return {k:s*v for k,v in a.items() if s*v}
def mul(a,b):
    d=defaultdict(int)
    for (p,m),v in a.items():
        for (q,n),w in b.items():d[p+q,tuple(sorted(m+n))]+=v*w
    return {k:v for k,v in d.items() if v}
def x(i):return {(0,(i,)):1}
def n(k):return {(0,()):k} if k else {}
def sq(a):return mul(a,a)
def sub(a,b):return add(a,sc(b,-1))
P=[1]
for r in (1,4,7,8):
    p=[0]*(len(P)+1)
    for i,v in enumerate(P):
        p[i]-=v*r*r
        p[i+1]+=v
    P=p
assert P==[50176,-55120,5073,-130,1]
def value(r,s):return add(n(P[0]),sc(r,P[1]),sc(s,P[2]),sc(mul(r,s),P[3]),sc(sq(s),P[4]))
expected={r['name']:read(r['terms']) for r in old['residuals']}
for k in ('contact.leftValue','contact.rightInverse','contact.asymmetric'):del expected[k]
assert len(expected)==40
F,H,u=map(x,(51,52,44))
expected['contact.leftScaledValue']=sub(mul(u,F),value(x(47),x(49)))
assert expected['contact.rightValue']==sub(mul(H,x(50)),value(x(48),x(50)))
expected['contact.harmonic']=sub(sub(mul(F,H),sq(H)),sc(mul(u,F),3))
actual={r['name']:read(r['terms']) for r in new['residuals']}
assert actual==expected and len(actual)==len(new['residuals'])==42 and new['variables']==52
assert set(i for d in actual.values() for p,m in d for i in m)==set(range(1,53))
assert all(len(m)<=2 for d in actual.values() for p,m in d)
out=add(*(sq(d) for d in actual.values()))
poly=json.loads((here/'polynomial.json').read_text())
assert poly['variables']==52 and read(poly['terms'])==out
assert max(len(m) for p,m in out)==4 and reduce(gcd,out.values())==1
assert out[0,(1,1,1,1)]==1
assert len(out)==cert['parameter_terms']==789
assert len({m for p,m in out})==cert['coordinate_monomials']==785
f=defaultdict(int)
for (p,m),v in out.items():f[m]+=v
f={m:v for m,v in f.items() if v}
def term(m,v,first):
    b='*'.join('x'+str(i)+('^'+str(k) if k>1 else '') for i,k in sorted(Counter(m).items()))
    return ('-' if v<0 else '' if first else '+')+('' if abs(v)==1 and b else str(abs(v))+('*' if b else ''))+b
txt=''.join(term(m,v,i==0) for i,(m,v) in enumerate(sorted(f.items())))
assert txt.encode('ascii')==(here/'expanded-B1.txt').read_bytes()
assert cert['fixture_B1']=={'expanded_bytes':len(txt),'monomials':len(f),'coefficient_height':str(max(map(abs,f.values())))}
assert Q(347,200)-Q(11,4)*Q(501,997)==Q(70409,199400)>0
for l in range(-32,33):
    for k in range(-32,33):
        if k<0 and k%4:continue
        a,b=k-l,-k
        if l==1 and (k<=0 or k%2):
            assert a!=b and min(a,b)<0 and min(a,b)%2
        if k==1 and l<=1:
            assert a!=b and min(a,b)==-1
for i in range(41):
    for j in range(41):
        for k in range(max(i,j)+1):
            if i!=j and k!=max(i,j):continue
            assert (i>0)+(j>0)<=(k>0)+i+j-k
print('PASS: 52 variables, 42 quadratics, 789 parameter terms, positive height margin')
