#!/usr/bin/env python3
"""Exact independent replay. Run from any directory in the checkout."""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha1
from math import gcd
from functools import reduce
import json
import re

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "harmonic_scalar_20261125"
C = 331**26
E = 1081567619
k = 2**20
K0 = 56*331

def read_blob(path, pin):
    b = path.read_bytes()
    assert sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest() == pin, path
    return b

def clean(d):
    return {m:c for m,c in d.items() if c}

def poly(*terms):
    d = defaultdict(int)
    for c,m in terms:
        d[tuple(sorted(m))] += c
    return clean(d)

def mul(a,b):
    return poly(*[(c*d,i+j) for i,c in a.items() for j,d in b.items()])

def add(*a):
    return poly(*[(c,m) for p in a for m,c in p.items()])

def scale(a,k):
    return {m:k*c for m,c in a.items()}

def norm(a):
    g=reduce(gcd, a.values(), 0)
    return {m:c//g for m,c in a.items()}

# In the symbolic polynomial C is indexed by 0.
W=poly((36000*k,(37,)),(34981,()))
V=poly((1,(89,)),(-K0,(0,0)))
T=poly((1,(77,)))
K=poly((K0,(0,0)))
L=add(scale(T,432000000),scale(V,-1053721))
expected=[
    norm(add(scale(mul(W,L),3),scale(K,2*E))),
    norm(add(scale(mul(T,L),1944000000),scale(mul(mul(K,W),V),E)))
]
pins={162:("8a9e8235b8441ac70888c982ba49252ef806fcc8","6052e1ace6b6590543ec83d0c9e3739510b2700e",136,2765,2782),
      177:("29433e60c785fb503879aa786b96ac2ed1f0804b","7e4906081cefd5aecec9d7dabd6f0e748a9d0fd5",149,3008,3025)}

def aspoly(row):
    return poly(*[(int(t["coefficient"]),(0,)*t["parameterPower"]+tuple(t["monomial"])) for t in row["terms"]])

def square_unordered(p):
    items=list(p.items())
    d=defaultdict(int)
    for i,(m,c) in enumerate(items):
        for j in range(i,len(items)):
            n,e=items[j]
            d[tuple(sorted(m+n))]+=(1 if i==j else 2)*c*e
    return clean(d)

for n,(oldpin,newpin,rows,profiles,terms) in pins.items():
    old=json.loads(read_blob(PARENT/f"quartic{n}.json",oldpin))
    new=json.loads(read_blob(HERE/f"quartic{n}.json",newpin))
    a,b=old["residuals"],new["residuals"]
    assert new["variables"]==n and len(a)==len(b)==rows
    assert [i for i,(u,v) in enumerate(zip(a,b)) if u!=v]==[13,14]
    assert [aspoly(b[i]) for i in (13,14)]==expected
    pp=[aspoly(q) for q in b]
    assert all(sum(x!=0 for x in m)<=2 for p in pp for m in p)
    sym=add(*(square_unordered(p) for p in pp))
    assert len(sym)==terms
    assert len({tuple(x for x in m if x) for m in sym})==profiles
    d=defaultdict(int)
    for m,c in sym.items():
        d[tuple(x for x in m if x)]+=c*C**m.count(0)
    d=clean(d)
    assert len(d)==profiles and d[(1,)*4]==1
    assert max(map(len,d))==4
    assert {x for m in d for x in m}==set(range(1,n+1))
    height=max(map(abs,d.values()))
    assert height.bit_length()==1923
    print(n,rows,profiles,terms,height.bit_length())
    if n==177:
        raw=read_blob(HERE/"expanded177.txt","ec1c9b14de964ec7b40878bf5547e749860186eb")
        assert len(raw)==72580 and len(str(height))==579
        t=raw.decode("ascii")
        pieces=re.findall(r"[+-]?[^+-]+",t)
        assert "".join(pieces)==t
        out={}
        for term in pieces:
            sign=-1 if term.startswith("-") else 1
            factors=term.lstrip("+-").split("*")
            coeff=sign
            if factors[0].isdigit():
                coeff*=int(factors.pop(0))
            m=[]
            for factor in factors:
                match=re.fullmatch(r"x(\d+)(?:\^(\d+))?",factor)
                assert match
                m.extend([int(match[1])]*int(match[2] or 1))
            key=tuple(sorted(m))
            assert key not in out
            out[key]=coeff
        assert out==d

# Independent rational identity from four evaluations of cubics.
def r(s):
    return (2401+2400*s)*(343+375*s)*(1+s)
e=F(-E,25920000)
for s in [F(0),F(1),F(-2),F(1,3)]:
    w=s+F(34981,36000)
    assert r(s)==e+900000*w**3-F(1053721,480)*w
p=331
for x in range(p):
    z=r(k*x*x)%p
    assert z and (25920000*z+E)%p
assert 900000%p and k%p
assert E==11*47*1019*2053
assert 25920000==2**9*3**4*5**4
assert 331**120>2**960
assert 47*1019*2053<2**27
assert r(0)%8==7 and (E*pow(25920000//512,-1,8))%8==3
assert (K0//8)%8==5
print("All exact replay checks passed.")
