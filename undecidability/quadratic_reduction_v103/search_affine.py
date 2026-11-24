from fractions import Fraction as F
import json,sys
from collections import defaultdict
import sympy as S
files=['undecidability/contact_endpoint_v102/endpoint_general_quadrics.json','undecidability/contact_endpoint_v102/endpoint_specified_quadrics.json','undecidability/pell_signed_branch_v101/signed_branch_abc_quadrics.json']
for path in files:
 d=json.load(open(path)); ns=d['variable_names']; params=S.symbols(' '.join(d['parameters'])); piv={};found=[]
 for j,row in enumerate(d['residuals']):
  q={}; a={}; w={j:F(1)}
  for t in row['terms']:
   m=tuple(t['monomial']);p=S.Poly(S.sympify(t['coefficient']),*params)
   for ex,c in p.terms():
    key=(m,ex)
    (q if len(m)==2 else a)[key]=F(int(c.p),int(c.q))
  while q:
   key=min(q)
   if key not in piv:
    scale=q[key];q={k:v/scale for k,v in q.items()};a={k:v/scale for k,v in a.items()};w={k:v/scale for k,v in w.items()};piv[key]=(q,a,w);break
   scale=q[key];b,c,v=piv[key]
   for target,src in [(q,b),(a,c),(w,v)]:
    for k,x in src.items():
     y=target.get(k,F(0))-scale*x
     if y:target[k]=y
     elif k in target:del target[k]
  else:
   found.append((row['name'],a,w))
 print(path, 'rank quad',len(piv),'dependencies',len(found))
 for name,a,w in found:
  print('dep',name,'affine',a,'witness',[(d['residuals'][k]['name'],str(v)) for k,v in w.items()])
