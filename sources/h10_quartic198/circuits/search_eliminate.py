from pathlib import Path
from collections import defaultdict
from fractions import Fraction as F
import json,itertools,time
P=Path(__file__).parent;d=json.loads((P.parent/'source/computation/quartic/reciprocal204_v27/unbalanced-quadratic.json').read_text())
parameter_support={x for r in d['residuals'] if any(t['parameterPower'] for t in r['terms']) for t in r['terms'] for x in t['monomial']}
rows={r['id']:{tuple(t['monomial']):F(t['coefficient']) for t in r['terms']} for r in d['residuals'] if not any(t['parameterPower'] for t in r['terms'])}
def clean(p):return {m:c for m,c in p.items() if c}
def add(p,q,c=F(1)):
 r=defaultdict(F,p)
 for m,a in q.items():r[m]+=c*a
 return clean(r)
def mul(p,q):
 r=defaultdict(F)
 for m,a in p.items():
  for n,b in q.items():r[tuple(sorted(m+n))]+=a*b
 return clean(r)
def sub(p,x,e):
 out={};pow=[{():F(1)},e,mul(e,e)]
 for m,a in p.items():
  n=m.count(x);mm=tuple(v for v in m if v!=x)
  out=add(out,{tuple(sorted(mm+k)):v*a for k,v in pow[n].items()})
 return out
def deg(p):return max(map(len,p),default=0)
def divides(m,n):return all(m.count(x)<=n.count(x) for x in m)
def quo(n,m):
 q=list(n)
 for x in m:q.remove(x)
 return tuple(q)
def termkey(m):return len(m),m
for rr,p in rows.items():
 for (x,),c in [(m,c) for m,c in p.items() if len(m)==1 and m[0]!=1 and all(m[0] not in n for n in p if n!=m)]:
  if x in parameter_support:continue
  e={m:-cc/c for m,cc in p.items() if m!=(x,)}
  if deg(e)>2:continue
  affected={r:sub(q,x,e) for r,q in rows.items() if r!=rr and any(x in m for m in q)}
  bad={r:q for r,q in affected.items() if deg(q)>2}
  if not bad:print('DIRECT',rr,x,flush=True);continue
  unaffected={r:q for r,q in rows.items() if all(x not in m for m in q)}
  high={m for q in bad.values() for m in q if len(m)>2};initial=len(high)
  # Saturate all multiples of unaffected quadrics that hit the current high monomials.
  reducers={};todo=list(high);seen=set(high);steps=0
  while todo and len(seen)<20000 and steps<15000:
   m=todo.pop();steps+=1
   for r,q in unaffected.items():
    for n in q:
     if len(n)!=2 or not divides(n,m):continue
     k=quo(m,n);key=(r,k)
     if key in reducers:continue
     z={tuple(sorted(k+a)):b for a,b in q.items()};reducers[key]=z
     for a in z:
      if len(a)>2 and a not in seen:seen.add(a);todo.append(a)
  if todo:print('SIZE',rr,x,len(seen),flush=True);continue
  # Echelon with all high-degree columns ordered before low-degree columns.
  pivots={}
  for z in reducers.values():
   while z:
    m=max(z,key=termkey)
    if len(m)<=2:break
    if m not in pivots:
     c=z[m];pivots[m]={n:b/c for n,b in z.items()};break
    z=add(z,pivots[m],-z[m])
  good=True;remainders={}
  for r,q in bad.items():
   z=q.copy()
   while z:
    m=max(z,key=termkey)
    if len(m)<=2:break
    if m not in pivots:good=False;break
    z=add(z,pivots[m],-z[m])
   remainders[r]=z
  if good:print('FOUND',rr,x,'reducers',len(reducers),flush=True)
  else:print('FAIL',rr,x,'high',initial,len(seen),'reducers',len(reducers),flush=True)
