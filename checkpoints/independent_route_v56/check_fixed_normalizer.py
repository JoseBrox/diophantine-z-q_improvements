#!/usr/bin/env python3
"""Exact checks accompanying fixed_normalizer_checkpoint.md.

The finite enumerations certify precisely the small-prime local cases used in
an all-primes proof. Symbolic assertions check the discriminant, singular
factorization, positivity identity, and Jacobian invariants. No rational
realization conjecture is inferred from bounded search.
"""
from fractions import Fraction
import json
from pathlib import Path
import sympy as sp

X,c,a,r=sp.symbols('X c a r')
assert sp.expand(2*(a**3+1)*(a**2+2)-(a**2+1)**2-(a**3*(2*a*a-a+4)+3))==0
for i in (1,2):
 f=c*c*X**4+X+i
 assert sp.expand(sp.discriminant(f,X)-c**4*(256*i**3*c*c-27))==0
 I=12*c*c*i
 J=-27*c*c
 jac= X**3-27*I*X-27*J
 assert sp.expand(sp.discriminant(jac,X)-3**12*sp.discriminant(f,X))==0
 # c4=-48 A for y^2=x^3+A*x+B; hence it is a unit away from 2,3,i,c.
 assert sp.expand(-48*(-27*I))==15552*c*c*i
assert sp.expand((X-r)**2*(X*X+2*r*X+3*r*r))==X**4-4*r**3*X+3*r**4

small=[]
for p in (3,5,7):
 squares={z*z%p for z in range(1,p)}
 for u in range(1,p):
  # Unit c. The proof fixes y=0 except for p=3,c=1.
  y=1 if p==3 and u==1 else 0
  hits=[x for x in range(p) if (u*(u*u*x**4+x+1)*(u*u*y**4+y+2))%p in squares]
  assert hits,(p,u,'unit')
  small.append({'prime':p,'unit':u,'case':'unit_c','x':hits[0],'y':y})
  # c=p^(-2k)*u with k>=1. Put x=p^k*X,y=0.
  hits=[x for x in range(p) if (2*u*(u*u*x**4+1))%p in squares]
  assert hits,(p,u,'even_pole')
  small.append({'prime':p,'unit':u,'case':'even_pole_c','normalized_x':hits[0],'y':0})

# At 3, every 3-integral a produces c=0 or 2 modulo 3, never 1.
assert {((t**3+1)*(t*t+2)*pow((t*t+1)**2,-1,3))%3 for t in range(3)}=={0,2}

# Independent examples showing odd discriminant primes with the required
# separation. This is illustrative: their existence for all inputs is proved.
examples=[]
for aa in (2,4,6,8,10,Fraction(2,9),Fraction(4,25)):
 aa=Fraction(aa)
 cc=(aa**3+1)*(aa**2+2)/(aa**2+1)**2
 assert cc>Fraction(1,2)
 selected=[]
 for i in (1,2):
  d=256*i**3*cc*cc-27
  fs=sp.factorint(d.numerator)
  candidates=[int(q) for q,e in fs.items() if q not in (2,3,7) and e%2==1]
  assert candidates
  q=min(candidates)
  assert cc.numerator%q and cc.denominator%q
  other=256*(3-i)**3*cc*cc-27
  assert other.numerator%q and other.denominator%q
  selected.append({'i':i,'prime':q,'valuation':int(fs[q])})
 examples.append({'a':str(aa),'c':str(cc),'discriminant_primes':selected})

output={'symbolic_checks':'passed','small_prime_certificates':small,'examples':examples}
out=Path(__file__).with_name('fixed_normalizer_certificate.json')
out.write_text(json.dumps(output,indent=2)+'\n')
print('All exact checks passed; wrote',out)
