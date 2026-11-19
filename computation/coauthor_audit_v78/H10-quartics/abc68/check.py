from collections import defaultdict
from fractions import Fraction as F
from functools import reduce
from itertools import product
from math import gcd,lcm
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
OUT=HERE/'results'
def load(name):return json.loads((OUT/name).read_text())
def poly(terms):return {(int(t['parameterPower']),tuple(t['monomial'])):int(t['coefficient']) for t in terms}
def combine(parts):
 q=defaultdict(F)
 for w,p in parts:
  for m,c in p.items():q[m]+=w*c
 return {m:c for m,c in q.items() if c}
def mult(a,b):
 q=defaultdict(F)
 for (e,m),c in a.items():
  for (j,n),d in b.items():q[e+j,tuple(sorted(m+n))]+=c*d
 return {m:c for m,c in q.items() if c}
def prim(p):
 d=lcm(*(c.denominator for c in p.values()))
 vals={m:int(c*d) for m,c in p.items()};g=gcd(*vals.values())
 if vals[min(vals)]<0:g=-g
 return {m:c//g for m,c in vals.items()}
def main():
 cert=load('certificate.json')
 raw=(OUT/'upstream-quadrics.json').read_bytes()
 assert hashlib.sha256(raw).hexdigest()==cert['upstreamSha256']=='480f2ab855b4d26b5ad60f6b8ea0fb4210974c2d9259a5acfafe1ab4cd0740e7'
 source=json.loads(raw)
 orig=[poly(r['terms']) for r in source['residuals']]
 assert cert['config']==[2,0,0,0,1]
 v=lambda i:{(0,(i,)):F(1)}
 k=lambda n,c=0:{(0,()):F(n)} if n else {}
 unit=k(1)
 mp={i:v(i) for i in range(1,69)}
 # u=(v-c-S)/a, w=(v-c+T)/a, a^{-1}=-1+sqrt(2)
 for ix,sg in [(3,-1),(5,1)]:
  p=combine([(1,v(7)),(-4,unit),(sg,v(ix))])
  q=combine([(1,v(8)),(2,unit),(sg,v(ix+1))])
  mp[ix]=combine([(-1,p),(2,q)]);mp[ix+1]=combine([(1,p),(-1,q)])
 for ix in [18,19]:
  mp[ix]=combine([(1,v(ix)),(-1,v(ix-6))])
 def sub(p):
  return prim(combine([(co,reduce(mult,[mp[j] for j in m],{(e,()):F(1)})) for (e,m),co in p.items()]))
 rows=list(map(sub,orig))
 stored=load('rows.json');base=[poly(z) for z in stored['residuals']]
 def kprod(a0,a1,b0,b1):return combine([(1,mult(a0,b0)),(2,mult(a1,b1))]),combine([(1,mult(a0,b1)),(1,mult(a1,b0))])
 def comp(p,q,z):return combine([(1,p),(1,q),(1,z)])
 r,i=kprod(v(7),v(8),combine([(1,v(7)),(1,v(5)),(-1,v(3))]),combine([(1,v(8)),(1,v(6)),(-1,v(4))]))
 ref=[prim(combine([(1,r),(-23,unit)])),prim(combine([(1,i),(17,unit)]))]
 st=kprod(v(3),v(4),v(5),v(6))
 ct=kprod(k(4),k(-2),combine([(1,v(5)),(-1,v(3)),(2,v(7))]),combine([(1,v(6)),(-1,v(4)),(2,v(8))]))
 ref.extend([prim(comp(st[n],ct[n],k([-46,34][n]))) for n in range(2)])
 five=rows[:4]+[rows[36]];new=ref+[rows[36]]
 keys=sorted(set.union(*(set(p) for p in five+new)))
 def rank(aa):
  basis={}
  for p in aa:
   p={m:F(p[m]) for m in p}
   for pivot in sorted(basis):
    if pivot in p:p=combine([(1,p),(-p[pivot],basis[pivot])])
   if p:
    pivot=min(p);basis[pivot]={m:c/p[pivot] for m,c in p.items()}
  return len(basis)
 assert rank(five)==rank(new)==rank(five+new)==5
 rows[:4]=ref
 for i,j,n,d in cert['ops']:
  assert i!=j and d
  rows[i]=prim(combine([(d,rows[i]),(n,rows[j])]))
 assert rows==base
 weights=[F(w) for w in cert['weights']]
 assert min(weights)>0
 report=load('report.json')
 for scaled,fn in [(False,'polynomial.json'),(True,'polynomial-scaled.json')]:
  pp=rows
  if scaled:
   powers=[0]+report['rescaled']['variableScalingPowers']
   assert powers[1]==0
   pp=[]
   for p in rows:
    q={(4*e+sum(powers[j] for j in m),m):co for (e,m),co in p.items()};s=min(e for e,m in q)
    pp.append({(e-s,m):co for (e,m),co in q.items()})
  expanded=prim(combine([(w,mult(p,p)) for w,p in zip(weights,pp)]))
  assert expanded==poly(load(fn)['terms'])
  supports=defaultdict(dict)
  for (e,m),c in expanded.items():supports[m][e]=c
  assert len(supports)==693 and max(map(len,supports))==4 and gcd(*expanded.values())==1
  assert set(j for m in supports for j in m)==set(range(1,69))
  assert all(all(v>0 for v in p.values()) or all(v<0 for v in p.values()) for p in supports.values())
  assert gcd(*(p[0] for p in supports.values() if set(p)=={0}))==1
  if scaled:
   assert all(len(p)==1 or m==() for m,p in supports.items())
   assert [max([abs(c) for (e,m),c in expanded.items() if e==j],default=0) for j in range(5)]==[758542,44,70,0,2]
   assert supports[()]=={0:758542,4:1}
  else:
   assert supports[()]=={0:758542,2:1}
 print('Verified both 693-monomial, 68-variable quartics and equivalence to the upstream zero set.')
if __name__=='__main__':main()
