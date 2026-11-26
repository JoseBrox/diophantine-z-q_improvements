#!/usr/bin/env python3
"""Independent exact arithmetic and literal-reconstruction checks."""
import json
from pathlib import Path
from fractions import Fraction as Q
from math import gcd, prod
from collections import defaultdict
from itertools import combinations

D = Path(__file__).resolve().parent
PARENT = D.parent / "reciprocal_depressed_scalar_20261126"
C = json.loads((D/"certificate.json").read_text())
F = json.loads((D/"family_certificate.json").read_text())
S = {2,3,5,7,11,13,17,37,41,2399}
G = S | {19,23}
R = [-77,23,21,-75,51]
THETA = [Q(0),Q(-1,2),Q(-1),Q(1,2399),Q(-32,407)]
assert [(973*v-77)/(1632*v+32) for v in THETA] == [Q(x,32) for x in R]
assert 973*32+77*1632 == 2**7*5**2*7**2 == 156800
assert max(map(abs,R))*2 < 5*32
assert len(set(map(abs,R)))==5 and all(R)
def strip(a):
    a=abs(a)
    assert a
    for p in G:
        while a%p==0:
            a//=p
    return a
assert all(strip(a)==1 for a in R)
for x,y in combinations(R,2):
    assert strip(x+y)==strip(x-y)==1
p=[1]
for a in R:
    q=[0]*(len(p)+1)
    for i,b in enumerate(p):
        q[i]-=a*a*b
        q[i+1]+=b
    p=q
assert p==[-20236648618580625,98933750608581,-151547683050,77366218,-15125,1]
J=prod(G)
CC=Q(74712001,10**6)*2**68*3**16*5**16*7**4*J**2*prod(Q(q+1,q) for q in G)
assert J==811898089212210<2**50
assert 2**68<CC<2**249
def prime(n):
    return n>=2 and all(n%d for d in range(2,int(n**.5)+1))
assert prod(Q(q+1,q) for q in range(2,1001) if prime(q) and q not in G)<Q(21,10)
assert 9*(2*21+1)//4+1==97 and 331**97>2**810
assert 2**21*Q(36036-2835,36036)>526500
assert 9*(2*285+1)//4+1==1285 and 331**1285>2**10280
assert 10280*(Q(1,3)-Q(5,36036))-3249>170
assert 1000*(54+Q(5*10280*7,60))<2**24

def row_dict(row):
    a=defaultdict(int)
    for t in row["terms"]:
        a[t["parameterPower"],tuple(sorted(t["monomial"]))]+=int(t["coefficient"])
    return {k:v for k,v in a.items() if v}
def quad(k,*a): return (0,tuple(sorted(a)),k)
def terms(*a):
    q=defaultdict(int)
    for e,m,k in a:q[e,m]+=k
    return {k:v for k,v in q.items() if v}

def verify_rows(n):
    name="quadrics.json" if n==175 else "quartic161.json"
    a=json.loads((D/name).read_text())
    b=json.loads((PARENT/f"quartic{n}.json").read_text())
    old={r["name"]:row_dict(r) for r in b["residuals"]}
    new={r["name"]:row_dict(r) for r in a["residuals"]}
    assert new.keys()==old.keys()
    charts=([(2,60,61,62,156),(68,69,70,71,157),(162,167,168,169,158)]
            if n==175 else [(2,60,61,62,155),(68,69,70,71,156)])
    for i,(t,r,s,d,w) in enumerate(charts):
        pref=f"additive.detector{i}."
        expected={
            "contactSquare":terms(quad(1024,t,t),quad(-1,r) if n==175 else quad(-1,r,159)),
            "contactCombination":terms(quad(1,r,s),quad(p[3],r,w),quad(p[3],r),
                quad(p[4],s,w),quad(p[4],s),quad(-1,d)),
            "contactRelation":terms(quad(p[1],r,w),quad(p[1],r),quad(p[2],s,w),
                quad(p[2],s),quad(p[0],w),quad(p[0]),quad(1,s,d))
        }
        for k,v in expected.items():
            assert new[pref+k]==v
            old[pref+k]=v
    assert new==old
    assert a["variables"]==n
    assert all(len(m)<=2 for row in new.values() for e,m in row)
    P=defaultdict(lambda:defaultdict(int))
    for row in new.values():
        ts=list(row.items())
        for i,((e,m),c) in enumerate(ts):
            for j,((f,l),b) in enumerate(ts[:i+1]):
                P[tuple(sorted(m+l))][e+f]+=c*b*(1 if i==j else 2)
    P={m:{e:c for e,c in a.items() if c} for m,a in P.items()}
    P={m:a for m,a in P.items() if a}
    return P,len(new)

def expand(P,N):
    C=331**N
    result={m:sum(c*C**e for e,c in a.items()) for m,a in P.items()}
    return {m:c for m,c in result.items() if c}
def literal(a):
    out=[]
    for m,c in sorted(a.items()):
        factors=[]
        for i in sorted(set(m)):
            e=m.count(i)
            factors.append(f"x{i}"+(f"^{e}" if e>1 else ""))
        sign="-" if c<0 else "+" if out else ""
        num=str(abs(c)) if abs(c)!=1 or not factors else ""
        out.append(sign+num+("*" if num and factors else "")+"*".join(factors))
    return "".join(out)
for n,N,cert in [(175,21,C),(161,21,F)]:
    P,rows=verify_rows(n)
    a=expand(P,N)
    assert len(a)==cert["monomials"]
    assert rows==cert["residuals"]
    assert max(map(len,a))==4
    assert set(i for m in a for i in m)==set(range(1,n+1))
    assert a[(1,1,1,1)]==1 and gcd(*a.values())==1
    txt=literal(a)
    if n==175:
        assert len(txt)==C["bytes"]==73080
        assert max(abs(c).bit_length() for c in a.values())==C["coefficient_bits"]==802
        assert (D/"expanded175.txt").read_text()==txt
    else:
        assert len(txt)==F["fixture_bytes"]==65282
        assert len(literal(expand(P,285)))==99875
        assert len(literal(expand(P,286)))==100005
        assert len(literal(expand(P,1)))==62664
        dependent=[a for a in P.values() if max(a)>0]
        assert len(dependent)==17
        for a in dependent:
            e=max(a)
            assert set(a)<={0,e}
            assert abs(a[e])*331**(2*e)>abs(a.get(0,0))+1
        assert all(abs(c)>1 for m,c in expand(P,2).items() if max(P[m])>0)
    print(f"{n}: {len(a)} monomials, degree 4, {len(txt)} bytes at N={N}")
print("All checks passed.")
