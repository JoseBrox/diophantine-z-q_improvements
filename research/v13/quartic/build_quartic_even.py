#!/usr/bin/env python3
"""Exact quartic tables using even valuations of reciprocal abscissas.

The coordinate/degree/height claims are exact finite algebra. Projection to Z
requires the arithmetic premises and proof in the companion manuscript.
"""
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from math import gcd,lcm
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
DEFAULT_SOURCE=HERE.parents[2]/'publication/computation/quartic'
PINS={297:'144f99f6f76cadf5fae3796f7a0a6c3f740659d89fe062237b278989bcef5ce8',342:'309d97f891bb9144a3a314b361f62ed1ed4d3064938b7d15121e763f7b99b12f'}
GROUPS=[['C2','H','U1','V0'],['C3','C1','U2','V2'],['C4','I','U3','V3'],['F','U4','V1','V4']]

def add(*polys):
 d=defaultdict(Fraction)
 for p in polys:
  for m,c in p.items():d[m]+=c
 return {m:c for m,c in d.items() if c}
def scale(p,c):return {m:c*v for m,v in p.items() if c*v}
def mul(p,q):
 d=defaultdict(Fraction)
 for (a,m),c in p.items():
  for (b,n),e in q.items():d[a+b,tuple(sorted(m+n))]+=c*e
 return {m:c for m,c in d.items() if c}
def V(i):return {(0,(i,)):Fraction(1)}
ONE={(0,()):Fraction(1)}
def primitive(p):
 den=lcm(*(c.denominator for c in p.values()))
 q={m:int(c*den) for m,c in p.items()};g=gcd(*q.values())
 if q[min(q)]<0:g=-g
 return {m:c//g for m,c in sorted(q.items())}
def fm(p,q):return (add(mul(p[0],q[0]),scale(mul(p[1],q[1]),2)),add(mul(p[0],q[1]),mul(p[1],q[0])))
def ts(p):return [{'parameterPower':a,'monomial':list(m),'coefficient':str(c)} for (a,m),c in sorted(p.items())]
def fourth(u,v):
 return (scale(add(scale(V(u),37249),scale(V(v),-34848)),Fraction(1,2401)),scale(add(V(u),scale(V(v),-1)),Fraction(-25476,2401)))
def eighth(u,v):
 return (scale(add(scale(V(u),72097),scale(V(v),101904)),Fraction(1,5764801)),scale(add(scale(V(u),50952),scale(V(v),72097)),Fraction(-1,5764801)))

def build(baseline,source_root=DEFAULT_SOURCE,output_root=HERE):
 raw=(source_root/f'family{baseline}'/f'quadratic-family{baseline}.json').read_bytes()
 assert sha256(raw).hexdigest()==PINS[baseline]
 old=json.loads(raw); oldmap={c['id']:c['sourceId'] for c in old['coordinates']}
 det=2 if baseline==297 else 3;number=281 if det==2 else 322
 removedcoords={c['sourceId'] for c in old['coordinates'] if c['name'].startswith('mixed.private.') or (c['name'].startswith('mixed.') and '.power' in c['name'] and not c['name'].startswith('mixed.det'))}
 assembled=[];removedrows=[]
 for r in old['residuals']:
  if (r['name'].startswith('mixed.det') and ('.factor' in r['name'] or '.product' in r['name'])) or (r['name'].startswith('mixed.') and '.power' in r['name'] and not r['name'].startswith('mixed.det')):
   removedrows.append(r['sourceId']);continue
  p={(t['parameterPower'],tuple(sorted(oldmap[x] for x in t['monomial']))):Fraction(int(t['coefficient'])) for t in r['terms']}
  assert all(i not in removedcoords for (a,m) in p for i in m)
  assembled.append((r,primitive(p)))
 coords=[dict(c,id=i+1) for i,c in enumerate(c for c in old['coordinates'] if c['sourceId'] not in removedcoords)]
 newcoords=[];newrows=[]
 def coordinate(sid,name):
  c={'id':len(coords)+len(newcoords)+1,'sourceId':sid,'name':name,'kind':'gate'};newcoords.append(c)
 def equation(sid,name,p):newrows.append(({'sourceId':sid,'name':name},primitive(p)))
 powers={}
 for i,sid in enumerate([255,257,259,261],1):powers[f'U{i}',2]=(V(sid),scale(V(sid+1),2))
 for i,(f,w2,w4) in enumerate([(178,180,182),(190,192,0),(196,198,200),(208,210,212),(220,222,224)]):
  powers[f'V{i}',2]=(V(f),scale(V(f+1),-2));powers[f'V{i}',4]=fourth(w2,w2+1)
  if w4:powers[f'V{i}',8]=eighth(w4,w4+1)
 for name,sid in [('C1',305),('H',311),('C2',313),('C3',315),('C4',317)]:powers[name,2]=(V(sid),scale(V(sid+1),2))
 powers['I',2]=(add(V(307),scale(V(232),-6),scale(V(248),306),scale(ONE,15015)),add(scale(V(308),2),scale(V(233),-6)))
 powers['F',2]=(add(V(319),scale(V(253),-2),ONE),add(scale(V(320),4),scale(V(254),-4)))
 specs=[]
 for name in ['C1','I','U1','U2','U3']:
  p=fm(powers[name,2],powers[name,2]);sids=[10000+len(newcoords),10001+len(newcoords)]
  for c,sid in enumerate(sids):
   coordinate(sid,f'even.{name}.power4.{c}');equation(sid,f'even.{name}.power4.{c}.definition',add(p[c],scale(V(sid),-1)))
  powers[name,4]=tuple(V(sid) for sid in sids);specs.append({'test':name,'power':4,'sourceCoordinates':sids})
 assert len(newcoords)==10
 factor_specs=[]
 for d in range(det):
  off=48*d;weights={'q':352+off,'q2':361+off,'q4':362+off,'q8':850+d,'q38':369+off,'q79':360+off}
  groupspecs=[ [('C2',2,'q79'),('H',2,'q38'),('U1',4,'q4'),('V0',8,'q8')],
               [('C3',2,'q79'),('C1',4,'q38'),('U2',4,'q4'),('V2',8,'q8')],
               [('C4',2,'q79'),('I',4,'q38'),('U3',4,'q4'),('V3',8,'q8')],
               [('F',2,'q79'),('U4',2,'q2'),('V1',4,'q4'),('V4',8,'q8')] ]
  start=11000+20*d
  for g,group in enumerate(groupspecs):
   for c in range(2):
    sid=start+2*g+c;coordinate(sid,f'even.det{d}.factor{g}.{c}')
    p=add(ONE if c==0 else {},*(mul(V(weights[w]),powers[name,power][c]) for name,power,w in group),scale(V(sid),-1))
    equation(sid,f'even.det{d}.factor{g}.{c}.definition',p)
   factor_specs.append({'detector':d,'factor':g,'terms':[{'test':n,'testPower':p,'qPower':int(w[1:] or '1')} for n,p,w in group]})
  acc=(V(start),V(start+1))
  for step in range(1,4):
   target=380+off if step==3 else start+8+2*(step-1);prod=fm(acc,(V(start+2*step),V(start+2*step+1)))
   for c in range(2):
    sid=target+c
    if step!=3:coordinate(sid,f'even.det{d}.product{step}.{c}')
    equation(12000+20*d+2*step+c,f'even.det{d}.product{step}.{c}.definition',add(prod[c],scale(V(sid),-1)))
   acc=tuple(V(target+c) for c in range(2))
 coords+=newcoords;mapping={c['sourceId']:c['id'] for c in coords};rows=[];coefs=defaultdict(int)
 for meta,p in assembled+newrows:
  p={(a,tuple(sorted(mapping[i] for i in m))):c for (a,m),c in p.items()}
  assert max(len(m) for a,m in p)<=2
  rows.append(dict(meta,terms=ts(p)))
  for (a,m),c in p.items():
   for (b,n),e in p.items():coefs[a+b,tuple(sorted(m+n))]+=c*e
 coefs={m:c for m,c in coefs.items() if c};ordinary=defaultdict(dict)
 for (a,m),c in coefs.items():ordinary[m][a]=c
 assert len(coords)==number and len(rows)==len(old['residuals'])-(baseline-number)
 assert ordinary[(mapping[489],mapping[489])]=={0:1,2:1}
 assert all(set(p) in ({0},{1},{0,2}) for p in ordinary.values())
 C=max(abs(p[0]) for p in ordinary.values() if set(p)=={0});L=max(abs(p[1]) for p in ordinary.values() if set(p)=={1})
 assert L==2*80989**2 and C>L*L
 A23=80989**47;A22=80989**45
 assert A23*A23+1>C>A22*A22+1 and A23>L
 support={i for a,m in coefs for i in m};assert support==set(range(1,number+1))
 assert gcd(*coefs.values())==1
 report={'status':'Exact algebraic specification; projection theorem has stated arithmetic dependencies.','baselineVariables':baseline,'variables':number,'quadraticResiduals':len(rows),'degree':max(len(m) for a,m in coefs),'symbolicTerms':len(coefs),'ordinaryMonomialsForEveryPositiveParameter':len(ordinary),'sourceSha256':PINS[baseline],'removedSourceCoordinates':sorted(removedcoords),'newSourceCoordinates':[c['sourceId'] for c in newcoords],'removedSourceRows':removedrows,'newSourceRows':[r['sourceId'] for r,p in newrows],'groups':GROUPS,'factorSpecifications':factor_specs,'newSharedPowers':specs,'requiredTestOrders':{'H':20,'C1':10,'I':10,'C2':40,'C3':40,'C4':40,'F':40,'U1':1,'U2':1,'U3':1,'U4':1,'V0':1,'V1':1,'V2':1,'V3':1,'V4':1},'weightRelationsUnchanged':True,'supportIndependentOfPositiveParameter':True,'constantCoefficientMaximum':str(C),'constantCoefficientMaximumBits':C.bit_length(),'linearCoefficientMultiplierMaximum':L,'heightFormulaForEveryPositiveParameter':'max(C,A^2+1), with C=constantCoefficientMaximum','exactHeightThresholdN':23,'effectiveness':'Ineffective eventual parameter' if det==2 else 'Every N>=27464; specified member A=80989^54929'}
 system=dict(old,format='integer-quadratic-family-v6',variables=number,source={'construction':f'quartic-family{baseline}','sha256':PINS[baseline]},coordinates=coords,residuals=rows)
 poly={'format':'integer-quartic-family-v6','variables':number,'degree':4,'inputCoordinate':1,'fixedParameter':old['fixedParameter'],'coordinates':coords,'terms':ts(coefs)}
 out=output_root/f'family{number}';out.mkdir(parents=True,exist_ok=True)
 for filename,data in [(f'quadratic-family{number}.json',system),(f'polynomial-family{number}.json',poly),(f'construction-report{number}.json',report)]: (out/filename).write_text(json.dumps(data,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ['variables','quadraticResiduals','degree','symbolicTerms','ordinaryMonomialsForEveryPositiveParameter','constantCoefficientMaximumBits','exactHeightThresholdN']}))

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,default=DEFAULT_SOURCE);p.add_argument('--output-root',type=Path,default=HERE);a=p.parse_args()
 for n in (297,342):build(n,a.source_root,a.output_root)
