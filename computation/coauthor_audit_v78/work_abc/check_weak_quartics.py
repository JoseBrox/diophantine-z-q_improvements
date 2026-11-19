"""Independent SymPy/stdlib audit of all new fixed-weak-abc quartics."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from itertools import product
from math import gcd
import hashlib,json,os
import sympy as s
HERE=Path(__file__).resolve().parent
BASE=Path(os.environ.get('ABC62_PARENT',HERE.parent/'H10-quartics/abc62'))
def read(p):return json.loads(p.read_text())
def parse(terms):return {(t['parameterPower'],tuple(t['monomial'])):int(t['coefficient']) for t in terms}
def sparse(poly,coords):
 p=s.Poly(poly,*coords)
 out={}
 for ex,co in p.terms():
  mon=tuple(i+1 for i,n in enumerate(ex) for _ in range(n));out[0,mon]=int(co)
 return out
def verify(folder,k,r,kappa):
 cert=read(folder/'certificate.json');quad=read(folder/'quadrics.json');poly=parse(read(folder/'polynomial.json')['terms'])
 roots=cert['contacts'];assert roots==({6:[1,31,37,41,46,61],8:[1,8,22,28,29,36,43,64]}[k])
 n=59+r if k==6 else 61+r
 assert quad['variables']==n and len(quad['residuals'])==n-12
 x=s.symbols('x1:'+str(n+1));t,v=s.symbols('t v')
 G=s.prod(t-c for c in roots).expand()
 if k==6:
  # z=2+60/(t-61), inverse t=61+60/(z-2).
  old=[F(0),F(-2),F(-1,2),F(1),F(-1),None]
  images=[F(61)+60/(z-2) if z is not None else F(61) for z in old]
  assert set(images)==set(roots)
  assert s.expand(v*(v+2)**3-(2*v+1)**3-(v-1)**3*(v+1))==0
 else:
  P=(v+4)*(v+20)**3*(v-5)**2;Q=(v-4)*(v-20)**3*(v+5)**2
  assert s.expand(P-Q)==108*v**5 and s.gcd(P,Q)==1
  old=[0,4,-4,5,-5,20,-20,None]
  images=[F(43)+F(210,z-10) if z is not None else F(43) for z in old]
  assert set(images)==set(roots)
 base=read(BASE/'quadrics.json');expected={q['name']:parse(q['terms']) for q in base['residuals']}
 for gate,w in [('gate0',35),('gate1',49)]:
  assert expected[gate].pop((0,(w,62)))==-1
 new_ids=[];g_index=62
 for j,(ti,ei,fi,wi) in enumerate(((2,33,34,35),(32,47,48,49))):
  T,E,H,W=x[ti-1],x[ei-1],x[fi-1],x[wi-1];cinv=x[61]
  expected[f'detector{j}.contactSquare']=sparse(T*E-cinv**2,x)
  expected[f'detector{j}.contactSum']=sparse(H*cinv-E**2,x)
  if k==8:
   g_index+=1;J=x[g_index-1];new_ids.append(g_index)
   expected[f'detector{j}.contactCube']=sparse(J*cinv-E*H,x)
  co=s.Poly(G,t)
  if k==6:
   terms=T**2+co.nth(5)*T*cinv+co.nth(4)*cinv**2+co.nth(3)*E*cinv+co.nth(2)*H*cinv+co.nth(1)*E*H+co.nth(0)*H**2
  else:
   terms=T**2+co.nth(7)*T*cinv+co.nth(6)*cinv**2+co.nth(5)*E*cinv+co.nth(4)*H*cinv+co.nth(3)*J*cinv+co.nth(2)*H**2+co.nth(1)*H*J+co.nth(0)*J**2
  expected[f'detector{j}.inverseContact']=sparse(W*cinv-terms,x)
  # Exact rational function recovery before Laurent rescaling.
  subst={T:t,E:1/t,H:1/t**2,W:s.Symbol('w'),cinv:1}
  if k==8:subst[J]=1/t**3
  assert s.cancel((W*cinv-terms).subs(subst)-(s.Symbol('w')-G/t**(k-2)))==0
 last=31
 for j in range(3,r):
  g_index+=1;new_ids.append(g_index)
  expected['height.power'+str(2**j)]=sparse(x[g_index-1]-x[last-1]**2,x);last=g_index
 assert g_index==n
 gap=expected['detector1.argument'];assert gap.pop((0,(31,31)))==1;gap[0,(last,last)]=1
 # Check the scale, rather than trusting arbitrary certificate exponents.
 expected_ws=read(BASE/'parameter-scaling.json')['variable_powers']+[0]*(n-62)
 expected_ws[30]=0;expected_ws[last-1]=1
 assert cert['variablePowers']==expected_ws and expected_ws[0]==0
 names=list(expected);scaled=[];divs=[]
 for name,p in expected.items():
  powers={key:4*key[0]+sum(expected_ws[i-1] for i in key[1]) for key in p};dd=min(powers.values());divs.append(dd)
  scaled.append({(powers[key]-dd,key[1]):co for key,co in p.items()})
 assert divs==cert['rowPowers']
 pivot=names.index('shared.unit');ops=[]
 for i,p in enumerate(scaled):
  if i==pivot:continue
  co=p.get((0,()),0)
  if co:
   z={key:p.get(key,0)+co*scaled[pivot].get(key,0) for key in p.keys()|scaled[pivot].keys()};z={key:val for key,val in z.items() if val};gg=gcd(*z.values());scaled[i]={key:val//gg for key,val in z.items()};ops.append([i,pivot,co,gg])
 assert ops==cert['rowOperations']
 assert names==[q['name'] for q in quad['residuals']]
 assert scaled==[parse(q['terms']) for q in quad['residuals']]
 total=defaultdict(int)
 for p in scaled:
  assert all(len(m)<=2 and 0<=e<=2 for e,m in p)
  for ((a,m),co),((b,mm),c) in product(p.items(),repeat=2):total[a+b,tuple(sorted(m+mm))]+=co*c
 total={key:co for key,co in total.items() if co}
 assert total==poly
 profiles=defaultdict(dict)
 for (e,m),co in total.items():profiles[m][e]=co
 assert len(profiles)==cert['monomials'] and len(total)==cert['parameterSeparatedTerms']
 assert profiles[()]=={4:1,0:1} and profiles[(1,1,1,1)]=={0:1}
 assert set(i for m in profiles for i in m)==set(range(1,n+1))
 assert all(len(p)==1 or m==() for m,p in profiles.items())
 caps=[max([abs(co) for (e,m),co in total.items() if e==j],default=0) for j in range(5)]
 assert caps==cert['coefficientCaps'] and caps[4]==1
 nn=cert['sufficientOddN'];assert nn%2 and all(caps[j]*nn**j<=nn**4+1 for j in range(4))
 # Ratios c_j/n^(4-j) decrease for all n>=nn, so this is a uniform bound.
 kap=F(kappa);gamma=F(2*(k-2))/kap-k;den=F(2**r)-kap*(2**(r-1)+2);ratio=4*(2*kap-1)/(gamma*den)
 assert den>0 and gamma>0 and ratio<1
 assert cert['absorption']==str(ratio) and cert['weakAbcExponent']==str(kap)
 result={'status':'PASS','variables':n,'quadrics':len(scaled),'degree':4,'monomials':len(profiles),'content':1,'weak_abc_exponent':str(kap),'strict_absorption':str(ratio),'height':'B+1 for B=n^4 and odd n>='+str(nn),'arithmetic_defining_threshold':'ineffective','sha256':hashlib.sha256((folder/'polynomial.json').read_bytes()).hexdigest()}
 (folder/'independent-verification.json').write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':
 reports=[verify(HERE/'weak_quartics'/name,k,r,kap) for name,k,r,kap in [('weak63',6,4,'9/8'),('weak64',6,5,'17/14'),('weak67',8,6,'7/5')]]
 print(json.dumps(reports,indent=2))
