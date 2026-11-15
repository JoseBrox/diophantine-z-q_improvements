#!/usr/bin/env python3
"""Independent Laurent-row reconstruction, generic chart identities, expansion."""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction as F
from math import gcd
from hashlib import sha256
import json,sympy as sp
H=Path(__file__).resolve().parent
old=json.loads((H/'affine200/quadratic.json').read_text());new=json.loads((H/'inverse198/quadratic.json').read_text())
assert sha256((H/'affine200/quadratic.json').read_bytes()).hexdigest()=='c64674ece62e299e119824fa3daaadb0b5baaf11456cc34441f05dc2ba8c2606'
x=sp.symbols('x1:229');A=sp.Symbol('A');X=lambda i:x[i-1]
lift_old={c['id']:c.get('source204Id',205+c['id']-191) for c in old['coordinates']};lift_new={c['id']:c['formalId'] for c in new['coordinates']};weights={c['formalId']:c['rescalingExponent'] for c in new['coordinates']}
def parse(row,lift=None):return {(t['parameterPower'],tuple(sorted(lift[i] if lift else i for i in t['monomial']))):F(t['coefficient']) for t in row['terms']}
def laurent(p,reverse=False):
 out=defaultdict(F)
 for (ap,mm),c in p.items():
  e=mm.count(118)+2*mm.count(117)
  if reverse:e-=sum(weights.get(i,0) for i in mm)
  rest=tuple(i for i in mm if i not in(117,118));out[ap,e,rest]+=c
 return {k:v for k,v in out.items() if v}
def normalize(p):
 if not p:return p
 lead=p[min(p)];return {k:v/lead for k,v in p.items()}
def pair(i):return sp.Matrix([X(i),X(i+1)])
def half(i):return sp.Matrix([X(i),2*X(i+1)])
def mul(u,v):return sp.Matrix([u[0]*v[0]+2*u[1]*v[1],u[0]*v[1]+u[1]*v[0]])
def sq(u):return mul(u,u)
def symparse(e):
 syms=sorted(e.free_symbols,key=str);q=sp.Poly(sp.expand(e),*syms);out={}
 for exps,c in q.terms():
  ap=0;mm=[]
  for sy,ep in zip(syms,exps):
   if sy==A:ap=ep
   else:mm.extend([int(str(sy)[1:])]*ep)
  out[ap,tuple(sorted(mm))]=F(c)
 return out
expected={r['name']:laurent(parse(r,lift_old)) for r in old['residuals'] if r.get('source204RowId') not in set(range(104,122))|set(range(140,145)) and r['name']!='scalar.r_power_2.definition'}
u,v,w,m,r,p,r2=[pair(i) for i in range(215,229,2)];D=sp.Matrix([11,-6]);R=sp.Matrix([X(118),0]);FU=half(56);FV=half(25);L=pair(35);LP=pair(37);Z=pair(107);S=pair(19);T=pair(183)
rels={
 'inverse_vieta.product':p-mul(u,v),'inverse_vieta.r':r-mul(p,w),'inverse_vieta.sum':mul(r,u+v+w+2*m)+D,
 'inverse_vieta.pair':p+mul(w,u+v)-sq(m),'inverse_vieta.r2':r2-sq(r),
 'inverse_vieta.fusquare':mul(FU,r2)-sq(u),'inverse_vieta.fvsquare':mul(FV,r2)-sq(v),
 'inverse_vieta.primary':mul(L,m+u)-2*mul(R,S),'inverse_vieta.alternate':mul(LP,m+v)+2*mul(R,T),
 'inverse_vieta.scalar':mul(R,mul(Z,m+w))+2*S}
for name,z in rels.items():
 for j in range(2):expected[name+'.'+str(j)]=laurent(symparse(z[j]))
count=0
for row in new['residuals']:
 if row['name'] in('scalar.r_power_2.definition','inverse_vieta.unweighted.aggregate'):continue
 got=laurent(parse(row,lift_new),True);shift=row['dividedRPower'];got={(ap,e+shift,mm):cf for (ap,e,mm),cf in got.items()}
 assert normalize(got)==normalize(expected.pop(row['name'])),row['name'];count+=1
assert not expected
rrow=next(r for r in new['residuals'] if r['name']=='scalar.r_power_2.definition');assert normalize(parse(rrow,lift_new))==normalize({(0,(117,)):F(1),(0,(118,118)):F(-1)})
agg=8*(X(4)-X(90))+56+4*X(225)
for fi,gi,si in [(185,189,193),(195,199,203),(205,209,213)]:agg+=4*(sq(pair(si))+mul(D,pair(fi)+pair(gi)))[0]
aggrow=next(r for r in new['residuals'] if r['name']=='inverse_vieta.unweighted.aggregate');assert normalize(parse(aggrow,lift_new))==normalize(symparse(agg))
# Generic unscaled normalized chart: both point equations and difference abscissa p.
u0,v0,w0,m0,r0,p0,d0=sp.symbols('u v w m r p D')
ideal=[p0-u0*v0,r0-p0*w0,r0*(u0+v0+w0+2*m0)+d0,p0+w0*(u0+v0)-m0*m0]
gb=sp.groebner(ideal,m0,r0,p0,d0,w0,v0,u0)
ids=[r0*u0*(m0+u0)**2-r0*r0+d0*u0*u0,r0*v0*(m0+v0)**2-r0*r0+d0*v0*v0,p0*(m0+w0)**2-p0*p0+d0]
for poly in ids:assert gb.reduce(poly)[1]==0
# Independent unordered term-pair expansion.
exp=defaultdict(F)
for row in new['residuals']:
 pp=list(parse(row).items())
 for i,((ap,mm),cf) in enumerate(pp):
  for j in range(i,len(pp)):
   (aq,nn),cc=pp[j];exp[ap+aq,tuple(sorted(mm+nn))]+=cf*cc*(1 if i==j else 2)
exp={key:val for key,val in exp.items() if val};assert exp==parse(json.loads((H/'inverse198/polynomial.json').read_text()))
profiles=defaultdict(dict)
for (ap,mm),cf in exp.items():profiles[mm][ap]=int(cf)
assert len(new['coordinates'])==198 and len(new['residuals'])==184
assert len(profiles)==2945 and len(exp)==2945 and max(len(mm) for ap,mm in exp)==4
assert {v for ap,mm in exp for v in mm}==set(range(1,199)) and gcd(*(int(v) for v in exp.values()))==1
assert all(len(p)==1 for p in profiles.values()) # no support cancellations for positive A
C0=max(abs(p.get(0,0)) for p in profiles.values());C1=max(abs(p.get(1,0)) for p in profiles.values());C2=max(abs(p.get(2,0)) for p in profiles.values());assert C2==1 and C1<=149**3
assert len(str(C0))==458 and 149**210<C0<=149**214
report=dict(variables=198,quadraticRows=184,degree=4,coordinateMonomials=2945,parameterSeparatedTerms=2945,content=1,independentLaurentRowChecks=count,genericChartIdentities=3,independentExpansion=True,exactHeight='max(C0,A^2)',C0=str(C0),C0DecimalDigits=458,coefficientCrossoverN=53,A='149^(2N+1),N>=1',scope='Algebraic checks; scalar arithmetic and completeness transfer remains separate.')
(H/'inverse198/independent-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
