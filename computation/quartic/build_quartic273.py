#!/usr/bin/env python3
"""Exact273-coordinate quartic family from the certified279-coordinate source."""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from math import gcd,lcm,comb
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
DEFAULT_SOURCE=HERE
PIN='9bf3b6e40af70d2a9313f3c211f07941fd6ef93068106d7332bafa73f0dd9069'

def add(*ps):
 out=defaultdict(F)
 for p in ps:
  for m,c in p.items():out[m]+=c
 return {m:c for m,c in out.items() if c}
def scale(p,c):return {m:x*c for m,x in p.items() if x*c}
def mul(p,q):
 out=defaultdict(F)
 for (a,m),c in p.items():
  for (b,n),d in q.items():out[a+b,tuple(sorted(m+n))]+=c*d
 return {m:c for m,c in out.items() if c}
def v(i):return {(0,(i,)):F(1)}
one={(0,()):F(1)}
def primitive(p):
 den=lcm(*(F(c).denominator for c in p.values()));r={m:int(c*den) for m,c in p.items()};g=gcd(*r.values())
 if r[min(r)]<0:g=-g
 return {m:c//g for m,c in sorted(r.items())}
def fm(x,y):return add(mul(x[0],y[0]),scale(mul(x[1],y[1]),2)),add(mul(x[0],y[1]),mul(x[1],y[0]))
def terms(p):return [{'parameterPower':a,'monomial':list(m),'coefficient':str(c)} for (a,m),c in sorted(p.items())]
def pmul(a,b):
 r=[F(0)]*(len(a)+len(b)-1)
 for i,c in enumerate(a):
  for j,d in enumerate(b):r[i+j]+=c*d
 return r
def pdiv(a,b):
 a=list(a);q=[F(0)]*max(1,len(a)-len(b)+1)
 for k in range(len(a)-len(b),-1,-1):
  c=a[k+len(b)-1]/b[-1];q[k]=c
  for j,d in enumerate(b):a[k+j]-=c*d
 while len(a)>1 and a[-1]==0:a.pop()
 return q,a

def build(source_root=DEFAULT_SOURCE,output_root=HERE):
 raw=(source_root/'family279/quadratic-family279.json').read_bytes();assert sha256(raw).hexdigest()==PIN
 old=json.loads(raw);ids={c['id']:c['sourceId'] for c in old['coordinates']};deleted={850,851,21006,21007,20003,20023};renames={};edits={};changed=[];removed=[]
 contact=[F(1)]
 for j in range(4):
  for theta in [F(0),F(-1,2),F(-1),F(1,2399),F(-32,407)]:contact=pmul(contact,[-theta-3*j,F(1)])
 V=[F(comb(10,k)*(-1)**(10-k)) for k in range(11)];S,R=pdiv(contact,V)
 diff=[S[k]-V[k] for k in range(11)];assert diff[10]==0
 a=diff[9];assert a!=0
 U=[c/a for c in diff[:10]];assert U[-1]==1
 low=[V[k]-(U[k-1] if k else 0) for k in range(10)];assert V[10]==U[9]
 contact_checks=[]
 for d in range(2):
  t=37 if d==0 else 391;t2=346 if d==0 else 392;t3=347 if d==0 else 393;outF=348 if d==0 else 394
  t6=20000+20*d;outU=20001+20*d;outV=20002+20*d
  basis={0:one,1:v(t),2:v(t2),3:v(t3),6:v(t6)}
  def represent(coeff):
   ps=[]
   for k,c in enumerate(coeff):
    if not c:continue
    if k in basis:p=basis[k]
    else:
     i,j=next((i,j) for i in sorted(basis) for j in sorted(basis) if i<=j and i+j==k)
     p=mul(basis[i],basis[j])
    ps.append(scale(p,c))
   return add(*ps)
  edits[f'detector{d}.Fmiddle.definition']=(f'compressed.det{d}.tPower3.definition',add(mul(v(t),v(t2)),scale(v(t3),-1)))
  edits[f'amplified.det{d}.tPower5.definition']=(f'compressed.det{d}.tPower6.definition',add(mul(v(t3),v(t3)),scale(v(t6),-1)))
  edits[f'amplified.det{d}.tPower8.definition']=(f'compressed.det{d}.quotient9.definition',add(represent(U),scale(v(outU),-1)))
  edits[f'amplified.det{d}.tPower9.definition']=(f'compressed.det{d}.deltaPower10.definition',add(mul(v(t),v(outU)),represent(low),scale(v(outV),-1)))
  edits[f'detector{d}.F.definition']=(f'compressed.det{d}.contactPolynomial.definition',add(mul(v(outV),v(outV)),scale(mul(v(outU),v(outV)),a),represent(R),scale(v(outF),-1)))
  if d==0:edits['detector0.eWeight.definition']=('detector0.eWeight.definition',add(mul(v(outF),v(350)),scale(mul(v(outV),v(outV)),-1)))
  renames.update({t3:f'compressed.det{d}.tPower3',t6:f'compressed.det{d}.tPower6',outU:f'compressed.det{d}.quotient9',outV:f'compressed.det{d}.deltaPower10'})
  contact_checks.append({'detector':d,'coordinateSources':{'t':t,'t2':t2,'t3':t3,'t6':t6,'U9':outU,'V10':outV,'F20':outF}})
 # Only C1^4, I^4, B1^4 remain as additional shared field values.
 pC1=(v(305),scale(v(306),2))
 pI=(add(v(307),scale(v(232),-6),scale(v(248),306),scale(one,15015)),add(scale(v(308),2),scale(v(233),-6)))
 pB1=(v(190),scale(v(191),-2))
 for name,previous,oldname,sids in [('I',pI,'U3',[21002,21003]),('V1',pB1,'U4',[21004,21005])]:
  value=fm(previous,previous)
  for c,sid in enumerate(sids):
   edits[f'amplified.{oldname}.power4.{c}.definition']=(f'residue.{name}.power4.{c}.definition',add(value[c],scale(v(sid),-1)))
   renames[sid]=f'residue.{name}.power4.{c}'
 powers={('C1',4):(v(21000),v(21001)),('I',4):(v(21002),v(21003)),('V1',4):(v(21004),v(21005))}
 for i,sid in enumerate([255,257,259,261],1):powers[f'U{i}',2]=(v(sid),scale(v(sid+1),2))
 for name,sid in [('H',311),('C2',313),('C3',315),('C4',317)]:powers[name,2]=(v(sid),scale(v(sid+1),2))
 powers['F',2]=(add(v(319),scale(v(253),-2),one),add(scale(v(320),4),scale(v(254),-4)))
 for i,sid in [(0,180),(2,198),(3,210),(4,222)]:
  powers[f'V{i}',4]=(scale(add(scale(v(sid),37249),scale(v(sid+1),-34848)),F(1,2401)),scale(add(v(sid),scale(v(sid+1),-1)),F(-25476,2401)))
 groups=[[('C2',2,23),('H',2,10),('V1',4,4)],[('F',2,23),('U3',2,2),('V0',4,4)],[('I',4,23),('U2',2,1),('U4',2,2),('V3',4,4)],[('C3',2,23),('C1',4,10),('V4',4,4)],[('C4',2,23),('U1',2,2),('V2',4,4)]]
 for d in range(2):
  off=48*d;weight={1:352+off,2:361+off,4:362+off,10:369+off,23:360+off};start=22000+30*d
  for g,group in enumerate(groups):
   for c in range(2):
    value=add(one if c==0 else {},*(mul(v(weight[a]),powers[n,p][c]) for n,p,a in group),scale(v(start+2*g+c),-1))
    name=f'amplified.det{d}.factor{g}.{c}.definition';edits[name]=(f'residue.det{d}.factor{g}.{c}.definition',value)
 coords=[dict(c,id=i+1,name=renames.get(c['sourceId'],c['name'])) for i,c in enumerate(c for c in old['coordinates'] if c['sourceId'] not in deleted)];mapping={c['sourceId']:c['id'] for c in coords};rows=[];coefs=defaultdict(int)
 for row in old['residuals']:
  name=row['name']
  if row['sourceId'] in deleted:removed.append(row['sourceId']);continue
  p={(t['parameterPower'],tuple(sorted(ids[i] for i in t['monomial']))):F(int(t['coefficient'])) for t in row['terms']}
  if name in edits:name,p=edits.pop(name);changed.append(row['sourceId'])
  p=primitive(p);assert all(i not in deleted for a,m in p for i in m),name
  q={(a,tuple(sorted(mapping[i] for i in m))):c for (a,m),c in p.items()};assert max(len(m) for a,m in q)<=2
  rows.append(dict(row,name=name,terms=terms(q)))
  for (a,m),c in q.items():
   for (b,n),d in q.items():coefs[a+b,tuple(sorted(m+n))]+=c*d
 assert not edits,edits
 coefs={m:c for m,c in coefs.items() if c};ordinary=defaultdict(dict)
 for (a,m),c in coefs.items():ordinary[m][a]=c
 assert len(coords)==273 and len(rows)==247
 assert {i for a,m in coefs for i in m}==set(range(1,274))
 assert gcd(*coefs.values())==1 and ordinary[(mapping[489],mapping[489])]=={0:1,2:1}
 assert all(set(p) in ({0},{1},{0,2}) for p in ordinary.values())
 maximum=max(abs(p[0]) for p in ordinary.values() if set(p)=={0});linear=max(abs(p[1]) for p in ordinary.values() if set(p)=={1})
 assert maximum.bit_length()==1520 and linear==13118436242 and maximum>linear*linear
 assert 80989**90+1<maximum<80989**94+1
 system=dict(old,format='integer-quadratic-family-v8',variables=273,source={'construction':'quartic-family279','sha256':PIN},coordinates=coords,residuals=rows)
 polynomial={'format':'integer-quartic-family-v8','variables':273,'degree':4,'inputCoordinate':1,'fixedParameter':old['fixedParameter'],'coordinates':coords,'terms':terms(coefs)}
 report={'status':'Exact coefficient source only; no integer-projection theorem is asserted for this normalization. The defining construction is family267.','variables':273,'quadraticResiduals':247,'degree':4,'symbolicTerms':len(coefs),'ordinaryMonomialsForEveryPositiveParameter':len(ordinary),'sourceSha256':PIN,'removedSourceCoordinates':sorted(deleted),'removedSourceRows':removed,'changedSourceRows':changed,'groups':groups,'requiredOrders':{'H':6,'C2':12,'C3':12,'C4':12,'F':12,'C1':3,'I':6,'allReciprocalAbscissas':1},'inputComparisonAfterCrossTest':3,'primaryInputCompletenessOrder':12,'newSharedPowers':['C1^4','I^4','B1^4'],'removedWeight':'q^8','contactCircuit':{'baseExponents':[0,1,2,3,6],'coordinateCountPerDetector':6,'leadingQuotientCoefficient':str(diff[9]),'contactCoefficients':[str(x) for x in contact],'U9Coefficients':[str(x) for x in U],'V10Coefficients':[str(x) for x in V],'R9Coefficients':[str(x) for x in R],'VMinus_tUCoefficients':[str(x) for x in low],'coordinates':contact_checks},'constantCoefficientMaximum':str(maximum),'constantCoefficientMaximumBits':maximum.bit_length(),'linearCoefficientMultiplierMaximum':linear,'heightFormulaForEveryPositiveParameter':'max(C,A^2+1)','exactHeightThresholdN':23,'exactHeightForNAtLeast23':'80989^(4*N+2)+1','effectiveness':'Coefficient family only. No defining theorem is asserted; see the independently normalized family267.'}
 output=output_root/'family273';output.mkdir(parents=True,exist_ok=True)
 for filename,data in [('quadratic-family273.json',system),('polynomial-family273.json',polynomial),('construction-report273.json',report)]: (output/filename).write_text(json.dumps(data,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ['variables','quadraticResiduals','degree','symbolicTerms','ordinaryMonomialsForEveryPositiveParameter','constantCoefficientMaximumBits']}))
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,default=DEFAULT_SOURCE);p.add_argument('--output-root',type=Path,default=HERE);args=p.parse_args();build(args.source_root,args.output_root)
