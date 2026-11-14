#!/usr/bin/env python3
"""Independent all-row, all-coefficient checks for the 224/260 and pole81 tables.
No producer is imported. The reference equation table is separately checked
against its complete ideal certificates and original source component rows.
"""
from fractions import Fraction as Q
from collections import defaultdict
from pathlib import Path
from math import gcd,lcm
from hashlib import sha256
from copy import deepcopy
import json
HERE=Path(__file__).resolve().parent
PINS={226:'ccc845018e4d89b9d19f797bbfeca10c17ec637fbde5cb5bc08ad3bba9da105b',262:'84c1130856dfda7d3a489f3077d7bc378cd8e594198dd8f3c03fe50463606a93'}
def ck(x,s):
 if not x:raise ValueError(s)
def clean(p):return {k:c for k,c in p.items() if c}
def add(*ps):
 o=defaultdict(Q)
 for p in ps:
  for k,c in p.items():o[k]+=c
 return clean(o)
def scale(p,c):return clean({k:c*v for k,v in p.items()})
def mul(p,q):
 o=defaultdict(Q)
 for (a,m),c in p.items():
  for (b,n),d in q.items():o[a+b,tuple(sorted(m+n))]+=c*d
 return clean(o)
def C(c):return {(0,()):Q(c)} if c else {}
def V(i):return {(0,(i,)):Q(1)}
def prim(p):
 d=lcm(*(c.denominator for c in p.values()));g=gcd(*(int(d*c) for c in p.values()))
 if p[min(p)]<0:g=-g
 return scale(p,Q(d,g))
def read(r):return {(t['parameterPower'],tuple(t['monomial'])):Q(t['coefficient']) for t in r['terms']}
def kp(x,y):return add(mul(x[0],y[0]),scale(mul(x[1],y[1]),2)),add(mul(x[0],y[1]),mul(x[1],y[0]))
def field_table(items,vals):
 out=({}, {})
 for t in items:
  p=C(t['c'][0]),C(t['c'][1])
  for i in t['m']:p=kp(p,vals[i-1])
  out=add(out[0],p[0]),add(out[1],p[1])
 return out

def expanded(rows):
 out=defaultdict(Q)
 for r in rows:
  terms=sorted(read(r).items())
  for j,((a,m),c) in enumerate(terms):
   for k in range(j,len(terms)):
    (b,n),d=terms[k];out[a+b,tuple(sorted(m+n))]+=(1 if k==j else 2)*c*d
 return clean(out)
def verify(n,obj,poly):
 raw=(HERE.parent/f'family{n}_v21'/f'quadratic-family{n}-v21.json').read_bytes();ck(sha256(raw).hexdigest()==PINS[n],'source hash');old=json.loads(raw)
 tab=json.loads((HERE.parent/'abc79_v27/reference-equations.json').read_text())['equations']
 k=lambda i,j,h=False:(V(i),scale(V(j),2 if h else 1))
 vals=[k(81,82),k(83,84),k(132,133,True),k(87,88,True),k(55,56)]
 replacements=[p for name in ('Q1','Mw+L','Q3') for p in field_table(tab[name],vals)]
 ids={i:j+1 for j,i in enumerate(c['id'] for c in old['coordinates'] if c['id'] not in (85,86))}
 expected=[]
 for r in old['residuals']:
  if r['id'] in (23,24):continue
  p=replacements[r['id']-17] if 17<=r['id']<=22 else read(r)
  ck(not any({85,86}&set(m) for a,m in p),'removed coordinate used');p=prim(p)
  p={(a,tuple(sorted(ids[i] for i in m))):c for (a,m),c in p.items()};expected.append(p)
 ck(len(obj['coordinates'])==n-2 and len(expected)==len(obj['residuals']),'count')
 ck([read(r) for r in obj['residuals']]==expected,'rows')
 full=expanded(obj['residuals']);ck(full==read(poly),'expanded coefficients')
 ck(gcd(*(int(c) for c in full.values()))==1 and max(len(m) for a,m in full)==4,'degree/content')
 ck({i for a,m in full for i in m}==set(range(1,n-1)),'coordinate occurrences')
 prof=defaultdict(dict)
 for (a,m),c in full.items():prof[m][a]=int(c)
 ck([p for p in prof.values() if 2 in p]==[{0:1,2:1}],'attained height')
 A=149**107
 for p in prof.values():
  ck(set(p) in ({0},{1},{0,2}),'profile')
  if set(p)=={0}:ck(abs(p[0])<A*A+1,'constant bound')
  if set(p)=={1}:ck(abs(p[1])<=A,'linear bound')
 return dict(variables=n-2,rows=len(expected),monomials=len(prof),heightForNAtLeast53='149^(4N+2)+1')

def verify81():
 folder=HERE.parent/'pole81_v27';old=json.loads((HERE.parent/'abc81_v25/quadratic-family.json').read_text());new=json.loads((folder/'quadratic.json').read_text());poly=json.loads((folder/'polynomial.json').read_text());ids={c['name']:c['id'] for c in old['coordinates']}
 expected=[]
 for r in old['residuals']:
  p=read(r)
  for j in (0,1):
   pre=f'detector{j}.';v=lambda s:V(ids[pre+s]);b,e,u,vv,p2,q2=(v(s) for s in ('poleInput','pole.e','pole.u','pole.v','pole.pSquare','pole.qSquare'))
   if r['name']==pre+'pole.first':p=add(mul(e,e),mul(b,p2),C(-1))
   elif r['name']==pre+'pole.factor':p=add(mul(u,vv),scale(e,-1),mul(e,b))
   elif r['name']==pre+'pole.second':p=add(mul(u,u),scale(mul(vv,vv),-1),scale(mul(b,q2),-1))
  expected.append(prim(p))
 ck(new['coordinates']==old['coordinates'] and [read(r) for r in new['residuals']]==expected,'81 rows')
 full=expanded(new['residuals']);ck(full==read(poly),'81 coefficients');prof=defaultdict(dict)
 for (a,m),c in full.items():prof[m][a]=int(c)
 ck(prof[()]=={0:630511,2:1},'81 constant');ck(max(abs(p[0]) for p in prof.values() if set(p)=={0})==4153456,'81 fixed height')
 ck(gcd(*(int(c) for c in full.values()))==1 and max(len(m) for a,m in full)==4,'81 degree/content')
 for p in prof.values():
  if 1 in p:ck(set(p)=={1} and abs(p[1])<=2,'81 linear')
  else:ck(set(p) in ({0},{0,2}),'81 profile')
 return dict(variables=81,rows=73,monomials=len(prof),height='max(4153456,B^2+630511)')

def main():
 results={};neg=0
 for n in (226,262):
  p=HERE/f'family{n-2}';obj=json.loads((p/'quadratic.json').read_text());poly=json.loads((p/'polynomial.json').read_text());results[str(n-2)]=verify(n,obj,poly)
  for typ in ('row','poly'):
   a=deepcopy(obj);b=deepcopy(poly)
   r=a['residuals'][17] if typ=='row' else b;r['terms'][0]['coefficient']=str(Q(r['terms'][0]['coefficient'])+1)
   try:verify(n,a,b)
   except ValueError:neg+=1
   else:raise ValueError('missed corruption')
 results['81']=verify81()
 report=dict(schema='reference-and-pole-independent-check/v27',status='PASS',results=results,corruptionsRejected=neg,independentImplementation=True,independentNonAuthorReview=False,scope='Exact all-row and all-coefficient checks. Point-domain equivalence uses the separately verified complete reference chart; arithmetic premises are unchanged for 224/260 and explicitly replaced for pole81.')
 (HERE/'independent-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
