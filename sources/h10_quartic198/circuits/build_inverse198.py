#!/usr/bin/env python3
"""Inverse Vieta scalar chart with exact R rescaling; arithmetic theorem separate."""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd
import importlib.util,json
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('affine',HERE/'build_affine200.py');a=importlib.util.module_from_spec(s);s.loader.exec_module(a);c=a.c
SOURCE=HERE/'affine200/quadratic.json'

def build():
 raw=SOURCE.read_bytes();old=json.loads(raw);lift={co['id']:co.get('source204Id',205+co['id']-191) for co in old['coordinates']}
 coords=[dict(co,id=lift[co['id']],source200Id=co['id']) for co in old['coordinates']]
 remove=set([2,3]+list(range(155,169)));coords=[co for co in coords if co['id'] not in remove]
 def pair(i):return c.var(i),c.var(i+1)
 def half(i):return c.var(i),c.scale(c.var(i+1),2)
 newrows=[]
 def kr(name,z):
  for j in range(2):newrows.append(dict(name=name+'.'+str(j),terms=c.serial(z[j])))
 D=c.kconst(11,-6);R=c.rational(c.var(118));u,v,w,m,r,p,r2=[pair(i) for i in range(215,229,2)]
 for i in range(215,229):coords.append(dict(id=i,name='scalar.inverseVieta.'+['u','v','w','m','r','p','r2'][(i-215)//2]+'.'+str((i-215)%2),unscaledFormalId=i))
 FU=half(56);FV=half(25);L=pair(35);LP=pair(37);Z=pair(107);S=pair(19);TH=pair(183)
 kr('inverse_vieta.product',c.diff(p,c.times(u,v)))
 kr('inverse_vieta.r',c.diff(r,c.times(p,w)))
 kr('inverse_vieta.sum',c.plus(c.times(r,c.plus(u,v,w,c.ktimes(2,m))),D))
 kr('inverse_vieta.pair',c.diff(c.plus(p,c.times(w,c.plus(u,v))),c.power2(m)))
 kr('inverse_vieta.r2',c.diff(r2,c.power2(r)))
 kr('inverse_vieta.fusquare',c.diff(c.times(FU,r2),c.power2(u)))
 kr('inverse_vieta.fvsquare',c.diff(c.times(FV,r2),c.power2(v)))
 kr('inverse_vieta.primary',c.diff(c.times(L,c.plus(m,u)),c.ktimes(2,c.times(R,S))))
 kr('inverse_vieta.alternate',c.plus(c.times(LP,c.plus(m,v)),c.ktimes(2,c.times(R,TH))))
 kr('inverse_vieta.scalar',c.plus(c.times(R,c.times(Z,c.plus(m,w))),c.ktimes(2,S)))
 remrows=set(range(104,122))|set(range(140,145));rows=[]
 for row in old['residuals']:
  if row.get('source204RowId') in remrows:continue
  pp={(ap,tuple(sorted(lift[i] for i in mm))):cf for (ap,mm),cf in a.read(row).items()}
  rows.append(dict(row,source200RowId=row['id'],terms=c.serial(pp)))
 rows.extend(newrows)
 weights={int(i):v for i,v in json.loads((HERE/'inverse-vieta-rescaling-search.json').read_text())['weights'].items()}
 rescaled=[]
 for row in rows:
  pp=a.read(row)
  if row['name']=='scalar.r_power_2.definition':e0=0 # retain defining equation R2=R^2, never simplify it away
  else:
   tt=[]
   for (ap,mm),cf in pp.items():
    e=sum(weights.get(i,0) for i in mm)+mm.count(118)+2*mm.count(117);nn=tuple(i for i in mm if i not in(117,118));tt.append((ap,nn,e,cf))
   e0=min(e for ap,nn,e,cf in tt);qq=defaultdict(Q)
   for ap,nn,e,cf in tt:
    e-=e0;assert e>=0
    factors=(117,)*(e//2)+(118,)*(e%2);monomial=tuple(sorted(nn+factors));assert len(monomial)<=2,(row['name'],monomial)
    qq[ap,monomial]+=cf
   pp={key:value for key,value in qq.items() if value}
  pp=c.prim(pp);rescaled.append(dict(row,dividedRPower=e0,terms=c.serial(pp)))
 # Native p is exactly the fourth reciprocal difference's abscissa x(Q2).
 agg=c.add(c.scale(c.sub(c.var(4),c.var(90)),8),c.con(56),c.scale(p[0],4))
 for fi,gi,si in [(185,189,193),(195,199,203),(205,209,213)]:agg=c.add(agg,c.scale(c.plus(c.power2(pair(si)),c.times(D,c.plus(pair(fi),pair(gi))))[0],4))
 rescaled.append(dict(name='inverse_vieta.unweighted.aggregate',terms=c.serial(c.prim(agg))))
 mapping={co['id']:i+1 for i,co in enumerate(coords)}
 for co in coords:
  oldid=co['id'];co.update(id=mapping[oldid],formalId=oldid,rescalingExponent=weights.get(oldid,0))
 for i,row in enumerate(rescaled):
  pp={(ap,tuple(sorted(mapping[j] for j in mm))):cf for (ap,mm),cf in a.read(row).items()};row.update(id=i+1,terms=c.serial(pp))
 poly=defaultdict(Q)
 for row in rescaled:
  for key,value in c.sq(a.read(row)).items():poly[key]+=value
 poly={key:value for key,value in poly.items() if value};profiles=defaultdict(dict)
 for (ap,mm),cf in poly.items():profiles[mm][ap]=int(cf)
 assert len(coords)==198 and len(rescaled)==184
 assert max(len(mm) for ap,mm in poly)==4 and gcd(*(int(cf) for cf in poly.values()))==1
 assert {v for ap,mm in poly for v in mm}==set(range(1,199))
 out=HERE/'inverse198';out.mkdir(exist_ok=True)
 system=dict(format='inverse-vieta198',variables=198,inputCoordinate=1,fixedParameter=old['fixedParameter'],coordinates=coords,residuals=rescaled)
 full=dict(format='inverse-vieta198-quartic',variables=198,degree=4,inputCoordinate=1,fixedParameter=old['fixedParameter'],terms=c.serial(poly))
 report=dict(status='Conditional arithmetic proof provided in ../../arithmetic/inverse_vieta_198.tex; inherited premises retained',variables=198,degree=4,quadraticRows=184,coordinateMonomials=len(profiles),parameterSeparatedTerms=len(poly),source200Sha256=sha256(raw).hexdigest(),rescalingWeights=weights,aggregate='7+Tr(x(Q1)+x(Q2)+x(Q3)+x(Q4))/4',scalarLabel='a=2*nu(Q2)',scalarQuotient='Z=2*z(Q2)/z(H)',guard='R!=0 follows positive scalar contact polynomial; r!=0 follows r*(u+v+w+2m)+D*R^2=0',scope='Compiler certifies the algebraic construction only; arithmetic projection is established separately under the inherited premises.')
 for fn,obj in [('quadratic.json',system),('polynomial.json',full),('construction-report.json',report)]: (out/fn).write_text(json.dumps(obj,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k!='rescalingWeights'},indent=2))
 return system
if __name__=='__main__':build()
