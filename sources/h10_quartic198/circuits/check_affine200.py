#!/usr/bin/env python3
"""Independent symbolic reconstruction and expansion, imports no producer."""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from math import gcd,lcm
import json,itertools
import sympy as sp
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'source/computation/quartic/reciprocal204_v27/unbalanced-quadratic.json'
CANDIDATE=HERE/'affine200/quadratic.json'
A=sp.Symbol('A');xx=sp.symbols('x1:215');x={i:xx[i-1] for i in range(1,215)}
def parse(row,ids=None):
 p={}
 for t in row['terms']:
  mm=tuple(sorted(ids[i] if ids else i for i in t['monomial']));p[t['parameterPower'],mm]=Fraction(t['coefficient'])
 return p
def expression(p):return sum(sp.Rational(c.numerator,c.denominator)*A**a*sp.prod(x[i] for i in m) for (a,m),c in p.items())
def terms(e):
 syms=sorted(e.free_symbols,key=str);p=sp.Poly(sp.expand(e),*syms);out={}
 for exps,c in p.terms():
  a=0;m=[]
  for s,v in zip(syms,exps):
   if s==A:a=v
   else:m.extend([int(str(s)[1:])]*v)
  out[a,tuple(sorted(m))]=Fraction(c)
 return out
def primitive(p):
 p={m:c for m,c in p.items() if c};den=lcm(*(c.denominator for c in p.values()));ints={m:int(c*den) for m,c in p.items()};gg=gcd(*ints.values());gg*=1 if ints[min(ints)]>0 else -1
 return {m:Fraction(c//gg) for m,c in ints.items()}
def pair(i,j,half=False):return sp.Matrix([x[i],(2 if half else 1)*x[j]])
def times(u,v):return sp.Matrix([u[0]*v[0]+2*u[1]*v[1],u[0]*v[1]+u[1]*v[0]])
def square(u):return times(u,u)

def check():
 raw=SOURCE.read_bytes();assert sha256(raw).hexdigest()=='21da11b4a5c9f11d8a3253162283cbd339c0f35599ab9d578a2302009f725536'
 old=json.loads(raw);new=json.loads(CANDIDATE.read_text());mapping={co['id']:co['source204Id'] if 'source204Id'in co else 205+co['id']-191 for co in new['coordinates']}
 assert len(mapping)==200 and set(mapping.values())==set(range(1,169))|set(range(183,215))
 rr={r['name']:parse(r,mapping) for r in new['residuals']};expected={}
 for r in old['residuals']:
  if r['id'] in set(range(122,140))|{2,3,4,5,6,7,144}:continue
  expected[r['name']]=parse(r)
 D=sp.Matrix([11,-6]);one=sp.Matrix([1,0]);R=sp.Matrix([x[118],0]);L2=pair(35,36);L3=pair(39,40);L4=pair(43,44);CC=pair(48,49);AT=pair(50,51);FF=pair(52,53,True)
 fields={
 'affine.Lucas.C':times(L2-R,L4)-times(R,CC),
 'affine.Lucas.AT':times(L2+R,L3)-times(R,AT),
 'affine.Lucas.F':square(L3)+square(CC)-times(CC,AT)-FF}
 f=pair(205,206);h=pair(207,208);g=pair(209,210);k=pair(211,212);s=pair(213,214)
 FU=pair(60,61,True);FV=pair(29,30,True);LP=pair(45,46);S=pair(19,20);T=pair(183,184)
 fields.update({
 'pair4.square.f':FU-square(f),'pair4.square.g':FV-square(g),
 'pair4.curve':square(h)-f+times(D,times(f,FU)),
 'pair4.secant':times(s,f-g)-h-k,
 'pair4.tangent':times(s,h-k)-one+times(D,FU+times(f,g)+FV),
 'pair4.ratio.primary.raw':times(h,L4-one)+4*times(f,S),
 'pair4.ratio.primary.regular':times(one-times(D,FU),L4-one)+4*times(h,S),
 'pair4.ratio.alternate.raw':times(k,LP-one)+4*times(g,T),
 'pair4.ratio.alternate.regular':times(one-times(D,FV),LP-one)+4*times(k,T)})
 for name,v in fields.items():
  for j in range(2):expected[name+'.'+str(j)]=primitive(terms(v[j]))
 qroots=[square(pair(193,194))+times(D,pair(185,186)+pair(189,190)),square(pair(203,204))+times(D,pair(195,196)+pair(199,200)),square(s)+times(D,f+g)]
 agg=8*(x[4]-x[90])+square(pair(159,160)-pair(161,162))[0]+4*sum(q[0] for q in qroots)
 expected['affine.weighted.aggregate']=primitive(terms(agg))
 assert set(rr)==set(expected)
 for name,p in expected.items():assert rr[name]==p,name
 # Independent unordered term-pair expansion, with parameter A formal.
 expanded=defaultdict(Fraction)
 for row in new['residuals']:
  p=list(parse(row).items())
  for i,((a,m),c) in enumerate(p):
   for j in range(i,len(p)):
    (b,n),e=p[j];expanded[a+b,tuple(sorted(m+n))]+=(1 if i==j else 2)*c*e
 expanded={m:c for m,c in expanded.items() if c};stored=parse(json.loads((HERE/'affine200/polynomial.json').read_text()));assert stored==expanded
 profiles=defaultdict(dict)
 for (a,m),c in expanded.items():profiles[m][a]=int(c)
 assert len(profiles)==3117 and len(expanded)==3118
 assert max(map(lambda key:len(key[1]),expanded))==4
 assert gcd(*(int(c) for c in expanded.values()))==1
 assert {v for a,m in expanded for v in m}==set(range(1,201))
 # Unique parameter-dependent support has A^2+1, so support is fixed for all A>0.
 pp=[p for p in profiles.values() if any(a for a in p)]
 assert len(pp)==3 and {tuple(sorted(p)) for p in pp}=={(1,),(0,2)}
 assert [p for p in pp if 2 in p]==[{0:1,2:1}]
 C0=max(abs(p.get(0,0)) for p in profiles.values());C1=max(abs(p.get(1,0)) for p in profiles.values())
 assert C1*C1<=4*C0 # C1*A <= max(C0,A^2+1) follows C1 small? Check below.
 # Direct C1 here is 44402; max(A^2+1,C0) controls it for A>=149^3.
 assert C1<=149**3
 report=dict(variables=200,quadraticRows=186,degree=4,content=1,coordinateMonomials=3117,parameterSeparatedTerms=3118,independentRowReconstruction=True,independentExpansion=True,exactHeight='max(C0,A^2+1)',C0=str(C0),A='149^(2N+1), N>=1',sourceSha256=sha256(raw).hexdigest(),scope='Exact algebraic reconstruction only. Arithmetic projection theorem is separate.')
 (HERE/'affine200/independent-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':check()
