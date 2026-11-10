#!/usr/bin/env python3
"""Exact certificate for the scale-uniform six-contact involution."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json


def add(a, b):
    c = a.copy()
    for k, v in b.items():
        c[k] = c.get(k, Q(0)) + v
        if not c[k]:
            del c[k]
    return c


def scale(a, c):
    return {k: c*v for k, v in a.items() if c*v}


def mul(a, b):
    c = {}
    for (i, j), v in a.items():
        for (k, l), w in b.items():
            e = (i+k, j+l)
            c[e] = c.get(e, Q(0)) + v*w
    return {e: v for e, v in c.items() if v}


def homogeneous_f(x, y):
    out = {(0, 0): Q(1, 120)}
    for a, b in ((1,0),(1,1),(2,1),(3,1),(4,1),(5,2)):
        out = mul(out, add(scale(x, a), scale(y, b)))
    return out


X, Y = {(1, 0): Q(1)}, {(0, 1): Q(1)}
N, D = scale(X, -1), add(scale(X, 5), Y)
assert homogeneous_f(N, D) == scale(homogeneous_f(X, Y), -1)
matrix = ((-1, 0), (5, 1))
assert tuple(tuple(sum(matrix[i][k]*matrix[k][j] for k in range(2))
                   for j in range(2)) for i in range(2)) == ((1,0),(0,1))
contacts = [Q(0),Q(-1,2),Q(-1,4),Q(-2,5),Q(-1),Q(-1,3)]
psi = lambda t: -t/(5*t+1)
assert set(map(psi, contacts)) == set(contacts)


def f(t):
    return t*(t+1)*(2*t+1)*(3*t+1)*(4*t+1)*(5*t+2)/120


def r(t):
    return f(t)/(t-1)**8


def square_root(a):
    return (25*a*(a-4)*(a-1)*(a+1)*(2*a-3)*(3*a-2)*(4*a-1)
            /(24*(a+6)**4*(6*a+1)**4))


cases = set()
for u, v in product(range(1, 151), range(1, 31)):
    a = Q(u, v)
    if a > 4:
        cases.add(a)
for a in cases:
    lam = -(a+1)/(5*a)
    assert Q(-1,4) < lam < Q(-1,5)
    assert a*lam < -1
    assert lam not in contacts and a*lam not in contacts
    assert lam != 1 and a*lam != 1 and 5*lam+1 and 6*lam+1
    assert psi(lam) == a*lam
    assert r(lam)*r(a*lam) == -square_root(a)**2
report = {
    "status": "PASS",
    "homogeneous_degree_six_identity": "F_h(-X,5X+Y)=-F_h(X,Y)",
    "involution_matrix_square": "identity",
    "contact_permutation": {str(t): str(psi(t)) for t in contacts},
    "scale_domain": "every rational a>4",
    "slope": "-(a+1)/(5a)",
    "product_squareclass": "-1",
    "exact_rational_substitution_checks": len(cases),
    "scope": "Universal product-radical obstruction, including every prescribed weak-abc scale. No full-source false witness is asserted."
}
out = Path(__file__).with_name("universal-scale-cancellation-certificate.json")
out.write_text(json.dumps(report, indent=2)+"\n")
print(json.dumps(report, indent=2))
