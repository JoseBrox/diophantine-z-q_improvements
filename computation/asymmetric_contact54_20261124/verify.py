#!/usr/bin/env python3
"""Independent exact reconstruction from the pinned v81 table."""
import hashlib, json
from pathlib import Path
from collections import defaultdict, Counter
from fractions import Fraction
from math import gcd
from functools import reduce

here=Path(__file__).resolve().parent
root=here.parents[1]
p=root/'computation/variable_reductions_v81/abc/quartic56/quadrics.json'
data=p.read_bytes()
assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()=='d47fe4f9636ac9415a79dc4a10ac04fea10cf087'
old=json.loads(data)
new=json.loads((here/'quadrics.json').read_text())
certificate=json.loads((here/'certificate.json').read_text())

def add(a,b):
    out=Counter(a)
    out.update(b)
    return {k:v for k,v in out.items() if v}
def neg(a): return {k:-v for k,v in a.items()}
def mul(a,b):
    d=defaultdict(int)
    for (pa,ma),v in a.items():
        for (pb,mb),w in b.items():
            d[pa+pb,tuple(sorted(ma+mb))]+=v*w
    return {k:v for k,v in d.items() if v}
def sub(a,b): return add(a,neg(b))
def n(v): return {(0,()):v} if v else {}
def var(i): return {(0,(i,)):1}
def read(ts):
    d=defaultdict(int)
    for t in ts: d[t['parameterPower'],tuple(t['monomial'])]+=int(t['coefficient'])
    return {k:v for k,v in d.items() if v}
def powp(a,k):
    out=n(1)
    for _ in range(k): out=mul(out,a)
    return out
r={v['name']:read(v['terms']) for v in new['residuals']}
expected={}
for v in old['residuals']:
    name=v['name']
    if name.startswith('contact.') or name=='height.M2': continue
    d={(t['parameterPower'],tuple(54 if i==56 else i for i in t['monomial'])):int(t['coefficient']) for t in v['terms']}
    if name=='height.M':
        d[0,(8,8)]=-32
        d[0,(30,30)]=-8
    expected[name]=d
a=add(var(45),n(16)); z=var(46)
expected['contact.leftSquare']=sub(var(47),powp(sub(a,z),2))
expected['contact.rightSquare']=sub(var(48),powp(add(a,z),2))
expected['contact.leftFourth']=sub(var(49),powp(var(47),2))
expected['contact.rightFourth']=sub(var(50),powp(var(48),2))

def quartic(R,S):
    # two opposite pair-products of equal sum of squares
    return mul(sub(add(S,n(64)),mul(n(65),R)),sub(add(S,n(784)),mul(n(65),R)))
# The product above is degree two in R,S; no reduction or floating point.
expected['contact.leftValue']=sub(var(51),quartic(var(47),var(49)))
expected['contact.rightValue']=sub(mul(var(52),var(50)),quartic(var(48),var(50)))
expected['contact.rightInverse']=sub(mul(var(53),var(52)),n(1))
expected['contact.asymmetric']=sub(mul(sub(add(var(43),n(1)),var(53)),var(51)),powp(var(52),2))
# In the degree-two pair-product formula the term R^2 may be reduced to S.
# The table uses the expanded quartic coefficients, not that redundant R^2.
for key,R,S in [('contact.leftValue',47,49),('contact.rightValue',48,50)]:
    d=expected[key]
    a0=d.pop((0,(R,R)),0)
    if a0:
        d[0,(S,)]=d.get((0,(S,)),0)+a0
    expected[key]={k:v for k,v in d.items() if v}
assert r==expected
assert new['variables']==54 and len(r)==44
assert set(i for d in r.values() for _,m in d for i in m)==set(range(1,55))
assert all(len(m)<=2 for d in r.values() for _,m in d)
out={}
for d in r.values():out=add(out,mul(d,d))
actual=read(json.loads((here/'polynomial.json').read_text())['terms'])
assert actual==out and max(len(m) for _,m in out)==4
assert reduce(gcd,out.values())==1 and out[0,(1,1,1,1)]==1
assert len(out)==certificate['parameter_terms']
assert len({m for _,m in out})==certificate['coordinate_monomials']
assert Fraction(23,20)-Fraction(1002,997)==Fraction(2891,19940)>0
assert (2*Fraction(398,100)-Fraction(201,200)-Fraction(4,100))/3>=Fraction(23,10)
assert Fraction(398,100)-Fraction(201,200)>=Fraction(23,10)
# Finite checks for the two valuation patterns; general proof is by inequalities.
for k in range(-100,101):
    if k<=0:
        assert 2*k-1<min(-k,0) and (2*k-1)%2
    elif k%2:
        assert -k<min(2*k-1,0) and (-k)%2
for l in range(-100,3):
    assert -1<min(2-l,0)
# Expansion at z=infinity: monic G(t)=t^8+O(t^6),
# H(t)=t^4+O(t^2). H(a+z)^2 has z^7 coefficient 8a,
# G(a-z) has z^7 coefficient -8a, hence difference 16a.
for a0 in [-17,1,17,12345]:
    for sg in [-1,1]:
        # exact z^7 coefficient from the 8 linear factors
        coeff=sg**7*sum(a0+r for r in (-8,-7,-4,-1,1,4,7,8))
        assert coeff==sg*8*a0
from collections import Counter as Counts
fixture=defaultdict(int)
for (_,m),v in out.items(): fixture[m]+=v
fixture={m:v for m,v in fixture.items() if v}
def ascii_term(m,v,first):
    a=abs(v)
    powers=Counts(m)
    body='*'.join('x'+str(i)+('^'+str(k) if k>1 else '') for i,k in sorted(powers.items()))
    return ('-' if v<0 else ('' if first else '+'))+('' if a==1 and body else str(a)+('*' if body else ''))+body
txt=''.join(ascii_term(m,v,i==0) for i,(m,v) in enumerate(sorted(fixture.items())))
assert (here/'expanded-B1.txt').read_bytes()==txt.encode('ascii')
f=certificate['fixture_B1']
assert f['expanded_bytes']==len(txt)
assert f['monomials']==len(fixture)
assert int(f['coefficient_height'])==max(map(abs,fixture.values()))
print('PASS 54 variables, 44 quadrics,',len(out),'parameter-separated quartic terms')
