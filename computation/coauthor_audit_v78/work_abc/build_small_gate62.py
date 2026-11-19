"""Build constant-free shared gates; arithmetic proof is in the companion TeX."""
from pathlib import Path
from collections import defaultdict
from itertools import product
from fractions import Fraction
from math import gcd
import json,os
HERE=Path(__file__).resolve().parent
BASE=Path(os.environ.get('ABC62_PARENT',HERE.parent/'H10-quartics/abc62'))
def read(p):return json.loads(p.read_text())
def parse(terms):return {(z['parameterPower'],tuple(z['monomial'])):int(z['coefficient']) for z in terms}
def serial(p):return [{'parameterPower':b,'monomial':list(m),'coefficient':str(v)}for(b,m),v in sorted(p.items())]
def expand(rr,weights=None):
 out=defaultdict(Fraction)
 for p,wgt in zip(rr,weights or [1]*len(rr),strict=True):
  for((e,m),a),((f,n),b)in product(p.items(),repeat=2):out[e+f,tuple(sorted(m+n))]+=a*b*Fraction(wgt)
 out={key:val for key,val in out.items()if val};assert all(v.denominator==1 for v in out.values());gg=gcd(*(int(v)for v in out.values()));return {key:int(val)//gg for key,val in out.items()}
def save(name,rows,poly,extra):
 out=HERE/'small_gate62'/name;out.mkdir(exist_ok=True,parents=True);pr=defaultdict(dict)
 for(e,m),v in poly.items():pr[m][e]=v
 cert={'variables':62,'quadrics':50,'degree':4,'monomials':len(pr),'parameterSeparatedTerms':len(poly),'content':1,**extra}
 (out/'quadrics.json').write_text(json.dumps({'variables':62,'residuals':[{'name':n,'terms':serial(r)}for n,r in zip(names,rows)]},separators=(',',':'))+'\n')
 (out/'polynomial.json').write_text(json.dumps({'variables':62,'terms':serial(poly)},separators=(',',':'))+'\n')
 (out/'certificate.json').write_text(json.dumps(cert,indent=2)+'\n');print(name,cert)
spec=read(BASE/'quadrics.json');names=[q['name']for q in spec['residuals']];rows=[parse(q['terms'])for q in spec['residuals']]
for name,w in [('gate0',35),('gate1',49)]:
 i=names.index(name);assert rows[i].pop((0,(w,62)))==-1
save('primitive',rows,expand(rows),{'parameter':'B','height':'B^2+4091 for B>=81'})
scale=read(BASE/'parameter-scaling.json');tr=[]
for i,p in enumerate(rows):
 tr.append({(4*b+sum(scale['variable_powers'][j-1]for j in m)-scale['row_powers'][i],m):v for(b,m),v in p.items()})
save('balanced',tr,expand(tr),{'parameter':'n','shift':'B=n^4','height':'B+4091 for odd n>=3'})
sparse=read(BASE/'sparsity.json');sr=[dict(p)for p in tr]
for i,j,a,b in sparse['ops']:
 r={key:b*sr[i].get(key,0)+a*sr[j].get(key,0)for key in sr[i].keys()|sr[j].keys()};r={key:v for key,v in r.items()if v};gg=gcd(*r.values())*(1 if r[min(r)]>0 else -1);sr[i]={key:v//gg for key,v in r.items()}
sp=expand(sr,sparse['weights']);pr=defaultdict(dict)
for(e,m),v in sp.items():pr[m][e]=v
print('SPARSECAPS',[max([abs(v)for(e,m),v in sp.items()if e==j],default=0)for j in range(5)],'mixed',[p for p in pr.values()if len(p)>1])
save('sparse',sr,sp,{'parameter':'n','shift':'B=n^4','weights':sparse['weights'],'height':'B+758541 for odd n>=3'})
pi=names.index('shared.unit');cl=[dict(p)for p in tr]
for i,p in enumerate(cl):
 if i==pi:continue
 a=p.get((0,()),0)
 if a:
  q={key:p.get(key,0)+a*cl[pi].get(key,0)for key in p.keys()|cl[pi].keys()};cl[i]={key:v for key,v in q.items()if v}
poly=expand(cl);profiles=defaultdict(dict)
for(e,m),v in poly.items():profiles[m][e]=v
assert [max([abs(v)for(e,m),v in poly.items()if e==j],default=0)for j in range(5)]==[1548,1280,4091,4,1]
assert [p for p in profiles.values()if len(p)>1]==[{4:1,0:1}]
save('height',cl,poly,{'parameter':'n','shift':'B=n^4','height':'max(4091*n^2,n^4+1); B+1 for odd n>=65'})
