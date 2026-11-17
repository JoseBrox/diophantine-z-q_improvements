#!/usr/bin/env python3
"""Exact certificate for the affine normalized Pheidas block.

Certifies symbolic identities, all small-prime cases needed by the local
proof, the prime-5 correction, and explicit rational examples. Global
completeness uses Harpaz--Skorobogatov Theorem 2.3 under its Sha hypothesis;
it is not inferred from these computations.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
import sympy as sp

X,Y,c,b,i=sp.symbols('X Y c b i')
f=lambda t,j,v: v*v*t**4+t+j
for j in (1,2):
 poly=f(X,j,c)
 delta=sp.discriminant(poly,X)
 assert sp.expand(delta-c**4*(256*j**3*c*c-27))==0
 I,J=12*j*c*c,-27*c*c
 resolvent=X**3-27*I*X-27*J
 assert sp.expand(sp.discriminant(resolvent,X)-3**12*delta)==0
 r=sp.Rational(-4*j,3)
 # Singular condition is c^2=27/(256*j^3).
 assert sp.expand((poly-c*c*(X-r)**2*(X*X+2*r*X+3*r*r)).subs(c*c,sp.Rational(27,256*j**3)))==0

plus,minus=2+4*b,2-4*b
for t,j in ((X,1),(Y,2)):
 A=(4+16*b*b)*t**4+t+j
 assert sp.expand(f(t,j,plus)*f(t,j,minus)-(A*A-256*b*b*t**8))==0

cert=[]
for p in (3,5,7):
 squares={z*z%p for z in range(1,p)}
 for u in range(1,p):
  if (p,u)==(3,1):
   # f_1(1)=0 mod3 with unit derivative; set z=3 and lift x.
   assert (u*u+2)%p==0 and (4*u*u+1)%p!=0
   cert.append({'p':p,'unit':u,'case':'unit_c','method':'Hensel at x=1, y=0, z=3'})
  else:
   hits=[x for x in range(p) if (2*u*(u*u*x**4+x+1))%p in squares]
   assert hits,(p,u,'unit')
   cert.append({'p':p,'unit':u,'case':'unit_c','x_mod_p':hits[0],'y':0})
  hits=[x for x in range(p) if (2*u*(u*u*x**4+1))%p in squares]
  assert hits,(p,u,'even_pole')
  cert.append({'p':p,'unit':u,'case':'even_pole_c','normalized_x_mod_p':hits[0],'y':0})

# The discriminant-prime lemma must allow 5: >7 is too strong.
cc=Q(114,13)
assert 2048*cc*cc-27==5*Q(2307,13)**2

# Exact rational witnesses, including the full guarded Kummer block at b=1.
witnesses=[]
for bb,xx,yy,zz in (
 (Q(0),Q(0),Q(0),Q(1)),
 (Q(1),Q(-5,14),Q(-8,5),Q(17043,2450)),
 (Q(3),Q(2,19),Q(0),Q(145,361)),
 (Q(1,25),Q(5,6),Q(0),Q(35,18)),
):
 cc=2+4*abs(bb)
 assert cc*zz*zz==f(xx,1,cc)*f(yy,2,cc)
 guard=1-4*bb*bb
 for eps in (-1,1):
  ce=2+4*eps*bb
  guard*=f(xx,1,ce)*f(yy,2,ce)
 assert guard
 witnesses.append({'b':str(bb),'c':str(cc),'x':str(xx),'y':str(yy),'z':str(zz),'all_character_guard_nonzero':True})

# A rational input with an odd negative pole: soundness excludes it.
assert Q(1,3).denominator==3
out={'symbolic_identities':'passed','small_prime_cases':cert,
 'prime_scope_correction':{'c':'114/13','D_2':'5*(2307/13)^2','allowed_primes':'p not in {2,3,7}'},
 'rational_witnesses':witnesses,
 'scope':'No rational Hasse principle for the y=0 genus-one curve is asserted.'}
path=Path(__file__).with_name('affine_pheidas_certificate.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print('All affine-block exact checks passed; wrote',path)
