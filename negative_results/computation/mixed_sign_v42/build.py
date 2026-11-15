#!/usr/bin/env python3
"""Reconstruct the finite-field mixed-reference-sign certificate."""
from pathlib import Path
from math import gcd,isqrt,lcm
import argparse,json
HERE=Path(__file__).resolve().parent

def factors(n):
 out=[]
 for q in range(2,isqrt(n)+1):
  if n%q:continue
  out.append(q)
  while n%q==0:n//=q
 if n>1:out.append(n)
 return out

def add(A,B,D,p):
 if A is None:return B
 if B is None:return A
 x,y=A;X,Y=B
 if x==X:
  if (y+Y)%p==0:return None
  slope=(3*x*x-D)*pow(2*y,-1,p)%p
 else:slope=(Y-y)*pow(X-x,-1,p)%p
 xx=(slope*slope-x-X)%p
 return [xx,(slope*(x-xx)-y)%p]

def multiply(P,n,D,p):
 out=None
 while n:
  if n&1:out=add(out,P,D,p)
  P=add(P,P,D,p);n>>=1
 return out

def data(p,rho,order):
 D=(11-6*rho)%p
 P=[(57*pow(8,-1,p)-7*pow(2,-1,p)*rho)%p,(-165*pow(8,-1,p)+417*pow(32,-1,p)*rho)%p]
 assert (rho*rho-2)%p==0 and D and (P[1]**2-P[0]**3+D*P[0])%p==0
 assert multiply(P,order,D,p) is None
 tests=[{'primeDivisor':q,'point':multiply(P,order//q,D,p)} for q in factors(order)]
 assert all(t['point'] is not None for t in tests)
 return {'prime':p,'rho':rho,'D':D,'P':P,'order':order,'properDivisorChecks':tests}

def build(out):
 p=76537
 assert all(p%d for d in range(2,isqrt(p)+1))
 first=data(p,26935,6375);second=data(p,49602,4786)
 h=28101000;period=lcm(first['order'],second['order'])
 assert gcd(first['order'],second['order'])==1
 assert multiply(first['P'],h,first['D'],p) is None
 assert multiply(second['P'],h-1,second['D'],p)==[0,0]
 assert multiply(second['P'],2393,second['D'],p)==[0,0]
 small=data(17,6,5)
 # Torsion would have a 3-part by the large-prime order, but good reduction
 # at17 injects prime-to17 torsion and the reduction there has order5.
 assert first['order']%3==0 and small['order']%3!=0
 result={'schema':'mixed-reference-signs/v42','field':'Q(sqrt(2))','curve':'y^2=x^3-(11-6sqrt(2))x','point':'P=(57/8-7sqrt(2)/2,-165/8+417sqrt(2)/32)=2R0','primeCertifiedBy':'Trial division through floor(sqrt(p))','embeddings':[first,second],'indexClass':{'h':h,'modulus':period,'firstCongruence':0,'secondCongruenceForHMinusOne':2393},'reductions':{'HAtFirstPrime':None,'HMinusPAtSecondPrime':[0,0]},'nonTorsionReduction':small,'scope':'Opposite torsion-translation signs occur for a single global reference multiple in 2E(K). No counterexample to the full defining system is asserted.'}
 out.mkdir(parents=True,exist_ok=True)
 (out/'certificate.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'prime':p,'h':h,'period':period,'orders':[6375,4786],'checks':'PASS'},indent=2))
 return result

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=HERE);args=parser.parse_args();build(args.output)
