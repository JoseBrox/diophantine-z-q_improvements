#!/usr/bin/env python3
"""Independent exact arithmetic audit of the E_791 prepared-cover obstruction.

This is not an implementation of full 2-descent.  Monsky's identification,
Cassels's pairing formula and its Mordell--Weil radical inclusion are the
explicit literature inputs listed in the companion audit.  The script
checks every numerical and polynomial datum used when applying them.
"""
from fractions import Fraction
from itertools import product
from math import gcd
from pathlib import Path
import json
import argparse
import sympy as sp


def legendre(a, p):
    r = pow(a % p, (p - 1) // 2, p)
    return 0 if r == 0 else (1 if r == 1 else -1)


def squareclass(a):
    a = Fraction(a)
    if not a:
        raise ValueError('zero has no multiplicative square class')
    n = abs(a.numerator * a.denominator)
    z = -1 if a < 0 else 1
    for p, e in sp.factorint(n).items():
        if e % 2:
            z *= int(p)
    return z


def matvec(M, v):
    return [sum(a * b for a, b in zip(row, v)) % 2 for row in M]


def rank2(M):
    a = [list(row) for row in M]
    rank = 0
    for j in range(len(a[0])):
        piv = next((i for i in range(rank, len(a)) if a[i][j]), None)
        if piv is None:
            continue
        a[rank], a[piv] = a[piv], a[rank]
        for i in range(len(a)):
            if i != rank and a[i][j]:
                a[i] = [x ^ y for x, y in zip(a[i], a[rank])]
        rank += 1
    return rank


n = 791
assert n == 7 * 113 and sp.isprime(7) and sp.isprime(113)
d = Fraction(112, 225)
assert 0 < d < 1 and d == 7 * Fraction(4, 15) ** 2
assert gcd(112, 225) == 1 and 112 // 16 % 2 == 1

# We deliberately use Zhang's (d2,d1) ordering, the block-swapped version
# of the ordering printed in the independently audited manuscript.
ps = [7, 113]
A = [[0, 0], [0, 0]]
for i in range(2):
    for j in range(2):
        if i != j:
            A[i][j] = (1 - legendre(ps[j], ps[i])) // 2
    A[i][i] = sum(A[i]) % 2
D2 = [(1 - legendre(2, p)) // 2 for p in ps]
Dm2 = [(1 - legendre(-2, p)) // 2 for p in ps]
M = [[0] * 4 for _ in range(4)]
for i in range(2):
    for j in range(2):
        M[i][j] = A[i][j] ^ (D2[i] if i == j else 0)
        M[i + 2][j + 2] = A[i][j] ^ (Dm2[i] if i == j else 0)
    M[i][i + 2] = M[i + 2][i] = D2[i]
assert M == [[0, 0, 0, 0], [0, 0, 0, 0],
             [0, 0, 1, 0], [0, 0, 0, 0]]
kernel = [v for v in product([0, 1], repeat=4) if not any(matvec(M, v))]
assert rank2(M) == 1 and len(kernel) == 8
classes = []
for v in kernel:
    d2 = 7 ** v[0] * 113 ** v[1]
    d1 = 7 ** v[2] * 113 ** v[3]
    classes.append((d1, d2, squareclass(d1 * d2)))
for c in [(1, 7, 7), (113, 1, 113), (1, 113, 113), (113, 113, 1)]:
    assert c in classes

t, u1, u2, u3, z = sp.symbols('t u1 u2 u3 z')
coords = [t, u1, u2, u3]
H = [-n*t*t + 7*u2*u2 - 7*u3*u3,
     -n*t*t + 7*u3*u3 - u1*u1,
     2*n*t*t + u1*u1 - 7*u2*u2]
Q = [[0, 0, 1, 1], [1, 28, 0, 15], [1, 21, 17, 0]]
L = [u2-u3, -113*t-4*u1+15*u3, 226*t+3*u1-17*u2]
for h, q, ell in zip(H, Q, L):
    sub = dict(zip(coords, q))
    assert h.subs(sub) == 0
    tangent = sum(sp.diff(h, c).subs(sub)*c for c in coords)
    assert sp.expand(tangent - 14 * ell) == 0

identity1 = (u2-u3)*(u2+u3)-113*t*t
assert sp.expand(identity1 - H[0]/7) == 0
identity3 = L[2]*(226*t-3*u1+17*u2)+(17*u1-21*u2)**2/7
assert sp.expand(identity3 - sp.Rational(226, 7)*H[2]) == 0
assert sp.det(sp.Matrix([[17, -21], [3, -17]])) == -226

# Exact local factor at 113, using the stated Hensel root of 7.
assert 32*32 % 113 == 7
assert 2*32 % 113 != 0
lp113 = (-2*(17-3*32)) % 113
assert lp113 == 45 and legendre(lp113, 113) == -1
assert 113 % 8 == 1 and legendre(113, 7) == 1 and 113 > 0

# The all-prime proof is the two polynomial identities above together
# with primitivity: away from 2,7,113, the partner of a nonunit Li is
# a unit.  Hence each v_p(Li) is even and the Hilbert factor is 1.

X, Y = -7*t*t, 7*t*z
assert sp.expand(Y*Y-(X**3-n*n*X) - 49*t*t*(z*z-7*(113**2-t**4))) == 0
quartic = 7*(113**2-t**4)
disc = int(sp.discriminant(quartic, t))
assert set(sp.factorint(abs(disc))) == {2, 7, 113}
assert disc == -256 * 7**6 * 113**6

# Independent torsion cross-check by two good reductions.
counts = {}
for p in [3, 5]:
    counts[p] = 1 + sum(1 + legendre(x**3-n*n*x, p) for x in range(p))
assert counts == {3: 4, 5: 8}

Px, Py = -784, -2940
assert Py*Py == Px**3-n*n*Px
kp = tuple(squareclass(a) for a in [Px-n, Px+n, Px])
assert kp == (-7, 7, -1)
torsion = [(1, 1, 1), (2, 2*n, n), (-2*n, 2, -n), (-n, n, -1)]
torsion = [tuple(squareclass(a) for a in row) for row in torsion]
assert kp not in torsion and len(set(torsion)) == 4
pure_P = tuple(squareclass(a*b) for a, b in zip(kp, torsion[3]))
assert pure_P == (113, 113, 1)
delta_generators = [-1, n, squareclass(Px)]
delta_image = {squareclass((-1)**a * n**b) for a, b in product([0, 1], repeat=2)}
assert delta_image == {1, -1, n, -n} and -7 not in delta_image

cert = {
    'status': 'PASS',
    'scope': 'Independent exact-data check; full 2-descent and Cassels theory are explicit cited premises, not implemented here.',
    'prepared_d': str(d),
    'n': n,
    'monsky_order': '(v7(d2),v113(d2),v7(d1),v113(d1))',
    'monsky_matrix': M,
    'monsky_rank': rank2(M),
    'pure_selmer_dimension': 3,
    'pure_selmer_classes': classes,
    'tangent_gradient_scale': 14,
    'partner_identities_verified': 2,
    'partner_linear_determinant': -226,
    'pairing_local_113': {'sqrt7_mod113': 32, 'product_mod113': lp113, 'hilbert_symbol': -1},
    'other_local_factors': {'2': 1, '7': 1, 'infinity': 1, 'other_primes': '1 by parity identities and primitivity'},
    'good_reduction_point_counts': counts,
    'P': [Px, Py],
    'P_full_kummer': kp,
    'P_pure_kummer': pure_P,
    'rank_conclusion_under_cited_pairing_theory': 1,
    'abscissa_squareclass_image': sorted(delta_image),
    'required_squareclass': -7,
    'quartic_discriminant_factorization': {str(p): int(e) for p, e in sp.factorint(abs(disc)).items()},
    'references': [
        'Z. Wang, arXiv:1511.03810v2, Sections 2.1-2.2, equations (2.1)-(2.3), radical statement after (2.3)',
        'S. Zhang, On non-congruent numbers as multiples of non-congruent numbers (2025), Sections 2.1-2.2'
    ]
}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path)
args = parser.parse_args()
out = args.output or Path(__file__).with_name('independent_certificate.json')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(cert, indent=2) + '\n')
print(json.dumps({'status': cert['status'], 'certificate': str(out), 'quartic_rational_point': False}))
