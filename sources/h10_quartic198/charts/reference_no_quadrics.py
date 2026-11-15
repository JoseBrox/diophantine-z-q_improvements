#!/usr/bin/env python3
"""Finite-field rank certificate excluding direct quadratic equations in S,T,f^2,g^2."""
import json,itertools
from pathlib import Path
p=1009
rho=pow(2,(p+1)//4,p) if p%4==3 else next(i for i in range(p) if i*i%p==2)
inv=lambda x:pow(x%p,-1,p)
D=(11-6*rho)%p
a=(57*inv(8)-7*inv(2)*rho)%p
b=(-165*inv(8)+417*inv(32)*rho)%p
mons=[()]+[(i,) for i in range(4)]+list(itertools.combinations_with_replacement(range(4),2))
rows=[];points=[];basis={};pivots=[]
for x in range(1,p):
 for y in range(p):
  if (y*y-x*x*x+D*x)%p:continue
  if x==a:continue
  slope=(y+b)*inv(x-a)%p
  xx=(slope*slope-x-a)%p
  yy=(-y+slope*(x-xx))%p
  if not xx:continue
  vals=[y*inv(x)%p,yy*inv(xx)%p,inv(x)**2%p,inv(xx)**2%p]
  row=[1 if not m else vals[m[0]] if len(m)==1 else vals[m[0]]*vals[m[1]]%p for m in mons]
  reduced=row[:]
  for pivot,base in sorted(basis.items()):
   c=reduced[pivot]
   reduced=[(u-c*v)%p for u,v in zip(reduced,base)]
  pivot=next((j for j,t in enumerate(reduced) if t),None)
  if pivot is not None:
   scale=inv(reduced[pivot]);reduced=[t*scale%p for t in reduced];basis[pivot]=reduced
   rows.append(row);points.append([x,y]);pivots.append(pivot)
  if len(basis)==15:break
 if len(basis)==15:break
assert len(basis)==15
report=dict(prime=p,rho=rho,D=D,a=a,b=b,variables=['S','T','f_squared','g_squared'],monomials=mons,curvePoints=points,evaluationRows=rows,rank=15,conclusion='The 15 coordinate monomials of degree at most2 are linearly independent in this function field specialization; hence there is no nonzero field quadratic relation among these four unchanged physical functions. Directly deleting the extra f coordinate cannot leave a quadratic chart in only these four outputs.')
Path(__file__).with_name('reference_no_quadrics.json').write_text(json.dumps(report,indent=2)+'\n')
print('Full rank15 certificate PASS at prime',p,'rho',rho)
