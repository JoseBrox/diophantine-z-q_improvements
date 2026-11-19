"""Independently verify a balanced family from its exact upstream rows and integer weights."""
from collections import Counter, defaultdict
from itertools import combinations_with_replacement
from math import gcd
from pathlib import Path
from hashlib import sha256
import json, sys
src,folder=map(Path,sys.argv[1:])
take=lambda p:json.loads(p.read_bytes())
data=take(src);res=take(folder/'quadrics.json');cert=take(folder/'certificate.json')
assert sha256(src.read_bytes()).hexdigest()==cert['source_sha256']
weights=[0]+cert['coordinate_weights'];assert weights[1]==0
new=Counter()
for a,b in zip(data['residuals'],res['residuals'],strict=True):
    assert a['name']==b['name']
    t=[(r['parameterPower']+sum(weights[i] for i in r['monomial']),tuple(r['monomial']),int(r['coefficient'])) for r in a['terms']]
    low=min(e for e,m,n in t);g=gcd(*(n for e,m,n in t))
    transformed={(e-low,m,n//g) for e,m,n in t}
    fitted={(r['parameterPower'],tuple(r['monomial']),int(r['coefficient'])) for r in b['terms']}
    assert fitted==transformed and all(e in (0,1) for e,m,n in fitted)
    for x,y in combinations_with_replacement(fitted,2):
        i,m,n=x;j,k,p=y
        new[i+j,tuple(sorted(m+k))]+=n*p*(1 if x==y else 2)
poly={(i,m):v for (i,m),v in new.items() if v}
assert poly=={(r['parameterPower'],tuple(r['monomial'])):int(r['coefficient']) for r in take(folder/'polynomial.json')['terms']}
by=defaultdict(lambda:[0,0,0])
for (i,m),v in poly.items():by[m][i]=v
assert len(by)==cert['monomials'] and by[(1,)*4]==[1,0,0]
K=126616122944180358034867798936
assert any(abs(a)==K and b==d==0 for a,b,d in by.values()) and any(abs(d)==22201 and a==b==0 for a,b,d in by.values())
for N in range(1,7):
    C=149**N;vs=[p+q*C+r*C*C for p,q,r in by.values()]
    assert all(vs) and max(map(abs,vs))==max(K,22201*C*C)
C=149**6
for a,b,d in by.values():
    s=1 if a+b*C+d*C*C>0 else -1
    assert min(s*(a+b*C+d*C*C),s*(b+2*d*C),s*d)>=0 and s*(a+b*C+d*C*C)>0
    for s in (1,-1):
        p,q,r=s*a,s*b,22201+s*d
        assert min(p+q*C+r*C*C,q+2*r*C,r)>=0
print('Balanced table checked',res['variables'],len(res['residuals']),len(by),'degree 4, primitive, exact height max(K,149^(2N+2)).')
