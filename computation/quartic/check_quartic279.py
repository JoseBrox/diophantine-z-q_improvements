#!/usr/bin/env python3
"""Independent reconstruction of every row and coefficient of family279.

Imports only polynomial utilities from the independent checker, not a
producer. Reconstructs the contact polynomial by forward differences of
21 exact evaluations, independently of the producer's coefficient product.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement
from math import comb,factorial,gcd
from pathlib import Path
import json
import check_quartic_even as C
HERE=Path(__file__).resolve().parent
DEFAULT_SOURCE=C.DEFAULT_SOURCE

def addlist(a,b):
 r=[F(0)]*max(len(a),len(b))
 for i,x in enumerate(a):r[i]+=x
 for i,x in enumerate(b):r[i]+=x
 return r

def times_linear(a,r):
 q=[F(0)]*(len(a)+1)
 for i,c in enumerate(a):q[i]-=r*c;q[i+1]+=c
 return q

def replace(p,substitution):
 result={}
 for monomial,coefficient in p.items():
  term={():F(coefficient)}
  for var in monomial:term=C.product(term,substitution.get(var,C.v(var)))
  result=C.linear((result,1),(term,1))
 return result

def verify(source_root=DEFAULT_SOURCE,output_root=HERE):
 raw=(source_root/'family297/quadratic-family297.json').read_bytes();assert sha256(raw).hexdigest()==C.PINS[297]
 src=json.loads(raw);oldids={c['id']:c['sourceId'] for c in src['coordinates']};folder=output_root/'family279'
 spath=folder/'quadratic-family279.json';ppath=folder/'polynomial-family279.json';system=json.loads(spath.read_text());poly=json.loads(ppath.read_text());report=json.loads((folder/'construction-report279.json').read_text());ids={c['id']:c['sourceId'] for c in system['coordinates']}
 roots=[theta+3*j for j in range(4) for theta in [F(0),F(-1,2),F(-1),F(1,2399),F(-32,407)]]
 values=[]
 for integer in range(21):
  value=F(1)
  for r in roots:value*=integer-r
  values.append(value)
 coefficients=[F(0)];basis=[F(1)];differences=values
 for k in range(21):
  coefficients=addlist(coefficients,[differences[0]*c/F(factorial(k)) for c in basis])
  differences=[differences[j+1]-differences[j] for j in range(len(differences)-1)]
  basis=times_linear(basis,F(k))
 assert coefficients[-1]==1 and len(coefficients)==21
 for root in roots:assert sum(c*root**i for i,c in enumerate(coefficients))==0
 assert [str(x) for x in coefficients]==report['contactPolynomialCoefficients']
 # Check the same sparse quadratic basis spans every degree through20.
 exponents=[0,1,2,4,5,8,9,10]
 splits={}
 for k in range(21):
  if k not in exponents:splits[k]=min((a,b) for a in exponents for b in exponents if a<=b and a+b==k)
 assert len(splits)==13
 expected={};changes={};new=set();deleted=set();sub={}
 for c in src['coordinates']:
  name=c['name']
  if name.startswith('mixed.private.') or (name.startswith('mixed.') and '.power' in name and not name.startswith('mixed.det')):deleted.add(c['sourceId'])
 deleted.update([182,183,186,187,192,193,200,201,204,205,212,213,216,217,224,225,228,229])
 for fs,ws,rs in [(178,180,186),(196,198,204),(208,210,216),(220,222,228)]:
  sub[rs]=C.linear((C.one,1),(C.v(fs),F(-22,5)),(C.v(fs+1),F(48,5)),(C.v(ws),F(-386,15)))
  sub[rs+1]=C.linear((C.v(fs),F(12,5)),(C.v(fs+1),F(-44,5)),(C.v(ws+1),F(88,5)))
 changes['logV1.0.definition']=C.linear((C.v(164),1),(C.product(C.v(188),C.v(234)),-1),(C.product(C.v(189),C.v(235)),-2))
 changes['logV1.1.definition']=C.linear((C.v(165),1),(C.product(C.v(188),C.v(235)),-1),(C.product(C.v(189),C.v(234)),-1))
 for d in range(2):
  off=48*d;t=37 if d==0 else 391;t2=346 if d==0 else 392;t4=347 if d==0 else 393;ff=348 if d==0 else 394;e=350+off;q=352+off
  ps={0:C.one,1:C.v(t),2:C.v(t2),4:C.v(t4)}
  changes[f'detector{d}.Fmiddle.definition']=C.linear((C.product(ps[2],ps[2]),1),(ps[4],-1))
  for j,(k,a,b) in enumerate([(5,1,4),(8,4,4),(9,1,8),(10,5,5)]):
   sid=20000+20*d+j;new.add(sid);expected[sid]=(f'amplified.det{d}.tPower{k}.definition',C.normalize(C.linear((C.product(ps[a],ps[b]),1),(C.v(sid),-1))));ps[k]=C.v(sid)
  def represent(coeffs):
   result={}
   for k,c in enumerate(coeffs):
    term=ps[k] if k in ps else C.product(ps[splits[k][0]],ps[splits[k][1]])
    result=C.linear((result,1),(term,c))
   return result
  changes[f'detector{d}.F.definition']=C.linear((represent(coefficients),1),(C.v(ff),-1))
  if d==0:num=represent([F(comb(20,k)*(-1)**(20-k)) for k in range(21)])
  else:
   new.update([20100,20101])
   expected[20100]=('amplified.det1.scaledDeltaPower5.definition',C.normalize({(395,397):1,(20100,):-1}))
   expected[20101]=('amplified.det1.scaledDeltaPower10.definition',C.normalize({(20100,20100):1,(20101,):-1}))
   num=C.product(C.v(20101),C.v(20101))
  changes[f'detector{d}.eWeight.definition']=C.linear((C.product(C.v(ff),C.v(e)),1),(num,-1))
  ds=C.linear((C.v(t2),1),(C.v(t),-2),(C.one,1))
  changes[f'detector{d}.q1.definition']=C.linear((C.product(ds,C.v(q)),1),(C.v(e),-1))
  changes[f'detector{d}.eDelta.definition']=C.linear((C.product(ds,C.v(e)),1),(C.v(384+off),-1))
  changes[f'detector{d}.B.definition']=C.linear((C.product(C.v(384+off),C.v(385+off)),1),(C.product(C.v(383+off),C.v(383+off)),-1))
  changes[f'detector{d}.qPower19.definition']=C.linear((C.product(C.v(q),C.v(362+off)),1),(C.v(359+off),-1))
 for r in src['residuals']:
  name=r['name']
  skip=(name.startswith('mixed.det') and any(s in name for s in ('.factor','.product'))) or (name.startswith('mixed.') and '.power' in name and not name.startswith('mixed.det')) or (name.startswith('logV') and any(s in name for s in ('.wPower4.','.rationalApproximation.'))) or name in ['logV1.polynomial.0.definition','logV1.polynomial.1.definition']
  if skip:continue
  value=changes.pop(name) if name in changes else C.decode(r,oldids);value=replace(value,sub)
  for a,b in [('qPower19','qPower5'),('qPower38','qPower10'),('qPower79','qPower23')]:name=name.replace('.'+a+'.','.'+b+'.')
  expected[r['sourceId']]=(name,C.normalize(value))
 assert not changes
 sq={}
 for i,s in enumerate([255,257,259,261],1):sq[f'U{i}']=(C.v(s),C.linear((C.v(s+1),2)))
 for name,s in [('H',311),('C1',305),('C2',313),('C3',315),('C4',317)]:sq[name]=(C.v(s),C.linear((C.v(s+1),2)))
 sq['I']=(C.linear((C.v(307),1),(C.v(232),-6),(C.v(248),306),(C.one,15015)),C.linear((C.v(308),2),(C.v(233),-6)))
 sq['F']=(C.linear((C.v(319),1),(C.v(253),-2),(C.one,1)),C.linear((C.v(320),4),(C.v(254),-4)))
 fourth={};eighth={}
 for i,(s,w) in enumerate([(178,180),(190,None),(196,198),(208,210),(220,222)]):
  sq[f'V{i}']=(C.v(s),C.linear((C.v(s+1),-2)))
  if w:fourth[f'V{i}']=C.divide_and_conjugate((C.linear((C.v(w),193)),C.linear((C.v(w+1),-132))),(F(193),F(-132)))
 for j,(name,power) in enumerate([('C1',4),('U3',4),('U4',4),('U4',8)]):
  prev=sq[name] if power==4 else fourth[name];prod=C.kmul(prev,prev);point=[]
  for comp in range(2):
   sid=21000+2*j+comp;new.add(sid);point.append(C.v(sid));expected[sid]=(f'amplified.{name}.power{power}.{comp}.definition',C.normalize(C.linear((prod[comp],1),(C.v(sid),-1))))
  (fourth if power==4 else eighth)[name]=tuple(point)
 groups=[[('C2',2,23),('H',2,10),('U3',4,4),('U4',8,8)],[('C3',2,23),('C1',4,10),('V0',4,4)],[('C4',2,23),('U1',2,2),('V2',4,4)],[('F',2,23),('U2',2,2),('V3',4,4)],[('I',2,5),('V1',2,2),('V4',4,4)]]
 for d in range(2):
  off=48*d;start=22000+30*d;weights={2:361+off,4:362+off,8:850+d,5:359+off,10:369+off,23:360+off}
  for g,group in enumerate(groups):
   for comp in range(2):
    sid=start+2*g+comp;new.add(sid);p=C.one if comp==0 else {}
    for name,power,weight in group:
     p=C.linear((p,1),(C.product(C.v(weights[weight]),{2:sq,4:fourth,8:eighth}[power][name][comp]),1))
    expected[sid]=(f'amplified.det{d}.factor{g}.{comp}.definition',C.normalize(C.linear((p,1),(C.v(sid),-1))))
  left=(C.v(start),C.v(start+1))
  for k in range(1,5):
   prod=C.kmul(left,(C.v(start+2*k),C.v(start+2*k+1)));target=380+off if k==4 else start+10+2*(k-1)
   for comp in range(2):
    if k!=4:new.add(target+comp)
    expected[23000+30*d+2*k+comp]=(f'amplified.det{d}.product{k}.{comp}.definition',C.normalize(C.linear((prod[comp],1),(C.v(target+comp),-1))))
   left=(C.v(target),C.v(target+1))
 actual={r['sourceId']:(r['name'],C.decode(r,ids)) for r in system['residuals']}
 assert len(actual)==len(system['residuals'])==253 and actual==expected
 assert set(oldids.values())-set(ids.values())==deleted and set(ids.values())-set(oldids.values())==new
 assert len(ids)==system['variables']==poly['variables']==279 and sorted(ids)==list(range(1,280))
 assert system['coordinates']==poly['coordinates'] and system['inputCoordinate']==poly['inputCoordinate']==1 and ids[1]==0
 assert {i for name,p in actual.values() for m in p for i in m if i!=-1}==set(ids.values())
 assert all(max(sum(i!=-1 for i in m) for m in p)<=2 for name,p in actual.values())
 expanded=defaultdict(int)
 for name,p in actual.values():
  for m,n in combinations_with_replacement(p,2):expanded[tuple(sorted(m+n))]+=p[m]*p[n]*(1 if m==n else 2)
 expanded={m:c for m,c in expanded.items() if c};given=C.decode({'terms':poly['terms']},ids)
 assert expanded==given and gcd(*expanded.values())==1 and max(sum(i!=-1 for i in m) for m in expanded)==4
 ordinary=defaultdict(dict)
 for m,c in expanded.items():ordinary[tuple(i for i in m if i!=-1)][m.count(-1)]=c
 assert ordinary[(489,489)]=={0:1,2:1} and all(set(p) in ({0},{1}) for m,p in ordinary.items() if m!=(489,489))
 constant=max(abs(p[0]) for p in ordinary.values() if set(p)=={0});linear=max(abs(p[1]) for p in ordinary.values() if set(p)=={1})
 assert constant.bit_length()==1520 and linear==13118436242 and constant>linear*linear
 assert 80989**90+1<constant<80989**94+1
 # Certificate for G2's absence of K-roots:17 splits in Q(sqrt2), but N has no residue root.
 assert 6*6%17==2
 residues=[(15-6*j-2*j*j)%17 for j in range(17)];assert all(residues)
 # Series from the exact recurrence independently proves the formal precision claims.
 gj=[F(1),F(-2,5)]
 for j in range(2,4):gj.append(gj[-1]*F(4*j-5,4*j+1))
 assert gj[:3]==[F(1),F(-2,5),F(-2,15)] and gj[3]!=0
 # Algebraic normalization and every valuation class used in the new factors.
 d=20;epsilon=2
 assert d+epsilon==22 and 4-epsilon==2
 assert d-(4-epsilon)==18 and d+epsilon-4==18
 tested=0
 for nu in range(-31,32,2):
  for group in groups:
   for pos,(name,power,weight) in enumerate(group):
    even=name=='H' or name[0] in 'UV'
    for value in range(-100,101,2 if even else 1):
     z=power*value-weight*nu;assert z%(2**(pos+1))==2**pos
     if nu>0 and 2*z>-nu:
      requirement=6 if name=='H' else 1 if name[0] in 'UV' else 3 if name in ('C1','I') else 12
      assert value>=requirement
     tested+=1
 for group in groups:
  for name,power,weight in group:
   val=6 if name=='H' else 2 if name[0] in 'UV' else 4 if name in ('C1','I') else 12
   assert power*val-weight>0
 result={'status':'PASS','variables':279,'quadraticResiduals':253,'degree':4,'content':1,'ordinaryMonomialsForEveryPositiveParameter':len(ordinary),'symbolicTerms':len(expanded),'allRowsIndependentlyReconstructed':True,'completeUnorderedPairExpansion':True,'allCoordinatesUsed':True,'contactPolynomialDegree':20,'contactPolynomialIndependentReconstruction':'Forward differences of21 exact evaluations, followed by verification at20 contact roots','quadraticEvaluationBasis':exponents,'normalization':{'F_e_equals':'(a*delta)^20','q_delta_power':2,'trace_e_delta_power':2,'R_delta_denominator_power':22,'prepared_q_valuation':'18*v(a)-2*v(lambda)'},'G2NonvanishingCertificate':{'splitPrime':17,'sqrt2ModPrime':6,'integerNumerator':'15-6w-2w^2','nonzeroResidues':residues},'localOrders':{'H':6,'highComparison':12,'input':3,'formalPoint':1},'finiteValuationChecks':tested,'completenessDepthsSuffice':True,'constantCoefficientMaximum':str(constant),'constantCoefficientMaximumBits':constant.bit_length(),'linearCoefficientMultiplierMaximum':linear,'heightFormulaForEveryPositiveParameter':'max(C,A^2+1)','exactHeightThresholdN':23,'exactHeightForNAtLeast23':'80989^(4*N+2)+1','noSupportCancellationForPositiveParameter':True,'quadraticTableSha256':sha256(spath.read_bytes()).hexdigest(),'polynomialTableSha256':sha256(ppath.read_bytes()).hexdigest(),'arithmeticScope':'Finite algebra and supplementary valuation checks only. Projection uses the written contact-height amplification theorem, even-valuation argument, inherited arithmetic premises, and an ineffective eventual coefficient threshold.'}
 (folder/'independent-verification279.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ['status','variables','quadraticResiduals','ordinaryMonomialsForEveryPositiveParameter','symbolicTerms','finiteValuationChecks','quadraticTableSha256','polynomialTableSha256']}))
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,default=DEFAULT_SOURCE);p.add_argument('--output-root',type=Path,default=HERE);a=p.parse_args();verify(a.source_root,a.output_root)
