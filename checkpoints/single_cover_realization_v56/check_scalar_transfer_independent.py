#!/usr/bin/env python3
"""Independent polynomial-gcd audit of the coefficient-seven scalar transfer."""
import json
from pathlib import Path
import sympy as sp
from sympy.polys.domains import ZZ
from sympy.polys.galoistools import gf_gcd, gf_pow_mod, gf_sub

p = 76249
x = sp.symbols('x')
beta = 216*x**4 + 450459
r = sp.Poly(beta*(beta-1)*(beta-2401)*(32*beta+343)*(2*beta-1), x)
rows = []
for name, polynomial in [('contact',r), ('old_denominator',1+17*r),
                         ('new_denominator',1+119*r)]:
    f = [int(c)%p for c in sp.Poly(polynomial,x).all_coeffs()]
    residue = gf_sub(gf_pow_mod([1,0],p,f,p,ZZ),[1,0],p,ZZ)
    gcd = gf_gcd(f,residue,p,ZZ)
    assert gcd == [1]
    rows.append({'polynomial':name, 'degree':len(f)-1,
                 'coefficients_mod_p':f, 'gcd_with_x_to_p_minus_x':[1]})

n = 116576341082536192
D = 5951086353
A = 1296233
Z = 12556178240
assert A == 17*p
b0 = 2*Z*Z-D*D
M = b0*(b0-n)*(b0-2401*n)*(32*b0+343*n)
aligned_r = M % p
aligned_C = (102**2*M)%p
aligned_new_den = (1+7*aligned_C*aligned_r)%p
assert aligned_r != 0 and aligned_new_den == 18888

out = {'status':'PASS', 'prime':p, 'method':'F_p polynomial gcd; no residue enumeration',
       'original_source':rows,
       'aligned_source':{'contact_constant':aligned_r,
                         'C_constant':aligned_C,
                         'new_denominator_constant':aligned_new_den},
       'scope':'All integral input residue classes at the consumed prime; no arithmetic realization claim.'}
Path(__file__).with_name('scalar_transfer_independent_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
