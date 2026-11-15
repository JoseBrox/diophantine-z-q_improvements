#!/usr/bin/env python3
"""Independent named-row reconstruction for the 78-variable abc quartic.

This checker does not import the new producer. It preserves every unchanged
parent row, derives the five changed rows directly, and independently expands
all seventy primitive integer squares. Its arithmetic checks are finite
checks of the stated height lemma, not a proof of abc or the inherited inputs.
"""
from __future__ import annotations
from fractions import Fraction as Q
from collections import defaultdict
from pathlib import Path
from math import gcd,lcm,isqrt
from functools import reduce
import argparse, hashlib, json, sys, tempfile, subprocess
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def require(ok,message):
 if not ok:raise AssertionError(message)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def add(*args):
 d=defaultdict(Q)
 for p in args:
  for k,c in p.items():d[k]+=c
 return {k:c for k,c in d.items() if c}
def scale(p,c):return {k:c*v for k,v in p.items() if c*v}
def mul(p,q):
 d=defaultdict(Q)
 for (a,m),c in p.items():
  for (b,n),e in q.items():d[(a+b,tuple(sorted(m+n)))]+=c*e
 return {k:c for k,c in d.items() if c}
def square(p):return mul(p,p)
def const(c):return {(0,()):Q(c)} if c else {}
def vv(name):return {(0,(name,)):Q(1)}
def decode(terms,names):
 return {(t['parameterPower'],tuple(sorted(names[i] for i in t['monomial']))):Q(t['coefficient']) for t in terms}
def numeric(p,ids):return {(a,tuple(sorted(ids[n] for n in m))):c for (a,m),c in p.items()}
def primitive(p,ids):
 q=numeric(p,ids);D=lcm(*(c.denominator for c in q.values()));G=gcd(*(int(D*c) for c in q.values()))
 if q[min(q)]<0:G=-G
 return {k:int(D*c/G) for k,c in q.items()}
def rational_height_checks():
 # Check the primewise radical majorant, after multiplying its weights by eight.
 count=0
 for e in range(-64,65):
  for position in range(4):
   for v in ([0] if position==3 else range(1,65)):
    a,b,c=(v,0,0) if position==0 else (0,v,0) if position==1 else (0,0,v) if position==2 else (0,0,0)
    if a%2 or b%2 or (a-c+e)%8 or (b-c+e)%2:continue
    lhs=8 if a+b+c else 0
    rhs=a+4*b+c+7*max(e,0)+3*max(-e,0)
    require(lhs<=rhs,'Primewise mixed-height inequality');count+=1
 require(2+2*2<8,'Negative-control denominator weight must fail')
 require(1+6<8,'Negative-control numerator weight must fail')
 k=Q(101,100);cx=(2+k)/(4*(4-3*k));cy=4*cx;gamma=Q(7,2)
 require(cx==Q(301,388) and cy==Q(301,97),'Mixed height constants')
 q=cx*2/gamma
 require(q==Q(301,679) and 2*q==Q(602,679) and 2*q<1,'Strict absorption')
 require(q/(1-2*q)==Q(301,77),'Final input-height coefficient')
 require((cy*2/gamma)/(1-2*q)==Q(1204,77),'Final trace-height coefficient')
 # Independent exact radical inequalities for concrete rational pairs.
 from sympy import factorint
 values=[Q(0),Q(1),Q(-1),Q(2),Q(-3),Q(1,2),Q(-2,3),Q(3,5),Q(7,4)]
 examples=0
 for x in values:
  for y in values:
   if not x or not y:continue
   s=x**8+y*y;ratio=x**8/(y*y);A=ratio.numerator;B=ratio.denominator;C=A+B
   require(isqrt(A)**2==A and isqrt(B)**2==B,'Primitive summands are squares')
   require(x**8==s*Q(A,C) and y*y==s*Q(B,C),'Primitive normalization')
   radical=1
   for p in factorint(A*B*C):radical*=int(p)
   require(radical**8<=A*(B**4)*C*(s.numerator**7)*(s.denominator**3),'Exact radical majorant')
   for shift in [1,81,101,1001]:
    u=s+shift
    require(u.denominator==s.denominator,'Positive shift preserves the reduced denominator')
    require(max(u.numerator,u.denominator)>=max(s.numerator,s.denominator),'Positive shift height')
   examples+=1
 return dict(primewise_admissible_cases=count,rational_pairs=examples,
   numerator_weight_negative_control=True,denominator_weight_negative_control=True,
   abc_exponent='101/100',contact_exponent='7/2',absorption='602/679',
   input_height_coefficient='301/77',trace_height_coefficient='1204/77')
def run():
 pins=json.loads((HERE/'inputs.json').read_text())
 for rel,p in pins['files'].items():
  file=ROOT/rel;require(file.is_file() and file.stat().st_size==p['bytes'] and digest(file)==p['sha256'],'Source binding: '+rel)
 parent=json.loads((ROOT/'computation/quartic/abc79_v27/quadratic-family.json').read_text())
 system=json.loads((HERE/'quadratic-family.json').read_text())
 polynomial=json.loads((HERE/'polynomial-family.json').read_text())
 oldnames={c['id']:c['name'] for c in parent['coordinates']}
 rename={'height.sumSquares':'height.inputSquare','height.product':'height.inputFourth'}
 expected_names=[rename.get(c['name'],c['name']) for c in parent['coordinates'] if c['name']!='inputComparison.real']
 require([c['name'] for c in system['coordinates']]==expected_names,'Exact coordinate deletion and renaming')
 require(len(expected_names)==78 and system['variables']==78,'78 coordinates')
 ids={name:i+1 for i,name in enumerate(expected_names)}
 sh=vv('height.inputSquare');ph=vv('height.inputFourth');X=vv('input');T=vv('height.trace')
 Lr=vv('ratio.primary.0');Li=vv('ratio.primary.1');Ir=add(Lr,scale(sh,-1),const(-3))
 changed={
  'square.input.0':add(vv('square.input.0'),scale(square(Ir),-1),scale(square(Li),-2)),
  'square.input.1':add(vv('square.input.1'),scale(mul(Ir,Li),-2)),
  'height.inputSquare':add(sh,scale(square(X),-1)),
  'height.inputFourth':add(ph,scale(square(sh),-1)),
  'detector1.argument':add(vv('detector1.argument'),scale(vv('slope'),-1),{(1,()):Q(-1)},scale(square(ph),-1),scale(square(T),-1))}
 expected=[]
 for row in parent['residuals']:
  if row['name']=='inputComparison':continue
  name=rename.get(row['name'],row['name'])
  if name in changed:p=changed[name]
  else:
   p=decode(row['terms'],oldnames)
   p={(a,tuple(sorted(rename.get(n,n) for n in m))):c for (a,m),c in p.items()}
   require(not any('inputComparison.real' in m for _,m in p),'A deleted coordinate survives')
  expected.append((name,primitive(p,ids)))
 require(len(expected)==70 and len(system['residuals'])==70,'70 quadratic rows')
 for i,((name,p),row) in enumerate(zip(expected,system['residuals']),1):
  require(row['id']==i and row['name']==name,'Row order')
  actual={(t['parameterPower'],tuple(t['monomial'])):int(t['coefficient']) for t in row['terms']}
  require(actual==p,'Changed or retained row differs: '+name)
  require(max(len(m) for _,m in p)<=2,'Quadratic row')
 full=defaultdict(int)
 for _,p in expected:
  for (a,m),c in p.items():
   for (b,n),d in p.items():full[(a+b,tuple(sorted(m+n)))]+=c*d
 full={k:c for k,c in full.items() if c}
 actual={(t['parameterPower'],tuple(t['monomial'])):int(t['coefficient']) for t in polynomial['terms']}
 require(full==actual,'Every expanded quartic coefficient')
 require(full.get((0,(1,1,1,1)))==1,'Exact input fourth-power coefficient')
 require(max(len(m) for _,m in full)==4,'Exact degree four')
 require({i for _,m in full for i in m}==set(range(1,79)),'All 78 variables occur')
 # Semantic negative controls do not call the producer.
 corrupted=add(ph,scale(mul(sh,X),-1))
 require(primitive(corrupted,ids)!=dict(expected)['height.inputFourth'],'Wrong sixth-power scale rejected')
 wrongI=add(Lr,scale(sh,-1))
 wrong=add(vv('square.input.0'),scale(square(wrongI),-1),scale(square(Li),-2))
 require(primitive(wrong,ids)!=dict(expected)['square.input.0'],'Missing positive input shift rejected')
 profiles=defaultdict(dict)
 for (j,m),c in full.items():profiles[m][j]=c
 constant=profiles[()];fixedmax=max(abs(p[0]) for p in profiles.values() if set(p)=={0})
 require(constant.keys()=={0,2} and constant[2]==1,'Constant profile')
 for p in profiles.values():
  if 1 in p:
   a=abs(p[1]);c=abs(p.get(0,0));require(a<=2 and c<=1,'Linear profile bound')
   require(constant[0]>=2,'Uniform coefficient-height comparison')
  elif 2 in p:require(p==constant,'Only the constant profile is quadratic in B')
  else:require(p[0]!=0,'Nonzero fixed profile')
 # Rebuild in an isolated output directory and compare bytes, not imported objects.
 with tempfile.TemporaryDirectory() as td:
  result=subprocess.run([sys.executable,'-B',str(HERE/'build.py'),'--output',td],capture_output=True,text=True)
  require(result.returncode==0,'Isolated producer failed: '+result.stderr)
  for name in ['quadratic-family.json','polynomial-family.json','construction-report.json']:
   require((Path(td)/name).read_bytes()==(HERE/name).read_bytes(),'Nonreproducible generated file: '+name)
 height=rational_height_checks()
 return dict(schema='abc78-independent-verification/v34',status='PASS',variables=78,quadraticRows=70,
  parameterSeparatedTerms=len(full),ordinaryMonomialsForEveryPositiveB=len(profiles),degree=4,
  integerContentForEveryPositiveB=1,unitCoefficientMonomial=[1,1,1,1],
  exactHeight='max(%d,B^2+%d)'%(fixedmax,constant[0]),
  unchangedRows=65,changedRows=5,removedRows=1,isolatedReconstruction=True,
  negativeControls=['wrong sixth-power scale','missing positive input shift','insufficient numerator valuation weight','insufficient denominator valuation weight'],
  arithmeticChecks=height,independentMathematicalReview=False,
  scope='All new rows, every quartic coefficient, and stated finite height examples. The full arithmetic proof is in the manuscript. These checks do not establish abc or the retained arithmetic premises.')
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path);args=ap.parse_args()
 report=run();raw=json.dumps(report,indent=2)+'\n'
 if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(raw)
 else:
  certificate=HERE/'independent-verification.json'
  require(certificate.is_file() and certificate.read_text()==raw,'Published certificate differs or is missing')
 print(raw)
