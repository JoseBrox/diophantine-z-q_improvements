#!/usr/bin/env python3
"""The lower-coefficient 81-variable presentation using Jaswal's pole input."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from hashlib import sha256
import importlib.util,json
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('arith81',HERE.parent/'abc81_v25/build.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
PARENT=HERE.parent/'abc81_v25/quadratic-family.json'
def build():
 raw=PARENT.read_bytes();old=json.loads(raw);ids={c['name']:c['id'] for c in old['coordinates']};rows=[]
 for r in old['residuals']:
  p={(t['parameterPower'],tuple(t['monomial'])):F(t['coefficient']) for t in r['terms']}
  for j in (0,1):
   pre=f'detector{j}.pole.';v=lambda s:m.var(ids[f'detector{j}.'+s]);b=v('poleInput');e=v('pole.e');u=v('pole.u');vv=v('pole.v');p2=v('pole.pSquare');q2=v('pole.qSquare')
   if r['name']==pre+'first':p=m.add(m.sq(e),m.mul(b,p2),m.con(-1))
   elif r['name']==pre+'factor':p=m.add(m.mul(u,vv),m.scale(e,-1),m.mul(e,b))
   elif r['name']==pre+'second':p=m.add(m.sq(u),m.scale(m.sq(vv),-1),m.scale(m.mul(b,q2),-1))
  rows.append(dict(r,terms=m.serial(m.prim(p))))
 full=defaultdict(F)
 for r in rows:
  p={(t['parameterPower'],tuple(t['monomial'])):F(t['coefficient']) for t in r['terms']}
  for k,c in m.sq(p).items():full[k]+=c
 full={k:c for k,c in full.items() if c};profiles=defaultdict(dict)
 for (a,mm),c in full.items():profiles[mm][a]=int(c)
 assert profiles[()]=={0:630511,2:1}
 assert max(abs(p[0]) for p in profiles.values() if set(p)=={0})==4153456
 system=dict(old,format='abc81-congruent-poles-v27',residuals=rows)
 poly=dict(format='abc81-congruent-poles-quartic-v27',variables=81,degree=4,inputCoordinate=1,fixedParameter=old['fixedParameter'],terms=m.serial(full))
 report=dict(schema='abc81-congruent-poles/v27',variables=81,quadraticRows=73,degree=4,ordinaryMonomials=len(profiles),parameterTerms=len(full),exactHeight='max(4153456,B^2+630511)',sourceSha256=sha256(raw).hexdigest(),scope='Ordinary rational abc, the retained elliptic and prime inputs, and Jaswal Theorem 1.2; same input projection as the corrected abc79 family for every fixed B.')
 for fn,obj in [('quadratic.json',system),('polynomial.json',poly),('construction-report.json',report)]:(HERE/fn).write_text(json.dumps(obj,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':build()
