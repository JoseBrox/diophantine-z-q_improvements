#!/usr/bin/env python3
"""Check all compressed-reference identities with rational arithmetic only.

No symbolic producer is imported. The equation table is reconstructed
against all six original rational component rows, including every imaginary
coefficient; certificates are checked against independently formed targets.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from copy import deepcopy
from math import gcd,lcm
import json,importlib.util
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('independent_field',HERE.parent/'abc81_v25/check_examples.py');mod=importlib.util.module_from_spec(sp)
import sys
sys.modules[sp.name]=mod;sp.loader.exec_module(mod);K=mod.K
Z=K();O=K(1)
def ck(b,m):
 if not b:raise ValueError(m)
def add(*ps):
 out={}
 for p in ps:
  for m,c in p.items():out[m]=out.get(m,Z)+c
 return {m:c for m,c in out.items() if c}
def sc(p,c):return {m:c*v for m,v in p.items() if c*v}
def mul(p,q):
 out={}
 for m,c in p.items():
  for n,d in q.items():
   k=tuple(a+b for a,b in zip(m,n));out[k]=out.get(k,Z)+c*d
 return {m:c for m,c in out.items() if c}
def const(c,n=3):return {(0,)*n:K.coerce(c)} if c else {}
def var(i,n=3):return {tuple(int(j==i) for j in range(n)):O}
def power(p,n):
 out=const(1,len(next(iter(p), (0,0,0))))
 for _ in range(n):out=mul(out,p)
 return out
def sub(p,q):return add(p,sc(q,-1))
def parsed(items):return {tuple(t['m']):K(F(t['c'][0]),F(t['c'][1])) for t in items if F(t['c'][0]) or F(t['c'][1])}
def tablepoly(items,values):
 ans={}
 for t in items:
  p=const(K(F(t['c'][0]),F(t['c'][1])),len(next(iter(values[0]))))
  for i in t['m']:p=mul(p,values[i-1])
  ans=add(ans,p)
 return ans
def normalize(p):
 p={m:c for m,c in p.items() if c};d=lcm(*(x.denominator for x in p.values()));g=gcd(*(int(d*x) for x in p.values()))
 if p[min(p)]<0:g=-g
 return {m:c*F(d,g) for m,c in p.items()}

def check(data,cert):
 T,S,f=(var(i) for i in range(3));one=const(1);D=K(11,-6);a=K(F(57,8),F(-7,2));b=K(F(-165,8),F(417,32))
 vals=[f,S,power(f,2),{},T]
 eq=data['equations'];Q1=tablepoly(eq['Q1'],vals);Q3=tablepoly(eq['Q3'],vals);M=tablepoly(eq['M'],vals);L=tablepoly(eq['L'],vals)
 ck(Q1==parsed(cert['Q1']) and Q3==parsed(cert['Q3']),'equation certificate binding')
 # Validate the full field equations against the retained 212 component rows.
 # The stored w and B imaginary coordinates are half coefficients in that file.
 vv=[]
 for j in range(5):vv.append(add(var(2*j,10),sc(var(2*j+1,10),K(0,2 if j in (2,3) else 1))))
 parent=json.loads((HERE.parent/'additive212_v25/unbalanced-quadratic.json').read_text())
 indices=[17,18,19,20,66,67,21,22,211,212]
 for name,rows in [('Q1',(181,182)),('Mw+L',(183,184)),('Q3',(185,186))]:
  pp=tablepoly(eq[name],vv)
  for k,rid in enumerate(rows):
   component={m:(c.a if k==0 else c.b) for m,c in pp.items() if (c.a if k==0 else c.b)}
   target={tuple(t['monomial'].count(i) for i in indices):F(t['coefficient']) for t in parent['residuals'][rid-1]['terms']}
   ck(normalize(component)==normalize(target),'source component '+name+str(k))
 # In particular Mw+L must literally be the displayed product plus L.
 fullvals=[var(j,5) for j in range(5)]
 ck(tablepoly(eq['Mw+L'],fullvals)==add(mul(tablepoly(eq['M'],fullvals),fullvals[3]),tablepoly(eq['L'],fullvals)),'M,w,L identity')
 g=sc(add(mul(add(sc(S,K(118,60)),const(K(156,F(69,2)))),T),sc(S,-K(156,F(69,2))),const(K(288,128))),1/K(252,-672))
 AP=a*a+D;BP=a*a-D
 Lf=sc(sub(sc(T,a),const(b)),2*b*D);Lg=sc(add(sc(S,a),const(b)),2*b*D)
 Qf=add(sc(mul(S,T),a*AP),sc(S,b*AP),sc(T,-b*BP),const(4*a*a*D))
 Qg=add(sc(mul(S,T),-a*AP),sc(S,-b*BP),sc(T,b*AP),const(-4*a*a*D))
 curve=add(mul(f,power(S,2)),sc(power(f,2),D),const(-1))
 targets={'curve':curve,'first':sub(mul(Lf,f),Qf),'second':sub(mul(Lg,power(g,2)),mul(f,Qg)),
 'third':add(sc(mul(f,power(g,2)),D*D),sc(add(power(f,2),power(g,2)),a*D),mul(f,add(sc(mul(S,T),a),sc(sub(S,T),b),const(D)))),
 'weight':add(mul(M,power(g,4)),mul(power(f,2),L))}
 for item in cert['identities']:
  name=item['name'];ck(parsed(item['target'])==targets[name],'wrong target '+name)
  ck(add(mul(parsed(item['U']),Q1),mul(parsed(item['V']),Q3))==targets[name],'failed identity '+name)
 ck(set(targets)=={i['name'] for i in cert['identities']},'identity inventory')
 NN=add(sc(S,b*AP),const(4*a*a*D),sc(f,2*b*b*D));DD=add(sc(f,2*a*b*D),sc(S,-a*AP),const(b*BP))
 for item in cert['forward']:
  ff={'Q1':Q1,'Q3':Q3}[item['name']];deg=max(m[0] for m in ff);ck(deg==item['degreeT'],'forward T degree')
  out={}
  for m,c in ff.items():out=add(out,sc(mul(mul(power(NN,m[0]),power(DD,deg-m[0])),mul(power(S,m[1]),power(f,m[2]))),c))
  ck(out==parsed(item['target']) and out==mul(parsed(item['quotient']),curve),'forward identity')
 # Independent exclusion of the exceptional coefficient M=0.
 A=M[(0,0,1)];JJ=M[(0,1,0)];CC=M[(0,0,0)]
 f0=K(F(-291,392),F(-17,196));u=K(F(52622151001413627,18285146020539272),F(-3405676270753831,9142573010269636));v=K(F(-49748909256632945837931754176,106615613836876012413675285169),F(17501993153580871856729407104,106615613836876012413675285169))
 quintic=add(mul(f,power(add(power(f,2),sc(f,A),const(CC)),2)),sc(add(sc(power(f,2),D),const(-1)),JJ*JJ))
 factor=mul(power(sub(f,const(f0)),3),add(power(f,2),sc(f,u),const(v)));ck(quintic==factor,'quintic factorization')
 disc=u*u-4*v;dn=disc.a*disc.a-2*disc.b*disc.b
 ck(dn==F(42669856913571796524289,458737743363289255936),'discriminant norm')
 num,den=dn.numerator,dn.denominator
 def valuation(x,p):
  n=0
  while x%p==0:x//=p;n+=1
  return n
 ck(valuation(num,73)-valuation(den,73)==1,'norm obstruction at 73')
 s0=-(f0*f0+A*f0+CC)/JJ;ck(s0==K(F(87,41),F(-129,164)),'exceptional S')
 q1at={}
 for m,c in Q1.items():
  mm=(m[0],0,0);q1at[mm]=q1at.get(mm,Z)+c*(s0**m[1])*(f0**m[2])
 q1at={m:c for m,c in q1at.items() if c}
 bad=K(F(-743972797947,65974395272),F(139322800357,16493598818))
 ck(q1at==const(bad) and bool(bad),'exceptional residual')
 return dict(idealIdentities=5,forwardIdentities=2,originalComponentRows=6,quinticFactorization=True,discriminantNorm=str(dn),normPrime=73,missingTermCorrected='(171357/235298 + (2519877/7529536)*sqrt(2))*f*S')

def main():
 data=json.loads((HERE/'reference-equations.json').read_text());cert=json.loads((HERE/'reference-certificate.json').read_text());result=check(data,cert);rejected=0
 for kind in ('certificate','missing_fS','equation'):
  d=deepcopy(data);c=deepcopy(cert)
  if kind=='certificate':c['identities'][0]['U'][0]['c'][0]=str(F(c['identities'][0]['U'][0]['c'][0])+1)
  elif kind=='missing_fS':
   for key in ('L','Mw+L'):d['equations'][key]=[t for t in d['equations'][key] if sorted(t['m'])!=[1,2]]
  else:d['equations']['Q1'][0]['c'][0]=str(F(d['equations']['Q1'][0]['c'][0])+1)
  try:check(d,c)
  except (ValueError,KeyError):rejected+=1
  else:raise ValueError('uncaught mutation '+kind)
 report=dict(schema='compressed-reference-check/v27',status='PASS',**result,corruptionsRejected=rejected,independentImplementation=True,independentNonAuthorReview=False,scope='Exact field polynomial identities and the full exceptional-stratum certificate; arithmetic projection is proved separately.')
 (HERE/'reference-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
