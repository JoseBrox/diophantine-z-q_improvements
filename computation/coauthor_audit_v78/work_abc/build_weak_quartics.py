"""Integer-contact weak-abc quartics, with exact constant-cleared height families."""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction as F
from math import gcd
from itertools import product
import json,os
HERE=Path(__file__).resolve().parent
BASE=Path(os.environ.get('ABC62_PARENT',HERE.parent/'H10-quartics/abc62'))
CONTACTS={6:[1,31,37,41,46,61],8:[1,8,22,28,29,36,43,64]}
def mul(a,b):
 out=[0]*(len(a)+len(b)-1)
 for i,c in enumerate(a):
  for j,d in enumerate(b):out[i+j]+=c*d
 return out
def Gpoly(roots):
 a=[1]
 for root in roots:a=mul(a,[-root,1])
 return a
def parse(items):return {(z['parameterPower'],tuple(z['monomial'])):int(z['coefficient']) for z in items}
def serial(poly):return [{'parameterPower':b,'monomial':list(m),'coefficient':str(c)} for (b,m),c in sorted(poly.items()) if c]
def row(terms):
 d=defaultdict(int)
 for c,m in terms:d[0,tuple(sorted(m))]+=c
 return {k:v for k,v in d.items() if v}
def expand(rr):
 out=defaultdict(int)
 for p in rr:
  for ((b,m),c),((e,n),d) in product(p.items(),repeat=2):out[b+e,tuple(sorted(m+n))]+=c*d
 return {k:v for k,v in out.items() if v}
def make(k,r,kappa,name):
 source=json.loads((BASE/'quadrics.json').read_text()); rows={p['name']:parse(p['terms']) for p in source['residuals']};a=Gpoly(CONTACTS[k]);nv=62
 for gate,w in [('gate0',35),('gate1',49)]:
  assert rows[gate].pop((0,(w,62)))==-1
 for j,(t,e,f,w) in enumerate(((2,33,34,35),(32,47,48,49))):
  g=None
  if k==8:nv+=1;g=nv
  prefix=f'detector{j}.'
  rows[prefix+'contactSquare']=row([(1,[t,e]),(-1,[62,62])])
  rows[prefix+'contactSum']=row([(1,[f,62]),(-1,[e,e])])
  if g:rows[prefix+'contactCube']=row([(1,[g,62]),(-1,[e,f])])
  mons=([[f,f],[e,f],[f,62],[e,62],[62,62],[t,62],[t,t]] if k==6 else [[g,g],[f,g],[f,f],[g,62],[f,62],[e,62],[62,62],[t,62],[t,t]])
  rows[prefix+'inverseContact']=row([(1,[w,62])]+[(-co,m) for co,m in zip(a,mons)])
 last=31;power_ids=[]
 for exponent in range(3,r):
  nv+=1;power_ids.append(nv);rows['height.power'+str(2**exponent)]=row([(1,[nv]),(-1,[last,last])]);last=nv
 gap=rows['detector1.argument'];assert gap.pop((0,(31,31)))==1;gap[0,(last,last)]=1
 kap=F(kappa);gamma=F(2*(k-2),1)/kap-k;den=F(2**r)-kap*(2**(r-1)+2);ratio=4*(2*kap-1)/(gamma*den)
 assert gamma>0 and den>0 and ratio<1
 # The input and original low powers are unchanged; scale the final gap power.
 ws=json.loads((BASE/'parameter-scaling.json').read_text())['variable_powers']+[0]*(nv-62)
 ws[30]=0;ws[last-1]=1
 tr=[];rp=[]
 for n,p in rows.items():
  ee={key:4*key[0]+sum(ws[i-1] for i in key[1]) for key in p};d=min(ee.values());rp.append(d)
  tr.append({(ee[key]-d,key[1]):co for key,co in p.items()})
 assert all(0<=e<=2 for p in tr for e,m in p)
 pi=list(rows).index('shared.unit');pivot=tr[pi];assert pivot[(0,())]==-1
 ops=[]
 for i,p in enumerate(tr):
  if i==pi:continue
  co=p.get((0,()),0)
  if co:
   q={key:p.get(key,0)+co*pivot.get(key,0) for key in p.keys()|pivot.keys()};q={key:val for key,val in q.items() if val};gg=gcd(*q.values());tr[i]={key:val//gg for key,val in q.items()};ops.append([i,pi,co,gg])
 total=expand(tr);profiles=defaultdict(dict)
 for (e,m),co in total.items():profiles[m][e]=co
 assert profiles[()]=={0:1,4:1}
 assert max(abs(co) for (e,m),co in total.items() if e==4)==1
 assert all(len(p)==1 or m==() for m,p in profiles.items())
 caps=[max([abs(co) for (e,m),co in total.items() if e==j],default=0) for j in range(5)]
 def dominated(n):return all(caps[j]*n**j<=n**4+1 for j in range(4))
 upper=1
 while not dominated(upper):upper*=2
 lower=upper//2
 while upper-lower>1:
  mid=(upper+lower)//2
  if dominated(mid):upper=mid
  else:lower=mid
 n0=upper
 folder=HERE/'weak_quartics'/name;folder.mkdir(exist_ok=True,parents=True)
 data={'variables':nv,'parameter':'n','residuals':[{'name':key,'terms':serial(p)} for key,p in zip(rows,tr)]}
 cert={'contacts':CONTACTS[k],'contactDegree':k,'gapExponent':2**r,'weakAbcExponent':str(kap),'contactHeightRate':str(gamma),'absorption':str(ratio),'variables':nv,'rows':len(tr),'degree':4,'monomials':len(profiles),'parameterSeparatedTerms':len(total),'coefficientCaps':caps,'exactHeightForPositiveN':'max('+','.join(str(caps[j])+('*n^'+str(j) if j else '') for j in range(4))+',n^4+1)','sufficientAlgebraicN':n0,'sufficientOddN':n0 if n0%2 else n0+1,'cofinalShift':'B=n^4','heightForSufficientOddN':'B+1','definingThreshold':'ineffective','variablePowers':ws,'rowPowers':rp,'rowOperations':ops}
 for fn,obj in [('quadrics.json',data),('polynomial.json',{'variables':nv,'parameter':'n','terms':serial(total)}),('certificate.json',cert)]:
  (folder/fn).write_text(json.dumps(obj,separators=(',',':'))+'\n')
 print(name,{key:cert[key] for key in ['variables','rows','monomials','weakAbcExponent','absorption','coefficientCaps','sufficientOddN']})
if __name__=='__main__':
 make(6,4,'9/8','weak63')
 make(6,5,'17/14','weak64')
 make(8,6,'7/5','weak67')
