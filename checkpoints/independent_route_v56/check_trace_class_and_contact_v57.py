#!/usr/bin/env python3
"""Exact identities and the explicitly scoped small-coefficient census."""
import itertools
import json
from pathlib import Path
import sympy as s

V, w, t = s.symbols('V w t')
D = V**2 + t*(V-1)*(V-2)
assert s.expand(s.discriminant(D, V)-t*(t-8)) == 0
assert [s.expand(D.subs(V,x)) for x in (0,1,2)] == [2*t,1,4]
assert s.expand(D.subs(t,1)) == 2*V**2-3*V+2

def positive_on_closed_interval(a,b,c):
    values = [s.Rational(c), s.Rational(4*a+2*b+c)]
    if a > 0:
        vertex = -s.Rational(b,2*a)
        if 0 <= vertex <= 2:
            values.append(a*vertex**2+b*vertex+c)
    return min(values)>0

def nonzero_integer_square(n):
    return n>0 and s.integer_nthroot(n,2)[1]

small = []
for a,b,c in itertools.product(range(-2,3), repeat=3):
    if c==0 or not positive_on_closed_interval(a,b,c):
        continue
    if not all(nonzero_integer_square(a*x*x+b*x+c) for x in (1,2)):
        continue
    small.append((a,b,c))
assert small == [(0,0,1),(1,2,1)], small

C = V**2+w*(2-V)
Q = s.expand(D.subs(t,1)*C)
assert s.expand(Q.subs(V,2)-16)==0
result={
  'safe_quadratic':'2*V^2-3*V+2',
  'discriminant':'t*(t-8)',
  'height_at_t_1':3,
  'height_at_most_two_census':small,
  'elliptic_quartic':str(Q),
  'reference_point':[2,4],
  'fresh_trace_residue':1,
  'fresh_trace_proof':'good-reduction formal-group contradiction, in manuscript',
  'actual_simultaneous_realization':'unproved',
  'new_defining_variable_bound':False,
}
dest=Path(__file__).with_name('trace_class_and_contact_v57_certificate.json')
dest.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
