#!/usr/bin/env python3
"""Independently reconstruct the 79-variable system and every coefficient."""
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict
from hashlib import sha256
from math import gcd,isqrt
from copy import deepcopy
import importlib.util,sys,json
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('independent_sparse',HERE.parent/'reciprocal204_v27/check.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
ck=p.ck;C=p.C;V=p.V;add=p.plus;neg=p.neg;scale=p.scaled;mul=p.prod;norm=p.norm;rd=p.read;ka=p.ka;km=p.km;kn=p.kn;K=p.K

def reconstruct(old,system):
 names={c['name']:c['id'] for c in system['coordinates']};oldnames={c['id']:c['name'] for c in old['coordinates']}
 ck(set(oldnames.values())-set(names)=={'common.g.0','common.g.1'},'coordinate removal')
 ck(len(names)==79 and names['input']==1,'variable count')
 def scalar(n):return V(names[n])
 def field(n):return scalar(n+'.0'),scalar(n+'.1')
 def fp(name,values,eq):
  out=K(0)
  for t in eq[name]:
   term=K(Q(t['c'][0]),Q(t['c'][1]))
   for j in t['m']:term=km(term,values[j-1])
   out=ka(out,term)
  return out
 equations=json.loads((HERE/'reference-equations.json').read_text())['equations']
 S=field('common.S');T=field('common.T');f=field('common.f');B=field('square.common.f');w=field('square.common.g')
 expected={}
 def kr(name,z):
  for j,t in enumerate(z):expected[name+'.'+str(j)]=norm(t)
 kr('common.fSquare',ka(B,kn(km(f,f))))
 for row,key in [('first','Q1'),('second','Mw+L'),('third','Q3')]:kr('common.'+row,fp(key,[f,S,B,w,T],equations))
 deleted={f'common.{n}.{j}' for n in ('first','second','third') for j in (0,1)}|{f'square.common.{n}.{j}' for n in ('f','g') for j in (0,1)}
 for row in old['residuals']:
  name=row['name']
  if name in deleted:continue
  poly={(a,tuple(sorted(names[oldnames[i]] for i in m))):c for (a,m),c in rd(row).items()}
  for j in (0,1):
   prefix=f'detector{j}.pole.';e=scalar(prefix+'e');u=scalar(prefix+'u');v=scalar(prefix+'v');bp=scalar(f'detector{j}.poleInput');p2=scalar(prefix+'pSquare');q2=scalar(prefix+'qSquare')
   if name==prefix+'first':poly=add(mul(e,e),mul(bp,p2),C(-1))
   if name==prefix+'factor':poly=add(mul(u,v),neg(e),mul(e,bp))
   if name==prefix+'second':poly=add(mul(u,u),neg(mul(v,v)),neg(mul(bp,q2)))
  expected[name]=norm(poly)
 ck(len(expected)==71,'expected row count')
 ck(len(system['residuals'])==71 and len({r['name'] for r in system['residuals']})==71,'row inventory')
 for r in system['residuals']:
  ck(r['name'] in expected and rd(r)==expected[r['name']],'row identity '+r['name'])
  ck(max(len(m) for a,m in rd(r))<=2,'quadratic degree')
 return expected

def check(old,system,poly):
 ex=reconstruct(old,system);ans=defaultdict(Q)
 for r in ex.values():
  ts=list(r.items())
  for i,((a,m),c) in enumerate(ts):
   for j in range(i,len(ts)):
    (b,n),d=ts[j];ans[a+b,tuple(sorted(m+n))]+=(1 if i==j else 2)*c*d
 ans={m:c for m,c in ans.items() if c};ck(ans==rd(poly),'full quartic')
 ck(gcd(*(int(x) for x in ans.values()))==1 and max(len(m) for a,m in ans)==4,'degree/content')
 ck({i for a,m in ans for i in m}==set(range(1,80)),'support census')
 profiles=defaultdict(dict)
 for (a,m),c in ans.items():profiles[m][a]=int(c)
 kk=max(abs(q[0]) for q in profiles.values() if set(q)=={0});hh=profiles[()][0]
 ck(all(set(q) in ({0},{1},{0,2}) for q in profiles.values()),'parameter profiles')
 ck(profiles[()][2]==1 and hh>0,'constant coefficient')
 sw=max(3,isqrt(max(0,kk-hh))+1)
 for q in profiles.values():
  if 1 in q:
   cc=abs(q[1]);ck(3*cc<=max(kk,hh+9),'small height')
   ck((sw-1)*cc<=kk if sw>3 else True,'middle height');ck(sw*sw+hh>=cc*sw and 2*sw>=cc,'large height')
 return dict(variables=79,quadraticRows=71,degree=4,content=1,coordinateMonomials=len(profiles),parameterSeparatedTerms=len(ans),largestFixedCoefficient=str(kk),constantCoefficient=str(hh))

def main():
 old=json.loads((HERE.parent/'abc81_v25/quadratic-family.json').read_text());system=json.loads((HERE/'quadratic-family.json').read_text());poly=json.loads((HERE/'polynomial-family.json').read_text())
 result=check(old,system,poly);rejected=0
 for label in ('pole','reference','coefficient'):
  ss=deepcopy(system);pp=deepcopy(poly)
  if label=='coefficient':pp['terms'][0]['coefficient']=str(int(pp['terms'][0]['coefficient'])+1)
  else:
   name='detector0.pole.first' if label=='pole' else 'common.second.0';rr=next(r for r in ss['residuals'] if r['name']==name);rr['terms'][0]['coefficient']=str(Q(rr['terms'][0]['coefficient'])+1)
  try:check(old,ss,pp)
  except ValueError:rejected+=1
  else:raise ValueError('undetected corruption '+label)
 report=dict(schema='abc79-independent-verification/v27',status='PASS',**result,corruptionsRejected=rejected,referenceCertificate='reference-verification.json',scope='Complete equation and coefficient reconstruction. The new congruent-twist pole proof and arithmetic projection require their written hypotheses and arguments; this is not a full external-source audit or a non-author review.')
 (HERE/'independent-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
