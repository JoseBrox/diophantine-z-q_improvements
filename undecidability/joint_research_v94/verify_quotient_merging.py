#!/usr/bin/env python3
"""Exact algebra and modular checks; no quotient-merging count is asserted."""
import json
from math import gcd
import sympy as sp

U,L=sp.symbols('U L')
d1=2*U*L**2-1
d2=4*(U+1)*L-5
R=8*U**2-9*U+8
assert sp.expand(R-U*d2*(d2+10)+8*(U+1)**2*d1)==0
for modulus in (2,5):
    assert all(not (int(d1.subs({U:u,L:l}))%modulus==0 and
                    int(d2.subs({U:u,L:l}))%modulus==0)
               for u in range(modulus) for l in range(modulus))
samples=0
for u in range(-20,21):
    for l in range(-20,21):
        a=2*u*l*l-1
        b=4*(u+1)*l-5
        g=gcd(a,b)
        assert (8*u*u-9*u+8)%g==0
        assert gcd(g,10)==1
        samples+=1
assert gcd(49,35)==7
print(json.dumps({'status':'PASS','polynomial_gcd_identity':True,
                  'excluded_common_primes':[2,5],
                  'checked_integer_pairs':samples,
                  'new_variable_count_claim':False,
                  'remaining_gaps':['Independent numerator integrality after predicate removal',
                                    'Uniform gcd control',
                                    'Completeness with the forced binomial value of s']},sort_keys=True))
