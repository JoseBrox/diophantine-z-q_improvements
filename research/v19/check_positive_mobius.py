from fractions import Fraction as Q
from itertools import permutations
from math import gcd,lcm,comb,isqrt
import json
from pathlib import Path
T=[Q(0),Q(-1,2),Q(-1,4),Q(-2,5),Q(-1),Q(-1,3)]
def det3(M):
 return M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])-M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])+M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0])
def canon(v):
 den=lcm(*(x.denominator for x in v));v=[int(x*den) for x in v];g=gcd(*v);v=[x//g for x in v]
 if next(x for x in v if x)<0:v=[-x for x in v]
 return tuple(v)
def maptriple(src,dst):
 M=[[x,Q(1),-y*x,-y] for x,y in zip(src,dst)]
 v=[(-1)**j*det3([[row[k] for k in range(4) if k!=j] for row in M]) for j in range(4)]
 return canon(v)
def val(M,x):
 a,b,c,d=M
 return (a*x+b)/(c*x+d) if c*x+d else None
def conv(a,b):
 v=[Q(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):v[i+j]+=x*y
 return v
F=[Q(1)]
for t in T:F=conv(F,[-t,Q(1)])
def transform(M):
 a,b,c,d=M;out=[Q(0)]*7
 for i,f in enumerate(F):
  v=conv([Q(comb(i,j)*a**j*b**(i-j)) for j in range(i+1)], [Q(comb(6-i,j)*c**j*d**(6-i-j)) for j in range(7-i)])
  out=[x+f*y for x,y in zip(out,v)]
 return out
maps=set()
for dst in permutations(T,3):
 M=maptriple(T[:3],dst)
 if {val(M,x) for x in T}==set(T):maps.add(M)
out=[]
for M in sorted(maps):
 a,b,c,d=M
 G=transform(M);j=next(i for i,f in enumerate(F) if f);k=G[j]/F[j]
 assert all(g==k*f for g,f in zip(G,F))
 cuts=sorted({Q(0)}|({-Q(b,a)} if a and -Q(b,a)>0 else set())|({-Q(d,c)} if c and -Q(d,c)>0 else set()))
 intervals=[]
 for i,lo in enumerate(cuts):
  hi=cuts[i+1] if i+1<len(cuts) else None
  t=(lo+hi)/2 if hi is not None else lo+1
  u=val(M,t)
  if u is not None and u>0:intervals.append([str(lo),str(hi) if hi is not None else 'infinity'])
 out.append({'matrix':M,'multiplier':str(k),'permutation':[T.index(val(M,x)) for x in T],'positive_intervals':intervals})
print(json.dumps(out,indent=2))
Path(__file__).with_name('positive-mobius-certificate.json').write_text(json.dumps({'contacts':[str(x) for x in T], 'automorphisms':out,'complete':True},indent=2)+'\n')

# Independent specializations of the positive norm family.
def Fval(t):
 result=Q(1)
 for theta in T:result*=t-theta
 return result
def Rval(t):return Fval(t)/(t-1)**8
for m in range(2,102):
 lam=Q(m*m+1,2*m*m);mu=Q(3*m*m+1,2);a=mu/lam
 assert lam>0 and mu>0 and a>4
 assert lam==Q(m+1,2*m)**2+Q(m-1,2*m)**2
 q=3*Fval(lam)*(2*lam-1)/((lam-1)**4*(lam-2)**4)
 assert Rval(lam)*Rval(mu)==3*q*q
# Exact group-law computation for the elliptic family.
xx=Q(210);yy=Q(2940);aa=Q(49);bb=Q(-10290)
assert yy*yy==(xx-105)*(xx+70)*(xx+84)
slope=(3*xx*xx+2*aa*xx+bb)/(2*yy)
x2=slope*slope-aa-2*xx
assert slope==Q(97,4) and x2==Q(1905,16)
assert 9*x2+147==Q(19497,16)
print('Positive norm family: 100 exact specializations passed. Elliptic non-torsion coordinate check passed.')
