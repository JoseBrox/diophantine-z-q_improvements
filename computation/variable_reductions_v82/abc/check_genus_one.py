#!/usr/bin/env python3
"""Read-only exact checks for the v82 genus-one criterion and menu obstruction.
Use --write only to create/update certificate.json.  PARI's algebraic ellrank
bounds are used; no analytic-rank approximation or BSD inference is used.
"""
from fractions import Fraction as Q
from pathlib import Path
from importlib import metadata
from itertools import product
from math import isqrt
import argparse,json
import sympy as sp
from sage.libs.pari import pari

HERE=Path(__file__).resolve().parent
M=(-1,-2,-3,-5,-6,-7,-10,-14,1,2,3,5,6,7,10,14)

def sf(a):
 a=Q(a);n=a.numerator*a.denominator
 assert n
 out=-1 if n<0 else 1
 for p,e in sp.factorint(abs(n)).items():
  if e%2:out*=int(p)
 return out

def vp(a,p):
 a=Q(a);m,n=a.numerator,a.denominator;e=0
 assert m
 while m%p==0:m//=p;e+=1
 while n%p==0:n//=p;e-=1
 return e

def pairmul(a,b):return tuple(sf(x*y) for x,y in zip(a,b))

def compute():
 # These identities are reconstructed without importing a polynomial producer.
 d,h,s,Y=sp.symbols('d h s Y');n=d*h
 curves=[d*(s**4-h**2),d*(s*s-h)*(s*s-2*h),d*(s*s+h)*(s*s+2*h)]
 xs=[d*s*s,d*s*s-n,d*s*s+n]
 for rhs,x in zip(curves,xs):
  expr=(d*s*Y)**2-x**3+n*n*x
  assert sp.rem(sp.Poly(expr,Y),sp.Poly(Y*Y-rhs,Y)).is_zero
 beta=119;eta=52985;N=beta*eta
 assert N==5*7*17*10597 and pari('isprime(10597)')==1
 E=pari(f'ellinit([0,0,0,-{N}^2,0])');rank=E.ellrank()
 assert int(rank[0])==int(rank[1])==1 and int(rank[2])==2
 tors=E.elltors();assert int(tors[0])==4
 x=Q(-6002500);y=Q(4729026750)
 assert y*y==x**3-N*N*x
 assert x==-2450**2 and x-N==-35*593**2 and x+N==35*93**2
 assert sf(x)==-1 and sf(x-N)==-35 and sf(x+N)==35
 T0=(-1,-N);TN=(N,2);R=(-1,-35)
 torsion={(1,1),T0,TN,pairmul(T0,TN)}
 assert R not in torsion
 kummer=set()
 for bits in product((0,1),repeat=3):
  q=(1,1)
  for bit,g in zip(bits,[T0,TN,R]):
   if bit:q=pairmul(q,g)
  kummer.add(q)
 assert len(kummer)==8
 coordinate_classes={a for q in kummer for a in (*q,sf(q[0]*q[1]))}
 # Add the nonzero exceptional coordinates at the rational two-torsion points.
 coordinate_classes.update([sf(q) for q in [N,-N,2*N,-2*N]])
 subgroup={sf((-1)**a*2**b*35**c*N**e) for a,b,c,e in product((0,1),repeat=4)}
 assert coordinate_classes<=subgroup
 assert all((vp(q,17)-vp(q,10597))%2==0 for q in subgroup)
 excluded=[sf(mu*beta*N**e) for mu in M for e in (0,1)]
 assert not set(excluded)&subgroup
 # A second algebraic descent on the 2-isogenous curve; same PARI algorithm.
 E2=pari(f'ellinit([0,0,0,{4*N*N},0])');rank2=E2.ellrank()
 assert int(rank2[0])==int(rank2[1])==1
 x2=x-Q(N*N,x);y2=y*(1+Q(N*N,x*x))
 assert y2*y2==x2**3+4*N*N*x2
 assert pow(7,8,17)==16 and 17%8==1
 assert pow(eta%7,3,7)==1 and pow(eta%17,8,17)==1
 assert 213**2+119*8**2==eta
 t=Q(19,16);u=17*t*t;r=t/(1+u);w=u/(1+u)**2
 dd=7*w;V=Q(213,8)*r;H=V*V+dd;e=4*dd/(V*V)
 assert dd==119*r*r and H==eta*(r/8)**2
 assert dd*H==N*(r*r/8)**2
 assert e==Q(30464,45369)==119*Q(16,213)**2
 assert 0<w<Q(1,4) and 0<V<2 and 0<e<1
 assert [vp(z,2) for z in [u,dd,V,e]]==[-8,8,1,8]
 assert vp(u,17)==1 and sf(dd)==119
 assert all(isqrt(z.denominator)**2==z.denominator for z in [dd,e])
 return {
  'runtime':{'PARI':str(pari('version()')),'passagemath-pari':metadata.version('passagemath-pari')},
  'symbolic_curve_maps':3,
  'curve':{'N':N,'factorization':{'5':1,'7':1,'17':1,'10597':1},'ellrank':str(rank),'torsion_order':4,'two_isogenous_ellrank':str(rank2)},
  'point':{'x':str(x),'y':str(y),'coordinate_classes':[-1,-35,35],'normalized_Kummer_pair':[1,180149]},
  'Kummer_image_mod_two':sorted([list(q) for q in kummer]),
  'coordinate_squareclasses':sorted(coordinate_classes),
  'containing_squareclass_subgroup':sorted(subgroup),
  'finite_menu':list(M),'excluded_target_classes':sorted(set(excluded)),
  'prepared_tuple':{k:str(v) for k,v in {'t':t,'u':u,'w':w,'r':r,'d':dd,'V':V,'H':H,'e':e}.items()},
  'valuations':{'v2u':-8,'v2d':8,'v2V':1,'v2e':8,'v17u':1},
  'scope':{
   'rank_evidence':'Unconditional algebraic ellrank intervals; the isogenous check is a second specialization of the same implementation.',
   'local_theorem':'Proved symbolically in the manuscript, not certified by finite place enumeration.',
   'exclusion':'All three shifted abscissas, every multiplier supported on {2,3,5,7}, and any power of N.',
   'actual_source':'Not asserted to be an actual contact detector or actual W-trace tuple.',
   'variable_bound':'No ten-variable definition is claimed.'}}

def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args()
 got=compute();path=HERE/'certificate.json'
 if args.write:path.write_text(json.dumps(got,indent=2,sort_keys=True)+'\n')
 else:assert json.loads(path.read_text())==got,'certificate mismatch'
 print('PASS: 3 exact curve maps; algebraic rank [1,1] on both isogenous curves; all 8 Kummer classes; prepared nonsquare-u counterexample.')
if __name__=='__main__':main()
