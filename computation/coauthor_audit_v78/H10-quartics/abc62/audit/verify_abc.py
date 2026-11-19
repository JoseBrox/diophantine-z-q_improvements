"""Independently undo the Laurent and hyperbolic substitutions from the delivered SOS."""
from pathlib import Path
from collections import Counter
from math import prod,gcd
import argparse,json
import sympy as s

parser=argparse.ArgumentParser();parser.add_argument('upstream',type=Path);parser.add_argument('record',type=Path);args=parser.parse_args()
a=json.loads(args.upstream.read_text());tab=json.loads((args.record/'quadrics.json').read_text());pol=json.loads((args.record/'polynomial.json').read_text());sol=json.loads((args.record/'weights.json').read_text())
y=s.symbols('y0:102');c,B=s.symbols('c B', nonzero=True);weights={int(i):v for i,v in sol['weights'].items()};ids=tab['sourceIds']
def pair(i):return y[i],y[i+1]
def add(p,q):return(p[0]+q[0],p[1]+q[1])
def sub(p,q):return(p[0]-q[0],p[1]-q[1])
def sc(p,n):return(p[0]*n,p[1]*n)
def bar(p):return(p[0],-p[1])
def mul(p,q):return(p[0]*q[0]+2*p[1]*q[1],p[1]*q[0]+p[0]*q[1])
def sq(p):return mul(p,p)
def fill(out,i,p):out[i],out[i+1]=p

a0=(1,1);c0=(4,-2);v=pair(7);S=sub(sub(v,c0),mul(a0,pair(3)));T=add(sub(mul(a0,pair(5)),v),c0)
phys=dict(enumerate(y));fill(phys,3,S);fill(phys,5,T)
# For paired physical terms P²-c²Q² the new coordinates store P+cQ and P-cQ.
U=pair(26);V=bar(pair(28));J=pair(22);Q=bar(pair(24))
slim=len(ids)==62
if slim:
 assert sol['seq']==[0,2,1,3] and sol['pairs']==[[0,2],[1,3]]
 fill(phys,26,add(U,sc(V,c)));fill(phys,28,sub(U,sc(V,c)))
 fill(phys,22,add(J,sc(Q,c)));fill(phys,24,sub(J,sc(Q,c)))
else:
 assert sol['seq']==[0,1,2,3] and sol['pairs']==[[0,2],[1,3]]
 Q=pair(69);fill(phys,26,add(U,sc(J,c)));fill(phys,22,sub(U,sc(J,c)))
 fill(phys,28,add(V,sc(Q,c)));fill(phys,69,sub(V,sc(Q,c)))
coords={j+1:phys[i]/c**weights[i] if i in weights else c if i==100 else 1/c for j,i in enumerate(ids)}
def ev(r,x):return s.expand(sum(int(t['coefficient'])*B**t['parameterPower']*prod(x[i] for i in t['monomial']) for t in r['terms']))
def coeff(x):return x.as_coefficients_dict() if x else {}
def same(f,g):
 f=s.expand(f);g=s.expand(g)
 if f==g:return True
 a=coeff(f);b=coeff(g)
 if set(a)!=set(b) or not a:return False
 i=next(iter(a));return all(a[k]*b[i]==a[i]*b[k] for k in a)
old={r['name']:ev(r,y) for r in a['residuals']};out={r['name']:s.expand(ev(r,coords)*c**sol['divs'][r['name']]) for r in tab['residuals'] if r['name']!='shared.unit'}
assert ev(tab['residuals'][-1],coords)==0
pnames=[f'reference.primitive.{i}' for i in range(1,5)]+['detector0.pole.first'];basis=[old[n] for n in pnames];new=[out[n] for n in pnames];keys=list(set().union(*(set(coeff(f)) for f in basis+new)))
def rk(aa):return s.Matrix([[coeff(f).get(k,0) for k in keys] for f in aa]).rank()
assert rk(basis)==rk(new)==rk(basis+new)==5
expected={n:p for n,p in old.items() if n in out and n not in pnames};
for name,target in [('C',sub(U,sq(sub(pair(10),S)))),('I',sub(pair(28),sq(sub(pair(12),T))))]+([] if slim else [('high',sub(Q,sq(bar(pair(24))))) ]):
 for im in (0,1):expected[name+str(im)]=target[im]
W=add(add((1,0),sc(sq(U),c)),add(sc(sq(V),c**2),add(sc(sq(J),-c**3),sc(sq(Q),-c**4))))
if slim:W=add(add((1,0),sc(sq(U),c)),add(sc(sq(J),c**2),add(sc(sq(V),-c**3),sc(sq(Q),-c**4))))
for im in (0,1):expected['product'+str(im)]=pair(40)[im]-W[im]
f=pair(40);D=y[71];expected['sharedD']=2*f[0]*D-(f[0]-1)**2+2*f[1]**2
for j in range(2):
 q=[y[73],c-y[73]][j];w=y[[35,53][j]];eta=y[[42,60][j]];b=y[[43,61][j]]
 expected[f'weight{j}']=q*w-1
 expected[f'gate{j}']=2*eta*w-w*(1+c**2)+2*c-q-D**2
 expected[f'pole{j}']=q*b-eta**2
 # Check reduction of the gate to the unscaled positive quadratic expression.
 assert s.factor((expected[f'gate{j}']*q-(2*eta-1-(c-q)**2-q*D**2)).subs(w,1/q))==0
assert set(out)==set(expected)|set(pnames), set(out)^set(expected)
for n,f in expected.items():assert same(out[n],f),n
squares=Counter();fout={(t['parameterPower'],tuple(t['monomial'])):int(t['coefficient']) for t in pol['terms']}
for r in tab['residuals']:
 for t in r['terms']:
  for v in r['terms']:
   squares[t['parameterPower']+v['parameterPower'],tuple(sorted(t['monomial']+v['monomial']))]+=int(t['coefficient'])*int(v['coefficient'])
g=gcd(*(n for n in squares.values() if n));assert {k:v//g for k,v in squares.items() if v}==fout
assert len(ids)==(62 if slim else 64) and len(tab['residuals'])==(50 if slim else 52) and max(len(k[1]) for k in fout)==4
print(f'PASS. Independently recovered {len(tab["residuals"])} quadrics, checked the common five-row span, both signed products and all {len(ids)}-variable quartic coefficients.')
