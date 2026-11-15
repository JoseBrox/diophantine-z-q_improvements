#!/usr/bin/env python3
"""Independent Jacobian-coordinate verification of mixed reference signs.

The checker imports neither the affine producer nor a computer algebra package.
The optional --certificate argument permits verification of a reconstructed file.
"""
from pathlib import Path
from math import isqrt,gcd,lcm
import argparse,json
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent

def distinct_prime_divisors(n):
 factors=[]
 for d in range(2,isqrt(n)+1):
  if n%d:continue
  factors.append(d)
  while n%d==0:n//=d
 if n>1:factors.append(n)
 return factors

class Jacobian:
 def __init__(self,p,A):self.p,self.A=p,A
 def double(self,P):
  p,A=self.p,self.A;X,Y,Z=P
  if not Z or not Y:return(0,1,0)
  xx=X*X%p;yy=Y*Y%p;yyyy=yy*yy%p;zz=Z*Z%p
  s=2*((X+yy)**2-xx-yyyy)%p;m=(3*xx+A*zz*zz)%p
  U=(m*m-2*s)%p;V=(m*(s-U)-8*yyyy)%p;W=((Y+Z)**2-yy-zz)%p
  return U,V,W
 def add_mixed(self,P,Q):
  p=self.p;X,Y,Z=P;x,y=Q
  if not Z:return x,y,1
  zz=Z*Z%p;u=x*zz%p;s=y*Z*zz%p;hh=(u-X)%p
  if not hh:return self.double(P) if s==Y else(0,1,0)
  H2=hh*hh%p;I=4*H2%p;J=hh*I%p;r=2*(s-Y)%p;v=X*I%p
  U=(r*r-J-2*v)%p;V=(r*(v-U)-2*Y*J)%p;W=((Z+hh)**2-zz-H2)%p
  return U,V,W
 def multiply(self,P,n):
  assert n>=0
  Q=(0,1,0)
  for bit in bin(n)[2:]:
   Q=self.double(Q)
   if bit=='1':Q=self.add_mixed(Q,P)
  p=self.p;X,Y,Z=Q
  if not Z:return None
  inv=pow(Z,-1,p)
  return [X*inv*inv%p,Y*inv**3%p]

def check_reduction(entry):
 p=entry['prime'];rho=entry['rho']
 assert p>2 and all(p%d for d in range(2,isqrt(p)+1))
 assert rho*rho%p==2
 D=(11-6*rho)%p
 assert D==entry['D'] and D
 P=[(57*pow(8,-1,p)-7*pow(2,-1,p)*rho)%p,(-165*pow(8,-1,p)+417*pow(32,-1,p)*rho)%p]
 assert P==entry['P'] and(P[1]**2-P[0]**3+D*P[0])%p==0
 J=Jacobian(p,-D)
 # Authenticate the doubled-point assertion independently at each reduction.
 R0=[(1+rho)%p,2*rho%p]
 assert J.multiply(R0,2)==P
 n=entry['order'];assert J.multiply(P,n) is None
 factors=distinct_prime_divisors(n)
 assert [r['primeDivisor'] for r in entry['properDivisorChecks']]==factors
 for check in entry['properDivisorChecks']:
  Q=J.multiply(P,n//check['primeDivisor'])
  assert Q is not None and Q==check['point']
 return J

def check(path):
 data=json.loads(path.read_text())
 # Exact quadratic-field authentication of the fixed point and its doubling.
 def plus(x,y):return(x[0]+y[0],x[1]+y[1])
 def minus(x,y):return(x[0]-y[0],x[1]-y[1])
 def times(x,y):return(x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
 def divide(x,y):
  norm=y[0]*y[0]-2*y[1]*y[1];assert norm
  return times(x,(y[0]/norm,-y[1]/norm))
 c=lambda n:(F(n),F(0))
 Dq=(F(11),F(-6));xr=(F(1),F(1));yr=(F(0),F(2))
 assert times(yr,yr)==minus(times(times(xr,xr),xr),times(Dq,xr))
 slope=divide(minus(times(c(3),times(xr,xr)),Dq),times(c(2),yr))
 xp=minus(times(slope,slope),times(c(2),xr));yp=minus(times(slope,minus(xr,xp)),yr)
 assert xp==(F(57,8),F(-7,2)) and yp==(F(-165,8),F(417,32))
 assert times(yp,yp)==minus(times(times(xp,xp),xp),times(Dq,xp))
 assert data['schema']=='mixed-reference-signs/v42'
 first,second=data['embeddings']
 assert first['prime']==second['prime']==76537 and first['prime']>76176
 assert [first['rho'],second['rho']]==[26935,49602]
 assert [first['order'],second['order']]==[6375,4786]
 J1,J2=check_reduction(first),check_reduction(second)
 assert (first['rho']+second['rho'])%first['prime']==0
 index=data['indexClass'];h=index['h'];period=index['modulus']
 assert h==28101000 and period==30510750
 assert gcd(first['order'],second['order'])==1
 assert period==lcm(first['order'],second['order'])
 assert h%first['order']==index['firstCongruence']==0
 assert (h-1)%second['order']==index['secondCongruenceForHMinusOne']==2393
 assert J1.multiply(first['P'],h) is None
 assert J2.multiply(second['P'],h-1)==[0,0]
 assert data['reductions']=={'HAtFirstPrime':None,'HMinusPAtSecondPrime':[0,0]}
 small=data['nonTorsionReduction'];check_reduction(small)
 assert (small['prime'],small['rho'],small['order'])==(17,6,5)
 assert first['order']%3==0 and small['order']%3!=0
 # Formal Laurent-polynomial verification of translation by T0.
 # Monomial exponents refer to D,x,y, and may be negative.
 def add(*polys):
  out={}
  for poly in polys:
   for monomial,coefficient in poly.items():out[monomial]=out.get(monomial,0)+coefficient
  return {m:c for m,c in out.items() if c}
 def mul(left,right):
  out={}
  for m,a in left.items():
   for n,b in right.items():
    key=tuple(u+v for u,v in zip(m,n));out[key]=out.get(key,0)+a*b
  return {m:c for m,c in out.items() if c}
 def neg(poly):return {m:-c for m,c in poly.items()}
 D={(1,0,0):1};x={(0,1,0):1};y={(0,0,1):1}
 xp={(1,-1,0):-1};yp={(1,-2,1):1}
 curve=add(mul(y,y),neg(mul(mul(x,x),x)),mul(D,x))
 translated=add(mul(yp,yp),neg(mul(mul(xp,xp),xp)),mul(D,xp))
 assert translated==mul({(2,-4,0):1},curve)
 assert mul(yp,{(-1,1,0):-1})=={(0,-1,1):-1}
 assert neg(mul(xp,{(-1,2,-1):1}))=={(0,1,-1):1}
 result={'schema':data['schema'],'checks':'PASS','independentMethod':'Jacobian doubling and mixed addition; exact order divisor tests; trial-division primality','prime':76537,'orders':[6375,4786],'indexProgression':[h,period],'nonTorsionPrimeTo17OrderDiscrepancy':3,'scope':'Automatic agreement of the two torsion-translation signs fails for doubled reference points; the full detector system is not tested.'}
 print(json.dumps(result,indent=2))
 return result

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json');args=parser.parse_args();check(args.certificate)
