#!/usr/bin/env python3
"""Exact algebra checks accompanying the manually proved saturation lemma.

No finite sampling is used as a proof of the valuation assertions.
The all-prime case analysis is in saturated_contact_normalization.md.
"""
import json
from pathlib import Path
import sympy as S

t,C=S.symbols('t C')
P=(t-7)*(t-11)
L=S.expand(P+4*t)
g=4*t/P
d=28*t*P/L**2
sigma=(t**2-77)/L
r=P**2*C**4/(t*(1+t**2*P*C**4))
assert S.cancel(7*g/(1+g)**2-d)==0
assert S.cancel(1+d-sigma**2)==0
assert S.expand(L-(t-7)**2)==28
assert S.limit(t*d,t,S.oo)==28
assert S.limit(t*r,t,S.oo)==1
assert r.subs(C,0)==0
# Verify both branches of each valuation simplification symbolically.
n,k,delta=S.symbols('n k delta')
branches=[
 ('positive_odd_t_large_denominator',4*k-n-(2*n+4*k),-3*n),
 ('positive_odd_t_unit_denominator',4*k-n,4*k-n),
 ('negative_odd_t_large_denominator',4*n+4*k-n-(4*n+4*k),-n),
 ('negative_odd_t_unit_denominator',4*n+4*k-n,4*(n+k)-n),
 ('positive_odd_P_large_denominator',2*delta+4*k-(delta+4*k),delta),
 ('positive_odd_P_unit_denominator',2*delta+4*k,delta+(delta+4*k)),
]
for _,lhs,rhs in branches:assert S.expand(lhs-rhs)==0
result={
 'scalar_identity':'(t^2-77)^2 - (t^2-14t+77)^2 = 28t(t-7)(t-11)',
 'L_positive_identity':'L=(t-7)^2+28',
 'limits':{'t*d':28,'t*r_C':'1 for fixed nonzero C','r_0':0},
 'valuation_branch_identities':[name for name,_,_ in branches],
 'scope':'Exact rational identities and branch-formula algebra only. The universal valuation, trace, source extraction and ordered completeness arguments are proved in the accompanying note. No smaller variable count.',
 'status':'PASS'
}
path=Path(__file__).with_suffix('.json')
if '--write' in __import__('sys').argv:path.write_text(json.dumps(result,indent=2)+'\n')
else:assert json.loads(path.read_text())==result
print('PASS: exact saturated-contact identities; see note for the universal valuation proof')
