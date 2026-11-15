"""Independent coefficient rescaling audit, using only complete table files."""
from pathlib import Path
from fractions import Fraction
from collections import defaultdict
from math import gcd,lcm
import json
P=Path(__file__).resolve().parents[1]/'circuits/affine200'
u=json.loads((P/'quadratic.json').read_text());b=json.loads((P/'balanced-quadratic.json').read_text());poly=json.loads((P/'balanced-polynomial.json').read_text())
def rowsparse(r):return {(t['parameterPower'],tuple(t['monomial'])):int(t['coefficient']) for t in r['terms']}
rids={v['id'] for v in u['coordinates'] if v.get('source204Id') in (117,118)}
for r0,r1 in zip(u['residuals'],b['residuals']):
 z=defaultdict(int)
 for (e,m),coef in rowsparse(r0).items(): z[(2*e+sum(i in rids for i in m),m)]+=coef*149**e
 shift=min(e for e,m in z)
 z={(e-shift,m):c for (e,m),c in z.items() if c};g=gcd(*z.values());g*=1 if z[min(z)]>0 else -1
 z={k:c//g for k,c in z.items()}
 assert z==rowsparse(r1),r0['name']
 assert max(e for e,m in z)<=1
out=defaultdict(int)
for r in b['residuals']:
 terms=list(rowsparse(r).items())
 for i,((e,m),c) in enumerate(terms):
  for j in range(i,len(terms)):
   (f,n),d=terms[j];out[(e+f,tuple(sorted(m+n)))]+=(1 if i==j else 2)*c*d
out={k:c for k,c in out.items() if c}
assert out==rowsparse(poly)
profiles=defaultdict(dict)
for (e,m),c in out.items(): profiles[m][e]=c
K=31581660**28;H=(5898050446009651968*K)**2
assert any(p=={0:H} for p in profiles.values()) and any(p=={2:K} for p in profiles.values())
for p in profiles.values():
 if set(p)=={1}: assert p[1]*p[1]<=H*K
 else: assert set(p)<={0,2} and abs(p.get(0,0))*K+abs(p.get(2,0))*H<=H*K
 # The positive allowed parameter cannot cancel any stored support.
 if len(p)>1: assert p.get(0,0)*p.get(2,0)>0
assert K*149**112<H<=K*149**114
report={'status':'PASS','all_rescaled_rows_authenticated':True,'all_expanded_coefficients_authenticated':True,'monomials':len(profiles),'parameter_separated_terms':len(out),'exact_height':'max((5898050446009651968*31581660^28)^2,31581660^28*149^(2N))','coefficient_crossover':57,'scope':'Coefficient threshold only; no sufficient defining parameter.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
