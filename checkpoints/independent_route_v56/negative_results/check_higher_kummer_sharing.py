#!/usr/bin/env python3
"""Exact identities/counterexamples for higher_kummer_sharing.md."""
from fractions import Fraction as Q
from pathlib import Path
from math import gcd, isqrt
import json
import sympy as sp

f=lambda c,j,x:c*c*x**4+x+j

def trial_prime(n):
 return n>=2 and all(n%d for d in range(2,isqrt(n)+1))

def vp(q,p):
 q=Q(q);n=q.numerator;d=q.denominator;out=0
 while n%p==0:n//=p;out+=1
 while d%p==0:d//=p;out-=1
 return out

# No common branch root if c1^2 != c2^2.
x,c1,c2=sp.symbols('x c1 c2')
assert sp.expand(f(c1,2,x)-f(c2,2,x)-(c1*c1-c2*c2)*x**4)==0

# Rational family for the three-factor counterexample.
t,u=sp.symbols('t u')
c=2*u*u;xx=1/u;yy=t/u;g=5+1/u
assert sp.factor((f(c,2,yy)-2*g).subs(u,(2-t)/(4*(t**4-2))))==0

simple={'b':Q(7,67),'c':Q(162,67),'x':Q(2),'y':Q(0),'Z':Q(18)}
assert simple['c']==2+4*simple['b']
assert simple['Z']**2==simple['c']*f(Q(2),1,simple['x'])*f(simple['c'],2,simple['y'])
assert vp(simple['b'],67)==-1 and vp(simple['b'],2)>=0

p=4441;xx=Q(912);N=f(Q(2),1,xx);k=1663489
bb=(k*k-N)/(2*N);cc=2*k*k/N;zz=2*k
assert sp.isprime(p) and sp.isprime((p+1)//2)
assert trial_prime(p) and trial_prime((p+1)//2)
assert p%8==1 and p%7==3
assert zz*zz==cc*N*f(cc,2,Q(0))
assert vp(bb,p)==-1 and vp(bb,2)>=0

tt=Q(110,91);uu=(2-tt)/(4*(tt**4-2));cc1=2*uu*uu;xx=1/uu;yy1=tt*xx
gg=f(cc1,1,xx);D=3507206794;ss=Q(1,24843);kk=41877
assert gg==D*ss*ss and D==2*7*13*17*1133551
assert all(sp.isprime(q) and trial_prime(q) for q in (2,7,13,17,1133551))
assert gcd(kk,D)==1
cc2=Q(4*kk*kk,D);bb1=(cc1-2)/4;bb2=(cc2-2)/4;zz1=2*uu*gg;zz2=8*cc2*kk*ss
assert zz1**2==cc1*gg*f(cc1,2,yy1)
assert zz2**2==cc2*gg*f(cc2,2,Q(-2))
assert bb1>0 and bb2>0 and cc1>2 and cc2>2
assert vp(bb1,2)>=0 and vp(bb2,2)>=0
assert sp.integer_nthroot(bb1.denominator,2)[1] and bb1.denominator%2
assert vp(bb2,1133551)==-1 and 1133551>76176
assert 1133551 not in (1875611,3828397,3982747) and 1133551%8==7
# Every raw factor needed for the displayed all-sign pole guards is nonzero.
for eps in (-1,1):
 ce1=2+4*eps*bb1;ce2=2+4*eps*bb2
 assert ce1 and ce2 and f(ce1,1,xx) and f(ce1,2,yy1) and f(ce2,2,Q(-2))

out={'symbolic_family':'passed','small_fixed_reference':{k:str(v) for k,v in simple.items()},
 'tailored_fixed_reference':{'prime':p,'b':str(bb),'c':str(cc),'x':str(Q(912)),'y':'0','Z':str(zz)},
 'valid_first_input_shared_reference':{'parameter':str(tt),'u':str(uu),'b1':str(bb1),'c1':str(cc1),'x':str(xx),'y1':str(yy1),'Z1':str(zz1),'g':str(gg),'D':D,'s':str(ss),'k':kk,'b2':str(bb2),'c2':str(cc2),'y2':'-2','Z2':str(zz2),'bad_prime':1133551,'all_sign_guards_nonzero':True},
 'scope':'These are counterexamples to the proposed shared-reference pole systems, not constructed actual detector tuples.'}
path=Path(__file__).with_name('higher_kummer_sharing_certificate.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print('All higher-Kummer sharing identities and counterexamples passed:',path)
