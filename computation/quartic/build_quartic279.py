#!/usr/bin/env python3
"""Construct the four-block contact-amplified quartic existence family.

Uses the contact-height amplification theorem and the even-valuation local
packing. The sufficient coefficient threshold is ineffective.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from math import gcd
from pathlib import Path
import json
import build_quartic_even as B
HERE=Path(__file__).resolve().parent
DEFAULT_SOURCE=B.DEFAULT_SOURCE
PIN=B.PINS[297]
THETA=[F(0),F(-1,2),F(-1),F(1,2399),F(-32,407)]
GROUPS=[['C2','H','U3','U4'],['C3','C1','V0'],['C4','U1','V2'],['F','U2','V3'],['I','V1','V4']]

def poly_mul(a,b):
 out=[F(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[i+j]+=x*y
 return out

def substitute(p,replacements):
 out={}
 for (a,m),c in p.items():
  value={(a,()):c}
  for variable in m:value=B.mul(value,replacements.get(variable,B.V(variable)))
  out=B.add(out,value)
 return out


def build(source_root=DEFAULT_SOURCE,output_root=HERE):
 raw=(source_root/'family297/quadratic-family297.json').read_bytes();assert sha256(raw).hexdigest()==PIN
 old=json.loads(raw);ids={c['id']:c['sourceId'] for c in old['coordinates']};byname={c['name']:c['sourceId'] for c in old['coordinates']}
 oldrows=[(r,{(t['parameterPower'],tuple(sorted(ids[x] for x in t['monomial']))):F(int(t['coefficient'])) for t in r['terms']}) for r in old['residuals']]
 deleted={c['sourceId'] for c in old['coordinates'] if c['name'].startswith('mixed.private.') or (c['name'].startswith('mixed.') and '.power' in c['name'] and not c['name'].startswith('mixed.det'))}
 deleted.update([182,183,186,187,192,193,200,201,204,205,212,213,216,217,224,225,228,229])
 rename={};newcoords=[];newrows=[];replacements={};changes={};removed=[];F20=[F(1)]
 for j in range(4):
  for theta in THETA:F20=poly_mul(F20,[-theta-3*j,F(1)])
 assert len(F20)==21 and F20[-1]==1
 delta20=[F(1)]
 for i in range(20):delta20=poly_mul(delta20,[-F(1),F(1)])
 def coord(sid,name):newcoords.append({'sourceId':sid,'name':name,'kind':'gate'})
 def row(sid,name,p):newrows.append(({'sourceId':sid,'name':name},B.primitive(p)))
 # Affine G2 values, computed from the existing f² and w² coordinates.
 for i,(fs,ws,rs) in enumerate([(178,180,186),(196,198,204),(208,210,216),(220,222,228)]):
  f2=(B.V(fs),B.scale(B.V(fs+1),2))
  D=(B.scale(B.ONE,11),B.scale(B.ONE,-6));w=B.fm(D,f2)
  w2=(B.scale(B.V(ws),193),B.scale(B.V(ws+1),-132))
  replacements[rs]=B.add(B.ONE,B.scale(w[0],F(-2,5)),B.scale(w2[0],F(-2,15)))
  replacements[rs+1]=B.add(B.scale(w[1],F(-2,5)),B.scale(w2[1],F(-2,15)))
 # V1 has G0=1, so its retained z value is the alternate numerator itself.
 changes['logV1.0.definition']=B.add(B.V(164),B.scale(B.mul(B.V(188),B.V(234)),-1),B.scale(B.mul(B.V(189),B.V(235)),-2))
 changes['logV1.1.definition']=B.add(B.V(165),B.scale(B.mul(B.V(188),B.V(235)),-1),B.scale(B.mul(B.V(189),B.V(234)),-1))
 bases=[]
 for d in range(2):
  off=48*d;t=37 if d==0 else 391;t2=346 if d==0 else 392;t4=347 if d==0 else 393;ff=348 if d==0 else 394;e=350+off;q=352+off
  rename[t4]=f'amplified.det{d}.tPower4';rename[ff]=f'amplified.det{d}.contactPolynomial'
  powers={0:B.ONE,1:B.V(t),2:B.V(t2),4:B.V(t4)}
  changes[f'detector{d}.Fmiddle.definition']=B.add(B.mul(B.V(t2),B.V(t2)),B.scale(B.V(t4),-1))
  for k,(exponent,left,right) in enumerate([(5,1,4),(8,4,4),(9,1,8),(10,5,5)]):
   sid=20000+20*d+k;coord(sid,f'amplified.det{d}.tPower{exponent}')
   row(sid,f'amplified.det{d}.tPower{exponent}.definition',B.add(B.mul(powers[left],powers[right]),B.scale(B.V(sid),-1)))
   powers[exponent]=B.V(sid)
  def evaluate(coefficients):
   terms=[]
   for degree,coefficient in enumerate(coefficients):
    if not coefficient:continue
    if degree in powers:term=powers[degree]
    else:
     left,right=next((a,b) for a in sorted(powers) for b in sorted(powers) if a<=b and a+b==degree)
     term=B.mul(powers[left],powers[right])
    terms.append(B.scale(term,coefficient))
   return B.add(*terms)
  fexpr=evaluate(F20)
  changes[f'detector{d}.F.definition']=B.add(fexpr,B.scale(B.V(ff),-1))
  if d==0:numerator=evaluate(delta20)
  else:
   x=B.V(395);x4=B.V(397)
   x5=20100;x10=20101
   coord(x5,'amplified.det1.scaledDeltaPower5');coord(x10,'amplified.det1.scaledDeltaPower10')
   row(x5,'amplified.det1.scaledDeltaPower5.definition',B.add(B.mul(x,x4),B.scale(B.V(x5),-1)))
   row(x10,'amplified.det1.scaledDeltaPower10.definition',B.add(B.mul(B.V(x5),B.V(x5)),B.scale(B.V(x10),-1)))
   numerator=B.mul(B.V(x10),B.V(x10))
  changes[f'detector{d}.eWeight.definition']=B.add(B.mul(B.V(ff),B.V(e)),B.scale(numerator,-1))
  delta2=B.add(B.V(t2),B.scale(B.V(t),-2),B.ONE)
  changes[f'detector{d}.q1.definition']=B.add(B.mul(delta2,B.V(q)),B.scale(B.V(e),-1))
  changes[f'detector{d}.eDelta.definition']=B.add(B.mul(delta2,B.V(e)),B.scale(B.V(384+off),-1))
  changes[f'detector{d}.B.definition']=B.add(B.mul(B.V(384+off),B.V(385+off)),B.scale(B.mul(B.V(383+off),B.V(383+off)),-1))
  changes[f'detector{d}.qPower19.definition']=B.add(B.mul(B.V(q),B.V(362+off)),B.scale(B.V(359+off),-1))
  rename[359+off]=f'amplified.det{d}.qPower5';rename[369+off]=f'amplified.det{d}.qPower10';rename[360+off]=f'amplified.det{d}.qPower23'
  bases.append({'detector':d,'powers':{str(k):next(iter(p))[1][0] if k else None for k,p in powers.items()},'contactCoordinate':ff,'contactDegree':20,'RDenominatorDeltaPower':22,'qClearingDeltaPower':2,'traceClearingDeltaPower':2})
 # The base squared tests, together with free high-point fourth powers.
 powers={}
 for i,s in enumerate([255,257,259,261],1):powers[f'U{i}',2]=(B.V(s),B.scale(B.V(s+1),2))
 for i,(fs,ws) in enumerate([(178,180),(190,None),(196,198),(208,210),(220,222)]):
  powers[f'V{i}',2]=(B.V(fs),B.scale(B.V(fs+1),-2))
  if ws:powers[f'V{i}',4]=B.fourth(ws,ws+1)
 for name,s in [('C1',305),('H',311),('C2',313),('C3',315),('C4',317)]:powers[name,2]=(B.V(s),B.scale(B.V(s+1),2))
 powers['I',2]=(B.add(B.V(307),B.scale(B.V(232),-6),B.scale(B.V(248),306),B.scale(B.ONE,15015)),B.add(B.scale(B.V(308),2),B.scale(B.V(233),-6)))
 powers['F',2]=(B.add(B.V(319),B.scale(B.V(253),-2),B.ONE),B.add(B.scale(B.V(320),4),B.scale(B.V(254),-4)))
 shared=[]
 for index,(name,power) in enumerate([('C1',4),('U3',4),('U4',4),('U4',8)]):
  value=B.fm(powers[name,power//2],powers[name,power//2]);sids=[21000+2*index,21001+2*index]
  for c,sid in enumerate(sids):coord(sid,f'amplified.{name}.power{power}.{c}');row(sid,f'amplified.{name}.power{power}.{c}.definition',B.add(value[c],B.scale(B.V(sid),-1)))
  powers[name,power]=tuple(B.V(sid) for sid in sids);shared.append({'test':name,'power':power,'sourceCoordinates':sids})
 factor_specs=[]
 lists=[ [('C2',2,23),('H',2,10),('U3',4,4),('U4',8,8)], [('C3',2,23),('C1',4,10),('V0',4,4)], [('C4',2,23),('U1',2,2),('V2',4,4)], [('F',2,23),('U2',2,2),('V3',4,4)], [('I',2,5),('V1',2,2),('V4',4,4)] ]
 for d in range(2):
  off=48*d;weights={2:361+off,4:362+off,8:850+d,5:359+off,10:369+off,23:360+off};start=22000+30*d
  for g,group in enumerate(lists):
   for c in range(2):
    sid=start+2*g+c;coord(sid,f'amplified.det{d}.factor{g}.{c}')
    p=B.add(B.ONE if c==0 else {},*(B.mul(B.V(weights[w]),powers[n,p][c]) for n,p,w in group),B.scale(B.V(sid),-1))
    row(sid,f'amplified.det{d}.factor{g}.{c}.definition',p)
   factor_specs.append({'detector':d,'factor':g,'terms':[{'test':n,'testPower':p,'qPower':w} for n,p,w in group]})
  acc=(B.V(start),B.V(start+1))
  for k in range(1,5):
   target=380+off if k==4 else start+10+2*(k-1);value=B.fm(acc,(B.V(start+2*k),B.V(start+2*k+1)))
   for c in range(2):
    if k!=4:coord(target+c,f'amplified.det{d}.product{k}.{c}')
    row(23000+30*d+2*k+c,f'amplified.det{d}.product{k}.{c}.definition',B.add(value[c],B.scale(B.V(target+c),-1)))
   acc=(B.V(target),B.V(target+1))
 assembled=[];changed=[]
 for r,p in oldrows:
  name=r['name']
  skip=((name.startswith('mixed.det') and any(s in name for s in ('.factor','.product'))) or (name.startswith('mixed.') and '.power' in name and not name.startswith('mixed.det')) or (name.startswith('logV') and any(s in name for s in ('.wPower4.','.rationalApproximation.'))) or name in ['logV1.polynomial.0.definition','logV1.polynomial.1.definition'])
  if skip:removed.append(r['sourceId']);continue
  if name in changes:p=changes.pop(name);changed.append(r['sourceId'])
  p=substitute(p,replacements)
  assert all(i not in deleted for a,m in p for i in m),name
  if '.qPower19.' in name:name=name.replace('.qPower19.','.qPower5.')
  if '.qPower38.' in name:name=name.replace('.qPower38.','.qPower10.')
  if '.qPower79.' in name:name=name.replace('.qPower79.','.qPower23.')
  assembled.append((dict(r,name=name),B.primitive(p)))
 assert not changes,changes
 coords=[dict(c,name=rename.get(c['sourceId'],c['name'])) for c in old['coordinates'] if c['sourceId'] not in deleted]+newcoords
 coords=[dict(c,id=i+1) for i,c in enumerate(coords)];mapping={c['sourceId']:c['id'] for c in coords};rows=[];expanded=defaultdict(int)
 assert len(mapping)==len(coords)
 for metadata,p in assembled+newrows:
  p={(a,tuple(sorted(mapping[i] for i in m))):c for (a,m),c in p.items()};assert max(len(m) for a,m in p)<=2
  rows.append(dict(metadata,terms=B.ts(p)))
  for (a,m),c in p.items():
   for (b,n),d in p.items():expanded[a+b,tuple(sorted(m+n))]+=c*d
 expanded={m:c for m,c in expanded.items() if c};ordinary=defaultdict(dict)
 for (a,m),c in expanded.items():ordinary[m][a]=c
 assert len(coords)==279,len(coords)
 assert len(rows)==253,len(rows)
 assert {i for a,m in expanded for i in m}==set(range(1,280))
 assert ordinary[(mapping[489],mapping[489])]=={0:1,2:1}
 assert all(set(p) in ({0},{1},{0,2}) for p in ordinary.values())
 C=max(abs(p[0]) for p in ordinary.values() if set(p)=={0});L=max(abs(p[1]) for p in ordinary.values() if set(p)=={1})
 assert C.bit_length()==1520 and L==2*80989**2 and C>L*L
 assert 80989**90+1<C<80989**94+1
 report={'status':'Exact algebraic coefficient source only; no integer-projection theorem is asserted for this intermediate table.','variables':279,'quadraticResiduals':len(rows),'degree':max(len(m) for a,m in expanded),'ordinaryMonomialsForEveryPositiveParameter':len(ordinary),'symbolicTerms':len(expanded),'sourceSha256':PIN,'removedSourceCoordinates':sorted(deleted),'newSourceCoordinates':[c['sourceId'] for c in newcoords],'removedSourceRows':removed,'modifiedSourceRows':changed,'contactBlocks':4,'contactShifts':[0,3,6,9],'contactPolynomialCoefficients':[str(c) for c in F20],'detectorBases':bases,'groups':GROUPS,'factorSpecifications':factor_specs,'newSharedPowers':shared,'highLogarithm':'G2(w)=1-2w/5-2w^2/15','lowLogarithm':'G0(w)=1','requiredTestOrders':{'H':6,'C1':3,'I':3,'C2':12,'C3':12,'C4':12,'F':12,'U1':1,'U2':1,'U3':1,'U4':1,'V0':1,'V1':1,'V2':1,'V3':1,'V4':1},'weightPowers':[1,2,4,8,5,10,23],'newExceptionalPrimes':[123121,161303],'supportIndependentOfPositiveParameter':True,'constantCoefficientMaximum':str(C),'constantCoefficientMaximumBits':C.bit_length(),'linearCoefficientMultiplierMaximum':L,'heightFormulaForEveryPositiveParameter':'max(C,A^2+1)','exactHeightThresholdN':23,'effectiveness':'Coefficient source only; the current projection theorem is proved for family267.'}
 system=dict(old,format='integer-quadratic-family-v7',variables=279,source={'construction':'quartic-family297','sha256':PIN},coordinates=coords,residuals=rows)
 poly={'format':'integer-quartic-family-v7','variables':279,'degree':4,'inputCoordinate':1,'fixedParameter':old['fixedParameter'],'coordinates':coords,'terms':B.ts(expanded)}
 out=output_root/'family279';out.mkdir(parents=True,exist_ok=True)
 for filename,data in [('quadratic-family279.json',system),('polynomial-family279.json',poly),('construction-report279.json',report)]: (out/filename).write_text(json.dumps(data,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ['variables','quadraticResiduals','degree','symbolicTerms','ordinaryMonomialsForEveryPositiveParameter','constantCoefficientMaximumBits']}))
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,default=DEFAULT_SOURCE);p.add_argument('--output-root',type=Path,default=HERE);a=p.parse_args();build(a.source_root,a.output_root)
