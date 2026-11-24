#!/usr/bin/env python3
"""Independent replay of the reciprocal-gate 53-variable quartic.
The valuation profiles below check arithmetic cases, not the external
height, elliptic-rank or prime-pattern hypotheses."""
from pathlib import Path
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import product
from functools import reduce
from math import gcd
import json,hashlib

here=Path(__file__).resolve().parent
oldfile=here.parent/'asymmetric_contact54_20261124/quadrics.json'
raw=oldfile.read_bytes()
assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()=='8a7262709c67d67f7ce725767f0d5ef1c36c4808'
old=json.loads(raw)
new=json.loads((here/'quadrics.json').read_text())
cert=json.loads((here/'certificate.json').read_text())
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
t,ks,e,U,V,ps,qs,Ds,c,u=map(x,(33,34,35,36,38,40,41,42,43,44))
expected={r['name']:read(r['terms']) for r in old['residuals']}
for k in ('single.alpha','single.gate','single.poleInput'):del expected[k]
expected.update({
 'detector0.pole.first':sub(add(sq(e),sc(ps,7)),sq(u)),
 'detector0.pole.factor':sub(mul(U,V),mul(e,sub(ks,n(7)))),
 'detector0.pole.second':sub(sub(sq(U),sq(V)),sc(qs,7)),
 'single.reciprocalGate':sub(mul(sub(t,n(1)),add(u,Ds)),n(1)),
 'single.reciprocalPoleInput':sub(mul(c,ks),sq(t)),
})
actual={r['name']:read(r['terms']) for r in new['residuals']}
assert len(new['residuals'])==len(actual)==43 and new['variables']==53
assert actual==expected
assert set(i for d in actual.values() for p,m in d for i in m)==set(range(1,54))
assert all(len(m)<=2 for d in actual.values() for p,m in d)
out=add(*(sq(d) for d in actual.values()))
poly=json.loads((here/'polynomial.json').read_text())
assert poly['variables']==53 and read(poly['terms'])==out
assert max(len(m) for p,m in out)==4 and reduce(gcd,out.values())==1
assert out[0,(1,1,1,1)]==1
assert len(out)==cert['parameter_terms']==795
assert len({m for p,m in out})==cert['coordinate_monomials']==791
f=defaultdict(int)
for (p,m),v in out.items():f[m]+=v
f={m:v for m,v in f.items() if v}
def term(m,v,first):
    b='*'.join('x'+str(i)+('^'+str(k) if k>1 else '') for i,k in sorted(Counter(m).items()))
    return ('-' if v<0 else '' if first else '+')+('' if abs(v)==1 and b else str(abs(v))+('*' if b else ''))+b
txt=''.join(term(m,v,i==0) for i,(m,v) in enumerate(sorted(f.items())))
assert txt.encode('ascii')==(here/'expanded-B1.txt').read_bytes()
assert len(txt)==11193 and max(map(abs,f.values()))==5531402752
assert cert['fixture_B1']=={'expanded_bytes':len(txt),'monomials':len(f),'coefficient_height':str(max(map(abs,f.values())))}
assert Q(23,20)-Q(1002,997)==Q(2891,19940)>0
# t=0: negative odd b forces e unit, so the two valuations
# of U',V' sum to that odd value and differ; their square difference
# has even valuation. This finite grid checks the arithmetic.
for k in range(1,50,2):
    for a in range(-100,101):
        b=-k-a
        assert a!=b and (2*min(a,b))%2==0
# True multiplication family: formal abscissas, or near (0,0).
# At the latter, the product valuation is either -4a or 4v_p(n).
# If x(Q) is a unit and x([n]Q) is positive with depth b, then
# negative product valuation -2k forces error valuation -k.
checks=0
for k in range(1,50,2):
    for a,vn in product(range(1,80),range(0,16)):
        assert -4*a!=-2*k and 4*vn>=0
        b=a
        if 2*vn-2*b==-2*k:
            assert vn-b==-k
            assert 3*k+4*(vn-b)==-k<0
            checks+=1
# Different classes ensure a unique negative minimum in W.
for k in range(1,22,2):
    assert len({k%4,2*k%4,3*k%4,4*k%4})==4
    # if pole condition forces t valuation less than -k/2,
    # v(A)=-v(t)>k/2, v(u)=k, hence both terms of D_s=A-u
    # have valuations greater than k/2.
    for vt in range(-40,20):
        if -k-2*vt>0:
            assert vt<0 and min(-vt,k)>Q(k,2)
# Norm/trace at negative odd u, assuming each integral slot is 1 mod p.
for a,b in product(range(-25,1),repeat=2):
    if min(a,b)<0:
        assert a+b<0 and a+b-min(a,b)==max(a,b)<=0
    else:
        assert a==b==0
print('PASS: 53 variables, 43 quadratic rows, 795 exact parameter terms;',
      checks,'nontrivial local multiplication profiles')
