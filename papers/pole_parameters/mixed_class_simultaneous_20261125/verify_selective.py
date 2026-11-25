"""Exact contact, marker, local-exponent and effective-threshold ledger."""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, lcm, prod

Theta=[F(0),-F(1,2),F(-1),F(1,2399),-F(32,407)]
C=[h+x for h in (2,4) for x in Theta]
s=[F(0),15+F(67,49),30+F(67,2401)]
new=[[[x+s[j]+4*g for x in C] for g in (0,1)] for j in range(3)]
old=[[x+4*j for x in C] for j in range(3)]
def mod(x,m):return x.numerator*pow(x.denominator,-1,m)%m
def v(x,p):
 assert x
 def val(n):
  z=0
  while n%p==0:n//=p;z+=1
  return z
 return val(x.numerator)-val(x.denominator)
sets=[{mod(x,67) for g in G for x in g}|{(-j-1)%67} for j,G in enumerate(new)]
assert all(len(a)==21 for a in sets)
assert not sets[0]&sets[1] and 0 not in sets[0]|sets[1]
for j,k in combinations(range(3),2):
 for g,h in product(range(2),repeat=2):
  assert all(v(x-y,7)<0 and v(x-y,7)%2==0 for x in new[j][g] for y in new[k][h])
assert all(min(G[0])>0 and max(G[0])<min(G[1]) for G in new)
# Local exponents: saturation and all factor minima are strict for odd alpha.
for alpha in range(-31,32,2):
 for d in range(-50,51):
  assert 2*d+alpha!=0
  w=2*d-min(0,alpha+2*d)
  assert w==max(2*d,-alpha)
  for k in (1,6):
   for eta in range(-7,8):assert ((1-2*k)*alpha+2*(eta+w))%2==1
   if alpha>0 and 4*w>(4*k-3)*alpha:
    assert d>0 and (k!=6 or d>=3)
for d in range(-100,101):
 w=max(2*d,-1)
 for k in (1,6):assert 1-2*k+2*(8+w)>=3
# Exact scalar fixture and 21-entry marker menus.
beta=2477;A=beta*(beta-1);B=(beta-2401)*(32*beta+343)
q0=F((1224*(67**2+1))**2*A,B)
d0=F(49,81)*102**2*67**3*q0/(1+7*q0)**2
qs=(113,233);H=3**30;M=67*prod(q*q for q in qs)
menus=[[m+l*M for l in range(21)] for m in (32764985881,4885738625)]
for i,q in enumerate(qs):
 other=qs[1-i];sign=(-1)**i
 assert v(d0,q)==0
 assert all(0<a<H and a%67==1 and a%other**2==0 and v(1-sign*d0*F(a,H)**2,q)==1 and v(1-sign*d0*F(a,H)**2,other)==0 for a in menus[i])
# Fixed exception bound.
constants=set(sum(old,[])+[x for G in new for g in G for x in g]+[F(-j-1) for j in range(3)]+[F(0),F(1),F(2401),-F(343,32)]+Theta)
assert len(constants)<128
assert all(abs(x.numerator)<2**40 and x.denominator<2**40 for x in constants)
assert all(a<2**40 for menu in menus for a in menu)
assert all(0<abs(a*a-b*b)<2**80 for menu in menus for a,b in combinations(menu,2))
q=4000000
assert 17*76176+3*23+128*80+comb(128,2)*161+42*40+2*comb(21,2)*80<q
assert all(abs((s[j]+4*g-4*j).numerator)<2**40 and (s[j]+4*g-4*j).denominator<2**40 for j,g in product(range(3),range(2)))
A0=q+201;m=4*q+10000
assert A0+3+5*m<2**27 and 3*(q+605)+6*27<m
C1=2*(q+605+2*(A0+1));assert C1<2**25
period=2*lcm(*(p*(p-1) for p in qs));L=period+3
assert L==171033187 and 6*(2*L+1)>max(349+3*q,m+1,27,11)
print('Selective contacts, exponent profiles, 42 marker entries, fixed-exception bound and L=171033187 PASS')
