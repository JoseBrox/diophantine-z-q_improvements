#!/usr/bin/env python3
"""Independent full-row and complete coefficient verification for 297/342.

Does not import the producer. Monomials encode the fixed parameter as -1;
expansion uses unordered pairs, independently of the producer's double loop.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement
from math import gcd
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
DEFAULT_SOURCE=Path(__file__).resolve().parents[2]/'bundle_v11/publication/computation/quartic'
PINS={301:'9917be941135778816ce25ecb0cbc872b4ed7c9f3691d79355e5e8352667a4fe',351:'452d063b6d7da598471aa1ec0302b9e37611a44168610592931ec56aac241966'}

def norm(p):
 p={tuple(sorted(m)):c for m,c in p.items() if c}
 first=min(p,key=lambda m:(m.count(-1),tuple(i for i in m if i!=-1)))
 g=gcd(*p.values());g= -g if p[first]<0 else g
 return {m:c//g for m,c in p.items()}

def decode(row,lookup):
 return {tuple(sorted([-1]*t['parameterPower']+[lookup[i] for i in t['monomial']])):int(t['coefficient']) for t in row['terms']}

def check(baseline,source_root=DEFAULT_SOURCE,output_root=HERE):
 number=297 if baseline==301 else 342;count=2 if baseline==301 else 3
 sourcepath=source_root/f'family{baseline}'/f'quadratic-family{baseline}.json';raw=sourcepath.read_bytes()
 assert sha256(raw).hexdigest()==PINS[baseline]
 source=json.loads(raw);out=output_root/f'family{number}'
 syspath=out/f'quadratic-family{number}.json';polpath=out/f'polynomial-family{number}.json'
 system=json.loads(syspath.read_text());polynomial=json.loads(polpath.read_text())
 oldmap={c['id']:c['sourceId'] for c in source['coordinates']};newmap={c['id']:c['sourceId'] for c in system['coordinates']}
 old={r['name']:(r['sourceId'],decode(r,oldmap)) for r in source['residuals']}
 actual={r['sourceId']:(r['name'],decode(r,newmap)) for r in system['residuals']}
 assert len(actual)==len(system['residuals'])
 expected={sid:(name,p) for name,(sid,p) in old.items()};removed_coords=set();new_coords=set()
 for d in range(count):
  q=352+48*d;q4=362+48*d;c=355+48*d;u=359+48*d;u2=369+48*d;v=360+48*d;q8=850+d
  removed_coords.update(s+48*d for s in (353,354,356))
  for suffix in ('a','b','d'):del expected[old[f'detector{d}.toric.{suffix}.definition'][0]]
  replacements=[('c','inverseCube',{(c,q4):1,(q,):-1}),('q10','qPower19',{(c,u):1,(q8,q8):-1}),('q40','qPower79',{(c,v):1,(u2,u2):-1})]
  for suffix,name,p in replacements:
   sid=old[f'detector{d}.toric.{suffix}.definition'][0]
   expected[sid]=(f'detector{d}.{name}.definition',norm(p))
  sid,p=old[f'detector{d}.E10.power2.definition'];expected[sid]=(f'detector{d}.qPower38.definition',p)
  if baseline==301:
   assert q8 not in oldmap.values();new_coords.add(q8)
   expected[q8]=(f'mixed.det{d}.q1Power8.definition',norm({(q4,q4):1,(q8,):-1}))
 assert expected==actual
 assert len(system['coordinates'])==number==system['variables']==polynomial['variables']
 assert len(actual)==(271 if number==297 else 314)
 oldcoords=set(oldmap.values());newcoords=set(newmap.values())
 assert oldcoords-newcoords==removed_coords and newcoords-oldcoords==new_coords
 assert len(newcoords)==number and system['coordinates']==polynomial['coordinates']
 assert sorted(newmap)==list(range(1,number+1))
 assert system['inputCoordinate']==polynomial['inputCoordinate']==1 and newmap[1]==0
 used={i for _,p in actual.values() for m in p for i in m if i!=-1};assert used==newcoords
 assert all(max(sum(i!=-1 for i in m) for m in p)<=2 for _,p in actual.values())
 exp=defaultdict(int)
 for _,p in actual.values():
  for a,b in combinations_with_replacement(p,2):exp[tuple(sorted(a+b))]+=p[a]*p[b]*(1 if a==b else 2)
 exp={m:c for m,c in exp.items() if c}
 given=decode({'terms':polynomial['terms']},newmap);assert exp==given
 assert max(sum(i!=-1 for i in m) for m in given)==4
 ordinary=defaultdict(dict)
 for m,c in exp.items():ordinary[tuple(i for i in m if i!=-1)][m.count(-1)]=c
 maxsum=max(sum(abs(c) for c in p.values()) for p in ordinary.values())
 A=pow(80989,54929);assert A>1+maxsum
 assert any(p=={0:1} for p in ordinary.values())
 exponents={'q':1,'q2':2,'q4':4,'c':-3,'q8':8,'q19':19,'q38':38,'q79':79}
 assert exponents['c']+exponents['q4']==exponents['q']
 assert exponents['c']+exponents['q19']==2*exponents['q8']
 assert exponents['c']+exponents['q79']==2*exponents['q38']
 for q in (F(1),F(-1),F(2,3),F(-7,5)):
  c=q/q**4;u=q**16/c;v=u**4/c
  assert c==q**-3 and u==q**19 and v==q**79
 cases=0
 for nu in range(-31,32,2):
  for m in (1,10,40):
   for j in range(4):
    for z in range(-80,81):
     val=2**j*((1-2*m)*nu+2*z)
     assert val%(2**(j+1))==2**j
     if nu>0 and 2*val> -nu:assert z>=m
     cases+=1
 data={'status':'PASS','variables':number,'quadraticResiduals':len(actual),'degree':4,'integerContent':1,'symbolicTerms':len(given),'ordinaryMonomialsForNAtLeast27464':len(ordinary),'coefficientSumBitLength':maxsum.bit_length(),'coefficientHeightBound':f'H(P_N)<2^{maxsum.bit_length()}*80989^(4*N+2)','completeUnorderedPairExpansion':True,'allRetainedRowsVerified':True,'allChangedWeightRowsVerified':True,'noCoordinateUnused':True,'inputCoordinate':1,'nonzeroDomainWeightExponents':exponents,'finiteValuationChecks':cases,'noCoefficientCancellationForNAtLeast27464':True,'quadraticTableSha256':sha256(syspath.read_bytes()).hexdigest(),'polynomialTableSha256':sha256(polpath.read_bytes()).hexdigest(),'arithmeticScope':'This is exact algebraic verification; the projection theorem retains the stated arithmetic dependencies.'}
 if number==342:
  ev={m:sum(c*A**a for a,c in p.items()) for m,p in ordinary.items()};height=max(abs(c) for c in ev.values())
  data.update(explicitParameter={'N':27464,'base':80989,'exponent':54929},largestCoefficientBinaryDigits=height.bit_length(),largestCoefficientMonomials=[list(m) for m,c in ev.items() if abs(c)==height])
  assert all(ev.values())
 (out/f'independent-verification{number}.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data,indent=2))
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,default=DEFAULT_SOURCE);p.add_argument('--output-root',type=Path,default=HERE);a=p.parse_args()
 for n in (301,351):check(n,a.source_root,a.output_root)
