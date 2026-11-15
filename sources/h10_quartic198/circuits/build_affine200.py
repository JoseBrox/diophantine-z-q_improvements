#!/usr/bin/env python3
"""Algebraic compiler of the affine-odd fourth-index candidate.
Arithmetic inheritance/completeness is a separate theorem, not verified here.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict
from hashlib import sha256
from math import gcd
import importlib.util,json
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'source/computation/quartic/reciprocal204_v27/unbalanced-quadratic.json'
spec=importlib.util.spec_from_file_location('core204',SOURCE.parent.parent/'abc81_v25/build.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)

def read(row):return {(t['parameterPower'],tuple(t['monomial'])):Q(t['coefficient']) for t in row['terms']}
def build():
 raw=SOURCE.read_bytes();old=json.loads(raw);removed=set(range(169,183));removed_rows=set(range(122,140))
 coords=[dict(x,source204Id=x['id']) for x in old['coordinates'] if x['id'] not in removed]
 nextid=205;newrows=[]
 def field(n):
  nonlocal nextid
  out=[]
  for j in range(2):
   coords.append(dict(id=nextid,name=n+'.'+str(j)));out.append(c.var(nextid));nextid+=1
  return tuple(out)
 def pair(i,j,half=False):return c.var(i),c.scale(c.var(j),2 if half else 1)
 def row(n,p):
  p=c.prim(p);assert max(len(m) for a,m in p)<=2,n
  newrows.append(dict(name=n,terms=c.serial(p)))
 def krow(n,p):row(n+'.0',p[0]);row(n+'.1',p[1])
 f=field('pair4.f');h=field('pair4.h');g=field('pair4.g');k=field('pair4.k');s=field('pair4.s')
 D=c.kconst(11,-6);one=c.kconst(1);FU=pair(60,61,True);FV=pair(29,30,True)
 L=pair(43,44);LP=pair(45,46);S=pair(19,20);T=pair(183,184)
 krow('pair4.square.f',c.diff(FU,c.power2(f)))
 krow('pair4.square.g',c.diff(FV,c.power2(g)))
 krow('pair4.curve',c.plus(c.power2(h),c.ktimes(-1,f),c.times(D,c.times(f,FU))))
 krow('pair4.secant',c.diff(c.times(s,c.diff(f,g)),c.plus(h,k)))
 krow('pair4.tangent',c.plus(c.times(s,c.diff(h,k)),c.ktimes(-1,one),c.times(D,c.plus(FU,c.times(f,g),FV))))
 for suffix,h1,f1,F1,L1,S1 in [('primary',h,f,FU,L,S),('alternate',k,g,FV,LP,T)]:
  affine=c.diff(L1,one)
  krow('pair4.ratio.'+suffix+'.raw',c.plus(c.times(h1,affine),c.ktimes(4,c.times(f1,S1))))
  krow('pair4.ratio.'+suffix+'.regular',c.plus(c.times(c.diff(one,c.times(D,F1)),affine),c.ktimes(4,c.times(h1,S1))))
 x4=c.plus(c.power2(s),c.times(D,c.plus(f,g)))
 R=c.rational(c.var(118));ls=c.pair if hasattr(c,'pair') else None
 L2=pair(35,36);L3=pair(39,40);L4=pair(43,44);CC=pair(48,49);AT=pair(50,51);FF=pair(52,53,True)
 changed={}
 for rid,n,p in [(2,'affine.Lucas.C',c.diff(c.times(c.diff(L2,R),L4),c.times(R,CC))), (4,'affine.Lucas.AT',c.diff(c.times(c.plus(L2,R),L3),c.times(R,AT))), (6,'affine.Lucas.F',c.diff(c.plus(c.power2(L3),c.power2(CC),c.ktimes(-1,c.times(CC,AT))),FF))]:
  changed[rid]=(n+'.0',c.prim(p[0]));changed[rid+1]=(n+'.1',c.prim(p[1]))
 agg=read(old['residuals'][143]);ce=c.diff(pair(173,174),pair(175,176));agg=c.add(agg,c.scale(c.power2(ce)[0],-1),c.scale(x4[0],4));changed[144]=('affine.weighted.aggregate',c.prim(agg))
 rr=[]
 for r in old['residuals']:
  if r['id'] in removed_rows:continue
  p=read(r);name=r['name']
  if r['id'] in changed:name,p=changed[r['id']]
  assert not any(set(m)&removed for a,m in p),name
  rr.append(dict(name=name,source204RowId=r['id'],terms=c.serial(p)))
 rr.extend(newrows);mapping={x['id']:i+1 for i,x in enumerate(coords)}
 for x in coords:x['id']=mapping[x['id']]
 for i,r in enumerate(rr):
  p={(a,tuple(sorted(mapping[v] for v in m))):coef for (a,m),coef in read(r).items()};r.update(id=i+1,terms=c.serial(p))
 poly=defaultdict(Q)
 for r in rr:
  for key,value in c.sq(read(r)).items():poly[key]+=value
 poly={key:value for key,value in poly.items() if value};profiles=defaultdict(dict)
 for (a,m),coef in poly.items():profiles[m][a]=int(coef)
 assert len(coords)==200 and len(rr)==186
 assert max(len(m) for a,m in poly)==4 and gcd(*(int(v) for v in poly.values()))==1
 assert {v for a,m in poly for v in m}==set(range(1,201))
 out=HERE/'affine200';out.mkdir(exist_ok=True)
 system=dict(format='affine-odd-fourth-index-candidate',variables=200,inputCoordinate=1,fixedParameter=old['fixedParameter'],coordinates=coords,residuals=rr)
 full=dict(format='affine200-quartic-candidate',variables=200,degree=4,inputCoordinate=1,fixedParameter=old['fixedParameter'],terms=c.serial(poly))
 report=dict(status='Algebraic construction. Arithmetic proof separately required.',sourceSha256=sha256(raw).hexdigest(),variables=200,quadraticRows=186,degree=4,coordinateMonomials=len(profiles),parameterSeparatedTerms=len(poly),coefficientContent=gcd(*(int(v) for v in poly.values())),removedSourceCoordinates=sorted(removed),removedSourceRows=sorted(removed_rows),changedSourceRows=sorted(changed),fourthLabel='b=4*nu(Q4)+1',lucasParameter='a+1',lucas='t^2-(a+1)*(a-1)*t*b+(a-1)^2*b^2-1',aggregate='Tr(x(Q1)+x(Q3)+x(Q4)+R^2*x(Q2))/4')
 for fn,obj in [('quadratic.json',system),('polynomial.json',full),('construction-report.json',report)]: (out/fn).write_text(json.dumps(obj,indent=2)+'\n')
 print(json.dumps(report,indent=2));return system
if __name__=='__main__':build()
