#!/usr/bin/env python3
"""Exact algebra and coefficient checks for the v56 checkpoint.

This does not prove the external simultaneous-twist theorem or the open
single-cover rational realization property.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import sympy as S

b, u, s, A, B, w = S.symbols("b u s A B w")
a = 7 * b
E = (a-u**2)/(a+u**2)
p = 2*a*u/(a+u**2)
H = 1-b/7
P = 343*b*(7*b+u**2)**2*s**4 - 7*b*(7*b-u**2)**2*(b-7)**2
assert S.factor(p**2-a*(1-E**2)) == 0
assert S.factor(P-(7*(a+u**2))**2*a*(s**4-E**2*H**2)) == 0
poly = S.Poly(P, b, u, s)

# Native single-cover radical and reciprocal-trace representative.
g = 1+w
N = A**2-2*B**2
D = g**2*N-2*g*A+1
V = 2*A/N
J = 1/N
native = (1-V/g+J/g**2)*(1+(1-V/2)/w)
reciprocal_trace = w*(g*N-A)/D
assert S.factor(native-reciprocal_trace*(D/(w*g*N))**2) == 0

rows = []
for k,e,d in [(F(25,24),8,6),(F(16,15),10,6),(F(121,100),16,12)]:
    epsilon = d-k*(F(d,2)+2)
    C = k*(F(3*d,2)+1)/epsilon+2
    alpha = F(e)/k-3
    gamma = 8/k-6
    q = C/(alpha*gamma)
    assert min(epsilon,alpha,gamma)>0 and q<2
    rows.append(dict(kappa=str(k),e=e,d=d,epsilon=str(epsilon),
                     C=str(C),alpha_gamma=str(alpha*gamma),q=str(q),ed=e*d))

certificate = dict(
    prepared_pole=dict(total_degree=int(poly.total_degree()),
                       monomials=len(poly.terms()),
                       coefficient_height=int(max(abs(c) for c in poly.coeffs())),
                       terms=[dict(exponents=list(m),coefficient=int(c))
                              for m,c in poly.terms()]),
    identities_checked=["first conic", "cleared second curve",
                        "native radical divided by reciprocal trace is a square"],
    optimized_height_rows=rows,
    scope="Exact algebra only; no actual single-cover realization is asserted."
)
target = Path(__file__).with_name("exact_certificate.json")
target.write_text(json.dumps(certificate,indent=2)+"\n")
print(json.dumps({"checks":"passed","certificate":str(target),
                  "degree":certificate["prepared_pole"]["total_degree"],
                  "monomials":certificate["prepared_pole"]["monomials"],
                  "height":certificate["prepared_pole"]["coefficient_height"]}))
