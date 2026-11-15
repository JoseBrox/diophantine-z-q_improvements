#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction
from collections import defaultdict
from math import gcd,lcm
import json
P=Path(__file__).parent/'affine200'
def read(r):return {(t['parameterPower'],tuple(t['monomial'])):Fraction(t['coefficient']) for t in r['terms']}
def primitive(p):
 d=lcm(*(c.denominator for c in p.values()));p={m:int(c*d) for m,c in p.items()};g=gcd(*p.values())*(1 if p[min(p)]>0 else -1);return {m:Fraction(c//g) for m,c in p.items()}
a=json.loads((P/'quadratic.json').read_text());b=json.loads((P/'balanced-quadratic.json').read_text());R={c['id'] for c in a['coordinates'] if c.get('source204Id') in(117,118)}
assert a['variables']==b['variables']==200 and len(a['residuals'])==len(b['residuals'])==186
for src,dst in zip(a['residuals'],b['residuals']):
 terms=read(src);p={(2*ap+sum(v in R for v in m),m):c*149**ap for (ap,m),c in terms.items()};smallest=min(ap for ap,m in p);p=primitive({(ap-smallest,m):c for (ap,m),c in p.items()});assert p==read(dst),src['name']
expanded=defaultdict(Fraction)
for r in b['residuals']:
 pp=list(read(r).items())
 for i,((ap,m),c) in enumerate(pp):
  for j in range(i,len(pp)):
   (aq,n),d=pp[j];expanded[ap+aq,tuple(sorted(m+n))]+=c*d*(1 if i==j else 2)
expanded={m:c for m,c in expanded.items() if c};assert expanded==read(json.loads((P/'balanced-polynomial.json').read_text()))
profiles=defaultdict(dict)
for (ap,m),c in expanded.items():profiles[m][ap]=int(c)
K=31581660**28;H=(5898050446009651968*K)**2
assert len(profiles)==3117 and len(expanded)==3118
assert [p for p in profiles.values() if len(p)>1]==[{0:1,2:22201}]
for p in profiles.values():
 if set(p)=={1}:assert p[1]**2<=H*K
 else:assert set(p)<={0,2} and abs(p.get(0,0))*K+abs(p.get(2,0))*H<=H*K
assert any(p=={0:H} for p in profiles.values()) and any(p=={2:K} for p in profiles.values())
assert K*149**112<H<=K*149**114
assert {v for ap,m in expanded for v in m}==set(range(1,201))
assert gcd(*(int(c) for c in expanded.values()))==1
report=dict(variables=200,degree=4,quadraticRows=186,coordinateMonomials=3117,parameterSeparatedTerms=3118,exactCoefficientHeight='max((5898050446009651968*31581660^28)^2,31581660^28*149^(2N))',coefficientCrossoverN=57,independentRescaling=True,independentExpansion=True,scope='Algebraic and coefficient verification, not arithmetic soundness/completeness')
(P/'balanced-independent-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
