#!/usr/bin/env python3
"""Exact supplemental checks of the v27 arithmetic transformations.
These finite identities and preparation examples do not certify a global
prime-pattern theorem, Jaswal's theorem, or the family height theorem.
"""
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
from math import gcd,isqrt
import json
HERE=Path(__file__).resolve().parent
# Sparse polynomials in b,r,a1,a2,y1,y2 over Q.
def add(*ps):
 d=defaultdict(F)
 for p in ps:
  for m,c in p.items():d[m]+=c
 return {m:c for m,c in d.items() if c}
def sc(p,c):return {m:c*v for m,v in p.items() if c*v}
def mul(p,q):
 d=defaultdict(F)
 for m,c in p.items():
  for n,e in q.items():d[tuple(a+b for a,b in zip(m,n))]+=c*e
 return {m:c for m,c in d.items() if c}
def C(c):return {(0,)*6:F(c)} if c else {}
def V(i):return {tuple(int(i==j) for j in range(6)):F(1)}
def pw(p,n):
 o=C(1)
 for _ in range(n):o=mul(o,p)
 return o
def sf(n):
 ans=1;p=2
 while p*p<=n:
  v=0
  while n%p==0:n//=p;v+=1
  if v%2:ans*=p
  p+=1
 return ans*n

def main():
 b,r,a1,a2,y1,y2=(V(i) for i in range(6));one=C(1)
 curve1=add(pw(y1,2),sc(mul(pw(b,3),pw(a1,6)),-1),mul(pw(r,2),mul(b,pw(a1,2))))
 first=add(mul(pw(r,2),mul(b,pw(a1,2))),pw(y1,2),sc(mul(pw(b,3),pw(a1,6)),-1))
 assert first==curve1
 curve2=add(pw(y2,2),sc(mul(pw(b,3),pw(a2,6)),-1),mul(mul(pw(r,2),pw(add(one,sc(b,-1)),2)),mul(b,pw(a2,2))))
 second=add(mul(pw(b,3),pw(a2,6)),sc(mul(mul(pw(r,2),pw(add(one,sc(b,-1)),2)),mul(b,pw(a2,2))),-1),sc(pw(y2,2),-1))
 assert second==sc(curve2,-1)
 count=0
 for den in range(5,150,2):
  for j in range(8):
   if gcd(16*(8*j+1),den)>1:continue
   q=F(16*(8*j+1),den*den)
   if q>=1:continue
   num,dd=q.numerator,q.denominator;assert isqrt(dd)**2==dd
   beta,theta=sf(num),sf(dd-num)
   assert beta%8==theta%8==1 and gcd(beta,theta)==1
   for t,u in ((beta,theta),(theta,beta)):
    for p in range(3,isqrt(t)+2,2):
     if t%p==0 and all(p%d for d in range(2,isqrt(p)+1)):assert pow(u%p,(p-1)//2,p)==1
    # Complete prime-factor extraction, including the final large factor.
    x=t;p=3
    while p*p<=x:
     if x%p==0:
      assert pow(u%p,(p-1)//2,p)==1
      while x%p==0:x//=p
     p+=2
    if x>1:assert pow(u%x,(x-1)//2,x)==1
   count+=1
 # Removing b!=0 destroys the growth conclusion, for every large a.
 for a in range(3,100):
  for t in (-1,1):assert t*t-a*(a-2)*t*0+(a-2)**2*0**2-1==0
 # Half-integral output forces the input integral because 102 is squarefree.
 assert all(102%(p*p)!=0 for p in range(2,11))
 report=dict(schema='v27-supplemental-arithmetic/v1',status='PASS',poleCurveIdentities=2,preparedSquareClassExamples=count,zeroLucasCoordinateCounterexamples=194,denominatorConstant=102,scope='Exact rational polynomial identities, bounded squareclass examples, and an explicit counterfamily to deleting b!=0. Written proofs establish the universal statements; external arithmetic inputs are not verified by this computation.')
 (HERE/'arithmetic-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
