#!/usr/bin/env python3
"""Independent complete-row/SOS/height verification of 281/322 quartics.

No import from the producer. Uses a separate monomial encoding, unordered
pair squaring, and reconstructs free field powers by arithmetic in Q(sqrt2).
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement
from math import gcd,lcm
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
DEFAULT_SOURCE=HERE.parents[2]/'publication/computation/quartic'
PINS={297:'144f99f6f76cadf5fae3796f7a0a6c3f740659d89fe062237b278989bcef5ce8',342:'309d97f891bb9144a3a314b361f62ed1ed4d3064938b7d15121e763f7b99b12f'}

def v(i):return {(i,):F(1)}
one={():F(1)}
def linear(*parts):
 out=defaultdict(F)
 for p,c in parts:
  for m,n in p.items():out[m]+=c*n
 return {m:c for m,c in out.items() if c}
def product(p,q):
 out=defaultdict(F)
 for m,c in p.items():
  for n,d in q.items():out[tuple(sorted(m+n))]+=c*d
 return {m:c for m,c in out.items() if c}
def normalize(p):
 p={m:c for m,c in p.items() if c};den=lcm(*(F(c).denominator for c in p.values()))
 ints={m:int(c*den) for m,c in p.items()};g=gcd(*ints.values())
 first=min(ints,key=lambda m:(m.count(-1),tuple(i for i in m if i!=-1)))
 if ints[first]<0:g=-g
 return {m:c//g for m,c in ints.items()}
def kmul(a,b):return linear((product(a[0],b[0]),1),(product(a[1],b[1]),2)),linear((product(a[0],b[1]),1),(product(a[1],b[0]),1))
def scalarkmul(a,b):return (a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def divide_and_conjugate(a,b):
 n=b[0]*b[0]-2*b[1]*b[1];iv=(b[0]/n,-b[1]/n)
 r=linear((a[0],iv[0]),(a[1],2*iv[1]));s=linear((a[0],iv[1]),(a[1],iv[0]))
 return r,linear((s,-1))
def decode(row,ids):return {tuple(sorted([-1]*x['parameterPower']+[ids[i] for i in x['monomial']])):int(x['coefficient']) for x in row['terms']}

def verify(baseline,source_root=DEFAULT_SOURCE,output_root=HERE):
 det=2 if baseline==297 else 3;number=281 if det==2 else 322
 srcpath=source_root/f'family{baseline}'/f'quadratic-family{baseline}.json';raw=srcpath.read_bytes();assert sha256(raw).hexdigest()==PINS[baseline]
 old=json.loads(raw);folder=output_root/f'family{number}';syspath=folder/f'quadratic-family{number}.json';ppath=folder/f'polynomial-family{number}.json'
 new=json.loads(syspath.read_text());pjson=json.loads(ppath.read_text());oldids={c['id']:c['sourceId'] for c in old['coordinates']};ids={c['id']:c['sourceId'] for c in new['coordinates']}
 deleted={c['sourceId'] for c in old['coordinates'] if c['name'].startswith('mixed.private.') or (c['name'].startswith('mixed.') and '.power' in c['name'] and not c['name'].startswith('mixed.det'))}
 expected={};removed=[]
 for r in old['residuals']:
  if (r['name'].startswith('mixed.det') and any(s in r['name'] for s in ('.factor','.product'))) or (r['name'].startswith('mixed.') and '.power' in r['name'] and not r['name'].startswith('mixed.det')):removed.append(r['sourceId']);continue
  expected[r['sourceId']]=(r['name'],decode(r,oldids))
 sq={}
 for i,s in enumerate([255,257,259,261],1):sq[f'U{i}']=(v(s),linear((v(s+1),2)))
 for name,s in [('H',311),('C1',305),('C2',313),('C3',315),('C4',317)]:sq[name]=(v(s),linear((v(s+1),2)))
 sq['I']=(linear((v(307),1),(v(232),-6),(v(248),306),(one,15015)),linear((v(308),2),(v(233),-6)))
 sq['F']=(linear((v(319),1),(v(253),-2),(one,1)),linear((v(320),4),(v(254),-4)))
 pow4={};pow8={};D=(F(11),F(-6));D2=scalarkmul(D,D);D4=scalarkmul(D2,D2)
 assert D2==(193,-132) and D4==(72097,-50952)
 for i,(s,s4,s8) in enumerate([(178,180,182),(190,192,0),(196,198,200),(208,210,212),(220,222,224)]):
  sq[f'V{i}']=(v(s),linear((v(s+1),-2)))
  pow4[f'V{i}']=divide_and_conjugate((linear((v(s4),193)),linear((v(s4+1),-132))),D2)
  if s8:pow8[f'V{i}']=divide_and_conjugate((v(s8),v(s8+1)),D4)
 added=set()
 for j,name in enumerate(['C1','I','U1','U2','U3']):
  fourth=kmul(sq[name],sq[name]);out=[]
  for comp in range(2):
   s=10000+2*j+comp;added.add(s);out.append(v(s));expected[s]=(f'even.{name}.power4.{comp}.definition',normalize(linear((fourth[comp],1),(v(s),-1))))
  pow4[name]=tuple(out)
 lists=[ [('C2',2,79),('H',2,38),('U1',4,4),('V0',8,8)], [('C3',2,79),('C1',4,38),('U2',4,4),('V2',8,8)], [('C4',2,79),('I',4,38),('U3',4,4),('V3',8,8)], [('F',2,79),('U4',2,2),('V1',4,4),('V4',8,8)] ]
 for d in range(det):
  off=48*d;weight={2:361+off,4:362+off,8:850+d,38:369+off,79:360+off};start=11000+20*d
  for g,terms in enumerate(lists):
   for comp in range(2):
    sid=start+2*g+comp;added.add(sid);p=linear((one,1)) if comp==0 else {}
    for name,power,exponent in terms:
     value={2:sq,4:pow4,8:pow8}[power][name][comp];p=linear((p,1),(product(v(weight[exponent]),value),1))
    expected[sid]=(f'even.det{d}.factor{g}.{comp}.definition',normalize(linear((p,1),(v(sid),-1))))
  left=(v(start),v(start+1))
  for k in (1,2,3):
   y=(v(start+2*k),v(start+2*k+1));z=kmul(left,y);target=380+off if k==3 else start+8+2*(k-1)
   for comp in range(2):
    if k!=3:added.add(target+comp)
    sid=12000+20*d+2*k+comp;expected[sid]=(f'even.det{d}.product{k}.{comp}.definition',normalize(linear((z[comp],1),(v(target+comp),-1))))
   left=(v(target),v(target+1))
 actual={r['sourceId']:(r['name'],decode(r,ids)) for r in new['residuals']}
 assert len(actual)==len(new['residuals']) and actual==expected
 assert len(actual)==(255 if det==2 else 294)
 assert len(ids)==number==new['variables']==pjson['variables']
 assert new['coordinates']==pjson['coordinates'] and sorted(ids)==list(range(1,number+1))
 assert new['inputCoordinate']==pjson['inputCoordinate']==1 and ids[1]==0
 assert set(oldids.values())-set(ids.values())==deleted and set(ids.values())-set(oldids.values())==added
 used={i for name,row in actual.values() for m in row for i in m if i!=-1};assert used==set(ids.values())
 assert all(max(sum(i!=-1 for i in m) for m in row)<=2 for name,row in actual.values())
 expanded=defaultdict(int)
 for name,row in actual.values():
  for m,n in combinations_with_replacement(row,2):expanded[tuple(sorted(m+n))]+=row[m]*row[n]*(1 if m==n else 2)
 expanded={m:c for m,c in expanded.items() if c};supplied=decode({'terms':pjson['terms']},ids)
 assert expanded==supplied and max(sum(i!=-1 for i in m) for m in expanded)==4 and gcd(*expanded.values())==1
 ordinary=defaultdict(dict)
 for m,c in expanded.items():ordinary[tuple(i for i in m if i!=-1)][m.count(-1)]=c
 assert ordinary[(489,489)]=={0:1,2:1}
 assert all(set(p) in ({0},{1}) for m,p in ordinary.items() if m!=(489,489))
 C=max(abs(p[0]) for p in ordinary.values() if set(p)=={0});L=max(abs(p[1]) for p in ordinary.values() if set(p)=={1})
 assert C.bit_length()==1520 and L==13118436242 and C>L*L
 A22=80989**45;A23=80989**47
 assert A22*A22+1<C<A23*A23+1 and A23>L
 # Independent valuations for every factor term. These supplement the infinite proof.
 tested=0
 for nu in range(-31,32,2):
  for group in lists:
   for position,(name,power,exponent) in enumerate(group):
    even=name=='H' or name[0] in 'UV'
    for val in range(-100,101,2 if even else 1):
     z=power*val-exponent*nu
     assert z%(2**(position+1))==2**position
     if nu>0 and 2*z>-nu:
      requirement=20 if name=='H' else 1 if name[0] in 'UV' else 10 if name in ('C1','I') else 40
      assert val>=requirement
     tested+=1
 # Check the original primary depth20 completeness already satisfies all new terms.
 for group in lists:
  for name,power,exponent in group:
   comp_depth=40 if name=='H' else 2 if name[0] in 'UV' else 12 if name in ('C1','I') else 40
   assert power*comp_depth-exponent>0
 report={'status':'PASS','variables':number,'quadraticResiduals':len(actual),'degree':4,'content':1,'ordinaryMonomialsForEveryPositiveParameter':len(ordinary),'symbolicTerms':len(expanded),'allRowsIndependentlyReconstructed':True,'allRetainedRowsVerified':True,'completeUnorderedPairExpansion':True,'freeFourthAndEighthPowersReconstructedInQsqrt2':True,'allCoordinatesUsed':True,'inputCoordinate':1,'originalWeightsAndScalarBlockRetained':True,'factorSpecifications':lists,'finiteValuationChecks':tested,'originalCompletenessDepthsSuffice':True,'constantCoefficientMaximum':str(C),'constantCoefficientMaximumBits':C.bit_length(),'linearCoefficientMultiplierMaximum':L,'heightFormulaForEveryPositiveParameter':'max(C,A^2+1)','exactHeightThresholdN':23,'exactHeightForNAtLeast23':'80989^(4*N+2)+1','noSupportCancellationForPositiveParameter':True,'quadraticTableSha256':sha256(syspath.read_bytes()).hexdigest(),'polynomialTableSha256':sha256(ppath.read_bytes()).hexdigest(),'arithmeticScope':'Finite verification checks all algebra and supplementary valuation cases; the full projection theorem additionally uses the stated arithmetic premises and written proof.'}
 if det==3:
  A=80989**54929;height=A*A+1
  assert height>C and A>L
  report.update(explicitParameterN=27464,explicitParameter='80989^54929',explicitCoefficientHeight='80989^109858+1',explicitHeightBinaryDigits=height.bit_length())
 (folder/f'independent-verification{number}.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ['status','variables','quadraticResiduals','ordinaryMonomialsForEveryPositiveParameter','symbolicTerms','finiteValuationChecks','quadraticTableSha256','polynomialTableSha256']}))

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,default=DEFAULT_SOURCE);p.add_argument('--output-root',type=Path,default=HERE);a=p.parse_args()
 for n in (297,342):verify(n,a.source_root,a.output_root)
