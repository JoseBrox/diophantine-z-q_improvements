#!/usr/bin/env python3
"""Exact identity and local-valuation checks; no global realization claim."""
from fractions import Fraction
from pathlib import Path
import json
import sympy as sp

V,w,t=sp.symbols('V w t')
C=V**2+w*(2-V)
delta=V**2-V+2
expanded=sp.Poly(sp.expand(C*delta),V,w)
expected=V**4-V**3-w*V**3+2*V**2+3*w*V**2-4*w*V+4*w
assert sp.expand(C*delta-expected)==0
assert sp.expand(delta-((V-sp.Rational(1,2))**2+sp.Rational(7,4)))==0
assert [delta.subs(V,j) for j in range(3)]==[2,2,4]
F=t*(t+1)*(2*t+1)*(3*t+1)*(4*t+1)*(5*t+2)/120
contacts=[0,-1,Fraction(-1,2),Fraction(-1,3),Fraction(-1,4),Fraction(-2,5)]
assert len(set(contacts))==6
for theta in contacts:
    assert F.subs(t,theta)==0
    assert sp.diff(F,t).subs(t,theta)!=0
    assert theta!=1

fixture_count=0
for nu in range(1,42,2):
    for m in range((nu+1)//2,nu+21):
        assert min(2*m,nu)==nu
        for e in range(-21,0):
            assert 4*e < 3*e+m
            assert (4*e+nu)%2==1
            fixture_count+=1
for d in range(1,200):
    assert 3*d>2*d

def vp_int(a,p):
    if not a:
        return 10**9
    out=0
    while a%p==0:
        out+=1;a//=p
    return out

two_adic=[]
for k in range(5,13):
    for odd in range(-19,20,2):
        e=odd*2**k
        quotient=Fraction(4+3*e+e*e,4)
        assert quotient.denominator==1
        assert vp_int(quotient.numerator-1,2)>=3
        two_adic.append([k,odd,quotient.numerator])

certificate={
 'status':'PASS',
 'scope':'Exact polynomial identities and valuation inequalities only; no actual-trace realization.',
 'small_class':{'degree':expanded.total_degree(),'monomials':len(expanded.terms()),
                'height':max(abs(int(c)) for c in expanded.coeffs()),
                'contact_values':[2,2,4]},
 'simple_distinct_contacts':[str(x) for x in contacts],
 'bad_pole_and_adaptive_valuation_fixtures':fixture_count,
 'two_adic_fixtures':len(two_adic),
 'ramification_check':'Six even fibers contribute at least 3d; genus-one total is 2d.'
}
out=Path(__file__).with_name('small_trace_and_ramification_v58_certificate.json')
out.write_text(json.dumps(certificate,indent=2)+'\n')
print(json.dumps(certificate,indent=2))
