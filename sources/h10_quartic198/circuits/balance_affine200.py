#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict
import json,importlib.util
P=Path(__file__).parent;s=importlib.util.spec_from_file_location('a',P/'build_affine200.py');a=importlib.util.module_from_spec(s);s.loader.exec_module(a);c=a.c
D=json.loads((P/'affine200/quadratic.json').read_text());rids={v['id'] for v in D['coordinates'] if v.get('source204Id') in (117,118)}
rr=[]
for r in D['residuals']:
 p=a.read(r);e=min(2*ap+sum(i in rids for i in mm) for ap,mm in p);p={(2*ap+sum(i in rids for i in mm)-e,mm):coeff*149**ap for (ap,mm),coeff in p.items()};p=c.prim(p)
 assert max(ap for ap,mm in p)<=1
 rr.append(dict(r,divided_C_power=e,terms=c.serial(p)))
poly=defaultdict(Q)
for r in rr:
 for key,v in c.sq(a.read(r)).items():poly[key]+=v
poly={k:v for k,v in poly.items() if v};profiles=defaultdict(dict)
for (ap,mm),v in poly.items():profiles[mm][ap]=int(v)
K=31581660**28;J=5898050446009651968;H0=(J*K)**2
assert max(abs(p.get(0,0)) for p in profiles.values())==H0
assert max(abs(p.get(2,0)) for p in profiles.values())==K
for p in profiles.values():
 if set(p)=={1}:assert p[1]**2<=H0*K
 else:assert set(p)<={0,2} and abs(p.get(0,0))*K+abs(p.get(2,0))*H0<=H0*K
parameter=dict(D['fixedParameter'],symbol='C',value='149^N');out=P/'affine200'
for fn,obj in [('balanced-quadratic.json',dict(D,residuals=rr,fixedParameter=parameter)),('balanced-polynomial.json',dict(format='balanced-affine200',variables=200,degree=4,inputCoordinate=1,fixedParameter=parameter,terms=c.serial(poly)))]: (out/fn).write_text(json.dumps(obj,indent=2)+'\n')
report=dict(variables=200,degree=4,quadraticRows=len(rr),coordinateMonomials=len(profiles),parameterSeparatedTerms=len(poly),exactHeight='max((5898050446009651968*31581660^28)^2,31581660^28*149^(2N))',coefficientCrossoverN=57,scope='Coefficientbound only; no definingthreshold asserted')
(out/'balanced-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
