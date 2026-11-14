#!/usr/bin/env python3
"""Independent reconstruction of every 204 row and quartic coefficient.

This checker imports no producer. Sparse polynomial arithmetic, field
arithmetic, changes of coordinates, and height envelopes are reconstructed
here. The weighted-height and arithmetic completeness proofs are not
certified by finite tests.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from hashlib import sha256
from math import gcd,lcm,isqrt
from copy import deepcopy
import json
HERE=Path(__file__).resolve().parent
PARENT=HERE.parent/'additive212_v25/unbalanced-quadratic.json'
PIN='b2f32d64ef1fb2591d37cfd41aadf8869ce691c39ed92e0e597ec10aaa53fc75'
def ck(b,msg):
 if not b:raise ValueError(msg)
def plus(*ps):
 z=defaultdict(F)
 for p in ps:
  for m,c in p.items():z[m]+=c
 return {m:c for m,c in z.items() if c}
def neg(p):return {m:-c for m,c in p.items()}
def scaled(p,c):return {m:c*v for m,v in p.items() if c*v}
def prod(p,q):
 z=defaultdict(F)
 for (a,m),c in p.items():
  for (b,n),d in q.items():z[a+b,tuple(sorted(m+n))]+=c*d
 return {m:c for m,c in z.items() if c}
def C(c):return {(0,()):F(c)} if c else {}
def V(i):return {(0,(i,)):F(1)}
def norm(p):
 ck(bool(p),'zero row');dd=lcm(*(x.denominator for x in p.values()));gg=gcd(*(int(dd*x) for x in p.values()))
 if p[min(p)]<0:gg=-gg
 return scaled(p,F(dd,gg))
def read(r):return {(int(t['parameterPower']),tuple(t['monomial'])):F(t['coefficient']) for t in r['terms']}
def ka(*xs):return (plus(*(x[0] for x in xs)),plus(*(x[1] for x in xs)))
def kn(x):return neg(x[0]),neg(x[1])
def km(x,y):return plus(prod(x[0],y[0]),scaled(prod(x[1],y[1]),2)),plus(prod(x[0],y[1]),prod(x[1],y[0]))
def ks(x,a):return scaled(x[0],a),scaled(x[1],a)
def K(a,b=0):return C(a),C(b)

def expected(parent,coordinates):
 old_to_new={c['parent212Id']:c['id'] for c in coordinates if 'parent212Id' in c}
 nm={c['name']:c['id'] for c in coordinates}
 # We reconstruct on the old indices, with the freshly named coordinates
 # mapped to fictitious indices above 212. This independently checks remapping.
 newids={name:213+i for i,name in enumerate([f'pair{j}.{v}.{k}' for j in (1,3) for v in ('f','h','g','k','s') for k in (0,1)])}
 mapping=dict(old_to_new);mapping.update({i:nm[n] for n,i in newids.items()})
 field=lambda a,b,half=False:(V(a),scaled(V(b),2 if half else 1))
 S=field(19,20);T=field(211,212);D=K(11,-6);one=K(1)
 def fresh(j,n):return field(newids[f'pair{j}.{n}.0'],newids[f'pair{j}.{n}.1'])
 roots=[];new=[]
 def kr(n,p):
  for k,q in enumerate(p):new.append((n+'.'+str(k),norm(q)))
 for j,fi,gi,li,pi,mult in [(1,(54,55),(23,24),(31,32),(33,34),1),(3,(58,59),(27,28),(39,40),(41,42),2)]:
  f,h,g,k,s=(fresh(j,n) for n in ('f','h','g','k','s'));FU=field(*fi,half=True);FV=field(*gi,half=True);L=field(*li);LP=field(*pi)
  kr(f'pair{j}.square.f',ka(FU,kn(km(f,f))));kr(f'pair{j}.square.g',ka(FV,kn(km(g,g))))
  kr(f'pair{j}.curve',ka(km(h,h),kn(f),km(D,km(f,FU))))
  kr(f'pair{j}.secant',ka(km(s,ka(f,kn(g))),kn(h),kn(k)))
  kr(f'pair{j}.tangent',ka(km(s,ka(h,kn(k))),kn(one),km(D,ka(FU,km(f,g),FV))))
  for name,jj,ff,fs,ll,ss in [('primary',h,f,FU,L,S),('alternate',k,g,FV,LP,T)]:
   kr(f'pair{j}.ratio.{name}.raw',ka(km(jj,ll),ks(km(ff,ss),mult)))
   kr(f'pair{j}.ratio.{name}.regular',ka(km(ka(one,kn(km(D,fs))),ll),ks(km(jj,ss),mult)))
  roots.append(ka(km(s,s),km(D,ka(f,g))))
 agg=scaled(plus(V(4),neg(V(90))),8)
 for c,e in [(173,175),(201,203)]:
  z=ka(field(c,c+1),kn(field(e,e+1)));agg=plus(agg,km(z,z)[0])
 agg=norm(plus(agg,*(scaled(x[0],4) for x in roots)))
 removed=set(range(155,169))|set(range(183,197));deleted=set(range(104,122))|set(range(140,158))
 weights={i:1 for i in list(range(39,47))+list(range(48,52))};weights.update({i:-1 for i in range(205,209)})
 out=[];rescalings=[]
 for row in parent['residuals']:
  p=read(row)
  if row['id'] in deleted:continue
  name=row['name']
  if row['id']==180:p=agg;name='weighted.aggregate.trace'
  elif any(set(m)&set(weights) for a,m in p):
   data=[(a,m.count(118)+2*m.count(117)+sum(weights.get(i,0) for i in m),tuple(i for i in m if i not in (117,118)),c) for (a,m),c in p.items()]
   lowest=min(e for a,e,m,c in data);z=defaultdict(F)
   for a,e,m,c in data:
    e-=lowest;ck(e in (0,1,2),'R exponent');m=m+(() if e==0 else ((118,) if e==1 else (117,)));z[a,tuple(sorted(m))]+=c
   p={m:c for m,c in z.items() if c};name='v27.'+name;rescalings.append((row['id'],lowest))
  ck(not any(set(m)&removed for a,m in p),'unremoved occurrence')
  out.append((name,norm(p)))
 out+=new;ck(len(out)==186,'row count')
 return out,mapping,rescalings

def check_systems(parent,systems,polynomials):
 ck(sha256(PARENT.read_bytes()).hexdigest()==PIN,'source hash')
 coords=systems['unbalanced']['coordinates'];ck(len(coords)==204,'coordinates')
 ex,mapping,rescalings=expected(parent,coords);results={}
 for variant,system in systems.items():
  ck(system['variables']==204 and system['inputCoordinate']==1,'metadata')
  ck(system['coordinates']==coords,'different coordinate dictionaries')
  rows=system['residuals'];ck(len(rows)==186,'rows')
  for r,(name,p) in zip(rows,ex):
   if variant=='balanced':
    ee=min(2*a+sum(i in (117,118) for i in m) for a,m in p)
    p={(2*a+sum(i in (117,118) for i in m)-ee,m):c*149**a for (a,m),c in p.items()};p=norm(p)
   p={(a,tuple(sorted(mapping[i] for i in m))):c for (a,m),c in p.items()}
   ck(name==r['name'] and p==read(r),'incorrect row '+name)
   ck(max(len(m) for a,m in p)<=2,'nonquadratic row')
  # Triangular expansion rather than the producer's ordered double sum.
  expanded=defaultdict(F)
  for r in rows:
   items=sorted(read(r).items())
   for i,((a,m),c) in enumerate(items):
    for j in range(i,len(items)):
     (b,n),d=items[j];expanded[a+b,tuple(sorted(m+n))]+=(1 if i==j else 2)*c*d
  expanded={m:c for m,c in expanded.items() if c};ck(expanded==read(polynomials[variant]),'quartic expansion')
  ck(max(len(m) for a,m in expanded)==4,'degree');ck(gcd(*(int(c) for c in expanded.values()))==1,'content')
  ck({i for a,m in expanded for i in m}==set(range(1,205)),'unused coordinate')
  profile=defaultdict(dict)
  for (a,m),c in expanded.items():profile[m][a]=int(c)
  if variant=='balanced':
   kk=31581660**28;hh=(5898050446009651968*kk)**2
   ck(max(abs(p.get(0,0)) for p in profile.values())==hh,'fixed height')
   ck(max(abs(p.get(2,0)) for p in profile.values())==kk,'quadratic height')
   for p in profile.values():
    if set(p)=={1}:ck(p[1]**2<=hh*kk,'linear height envelope')
    else:ck(set(p)<={0,2} and abs(p.get(0,0))*kk+abs(p.get(2,0))*hh<=hh*kk,'even height envelope')
   ck(149**112*kk<hh<=149**114*kk,'N=57 switch')
  results[variant]=dict(rows=len(rows),profiles=len(profile),parameterTerms=len(expanded))
 return results,rescalings

def prime_checks():
 def prime(p):return p>=2 and all(p%d for d in range(2,isqrt(p)+1))
 def symbol(a,p):return pow(a%p,(p-1)//2,p)
 # Both square classes 1 +/- sqrt(2) can be checked without extracting sqrt(2):
 # factor x^4-2x^2-1 via explicit square roots of 2 +/- 2i.
 count=0
 for a in range(9,250,16):
  for b in range(16,145,16):
   p=a*a+b*b
   if not prime(p):continue
   ii=a*pow(b,-1,p)%p;ck(ii*ii%p==p-1,'Gaussian square root')
   ck(symbol(b,p)==1 and symbol(a+b,p)==1 and symbol(2,p)==1,'reciprocity classes')
   ck(symbol(2+2*ii,p)==1 and symbol(2-2*ii,p)==1,'doubling radicals');count+=1
 ck(count>20,'too few examples')
 ck(prime(281) and symbol(2+2*(5*pow(16,-1,281)%281),281)==280,'wrong-residue negative control')
 return count

def main():
 parent=json.loads(PARENT.read_text());systems={v:json.loads((HERE/f'{v}-quadratic.json').read_text()) for v in ('unbalanced','balanced')};polys={v:json.loads((HERE/f'{v}-polynomial.json').read_text()) for v in systems}
 results,rescalings=check_systems(parent,systems,polys)
 rejected=0
 for label in ('row','quartic','ratio','aggregate'):
  a=deepcopy(systems);b=deepcopy(polys)
  if label=='quartic':b['balanced']['terms'][0]['coefficient']=str(int(b['balanced']['terms'][0]['coefficient'])+1)
  else:
   target=next(r for r in a['unbalanced']['residuals'] if (label=='row' or ('pair3.ratio.primary.raw.0'==r['name'] if label=='ratio' else r['name']=='weighted.aggregate.trace')))
   target['terms'][0]['coefficient']=str(F(target['terms'][0]['coefficient'])+1)
  try:check_systems(parent,a,b)
  except ValueError:rejected+=1
  else:raise ValueError('corruption not detected: '+label)
 report=dict(schema='reciprocal204-independent-verification/v27',status='PASS',sourceSha256=PIN,sourceRows=186,newRows=186,variables=204,results=results,exactRescalingRows=rescalings,selectedGaussianPrimeExamples=prime_checks(),corruptionsRejected=rejected,arithmeticProofCertifiedByComputation=False,independentNonAuthorReview=False,scope='Independent implementation of polynomial identities and full coefficient tables, with exact height envelopes and bounded prime examples. Does not certify the infinite arithmetic hypotheses or mathematical proof.')
 (HERE/'independent-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
