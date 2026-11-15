#!/usr/bin/env python3
"""Independent balancing identities and coefficient-height certificate."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from math import gcd,lcm
import json
H=Path(__file__).parent/'inverse198'
def read(r):return {(t['parameterPower'],tuple(t['monomial'])):F(t['coefficient']) for t in r['terms']}
def primitive(p):
 d=lcm(*(c.denominator for c in p.values()));p={m:int(c*d) for m,c in p.items()};g=gcd(*p.values())*(1 if p[min(p)]>0 else -1);return {m:F(c//g) for m,c in p.items()}
a=json.loads((H/'quadratic.json').read_text());b=json.loads((H/'balanced-quadratic.json').read_text());weights={int(i):v for i,v in json.loads((H/'balancing-weights.json').read_text())['weights'].items()}
assert a['variables']==b['variables']==198 and len(a['residuals'])==len(b['residuals'])==184
assert set(weights)==set(range(1,199)) and weights[1]==0
for src,dst in zip(a['residuals'],b['residuals']):
 p={(2*ap+sum(weights[i] for i in m),m):c*149**ap for (ap,m),c in read(src).items()};smallest=min(ap for ap,m in p);p=primitive({(ap-smallest,m):c for (ap,m),c in p.items()});assert p==read(dst),src['name'];assert max(ap for ap,m in p)<=1
exp=defaultdict(F)
for row in b['residuals']:
 pp=list(read(row).items())
 for i,((ap,mm),cf) in enumerate(pp):
  for j in range(i,len(pp)):
   (aq,nn),cc=pp[j];exp[ap+aq,tuple(sorted(mm+nn))]+=cf*cc*(1 if i==j else 2)
exp={key:val for key,val in exp.items() if val};assert exp==read(json.loads((H/'balanced-polynomial.json').read_text()))
profiles=defaultdict(dict)
for (ap,mm),cf in exp.items():profiles[mm][ap]=int(cf)
K=31581660**28;H0=(5898050446009651968*K)**2
assert len(profiles)==2945 and len(exp)==2959
for p in profiles.values():
 if set(p)=={1}:assert p[1]**2<=H0*K
 else:
  assert set(p)<={0,2} and abs(p.get(0,0))*K+abs(p.get(2,0))*H0<=H0*K
  if p.get(0,0)*p.get(2,0)<0:assert p[0]%2==0 and p[2]%2==1 # C=149^N is odd, so coefficient cannot vanish.
assert any(p=={0:H0} for p in profiles.values()) and any(p=={2:K} for p in profiles.values())
assert K*149**112<H0<=K*149**114
assert {v for ap,mm in exp for v in mm}==set(range(1,199)) and gcd(*(int(c) for c in exp.values()))==1
assert max(len(mm) for ap,mm in exp)==4
report=dict(variables=198,quadraticRows=184,degree=4,content=1,coordinateMonomials=2945,parameterSeparatedTerms=2959,independentRescalingChecks=184,independentExpansion=True,exactHeight='max((5898050446009651968*31581660^28)^2,31581660^28*149^(2N))',coefficientCrossoverN=57,supportFixedForEveryNAtLeast1=True,scope='Algebraic and coefficient verification. Defining threshold remains ineffective under the inherited arithmetic premises.')
(H/'balanced-independent-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
