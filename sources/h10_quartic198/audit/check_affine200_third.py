"""Third implementation of candidate row and coefficient auditing.
Uses symbolic sqrt(2) and direct coefficient extraction; imports no producer/checker.
"""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction
from math import gcd,lcm
import sympy as s
import json,hashlib
BASE=Path(__file__).resolve().parents[1]
source=BASE/'source/computation/quartic/reciprocal204_v27/unbalanced-quadratic.json'
candidate=BASE/'circuits/affine200/quadratic.json'
old=json.loads(source.read_text());new=json.loads(candidate.read_text());rho=s.sqrt(2)
A=s.Symbol('A');X=s.symbols('x1:215');v={i:X[i-1] for i in range(1,215)}
name_to_fresh={f'pair4.{name}.{bit}':205+2*i+bit for i,name in enumerate(('f','h','g','k','s')) for bit in (0,1)}
mapnew={c['id']:c['source204Id'] if 'source204Id' in c else name_to_fresh[c['name']] for c in new['coordinates']}
def expression(row,mapping=None):
 return s.expand(sum(s.Rational(t['coefficient'])*A**t['parameterPower']*s.prod(v[mapping[i] if mapping else i] for i in t['monomial']) for t in row['terms']))
def primitive(expr):
 p=s.Poly(s.expand(expr),A,*X);tt=p.terms();den=s.ilcm(*[c.q for _,c in tt]);gg=gcd(*(int(c*den) for _,c in tt));return s.expand(expr*den/gg)
def equal_primitive(a,b):
 aa=primitive(a);bb=primitive(b);return s.expand(aa-bb)==0 or s.expand(aa+bb)==0
def kpair(a,b,half=False):return v[a]+(2 if half else 1)*rho*v[b]
def components(expr):
 expr=s.expand(expr);return s.expand(expr).coeff(rho,0),s.expand(expr).coeff(rho,1)
changes={}
def field(name,expr):
 for j,p in enumerate(components(expr)):changes[name+'.'+str(j)]=p
R=v[118];L2=kpair(35,36);L3=kpair(39,40);L4=kpair(43,44);CC=kpair(48,49);AT=kpair(50,51);FF=kpair(52,53,True)
field('affine.Lucas.C',(L2-R)*L4-R*CC)
field('affine.Lucas.AT',(L2+R)*L3-R*AT)
field('affine.Lucas.F',L3**2+CC**2-CC*AT-FF)
f,h,g,k,ss=[kpair(i,i+1) for i in range(205,215,2)];D=11-6*rho;FU=kpair(60,61,True);FV=kpair(29,30,True)
field('pair4.square.f',FU-f*f);field('pair4.square.g',FV-g*g)
field('pair4.curve',h*h-f+D*f*FU)
field('pair4.secant',ss*(f-g)-h-k)
field('pair4.tangent',ss*(h-k)-1+D*(FU+f*g+FV))
for name,ff,hh,FF0,ll,ref in [('primary',f,h,FU,L4,kpair(19,20)),('alternate',g,k,FV,kpair(45,46),kpair(183,184))]:
 field('pair4.ratio.'+name+'.raw',hh*(ll-1)+4*ff*ref)
 field('pair4.ratio.'+name+'.regular',(1-D*FF0)*(ll-1)+4*hh*ref)
x4=ss*ss+D*(f+g)
agg=expression(old['residuals'][143])
agg=agg-components((kpair(173,174)-kpair(175,176))**2)[0]+4*components(x4)[0]
changes['affine.weighted.aggregate']=s.expand(agg)
seen=set()
oldnames={r['name']:r for r in old['residuals']}
for row in new['residuals']:
 expr=expression(row,mapnew)
 expected=changes.get(row['name'])
 if expected is None:expected=expression(oldnames[row['name']])
 assert equal_primitive(expr,expected),row['name']
 seen.add(row['name'])
assert set(changes)<=seen
assert len(new['coordinates'])==200 and len(new['residuals'])==186
# Exact integer sparse expansion performed independently with ordered pairs.
expanded=defaultdict(int)
for r in new['residuals']:
 for t in r['terms']:
  for u0 in r['terms']:
   expanded[(t['parameterPower']+u0['parameterPower'],tuple(sorted(t['monomial']+u0['monomial'])))]+=int(t['coefficient'])*int(u0['coefficient'])
expanded={k:c for k,c in expanded.items() if c}
poly=json.loads((candidate.parent/'polynomial.json').read_text())
stored={(t['parameterPower'],tuple(t['monomial'])):int(t['coefficient']) for t in poly['terms']}
assert expanded==stored
assert max(len(m) for a,m in expanded)==4
assert len({m for a,m in expanded})==3117
out={'status':'PASS','rows':186,'variables':200,'ordinary_monomials':3117,'all_rows_authenticated':True,'exact_quartic_expansion_authenticated':True,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'candidate_sha256':hashlib.sha256(candidate.read_bytes()).hexdigest(),'scope':'Algebraic rows and expansion, not the infinite arithmetic assumptions or arithmetic projection theorem.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
