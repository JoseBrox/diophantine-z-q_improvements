#!/usr/bin/env python3
"""Independent exact audit of the 178-variable weighted specified quartic."""
import hashlib,json
from pathlib import Path
from collections import defaultdict,Counter
from fractions import Fraction as F
from math import gcd
from functools import reduce
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
cert=json.loads((HERE/'certificate.json').read_text())
raw=(ROOT/cert['parent']).read_bytes()
assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==cert['parent_blob']
old=json.loads(raw)
new=json.loads((HERE/'quadrics.json').read_text())
def polynomial(ts):
    d=defaultdict(int)
    for t in ts:
        assert t['parameterPower']==0
        d[tuple(t['monomial'])]+=int(t['coefficient'])
    return {k:v for k,v in d.items() if v}
o={r['name']:polynomial(r['terms']) for r in old['residuals']}
n={r['name']:polynomial(r['terms']) for r in new['residuals']}
assert old['variables']==179 and len(o)==151 and new['variables']==178 and len(n)==150
assert o.pop('unit.R_inverse')=={():-1,(90,91):1}
assert o['unit.R_square']=={(89,):1,(90,90):-1}
scaled={11,12,13,14,81,82,83,84,85}
affected={name for name,row in o.items() if any(scaled.intersection(m) for m in row)}
assert affected=={'v82.scalar.inverse','v82.scalar.input','v82.scalar.p2','v82.scalar.q2','bbnative.v82.scalar.first','bbnative.v82.scalar.middle','bbnative.v82.scalar.second'}
for name in affected-{'v82.scalar.inverse','v82.scalar.input'}:
    assert all(len(m)==2 and len(scaled.intersection(m))>=1 and set(m)<=scaled for m in o[name])
for name,v in [('new.aggregate',114),('new.aggregate_shift',115)]:
    assert o[name].pop((91,v))==1
    assert (v,) not in o[name]
    o[name][(v,)]=1
assert o['v82.scalar.inverse']=={(81,88):1,(89,90):-1}
o['v82.scalar.inverse']={(81,88):1,(89,89):-1}
assert o['v82.scalar.input']=={():-1,(81,82):1,(91,):-9792}
o['v82.scalar.input']={(89,):-1,(81,82):1,(90,):-9792}
assert all(91 not in m for row in o.values() for m in row)
assert n=={name:{tuple(v-(v>91) for v in m):c for m,c in row.items()} for name,row in o.items()}
# Independent scalar r identity, in the polynomial ring Q[T], T=X^2.
def add(a,b):
    d=defaultdict(F,a)
    for k,v in b.items(): d[k]+=v
    return {k:v for k,v in d.items() if v}
def mul(a,b):
    d=defaultdict(F)
    for i,v in a.items():
        for j,w in b.items(): d[i+j]+=v*w
    return {k:v for k,v in d.items() if v}
def scale(a,c):return {k:v*c for k,v in a.items() if v*c}
def power(a,k):
    r={0:F(1)}
    for _ in range(k):r=mul(r,a)
    return r
T={1:F(1)}
beta={1:F(51),0:F(2504)}
pair=scale(power({1:F(51),0:F(2501)},2),F(1,4))
r={0:F(1)}
for f in (beta,add(beta,{0:F(-1)}),add(beta,{0:F(-2401)}),add(scale(beta,32),{0:F(343)})):
    r=mul(r,f)
assert o['inputSquare.definition']=={(1,1):1,(37,163):-1}
assert o['unit.c_inverse']=={():-1,(162,163):1}
def specialize(row,env,skip=()):
    val={}
    for m,c in row.items():
        if m in skip:continue
        x={0:F(c)}
        for v in m:x=mul(x,env[v])
        val=add(val,x)
    return val
env={37:T,77:pair,162:{0:F(1)}}
assert not specialize(o['scalar.rPair1.definition'],env)
assert specialize(o['scalar.four_contact_product.definition'],env,((78,90),))==scale(r,-1)
A=int(cert['scalar_A'])
assert o['scalar.forced_prime.definition']=={(78,):-A,(78,90):25,(162,162):1}
assert A<2**375 and A>26*100
# Fixed numerical estimates used by the proof.
assert F(375+21)*F(7,10)<300
a=2**960
assert a*a>2*(720*a+110500)
assert 2**20*F(2723,3003)>614000
assert F(1,3)-F(5,36036)>F(5,324)
assert F(242)*F(3,2)*F(5,2)*F(10001,10000)<1000
assert 960*529<2**19 and F(23,22)*323*F(7,10)<240
# Actual expanded polynomial.
ex=defaultdict(int)
for row in n.values():
    for m,c in row.items():
        assert len(m)<=2
        for mm,cc in row.items():ex[tuple(sorted(m+mm))]+=c*cc
ex={k:v for k,v in ex.items() if v}
assert polynomial(json.loads((HERE/'polynomial.json').read_text())['terms'])==ex
assert set(v for m in ex for v in m)==set(range(1,179))
assert len(ex)==cert['monomials'] and max(map(len,ex))==4
assert ex[(1,1,1,1)]==1 and reduce(gcd,ex.values())==1
assert max(map(abs,ex.values()))==int(cert['coefficient_height'])
def term(m,c,first):
    body='*'.join('x'+str(v)+('^'+str(k) if k>1 else '') for v,k in sorted(Counter(m).items()))
    a=abs(c)
    return ('-' if c<0 else '' if first else '+')+('' if a==1 and body else str(a)+('*' if body else ''))+body
literal=''.join(term(m,c,i==0) for i,(m,c) in enumerate(sorted(ex.items())))
assert (HERE/'expanded.txt').read_bytes()==literal.encode('ascii')
assert len(literal)==cert['expanded_bytes']
print('PASS: 178 coordinates, 150 quadrics,',len(ex),'monomials,',len(literal),'bytes')
