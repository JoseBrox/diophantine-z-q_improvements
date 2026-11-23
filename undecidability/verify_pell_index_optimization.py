#!/usr/bin/env python3
"""Exact identities and finite illustrations for the new Pell optimization.

The general theorems are proved in papers/pell_index_optimization.tex.
Finite residue checks are explicitly illustrative; the algebraic identities
are checked symbolically. The negative-n source obstruction is checked too.
"""
from pathlib import Path
import argparse
import itertools
import json
import sympy as sp

BASE = Path(__file__).resolve().parent


def pell(a, n):
    D = a*a-1
    answer, base = (1, 0), (a, 1)
    while n:
        if n & 1:
            x, y = answer
            u, v = base
            answer = (x*u+D*y*v, x*v+y*u)
        x, y = base
        base = (x*x+D*y*y, 2*x*y)
        n //= 2
    return answer


def symbolic_identities():
    a, X, Y, c, F, i, p, k, r, s, w, n = sp.symbols("a X Y c F i p k r s w n")
    D = a*a-1
    odd_square = (a-1)*(X+(a+1)*Y)**2-(a+2*a*D*Y*Y+2*D*X*Y-1)
    assert sp.rem(sp.Poly(odd_square, X), sp.Poly(X*X-D*Y*Y-1, X)).as_expr() == 0
    oldR = X-(a-2)*Y
    newR = (a*X+D*Y)-(a-2)*(X+a*Y)
    assert sp.expand(newR-2*oldR-(4*a-5)*Y) == 0
    newG = a+(1+D*i*i*c**4)*(c+1-a)
    assert sp.expand(newG-1-c-D*i*i*c**4*(c+1-a)) == 0
    assert sp.expand((p*p*k*k-k*k+1)-(p*k-1)**2-k*(2*p-k)) == 0
    assert sp.expand((p*k)**2-(p*p*k*k-k*k+1)-(k*k-1)) == 0
    assert sp.expand(8*r*r-5*r-3-(r-1)*(8*r+3)) == 0
    p0 = 2*w*s*s*r*r*n*n
    a0 = (w*n*n+1)*r*s*n*n
    gap = 2*r*s*n*n*(w*n*n*(2*w*s**3*r**3-1)-1)
    assert sp.expand(p0*p0-2*a0-gap) == 0
    return {"odd_index_square_identity": "PASS", "power_two_congruence_recurrence": "PASS",
            "new_bridge_residue_identity": "PASS", "positivity_bound_identities": "PASS",
            "coordinate_savings": {"old_d_square_register": 1, "I_positive_wrapper": 3,
                                   "phi_positive_wrapper": 3, "gamma_wrapper_to_one_square": 2},
            "total_coordinate_saving": 9, "total_equation_saving": 3}


def pell_examples():
    trace_cases = 0
    for a in range(2, 9):
        for q in range(2, 21):
            F = pell(a, q)[0]
            for p in range(1, q):
                d = pell(a, p)[0]
                residues = [t for t in range(4*q) if (pell(a, t)[0]-d) % F == 0]
                assert residues == [p, 4*q-p]
                signed = [t for t in range(4*q)
                          if (pell(a, t)[0]-d) % F == 0 or (pell(a, t)[0]+d) % F == 0]
                assert signed == sorted({p, 4*q-p, 2*q-p, 2*q+p})
                trace_cases += 1
    positive = []
    for a, B, general in ((2, 3, False), (3, 3, False), (2, 5, False),
                           (2, 2, True), (3, 4, True)):
        d, c = pell(a, B)
        q = (2 if general else 1)*B*c
        F, E = pell(a, q)
        divisor = (2 if general else 1)*c*c
        assert E % divisor == 0
        i = E//divisor
        assert i > 0 and F*F == (a*a-1)*E*E+1
        choices = {"general": a+F*F*(2*c+1-a)} if general else {
            "old": a+F*F*(d*d-a), "new": a+F*F*(c+1-a)}
        for name, G in choices.items():
            I, H = pell(G, B)
            H_divisor = (2 if general else 1)*c
            assert (H-B) % H_divisor == 0 and (I-d) % F == 0
            j, o = (H-B)//H_divisor, (I-d)//F
            assert j > 0 and o > 0
            assert (d+o*F)**2 == (G*G-1)*(B+H_divisor*j)**2+1
            positive.append({"a": a, "index": B, "c": c, "Pell_q": q, "bridge": name,
                             "largest_witness_bit_length": max(v.bit_length() for v in (F, i, j, o))})
    signed_cases = 0
    a, B = 2, 3
    d0, C = pell(a, B)
    q = B*C
    F0, E = pell(a, q)
    for sign_c, sign_d, sign_F, sign_H in itertools.product((-1, 1), repeat=4):
        c, d, F = sign_c*C, sign_d*d0, sign_F*F0
        G = a+F*F*(c+1-a)
        t = B if sign_H == 1 else 4*q-B
        xt, yt = pell(G, t)
        I, H = sign_d*xt, sign_H*yt
        assert (I-d) % F == 0 and (H-B) % c == 0
        o, j = (I-d)//F, (H-B)//c
        assert I == d+o*F and H == B+j*c
        assert I*I == (G*G-1)*H*H+1
        assert abs(c) == C and abs(d) == d0
        signed_cases += 1
    for a in range(2, 9):
        for r in range(21):
            d, c = pell(a, 2*r+1)
            plus = pell(a, r+1)[1]+pell(a, r)[1]
            assert d-1 == (a-1)*plus*plus
            zeta = (a-1)*plus
            assert zeta*zeta == (a-1)*(d-1)
    return {"trace_residue_parameter_cases": trace_cases, "positive_witness_examples": positive,
            "signed_witness_examples": signed_cases,
            "scope": "Exact finite illustrations; the general proofs are in the manuscript."}


def negative_source_identity():
    Z, sourceY, mu, n = sp.symbols("Z sourceY mu n")
    b, f, g, l, x, w, y = map(sp.Integer, (1, 0, 0, 0, 0, 2, 0))
    X, h, k = 2*Z, 2*Z, Z
    U, V = 2*l*X*sourceY, 4*g*w*sourceY
    A, B1 = U*(V+1), 2*X+1
    C = sp.expand(B1+(A-2)*h)
    D = sp.expand((A*A-4)*C*C+4)
    E = C*C*D*x
    F = sp.expand(4*(A*A-4)*E*E+1)
    G = sp.expand(1+C*D*F-2*(A+2)*(A-2)**2*E*E)
    H = C+B1*F+(2*y-1)*C*F
    I = sp.expand((G*G-1)*H*H+1)
    J = sp.expand(X+1+k*(U*U*V-2))
    A1, A2, A3 = b, sp.expand(D*F*I), sp.expand((U**4*V*V-4)*J*J+4)
    S = 2*A-5
    T = sp.expand(3*b*w*C-2*(b*b*w*w-1))
    R = sp.expand(f*f*l*l*x*x*(8*mu**3*g*J*J-g*g*(32*(C-l*J*sourceY)**2*mu**3+g*g*J*J)))
    assert (A1, A2, A3, S, T, R) == (1, 0, 0, -5, 0, 0)
    Z0 = 1+A1*A1+A2*A2+A3*A3
    Q = sp.prod(S*S*n+T*T-S*S*(2*R-1)*(T*T+Z0**3+e1)
                for e1, e2, e3 in itertools.product((-1, 1), repeat=3))
    assert sp.expand(Q-25**8*(n+9)**4*(n+7)**4) == 0
    N1, T1, S0 = sp.symbols("N1 T1 S0")
    codingX = (2*N1-1)*((S0+2*T1+2)*2*N1+2*T1+2)
    assert all(int(coefficient) % 2 == 0 for coefficient in sp.Poly(codingX, N1, T1, S0).coeffs())
    return {"status": "PASS", "universal_negative_integer_witnesses": [-7, -9],
            "specialized_source_polynomial": "25^8*(n+9)^4*(n+7)^4",
            "coding_X_even_identity": "PASS",
            "scope": "An exact obstruction for every supplied source polynomial P; this is not a counterexample to the correctly restricted BDHMS theorem."}


def verify():
    return {"status": "PASS", "symbolic_identities": symbolic_identities(),
            "pell_examples": pell_examples(), "negative_source_obstruction": negative_source_identity(),
            "source_universality_claim": "Not established. The older n^2 versus modern n^6 comparison remains explicitly unresolved."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = verify()
    output = json.dumps(result, indent=2)+"\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output)
    print(output, end="")
