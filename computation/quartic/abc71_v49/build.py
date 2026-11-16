#!/usr/bin/env python3
"""Reconstruct the complete 71-variable inverse-parameter quartic.

All arithmetic is exact. The stored matrix and pivot are specified invertible
row operations, not a new optimization search. Only unchanged native detector
rows are read from the pinned retained source. The independent checker rebuilds
all rows without that table or this producer.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict
from hashlib import sha256
from math import gcd,lcm
from itertools import permutations
import argparse,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def clean(p):
    return {m: Q(c) for m, c in p.items() if c}


def add(*polys):
    result = defaultdict(Q)
    for p in polys:
        for m, c in p.items():
            result[m] += c
    return clean(result)


def scale(p, c):
    return clean({m: c*v for m, v in p.items()})


def multiply(p, q):
    result = defaultdict(Q)
    for (j, m), c in p.items():
        for (k, n), d in q.items():
            result[j+k, tuple(sorted(m+n))] += c*d
    return clean(result)


def square(p):
    return multiply(p, p)


def variable(name):
    return {(0, (name,)): Q(1)}


def kplus(*values):
    return tuple(add(*(v[j] for v in values)) for j in range(2))


def ktimes(x, y):
    return (add(multiply(x[0], y[0]), scale(multiply(x[1], y[1]), 2)),
            add(multiply(x[0], y[1]), multiply(x[1], y[0])))


def ksquare(x):
    return ktimes(x, x)


def kminus(x, y):
    return (add(x[0], scale(y[0], -1)), add(x[1], scale(y[1], -1)))


def rational(p):
    return (p, {})


def field(name):
    return (variable(name+'.0'), variable(name+'.1'))


def conjugate(x):
    return (x[0], scale(x[1], -1))


ONE={(0,()):Q(1)}
PARAM={(1,()):Q(1)}
def kc(a,b=0):return(scale(ONE,a),scale(ONE,b))
def km(k,z):return (scale(z[0],k),scale(z[1],k))

def build(output):
 basis=json.loads((HERE/'basis-transformation.json').read_text())
 D=kc(11,-6);a0=kc(1,1);c0=kc(4,-2);delta0=kc(-23,17)
 parent_path=ROOT/'computation/quartic/abc74_v46/quadratic-family.json';raw=parent_path.read_bytes();parent=json.loads(raw)
 assert sha256(raw).hexdigest()=='44499a87b0188f64d7e6d2c01046883a19326c40fa9956dcf31a1eb6e7a142dc'
 blocks=[]
 for j in range(2):
  blocks.append([x['name'] for x in parent['coordinates'] if x['name'].startswith(f'detector{j}.') and x['name']!=f'detector{j}.argument'])
 assert list(map(len,blocks))==[18,18]
 field_names=['reference.u','reference.w','reference.v','pair.a','pair.c','pair.delta','pair.S','pair.T','pair.v','numerator.f','numerator.g','product.first','product.second','comparison.firstSquare','comparison.secondSquare']
 names=['input','slope']+[f'{x}.{i}' for x in field_names for i in range(2)]+['height.betaSquare','height.betaFourth','detector1.argument']+blocks[0]+blocks[1]
 assert len(names)==len(set(names))==71
 ids={n:i+1 for i,n in enumerate(names)}
 oldnames={c['id']:c['name'] for c in parent['coordinates']}
 rows=[]
 def primitive(p):
  p={(j,tuple(sorted(ids[n] if isinstance(n,str) else n for n in m))):Q(c) for (j,m),c in p.items() if c}
  den=lcm(*(c.denominator for c in p.values()));cont=gcd(*(int(den*c) for c in p.values()));sign=1 if p[min(p)]>0 else -1
  return {m:sign*int(den*c)//cont for m,c in p.items()}
 def put(name,p):rows.append((name,primitive(p)))
 def putk(name,p):
  for i in range(2):put(f'{name}.{i}',p[i])
 uH,wH,vH=(field(x) for x in field_names[:3]);a,c,delta,s,t,v=(field(x) for x in field_names[3:9]);F,G,J,K=(field(x) for x in field_names[9:13]);C2,I2=(field(x) for x in field_names[13:])
 S=kminus(kminus(vH,c0),ktimes(a0,uH));TH=kplus(kminus(ktimes(a0,wH),vH),c0)
 b2=variable('height.betaSquare');b4=variable('height.betaFourth')
 putk('reference.product',kminus(ktimes(a0,ktimes(uH,wH)),kc(1)))
 putk('reference.unit',kminus(ktimes(vH,kminus(kminus(vH,ktimes(a0,kplus(uH,wH))),km(2,c0))),delta0))
 # The specified unimodular basis is part of the exact polynomial definition.
 ref_mons=sorted(set(m for _,p in rows for m in p))
 matrix=[[int(z) for z in row] for row in basis['referenceMatrix']]
 assert len(matrix)==4 and all(len(row)==4 for row in matrix)
 determinant=0
 for perm in permutations(range(4)):
  inversions=sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4))
  z=(-1)**inversions
  for i in range(4):z*=matrix[i][perm[i]]
  determinant+=z
 assert determinant in (-1,1)
 reference=rows
 rows=[]
 for i,coeffs in enumerate(matrix):
  p=defaultdict(Q)
  for coefficient,(_,rr) in zip(coeffs,reference):
   for monomial,z in rr.items():p[monomial]+=coefficient*z
  rows.append((f'reference.primitive.{i+1}',primitive(dict(p))))
 putk('pair.product',kminus(ktimes(a,delta),ktimes(D,rational(b4))))
 putk('pair.curve',kminus(kminus(a,ksquare(c)),delta))
 putk('pair.unit',kplus(ktimes(v,kplus(v,t,km(-1,s))),delta))
 putk('pair.line',kplus(ktimes(s,t),ktimes(c,kminus(t,s)),km(2,ktimes(c,v)),km(2,delta)))
 U=kminus(kminus(v,s),c);W=kminus(kplus(v,t),c);Vbar=kminus(kplus(v,t),s)
 putk('numerator.first',kplus(ktimes(D,F),ktimes(U,Vbar)))
 putk('numerator.second',kplus(ktimes(D,G),ktimes(W,Vbar)))
 putk('product.first',kminus(ktimes(vH,J),ktimes(uH,F)));putk('product.second',kminus(ktimes(vH,K),ktimes(wH,G)))
 putk('comparison.first',kminus(C2,ksquare(kminus(s,S))))
 putk('comparison.second',kminus(I2,ksquare(kminus(t,TH))))
 put('height.betaSquare',add(b2,scale(square(variable('input')),-1)))
 put('height.betaFourth',add(b4,scale(square(b2),-1)))
 put('detector1.argument',add(variable('detector1.argument'),scale(variable('slope'),-1),scale(PARAM,-1),scale(square(b4),-1),scale(square(a[0]),-4)))
 assert len(rows)==27
 changes={}
 for j in range(2):
  w=variable(f'detector{j}.inverseWeight')
  for number,comp,prod in [(1,C2,J),(2,conjugate(I2),conjugate(K))]:
   A1=field(f'detector{j}.factor{number}')
   eq=kminus(ktimes(rational(w),A1),kplus(rational(square(w)),ktimes(rational(w),comp),ksquare(prod)))
   for i in range(2):changes[f'detector{j}.factor{number}.{i}']=eq[i]
 for row in parent['residuals']:
  name=row['name']
  if not name.startswith('detector') or name=='detector1.argument':continue
  p=changes.get(name)
  if p is None:p={(t['parameterPower'],tuple(oldnames[i] for i in t['monomial'])):Q(t['coefficient']) for t in row['terms']}
  put(name,p)
 assert len(rows)==59
 assert {i for _,p in rows for _,m in p for i in m}==set(range(1,72))

 def expand(rs):
  pp=defaultdict(int)
  for _,p in rs:
   assert max(len(m) for _,m in p)<=2
   for (j,m),x in p.items():
    for (k,n),y in p.items():pp[j+k,tuple(sorted(m+n))]+=x*y
  return {m:c for m,c in pp.items() if c}
 def ser(p):return [{'parameterPower':j,'monomial':list(m),'coefficient':str(z)} for (j,m),z in sorted(p.items())]
 # Fixed unit-constant pivot; no search occurs during reconstruction.
 base=rows[:];pivot=basis['constantPivot']-1;pp=base[pivot][1]
 assert pp.get((0,()),0)==1
 rows=[];constant_ops=[]
 for i,(name,p) in enumerate(base):
  mul=p.get((0,()),0) if i!=pivot else 0
  qq=p.copy()
  if mul:
   for key,z in pp.items():qq[key]=qq.get(key,0)-mul*z
  qq={m:z for m,z in qq.items() if z}
  content=gcd(*qq.values());sign=1 if qq[min(qq)]>0 else -1
  rows.append((name,primitive(qq)))
  constant_ops.append({'row':i+1,'pivotMultiple':mul,'content':content,'sign':sign})
 assert constant_ops==basis['constantOperations']
 poly=expand(rows);profiles=defaultdict(dict)
 for (j,m),z in poly.items():profiles[m][j]=z
 fixed=max(abs(p[0]) for p in profiles.values() if set(p)=={0})
 assert profiles[()]=={0:1,2:1}
 assert poly[0,(1,1,1,1)]==1
 assert gcd(*poly.values())==1
 assert fixed==3554 and len(profiles)==1187 and len(poly)==1190
 for p in profiles.values():
  if 1 in p:
   assert abs(p[1])<=8 and p[1]*p.get(0,0)>=0
   assert 81**2+1>=abs(p[1]*81+p.get(0,0))
  elif 2 in p:assert p=={0:1,2:1}
 system={'format':'integer-quadratic-family-inverse-parameters71-v49','variables':71,'inputCoordinate':1,'fixedParameter':{'symbol':'B','quantified':False,'domain':'fixed odd integer B>=81','sufficientThresholdEffective':False},'coordinates':[{'id':i+1,'name':n} for i,n in enumerate(names)],'residuals':[{'id':i+1,'name':n,'terms':ser(p)} for i,(n,p) in enumerate(rows)]}
 polynomial={'variables':71,'degree':4,'terms':ser(poly)}
 report={'status':'EXACT_CONDITIONAL_SPECIFICATION','variables':71,'quadraticRows':59,'degree':4,'constantCoefficient':'B^2+1','largestFixedCoefficient':fixed,'exactHeight':'B^2+1','coordinateMonomials':len(profiles),'parameterSeparatedTerms':len(poly),'content':1,'referenceMatrix':basis['referenceMatrix'],'constantPivot':pivot+1,'constantOperations':constant_ops,'parentSha256':sha256(raw).hexdigest(),'candidateIndexLabel':'relative to R0, integer','height':'Tr(a)=X^2 Tr x(A), no retained trace coordinate','comparison':'s-S and conjugate(t-TH), no retained ratios'}
 system['parentQuadraticSha256']=sha256(raw).hexdigest()
 system['coordinateConvention']='beta=X; reference uH,wH,vH are automatic units; pair a,c,delta,s,t,v encode the difference on the X-scaled curve; Tr(a) is the scaled trace; pole input is native b=w*tau^2.'
 polynomial.update(format='integer-quartic-family-inverse-parameters71-v49',inputCoordinate=1,fixedParameter=system['fixedParameter'],coordinates=system['coordinates'])
 report.update(parameterThresholdEffective=False,heightAbsorption='602/679',extraGuards=0,ordinaryMonomialsForEveryBAtLeast81=1187,integerContentForEveryIntegerB=1,scope='Defining quartic under ordinary rational abc and the elliptic-group, simultaneous-prime, trace-height and simultaneous congruent-twist premises stated in the companion paper. B is fixed odd, at least81 and sufficiently large; no numerical sufficient threshold is asserted.')
 out=output;out.mkdir(parents=True,exist_ok=True)
 for name,obj in [('quadratic-family.json',system),('polynomial-family.json',polynomial),('construction-report.json',report),('basis-transformation.json',basis)]: (out/name).write_text(json.dumps(obj,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ['referenceMatrix','constantOperations']},indent=2))
 return report

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--output',type=Path,default=HERE)
 build(parser.parse_args().output)
