#!/usr/bin/env python3
"""Exact algebraic certificates for the unit-trace chamber theorem.

The proof's positivity estimates are in the fixed-trace obstruction manuscript.
This script verifies all polynomial/rational identities used there.
"""
from pathlib import Path
import json
import sympy as s

t,u,z,w=s.symbols('t u z w',positive=True)
F=t*(t+1)*(2*t+1)*(3*t+1)*(4*t+1)*(5*t+2)/120
delta=t-1
weight=F/(4*delta**8)
alpha=delta**4/F
H=120*t**6-211*t**5-745*t**4-610*t**3-205*t**2-28*t-1
assert s.cancel(4*F-delta*s.diff(F,t)+H/60)==0
assert s.cancel(s.diff(weight,t)/weight-(s.diff(F,t)/F-8/delta))==0
assert s.cancel(s.diff(alpha,t)/alpha-(4/delta-s.diff(F,t)/F))==0
shift=s.Poly(H.subs(t,u+s.Rational(19,5)),u)
assert all(c>0 for c in shift.all_coeffs())
w_bound=s.factor(weight.subs(t,s.Rational(19,5)))
assert w_bound==s.Rational(153861525,421654016)
assert w_bound>s.Rational(1,3)
plus=(z+1)/(1+w)
minus=(1/z+1)/(1+w)
S=2+z+1/z
elasticity_bound=(plus-1)*(1+1/z)+(minus-1)*(1+z)
assert s.factor(elasticity_bound-(1-w)*S/(1+w))==0
f,d=s.symbols('f d',positive=True)
bracket=w*(f-8/d)+(1-w)*(4/d-f)
assert s.expand(bracket-((2*w-1)*f+(4-12*w)/d))==0
assert s.expand(((2*w-1)*6+(4-12*w))+2)==0

receipt={
    'status':'PASS_EXACT_ALGEBRAIC_CERTIFICATES',
    'H_shift_coefficients':[str(c) for c in shift.all_coeffs()],
    'w_19_over_5':str(w_bound),
    'w_19_over_5_minus_one_third':str(w_bound-s.Rational(1,3)),
    'scope':'The accompanying proof establishes exactly one real normalized unit-trace solution on t>1 for any fixed nonnegative test arrays. No rational-root or unrestricted nonexistence claim.',
}
import argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path)
out=parser.parse_args().output or Path(__file__).with_name('chamber_certificate.json')
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
