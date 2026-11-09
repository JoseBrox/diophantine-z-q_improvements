#!/usr/bin/env python3
"""Exact orbit and polynomial checks for the weighted-contact research note.

This proves finite algebraic identities, not a defining-polynomial theorem.
"""
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
import json


def g(x):
    if x is None:
        return Q(1)
    return None if x == -1 else (x-1)/(x+1)


def phi(x):
    return Q(0) if x is None else 1/(x-2)


def mul(a, b):
    c = [Q(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return c


def add(a, b, c=1):
    out = [Q(0)]*max(len(a), len(b))
    for i, x in enumerate(a):
        out[i] += x
    for i, x in enumerate(b):
        out[i] += c*x
    return out


def factor(n):
    n = abs(n)
    out = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0)+1
            n //= p
        p = 3 if p == 2 else p+2
    if n > 1:
        out[n] = out.get(n, 0)+1
    return out


base = [None, Q(0), Q(1), Q(2401), Q(-343, 32)]
orbits = []
for seed in base:
    orbit = []
    x = seed
    for _ in range(4):
        orbit.append(x)
        x = g(x)
    assert x == seed and len(set(orbit)) == 4
    assert Q(2) not in orbit
    orbits.append(orbit)
blocks = [[phi(orbits[i][j]) for i in range(5)] for j in range(4)]
weighted = Counter(theta for block in blocks for theta in block)
assert len(weighted) == 12
assert Counter(weighted.values()) == {3: 4, 1: 8}
assert sum(weighted.values()) == 20
assert blocks[0] == [Q(0), Q(-1,2), Q(-1), Q(1,2399), Q(-32,407)]

# A(2u+1,u) and J(2u+1,u), with A=zw(z^2-w^2),
# J=z^4-6z^2w^2+w^4.  J/A is invariant under g.
A = [Q(0), Q(1), Q(6), Q(11), Q(6)]
J = [Q(1), Q(8), Q(18), Q(8), Q(-7)]
assert A == mul(mul([0,1], [1,1]), mul([1,2], [1,3]))
z, w = [Q(1),Q(2)], [Q(0),Q(1)]
z2, w2 = mul(z,z), mul(w,w)
assert J == add(add(mul(z2,z2), mul(z2,w2), -6), mul(w2,w2))
invariants = [(c**4-6*c*c+1)/(c**3-c) for c in base[-2:]]
form = mul(mul(mul(A,A),A), mul(add(J,A,-invariants[0]), add(J,A,-invariants[1])))
direct = [Q(1)]
for theta, multiplicity in weighted.items():
    for _ in range(multiplicity):
        direct = mul(direct, [-theta,1])
assert len(form) == 21 and form[-1] != 0
assert [x/form[-1] for x in form] == direct

# q_j=g^{-j}(2+1/u), so u contacts are the corresponding blocks.
matrices = [((2,1),(1,0)), ((3,1),(-1,-1)), ((-1,0),(2,1)), ((1,1),(3,1))]
inverse_row_bounds = []
for matrix in matrices:
    (a,b),(c,d) = matrix
    assert abs(a*d-b*c) in (1,2)
    inverse_row_bounds.append(max(abs(d)+abs(b), abs(c)+abs(a)))
assert inverse_row_bounds == [3,4,3,4]

# A finite bad-prime set sufficient for the affine contact comparisons.
bad = {2}
roots = sorted(weighted)
for t in roots:
    bad.update(factor(t.denominator))
for i, a in enumerate(roots):
    for b in roots[i+1:]:
        bad.update(factor((a-b).numerator))
extra = sorted(p for p in bad if p > 76176)

out = {
    'status': 'PASS',
    'scope': 'Weighted height amplification and finite polynomial identities only. No improved defining polynomial or variable count is claimed.',
    'mobius_map': '(z-1)/(z+1)',
    'affine_coordinate': 'u=1/(z-2)',
    'blocks': [[str(t) for t in block] for block in blocks],
    'weighted_contacts': [{'contact':str(t),'multiplicity':weighted[t]} for t in roots],
    'distinct_contacts': 12,
    'weighted_degree': 20,
    'orbit_invariants': [str(x) for x in invariants],
    'A_coefficients_low_to_high': [str(x) for x in A],
    'J_coefficients_low_to_high': [str(x) for x in J],
    'weighted_form_identity': 'A^3*(J-s*A)*(J-t*A), normalized to be monic',
    'inverse_height_row_bounds': inverse_row_bounds,
    'extra_exceptional_primes_above_76176': extra,
    'height_bound': 'h(u)<=log(4)+H*E^19*M_weighted(u)^(19/4)',
    'existing_source_obstructions': [
        'At multiplicity3 with nu=3, G2 alternate precision is only24; weighted high order8 gives B^(19/8), insufficient for the Lucas contradiction.',
        'Completeness would require alternate depth>=2 together with the existing primary depth>=2, imposing incompatible h=1 and h=0 modulo the same contact prime.'
    ],
}
path = Path(__file__).with_name('weighted_contact_orbits_certificate.json')
path.write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps({'status':'PASS','distinct_contacts':12,'weighted_degree':20,
                  'extra_exceptional_primes':extra,'certificate':str(path)}))
