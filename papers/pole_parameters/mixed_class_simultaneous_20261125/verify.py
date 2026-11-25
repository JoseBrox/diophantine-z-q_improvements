"""Exact checks of the mixed-class theorem; standard library only."""
from fractions import Fraction as F
from math import lcm, prod, factorial
from itertools import product
from functools import cache
from random import Random

TYPES=(3,3,1,1,1,1,3,7)
BASE=((0,0,0,0,1,0,0,1),(1,1,0,0,0,0,0,0),(0,0,0,0,1,0,0,1),(0,0,0,0,1,0,1,0),(1,0,1,1,0,1,0,0),(0,0,0,0,1,1,1,1),(1,1,0,1,0,1,0,0),(0,1,1,0,0,1,1,0))
def yz(t):return int(t in (3,7)),int(t in (3,5))
def rows(A,typ):
 n=len(A);y,z=zip(*map(yz,typ));return [sum(A[i][j]<<j for j in range(n))^(y[i]<<(n+i)) for i in range(n)]+[(sum(A[i][j]<<(n+j) for j in range(n))^(y[i]<<(n+i))^(z[i]<<i)) for i in range(n)]
def elim(rs):
 d={}
 for a in rs:
  while a:
   i=a.bit_length()-1
   if i in d:a^=d[i]
   else:d[i]=a;break
 return d
def rank(rs):return len(elim(rs))
def kernel_line(rs,n):
 d=elim(rs);assert len(d)==n-1
 x=1<<next(j for j in range(n) if j not in d)
 for j,r in sorted(d.items()):
  if (r&x).bit_count()%2:x^=1<<j
 return x
def diag(A):
 for i,r in enumerate(A):r[i]=0;r[i]=sum(r)%2

def check_core(bit,i,g):
 A=[list(r) for r in BASE];A[0][1]=bit;A[1][0]=bit^1
 if g:
  j=3 if i==1 else 2
  A[4][j]^=1;A[j][4]^=1;A[4][5]^=1;A[5][4]^=1
 diag(A)
 a,b=(12,244) if not g else ((32,216) if i==1 else (32,244))
 y,z=zip(*map(yz,TYPES));assert all(sum(r)%2==0 for r in A)
 assert all(A[j][k]^A[k][j]==y[j]*y[k] for j in range(8) for k in range(j))
 rs=rows(A,TYPES);assert kernel_line(rs,16)==a|(b<<8)
 assert prod(t for j,t in enumerate(TYPES) if a>>j&1)%8==1
 assert prod(t for j,t in enumerate(TYPES) if b>>j&1)%8==5
 assert (a^b)==248 if i==1 else b==244
 return A,a,b

def first_genus_sum(A):
 @cache
 def gamma(mask):
  I=[i for i in range(8) if mask>>i&1];n=len(I)
  B=[[A[i][j] if i!=j else 0 for j in I] for i in I];diag(B)
  for i in range(n):B[i][-1]=yz(TYPES[I[i]])[1]
  return rank([sum(v<<j for j,v in enumerate(row)) for row in B])==n
 @cache
 def typ(mask):return prod(TYPES[i] for i in range(8) if mask>>i&1)%8
 @cache
 def gs(mask,has5):
  if not mask:return int(has5)
  ans=0;b=mask&-mask;m=mask
  while m:
   if m&b:
    t=typ(m)
    if (t==1 or (t==5 and not has5)) and gamma(m):ans^=gs(mask^m,has5 or t==5)
   m=(m-1)&mask
  return ans
 return gs(255,False)
for bit in (0,1):
 for i,g in product((1,2),(0,1)):
  A,*_=check_core(bit,i,g);assert first_genus_sum(A)==1
print('8 core ranks, Kummer masks and direct first-genus sums PASS')

# Independently test the full-support lifting with random internal Legendre
# symbols, optional overlaps, and both possible cross-group aggregate bits.
# These are symbol configurations, not numerical prime choices; CRT/Dirichlet
# and the subdivision proof justify the unrestricted quantifiers.
RNG=Random(20261125)
def lift_fixture(bit,g1,g2):
 groups=[[0],[1,2,3],[4,5,6],[7,8,9],[10],[11],[12],[13]]
 typ=[3,3,5,5,1,1,1,1,1,1,1,1,3,7,3,3,1,3,1]
 K1=[14,15,16];K2=[14,17,18]  # overlap of type 3, exclusive type-1 markers
 edges=[(i,G[0]) for G in groups[:4] for i in G[1:]]+[(q,10) for q in [14,15,16,17,18]]
 n_orig=len(typ);typ+= [1]*len(edges);n=len(typ);A=[[0]*n for _ in range(n)];y,z=zip(*map(yz,typ))
 def setedge(i,j,x):A[i][j]=x;A[j][i]=x^(y[i]&y[j])
 for G in groups[:4]:
  for i in G:
   for j in G:
    if i<j:setedge(i,j,RNG.randrange(2))
 w=[RNG.randrange(2),RNG.randrange(2)];w.append(bit^w[0]^w[1])
 for j,x in zip(groups[1],w):setedge(0,j,x)
 # J symbols can vary subject to both support constraints.
 for p in groups[0]+groups[1]:
  v=[RNG.randrange(2) for _ in range(3)]
  out=[v[0],v[1],v[0]^v[1],v[2],v[0]^v[2]]
  for q,x in zip(range(14,19),out):setedge(p,q,x)
 for group,K,other,g,sign in [(groups[2],K1,K2,g2,0),(groups[3],K2,K1,g1,1)]:
  # Prescribe column sums to ensure [j_i/q] = sign*y_q.
  c={q:((sign*y[q])^sum(A[q][p] for p in groups[0]+groups[1])%2) for q in K}
  missing=[q for q in other if q not in K];assert len(missing)==2
  c[missing[0]]=RNG.randrange(2)
  c[missing[1]]=g^c[missing[0]]^sum(c[q] for q in other if q in K)%2
  assert sum(c[q] for q in K)%2==0
  for p in group[1:]:
   vals=[RNG.randrange(2) for _ in range(4)];v=dict(zip(range(14,18),vals))
   v[18]=RNG.randrange(2)
   v[K[-1]]=sum(v[q] for q in K[:-1])%2
   for q,x in v.items():setedge(p,q,x)
  for q,x in c.items():setedge(group[0],q,x^sum(A[p][q] for p in group[1:])%2)
 # The core margins from each fixed group toward the permanent centers.
 C,_,_=check_core(bit,1,0)
 for j,G in enumerate(groups[:4]):
  for p in G[1:]:setedge(p,10,1)
  for k,h in enumerate(range(10,14),4):setedge(G[0],h,C[j][k]^sum(A[p][h] for p in G[1:])%2)
 for j in range(4,8):
  for k in range(j+1,8):setedge(groups[j][0],groups[k][0],C[j][k])
 for q in range(14,19):
  for r in range(q+1,19):setedge(q,r,RNG.randrange(2))
  setedge(q,10,RNG.randrange(2));setedge(q,11,g1 if q==16 else g2 if q==18 else 0)
 for s,(p,q) in enumerate(edges,n_orig):setedge(s,p,1);setedge(s,q,1)
 for ii,K in [(0,[]),(1,K1),(2,K2)]:
  I=list(range(14))+K+list(range(n_orig,n));T=[typ[p] for p in I];l=len(I)
  B=[[A[p][q] if p!=q else 0 for q in I] for p in I];diag(B)
  k=kernel_line(rows(B,T),2*l);u=k&((1<<l)-1);v=k>>l
  support=lambda labels:{p for j,p in enumerate(I) if labels>>j&1}
  assert prod(t for j,t in enumerate(T) if u>>j&1)%8==1
  assert prod(t for j,t in enumerate(T) if v>>j&1)%8==5
  if ii==0:
   assert support(u)==set(groups[2]+groups[3]);assert support(v)==set(I)-set(groups[0]+groups[1]+groups[3])
  elif ii==1:assert support(u^v)==set(I)-set(groups[0]+groups[1]+groups[2])
  else:assert support(v)==set(I)-set(groups[0]+groups[1]+groups[3])
for bit,g1,g2 in product((0,1),repeat=3):
 for _ in range(30):lift_fixture(bit,g1,g2)
print('240 randomized full symbol graphs, 720 lifted rank/Kummer checks PASS')

# Both fixed contact preparations; no collision between first two sets at 67.
Theta=[F(0),-F(1,2),F(-1),F(1,2399),-F(32,407)]
C=[h+x for h in (2,4) for x in Theta]
def mod(x,m):return x.numerator*pow(x.denominator,-1,m)%m
def vp(x,p):
 def v(n):
  z=0
  while n%p==0:n//=p;z+=1
  return z
 return v(x.numerator)-v(x.denominator)
assert [mod(x,49) for x in C]==[2,26,1,26,26,4,28,3,28,28]
for j in (1,2):
 delta={1:2751,2:2219}[j];assert delta%49==7*j and delta%67==4*j
for j,k in [(0,1),(0,2),(1,2)]:
 shifts=[0,2751,2219];d=shifts[k]-shifts[j]
 A=[[int(vp(x-y-d,7)==1) for y in C] for x in C]
 assert all(sum(r)%2 for r in A) and all(sum(r[i] for r in A)%2 for i in range(10))
 shifts=[F(0)]+[4*i+F(67,7**(2*i)) for i in (1,2)]
 assert all(vp(x+shifts[j]-y-shifts[k],7)%2==0 for x in C for y in C)
assert not ({mod(x,67) for x in C}|{66}) & ({mod(x+4,67) for x in C}|{65})
# Smooth reduction group orders and nonsingularity of P at 7.
for r,order in [(3,7),(4,8)]:
 D=(11-6*r)%7
 affine=[(x,y) for x,y in product(range(7),repeat=2) if (y*y-x*x*x+D*x)%7==0 and not (2*y%7==0 and (D-3*x*x)%7==0)]
 assert 1+len(affine)==order
 assert (mod(F(57-28*r,8),7),mod(F(-660+417*r,32),7)) in affine
assert factorial(466)%(56*113**2*233**2)==0
# Explicit exclusive markers and finite square multiplier menus.
B=2477;A=B*(B-1);B0=(B-2401)*(32*B+343);u=F((1224*(67**2+1))**2*A,B0)
d0=F(49,81)*102**2*67**3*u/(1+7*u)**2
qs=(113,233);period=2*lcm(*(q*(q-1) for q in qs));assert period==171033184
assert vp(d0,7)==2 and vp(d0,3)==2 and vp(d0,11)==1
M=67*prod(q*q for q in qs);H=3**30;assert M==46445488147
for i,q in enumerate(qs):
 other=qs[1-i];sgn=1 if i==0 else -1
 assert vp(d0,q)==0
 m=[32764985881,4885738625][i];menu=[m+M*j for j in range(11)]
 assert all(0<t<H and t%67==1 and t%other**2==0 and vp(1-sgn*d0*F(t,H)**2,q)==1 for t in menu)
 assert all(vp(1-sgn*d0*F(t,H)**2,other)==0 for t in menu)
 print('marker',q,'menu base',m,'step',M)
print('Contact, reduction-group and marker checks PASS')
