#!/usr/bin/env python3
"""Exact coefficient data supporting the multiplication-surface proof.

This checks the six contact values, their simple orders, both weight
normalizations and the multiplier identities.  The geometric divisor
argument and Riemann--Hurwitz deduction are proved in the manuscript;
this script does not claim to replace that proof by finite testing.
"""
from pathlib import Path
import json
import sympy as s

t,V,w,q=s.symbols('t V w q')
F=t*(t+1)*(2*t+1)*(3*t+1)*(4*t+1)*(5*t+2)/120
roots=[s.Rational(0),s.Rational(-1),s.Rational(-1,2),
       s.Rational(-1,3),s.Rational(-1,4),s.Rational(-2,5)]
assert s.degree(F,t)==6
assert len(set(roots))==6 and 1 not in roots
assert s.gcd(s.Poly(F,t),s.Poly(s.diff(F,t),t)).degree()==0
assert F.subs(t,1)==7
w0=F/(4*(t-1)**8)
w1=4*w0/(1-w0)**2
contact=[]
for theta in roots:
    assert F.subs(t,theta)==0 and s.diff(F,t).subs(t,theta)!=0
    r0=s.cancel(w0/F).subs(t,theta)
    r1=s.cancel(w1/F).subs(t,theta)
    assert r0!=0 and r1!=0
    assert r0==1/(4*(theta-1)**8)
    assert r1==1/(theta-1)**8
    contact.append({'theta':str(theta),'F_derivative':str(s.diff(F,t).subs(t,theta)),
                    'original_weight_over_F':str(r0),
                    'normalized_weight_over_F':str(r1)})

C=V*V+w*(2-V)
assert s.expand(C-2*w)==V*V-V*w
adaptive=s.expand((q*q-2*q-1)**2+4*q*(q*q-1)*V)
assert s.Poly(adaptive,q).degree()==4 and s.Poly(adaptive,q).LC()==1
assert adaptive.subs({q:2,V:0})==1
assert s.expand(adaptive.subs(V,1)-(q*q+1)**2)==0
assert s.expand(adaptive.subs(V,2)-(q*q+2*q-1)**2)==0
multipliers=[1+24*V,1+3*(V-1)**2,V+2,1+w*(2-V)]
origin_values=[p.subs({V:0,w:0})for p in multipliers]
assert origin_values==[1,4,2,1]

report={'status':'PASS','scope':'exact coefficient data; geometry is proved in the manuscript',
        'F_degree':6,'F_separable':True,'F_at_one':'7',
        'contact_data':contact,
        'adaptive_class_coefficients_descending_in_q':[str(a)for a in s.Poly(adaptive,q).all_coeffs()],
        'regular_multiplier_origin_values':[str(a)for a in origin_values],
        'generic_elliptic_fiber_ramification_budget':{'six_even_fibers_at_least':'3m',
                                                    'total_by_Riemann_Hurwitz':'2m'},
        'individual_rational_witness_nonexistence_claimed':False}
out=Path(__file__).with_name('actual_multiplication_surface_certificate.json')
out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','simple_contacts':len(contact)}))
