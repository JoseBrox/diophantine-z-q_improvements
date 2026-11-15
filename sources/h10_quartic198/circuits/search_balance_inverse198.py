#!/usr/bin/env python3
from pathlib import Path
import json,numpy as np,importlib.util
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
from fractions import Fraction as Q
from collections import defaultdict
H=Path(__file__).parent;s=importlib.util.spec_from_file_location('a',H/'build_affine200.py');a=importlib.util.module_from_spec(s);s.loader.exec_module(a);c=a.c
d=json.loads((H/'inverse198/quadratic.json').read_text());n=d['variables'];rows=d['residuals'];cons=[];lo=[];hi=[]
for ri,r in enumerate(rows):
 for t in r['terms']:
  q={}
  for v in t['monomial']:q[v-1]=q.get(v-1,0)+1
  q[n+ri]=-1;cons.append(q);lo.append(-2*t['parameterPower']);hi.append((0 if abs(int(t['coefficient'])*149**t['parameterPower'])>31581660**14 else 1)-2*t['parameterPower'])
mat=lil_matrix((len(cons),n+len(rows)))
for r,q in enumerate(cons):
 for col,v in q.items():mat[r,col]=v
lb=np.full(mat.shape[1],-50.);ub=np.full(mat.shape[1],50.);lb[0]=ub[0]=0
res=milp(np.zeros(mat.shape[1]),integrality=np.ones(mat.shape[1]),bounds=Bounds(lb,ub),constraints=LinearConstraint(mat.tocsr(),np.array(lo),np.array(hi)),options={'time_limit':25})
print(res.message,flush=True)
if res.x is None:raise SystemExit()
w={i+1:int(round(res.x[i])) for i in range(n)};rr=[]
for r in rows:
 p=a.read(r);power=min(2*ap+sum(w[i] for i in mm) for ap,mm in p);p={(2*ap+sum(w[i] for i in mm)-power,mm):cf*149**ap for (ap,mm),cf in p.items()};assert max(ap for ap,mm in p)<=1
 rr.append(dict(r,dividedCPower=power,terms=c.serial(c.prim(p))))
poly=defaultdict(Q)
for r in rr:
 for key,val in c.sq(a.read(r)).items():poly[key]+=val
poly={key:val for key,val in poly.items() if val};profiles=defaultdict(dict)
for (ap,mm),cf in poly.items():profiles[mm][ap]=int(cf)
C0=max(abs(p.get(0,0)) for p in profiles.values());C2=max(abs(p.get(2,0)) for p in profiles.values());C1=max(abs(p.get(1,0)) for p in profiles.values());print('vars',n,'monomials',len(profiles),'terms',len(poly),'C0digits',len(str(C0)),'C2digits',len(str(C2)),'C1digits',len(str(C1)),flush=True)
K=31581660**28;H0=(5898050446009651968*K)**2
print('same height targets?',C0==H0,C2==K,flush=True)
parameter=dict(d['fixedParameter'],symbol='C',value='149^N')
report=dict(status='Coefficient balancing of the conditional198construction; arithmetic proof separate',weights=w,variables=n,quadraticRows=len(rr),coordinateMonomials=len(profiles),parameterSeparatedTerms=len(poly),C0=str(C0),C1=str(C1),C2=str(C2),exactHeight='max((5898050446009651968*31581660^28)^2,31581660^28*149^(2N))',coefficientCrossoverN=57)
for fn,obj in [('balanced-quadratic.json',dict(d,fixedParameter=parameter,residuals=rr)),('balanced-polynomial.json',dict(format='balanced-inverse198',variables=n,degree=4,inputCoordinate=1,fixedParameter=parameter,terms=c.serial(poly))),('balanced-report.json',report)]: (H/'inverse198'/fn).write_text(json.dumps(obj,indent=2)+'\n')
