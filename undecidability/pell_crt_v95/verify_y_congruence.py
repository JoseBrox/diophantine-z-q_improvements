#!/usr/bin/env python3
"""Independent exact audits of the Y-coordinate Pell congruence and CRT bridge.

The finite ranges below are regression evidence. The quantified lemma follows
from the displayed folding identities and strict bound, as proved in the
accompanying paper; no finite search is presented as its proof.
"""
from __future__ import annotations

from math import gcd
import json

import sympy as sp


def pell(a, n):
    """Return X_n(a),Y_n(a) exactly by binary powering of a+sqrt(a²−1)."""
    assert n >= 0
    d = a*a-1
    x, y = 1, 0
    u, v = a, 1
    while n:
        if n & 1:
            x, y = x*u+d*y*v, x*v+y*u
        u, v = u*u+d*v*v, 2*u*v
        n //= 2
    return x, y


def check():
    xq, yq, xj, yj, a = sp.symbols('xq yq xj yj a')
    x2q, y2q = 2*xq*xq-1, 2*xq*yq
    assert sp.expand(x2q*yj+y2q*xj+yj-2*xq*(xq*yj+yq*xj)) == 0
    assert sp.expand(y2q*xj-x2q*yj-yj-2*xq*(yq*xj-xq*yj)) == 0
    assert sp.expand(x2q*x2q-(a*a-1)*y2q*y2q-1
                     -4*xq*xq*(xq*xq-(a*a-1)*yq*yq-1)) == 0
    c, f, b, j = sp.symbols('c f b j')
    h = c+f*f*(b-c)+c*f*j
    assert sp.expand(h-b-(f*f-1)*(b-c)-c*f*j) == 0
    assert sp.expand(h-c-f*(f*(b-c)+c*j)) == 0

    congruences, signed_identities = 0, 0
    for A in range(2, 11):
        for q in range(2, 15):
            Xq, Yq = pell(A, q)
            assert Yq+pell(A, q-1)[1] < Xq
            for t in range(1, q):
                Yt = pell(A, t)[1]
                for v in range(8*q+1):
                    Yv = pell(A, v)[1]
                    lhs = (Yv-Yt) % Xq == 0 or (Yv+Yt) % Xq == 0
                    rhs = (v-t) % (2*q) == 0 or (v+t) % (2*q) == 0
                    assert lhs == rhs, (A, q, t, v)
                    congruences += 1
            for v in range(1, 2*q+1):
                Xv, Yv = pell(A, v)
                Xm, Ym = pell(-A, v)
                assert Xm == (-1)**v*Xv
                assert Ym == (-1)**(v-1)*Yv
                signed_identities += 2

    # A full second-Pell fixture, with c² dividing Y_q and q a multiple of c.
    # This checks all signs of a,c and both signs of F. It also checks the
    # large-index choice giving positive J for a positive source witness.
    A, B = 2, 3
    C = pell(A, B)[1]
    q = B*C
    F, Yq = pell(A, q)
    assert Yq % (C*C) == 0 and q % C == 0 and q > B
    index_quotient = Yq // (C*C)
    assert F*F-(A*A-1)*index_quotient**2*C**4 == 1
    fixtures = []
    for aa in (A, -A):
        for cc in (C, -C):
            G = aa+F*F*(cc+1-aa)
            assert abs(G) >= 2
            assert (G-1) % C == 0 and (G-aa) % F == 0
            v = B if cc > 0 else B+2*q
            I, H = pell(G, v)
            assert H != 0 and (H-B) % C == 0 and (H-cc) % F == 0
            for ff in (F, -F):
                assert gcd(abs(cc), abs(ff)) == 1
                numerator = H-cc-ff*ff*(B-cc)
                assert numerator % (cc*ff) == 0
                J = numerator // (cc*ff)
                assert H == cc+ff*ff*(B-cc)+cc*ff*J
                assert I*I-(G*G-1)*H*H == 1
                fixtures.append({'a_sign': 1 if aa > 0 else -1,
                                 'c_sign': 1 if cc > 0 else -1,
                                 'F_sign': 1 if ff > 0 else -1,
                                 'index': v})
    aa, cc = A, C
    G = aa+F*F*(cc+1-aa)
    v = B+4*q
    I, H = pell(G, v)
    numerator = H-cc-F*F*(B-cc)
    assert numerator % (cc*F) == 0
    J = numerator // (cc*F)
    assert J > 0 and I > 0 and H > 0
    assert (H-B) % cc == 0 and (H-cc) % F == 0
    assert I*I-(G*G-1)*H*H == 1
    return {
        'status': 'PASS', 'exact_polynomial_identities': 5,
        'finite_congruence_equivalences': congruences,
        'finite_signed_Pell_identities': signed_identities,
        'all_eight_signed_bridge_fixtures': fixtures,
        'positive_J_large_index_fixture': {'A': A, 'B': B, 'C': C,
                                           'q': q, 'v': v, 'J_bits': J.bit_length()},
        'quantified_lemma': 'For A>=2 and 0<t<q, Y_v(A)=±Y_t(A) modulo X_q(A) if and only if v=±t modulo 2q.',
        'proof_mechanism': 'Fold by the two exact identities to ±Y_j with 0<=j<=q. The strict bound Y_q+Y_(q-1)<X_q excludes opposite-sign collisions. Monotonicity gives j=t.',
        'finite_verification_is_not_a_quantified_proof': True}


if __name__ == '__main__':
    print(json.dumps(check(), sort_keys=True, indent=2))
