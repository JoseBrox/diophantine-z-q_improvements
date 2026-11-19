"""Independent checks of the constant-free gate and all expanded quartics."""
from pathlib import Path
from collections import defaultdict
from itertools import product
from fractions import Fraction
from math import gcd
import hashlib,json,os
import sympy as s
HERE=Path(__file__).resolve().parent;BASE=Path(os.environ.get('ABC62_PARENT',HERE.parent/'H10-quartics/abc62'));OUT=HERE/'small_gate62'
def read(p):return json.loads(p.read_text())
def parse(ts):return {(t['parameterPower'],tuple(t['monomial'])):int(t['coefficient'])for t in ts}
def exp(rows,ww=None):
 d=defaultdict(Fraction)
 for r,w in zip(rows,ww or [1]*len(rows),strict=True):
  for((e,m),a),((f,n),b)in product(r.items(),repeat=2):d[e+f,tuple(sorted(m+n))]+=a*b*Fraction(w)
 d={k:v for k,v in d.items()if v};assert all(v.denominator==1 for v in d.values());gg=gcd(*(int(v)for v in d.values()));return{k:int(v)//gg for k,v in d.items()}
def compare(folder,rr,ww,caps,count,mixed):
 quad=read(folder/'quadrics.json');assert [parse(q['terms'])for q in quad['residuals']]==rr
 p=exp(rr,ww);assert p==parse(read(folder/'polynomial.json')['terms'])
 pp=defaultdict(dict)
 for(e,m),v in p.items():pp[m][e]=v
 assert len(pp)==count and max(map(len,pp))==4 and set(i for m in pp for i in m)==set(range(1,63))
 assert pp[(1,1,1,1)]=={0:1}
 assert [max([abs(v)for(e,m),v in p.items()if e==j],default=0)for j in range(len(caps))]==caps
 assert [q for q in pp.values()if len(q)>1]==mixed
 result={'status':'PASS','variables':62,'rows':50,'degree':4,'monomials':count,'parameterSeparatedTerms':len(p),'content':1,'coefficientCaps':caps,'polynomial_sha256':hashlib.sha256((folder/'polynomial.json').read_bytes()).hexdigest()}
 (folder/'independent-verification.json').write_text(json.dumps(result,indent=2)+'\n');return result
# The physical constant-free gate is exactly the decoded transformed quadric.
q,c,D,tau=s.symbols('q c D tau',nonzero=True)
assert s.expand(q*(2*tau/q-c*c/q+2*c-q-D*D)-(2*tau-(c-q)**2-q*D*D))==0
# Exact zero-fiber reference check, independently doubling R0 over Q(sqrt(2)).
def kadd(a,b):return (a[0]+b[0],a[1]+b[1])
def ksub(a,b):return (a[0]-b[0],a[1]-b[1])
def kmul(a,b):return (a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def kdiv(a,b):
 nn=b[0]*b[0]-2*b[1]*b[1]
 assert nn
 return kmul(a,(b[0]/nn,-b[1]/nn))
xx=(Fraction(1),Fraction(1));yy=(Fraction(0),Fraction(2));delta=(Fraction(11),Fraction(-6))
slope=kdiv(ksub(kmul((3,0),kmul(xx,xx)),delta),kmul((2,0),yy))
xd=ksub(kmul(slope,slope),kmul((2,0),xx));yd=ksub(kmul(slope,ksub(xx,xd)),yy)
S=kdiv(yd,xd);T=kdiv(yy,xx);diff=ksub(S,T)
assert S==(Fraction(-87,41),Fraction(129,164)) and T==(Fraction(4),Fraction(-2))
assert diff[0]**2-2*diff[1]**2==Fraction(7199,328)
# Native pole witness identities from the two retained congruent twists.
b,r,a1,a2,Y1,Y2=s.symbols('b r a1 a2 Y1 Y2',nonzero=True)
e=r/(b*a1*a1);p2=Y1/(b**4*a1**6);u=a2/a1;v=e*(1-b)/u;q2=Y2/(b**4*a1**6*u**4)
assert s.cancel((e*e+b*p2-1).subs(Y1,b**3*a1**6-r*r*b*a1*a1))==0
assert s.cancel(u*v-e*(1-b))==0
assert s.cancel((u*u-v*v-b*q2).subs(Y2,b**3*a2**6-r*r*b*(1-b)**2*a2*a2))==0
base=read(BASE/'quadrics.json');names=[q['name']for q in base['residuals']];rr=[parse(q['terms'])for q in base['residuals']]
for name,w in [('gate0',35),('gate1',49)]:
 i=names.index(name);assert rr[i].pop((0,(w,62)))==-1
reports=[]
reports.append(compare(OUT/'primitive',rr,None,[4091,8,1],825,[{0:4091,2:1},{0:1,1:8},{0:1,1:2}]))
scale=read(BASE/'parameter-scaling.json');ss=[]
for j,p in enumerate(rr):ss.append({(4*b+sum(scale['variable_powers'][i-1]for i in m)-scale['row_powers'][j],m):v for(b,m),v in p.items()})
reports.append(compare(OUT/'balanced',ss,None,[4091,16,44,4,1],825,[{0:4091,4:1}]))
sp=[dict(r)for r in ss];recipe=read(BASE/'sparsity.json')
for i,j,a,b in recipe['ops']:
 assert i!=j and b
 d={k:b*sp[i].get(k,0)+a*sp[j].get(k,0)for k in sp[i].keys()|sp[j].keys()};d={k:v for k,v in d.items()if v};g=gcd(*d.values())*(1 if d[min(d)]>0 else -1);sp[i]={k:v//g for k,v in d.items()}
assert all(Fraction(w)>0 for w in recipe['weights'])
reports.append(compare(OUT/'sparse',sp,recipe['weights'],[758541,16,44,4,1],752,[{0:758541,4:1}]))
cl=[dict(r)for r in ss];pi=names.index('shared.unit')
for i,p in enumerate(cl):
 if i==pi:continue
 a=p.get((0,()),0)
 if a:
  d={k:p.get(k,0)+a*cl[pi].get(k,0)for k in p.keys()|cl[pi].keys()};cl[i]={k:v for k,v in d.items()if v}
reports.append(compare(OUT/'height',cl,None,[1548,1280,4091,4,1],840,[{0:1,4:1}]))
print(json.dumps({'checks':'gate identity, native twist witness identities, all coefficient transfers and full expansions','reports':reports},indent=2))
