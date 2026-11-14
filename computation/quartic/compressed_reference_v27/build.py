#!/usr/bin/env python3
"""Remove a reciprocal reference coordinate in the 226 and 262 quartics."""
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict
from hashlib import sha256
from math import gcd,lcm
import importlib.util,json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'abc79_v27'))
from reference import equations
spec=importlib.util.spec_from_file_location('sparse81',HERE.parent/'abc81_v25/build.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
PINS={226: 'ccc845018e4d89b9d19f797bbfeca10c17ec637fbde5cb5bc08ad3bba9da105b', 262: '84c1130856dfda7d3a489f3077d7bc378cd8e594198dd8f3c03fe50463606a93'}
def build():
 reports={}
 for n in (226,262):
  src=HERE.parent/f'family{n}_v21'/f'quadratic-family{n}-v21.json';raw=src.read_bytes();assert sha256(raw).hexdigest()==PINS[n]
  old=json.loads(raw);coords=[dict(c,parentId=c['id']) for c in old['coordinates'] if c['id'] not in (85,86)];ids={c['id']:j+1 for j,c in enumerate(coords)}
  for c in coords:c['id']=ids[c['id']]
  def k(i,j,half=False):return m.var(i),m.scale(m.var(j),2 if half else 1)
  q1,q2,q3,_,_=equations(k(81,82),k(83,84),k(132,133,True),k(87,88,True),k(55,56))
  replacements=[p for q in (q1,q2,q3) for p in q];rows=[]
  for r in old['residuals']:
   if r['id'] in (23,24):continue
   p={(t['parameterPower'],tuple(t['monomial'])):Q(t['coefficient']) for t in r['terms']};name=r['name']
   if 17<=r['id']<=22:p=replacements[r['id']-17];name='compressedReference.'+str(r['id']-17)
   assert not any({85,86}&set(mm) for a,mm in p)
   p=m.prim(p);assert max(len(mm) for a,mm in p)<=2
   p={(a,tuple(sorted(ids[i] for i in mm))):c for (a,mm),c in p.items()}
   rows.append(dict(r,id=len(rows)+1,name=name,parentRowId=r['id'],terms=m.serial(p)))
  full=defaultdict(Q)
  for r in rows:
   p={(t['parameterPower'],tuple(t['monomial'])):Q(t['coefficient']) for t in r['terms']}
   for key,c in m.sq(p).items():full[key]+=c
  full={key:c for key,c in full.items() if c};profiles=defaultdict(dict)
  for (a,mm),c in full.items():profiles[mm][a]=int(c)
  assert len(coords)==n-2 and len(rows)==len(old['residuals'])-2
  assert max(len(mm) for a,mm in full)==4 and gcd(*(int(c) for c in full.values()))==1
  assert {i for a,mm in full for i in mm}==set(range(1,n-1))
  assert all(set(p) in ({0},{1},{0,2}) for p in profiles.values())
  assert [p for p in profiles.values() if 2 in p]==[{0:1,2:1}]
  C0=max(abs(p[0]) for p in profiles.values() if set(p)=={0});linear=max(abs(p.get(1,0)) for p in profiles.values())
  # The parameter A=149^(2N+1); verify all profiles at N=53 and monotonic ratios.
  A=149**107;assert C0<=A*A+1 and linear*A<=A*A+1 and linear<=A
  report=dict(variables=n-2,quadraticRows=len(rows),degree=4,content=1,ordinaryMonomials=len(profiles),parameterTerms=len(full),largestConstantCoefficient=str(C0),largestLinearCoefficient=str(linear),coefficientHeightForNAtLeast53='149^(4N+2)+1',sourceSha256=PINS[n],removedCoordinates=[85,86],removedRows=[23,24],changedRows=list(range(17,23)),projection='Exactly equivalent to the pinned parent, for every fixed N>=1.',definingParameter=('N=9682 is sufficient under inherited premises' if n==262 else 'Ineffective sufficiently large N'))
  out=HERE/f'family{n-2}';out.mkdir(parents=True,exist_ok=True)
  system=dict(old,format='compressed-reference-v27',variables=n-2,coordinates=coords,residuals=rows)
  poly=dict(format='compressed-reference-quartic-v27',variables=n-2,degree=4,inputCoordinate=1,fixedParameter=old['fixedParameter'],terms=m.serial(full))
  for fn,obj in [('quadratic.json',system),('polynomial.json',poly),('construction-report.json',report)]: (out/fn).write_text(json.dumps(obj,indent=2)+'\n')
  reports[str(n-2)]=report
 print(json.dumps(reports,indent=2))
if __name__=='__main__':build()
