#!/usr/bin/env python3
"""Exact certificate for the six-contact Möbius obstruction.

The finite checks certify the displayed identities and arithmetic fixtures.
The Chebotarev infinitude argument is proved in the companion manuscript.
No search result is used as evidence for an unproved rational-point theorem.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from functools import reduce
from hashlib import sha256
from itertools import permutations
import json
from math import gcd, isqrt, lcm
from pathlib import Path

import sympy as sp


SOURCE_COMMIT = "9aa0e31ede062c6bfee592e72468444611642ce5"
ROOT = Path(__file__).resolve().parents[3]
PAPER = ROOT / "negative_results/papers/pole_parameters/six_contact_mobius_obstruction_20261117_v62.tex"
t, a, p_sym, q_sym = sp.symbols("t a p q")
F = t * (t + 1) * (2*t + 1) * (3*t + 1) * (4*t + 1) * (5*t + 2) / 120
roots = tuple(map(sp.Rational, [0, -1])) + tuple(
    sp.Rational(n, d) for n, d in [(-1, 2), (-1, 3), (-1, 4), (-2, 5)]
)
MATRICES = [
    (1, 0, 0, 1), (1, 0, -5, -1), (1, 1, 2, -1),
    (4, 1, -7, -1), (2, 1, -3, -2), (3, 1, -7, -2),
    (2, 1, -7, -3), (3, 1, -8, -3), (1, 1, -7, -4),
    (4, 1, -13, -4), (5, 2, -11, -5), (5, 2, -14, -5),
]
MULTIPLIERS = [1, -1, 27, -27, -1, 1, 1, -1, -27, 27, 27, -27]


def norm_matrix(vec):
    denom = lcm(*(int(sp.denom(x)) for x in vec))
    ints = [int(x * denom) for x in vec]
    content = reduce(gcd, (abs(x) for x in ints))
    ints = [x // content for x in ints]
    first = next(x for x in ints if x)
    if first < 0:
        ints = [-x for x in ints]
    return tuple(ints)


def enumerate_mobius():
    found = set()
    tried = 0
    for image in permutations(roots, 3):
        tried += 1
        equations = sp.Matrix([
            [x, 1, -x*y, -y] for x, y in zip(roots[:3], image)
        ])
        basis = equations.nullspace()
        assert len(basis) == 1
        matrix = norm_matrix(basis[0])
        A, B, C, D = matrix
        if A*D - B*C == 0 or any(C*x + D == 0 for x in roots):
            continue
        images = {(A*x+B)/(C*x+D) for x in roots}
        if images == set(roots):
            found.add(matrix)
    assert tried == 120
    assert found == set(MATRICES)
    table = []
    for matrix, kappa in zip(MATRICES, MULTIPLIERS):
        A, B, C, D = matrix
        phi = (A*t + B)/(C*t + D)
        assert sp.cancel(F.subs(t, phi) * (C*t+D)**6 - kappa*F) == 0
        table.append({"matrix": matrix, "multiplier": kappa})
    return {"ordered_image_triples": tried, "automorphisms": table}


def square_gaps():
    rows = []
    for exponent in (4, 6):
        q = 4**exponent
        minimum_p = q*4**exponent + 57**exponent
        assert minimum_p % 2 == 1
        for A, B, C, D in MATRICES[2:]:
            assert B*C*D != 0
            determinant = A*D-B*C
            K = 4*B*C*determinant
            G = (D*p_sym-A*q_sym)**2 + 4*C*B*p_sym*q_sym
            N = D**2*p_sym + (-D*A+2*C*B)*q_sym
            assert sp.expand(D**2*G - N**2 - K*q_sym**2) == 0
            minimum_N = D**2*minimum_p + (-D*A+2*C*B)*q
            gap = 2*minimum_N - 1 - abs(K)*q*q
            assert minimum_N > 0 and K != 0 and gap > 0
            rows.append({
                "exponent": exponent, "matrix": [A, B, C, D],
                "constant_K": K, "denominator": q,
                "minimum_numerator": minimum_p,
                "minimum_N": minimum_N, "strict_square_gap_margin": gap,
            })
    return rows


def is_prime_trial(n):
    assert n > 1
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    return all(n % d for d in range(3, isqrt(n)+1, 2))


def valuation(x, prime):
    x = Fraction(x)
    assert x
    numerator, denominator = abs(x.numerator), x.denominator
    v = 0
    while numerator % prime == 0:
        numerator //= prime
        v += 1
    while denominator % prime == 0:
        denominator //= prime
        v -= 1
    return v


def rational_residue(x, modulus):
    x = Fraction(x)
    return x.numerator * pow(x.denominator, -1, modulus) % modulus


def f_exact(x):
    return x*(x+1)*(2*x+1)*(3*x+1)*(4*x+1)*(5*x+2)/120


def h_exact(x):
    return (x*x-1)*(4*x-1)*(3*x-2)*(2*x-3)*(x-4)


def finite_point_order(prime):
    """Independent integer arithmetic in F_p[s]/(s^2-2)."""
    def add(x, y):
        return ((x[0]+y[0]) % prime, (x[1]+y[1]) % prime)
    def neg(x):
        return (-x[0] % prime, -x[1] % prime)
    def sub(x, y):
        return add(x, neg(y))
    def mul(x, y):
        return ((x[0]*y[0]+2*x[1]*y[1]) % prime,
                (x[0]*y[1]+x[1]*y[0]) % prime)
    def inv(x):
        n = pow((x[0]*x[0]-2*x[1]*x[1]) % prime, -1, prime)
        return (x[0]*n % prime, -x[1]*n % prime)
    def div(x, y):
        return mul(x, inv(y))
    curve_D = (11, -6 % prime)
    point = (mul((57, -28 % prime), (pow(8, -1, prime), 0)),
             mul((-660 % prime, 417), (pow(32, -1, prime), 0)))
    def on_curve(P):
        if P is None:
            return True
        x, y = P
        return mul(y, y) == sub(mul(mul(x, x), x), mul(curve_D, x))
    def ecadd(P, Q):
        if P is None:
            return Q
        if Q is None:
            return P
        x, y = P
        u, v = Q
        if x == u:
            if add(y, v) == (0, 0):
                return None
            slope = div(sub(mul((3, 0), mul(x, x)), curve_D), mul((2, 0), y))
        else:
            slope = div(sub(v, y), sub(u, x))
        z = sub(sub(mul(slope, slope), x), u)
        result = (z, sub(mul(slope, sub(x, z)), y))
        assert on_curve(result)
        return result
    def smul(n, P):
        result = None
        while n:
            if n & 1:
                result = ecadd(result, P)
            P = ecadd(P, P)
            n >>= 1
        return result
    order = 16518755
    factors = [5, 11, 157, 1913]
    assert order == 5*11*157*1913
    assert all(is_prime_trial(q) for q in factors)
    assert on_curve(point) and point is not None
    assert smul(order, point) is None
    witnesses = {q: smul(order//q, point) for q in factors}
    assert all(P is not None for P in witnesses.values())
    return {"point": point, "exact_order": order, "prime_factors": factors,
            "proper_quotient_multiples": witnesses,
            "used_in_proof": "Only the nonidentity reduction is needed; the exact order is supplementary."}


def check_point_and_fixtures():
    s2 = sp.sqrt(2)
    xP = (57-28*s2)/8
    yP = (-660+417*s2)/32
    curve_D = (3-s2)**2
    assert sp.expand(yP*yP-xP**3+curve_D*xP) == 0
    assert sp.expand(xP+xP.subs(s2, -s2)) == sp.Rational(57, 4)
    assert sp.expand(curve_D*curve_D.subs(s2, -s2)) == 49
    H = (a*a-1)*(4*a-1)*(3*a-2)*(2*a-3)*(a-4)
    lam = -(a+1)/(5*a)
    assert sp.cancel(-F.subs(t, lam)-H/(375000*a**6)) == 0
    assert sp.cancel(F.subs(t, a*lam)-H/375000) == 0
    prime = 76253
    assert is_prime_trial(prime)
    assert prime > 76176 and prime % 8 == 5
    assert pow(2, (prime-1)//2, prime) == prime-1
    assert prime*prime == 5814520009
    fixtures = []
    for exponent, shift, root in [(4, 88285, Fraction(4)), (6, 99329, Fraction(2, 3))]:
        scale = Fraction((shift+1)**exponent) + Fraction(57, 4)**exponent
        assert shift % 2 == 1 and shift >= 3
        assert rational_residue(scale-root, prime) == 0
        assert valuation(h_exact(scale), prime) == 1
        lam = -(scale+1)/(5*scale)
        assert valuation(f_exact(lam), prime) == 1
        assert valuation(f_exact(scale*lam), prime) == 1
        for guard in [scale, lam, lam-1, scale*lam-1, 5*lam+1]:
            assert valuation(guard, prime) == 0
        assert valuation(f_exact(lam)/(4*(lam-1)**8), prime) == 1
        modulus = 2*prime**2
        # Polynomial substitution modulo p^2 proves invariance on the entire
        # progression; this additional point is an independently recomputed fixture.
        shifted_scale = Fraction((shift+modulus+1)**exponent) + Fraction(57, 4)**exponent
        assert rational_residue(scale, prime**2) == rational_residue(shifted_scale, prime**2)
        assert valuation(h_exact(shifted_scale), prime) == 1
        hderivative = sp.diff(H, a).subs(a, sp.Rational(root.numerator, root.denominator))
        assert rational_residue(Fraction(hderivative), prime) != 0
        derivative = exponent*pow(shift+1, exponent-1, prime) % prime
        assert derivative != 0
        fixtures.append({
            "exponent": exponent, "shift": shift,
            "scale": str(scale), "contact_root_mod_p": str(root),
            "H_valuation": 1, "first_contact_valuation": 1,
            "second_contact_valuation": 1,
            "H_mod_p_squared": rational_residue(h_exact(scale), prime**2),
            "scale_derivative_mod_p": derivative,
            "progression_modulus": modulus,
        })
    return {
        "prime": prime, "trial_division_limit": isqrt(prime),
        "tested_divisors": [2]+list(range(3, isqrt(prime)+1, 2)),
        "nonzero_division_remainders": [prime % d for d in [2]+list(range(3, isqrt(prime)+1, 2))],
        "Euler_criterion_2": pow(2, (prime-1)//2, prime),
        "curve_norm_D": 49, "trace_x_P": "57/4",
        "point_order_certificate": finite_point_order(prime),
        "fixtures": fixtures,
    }


def eisenstein_data():
    expected = {4: {17: 1, 193: 1, 3217: 1}, 6: {5: 1, 47: 1, 3943: 1, 37013: 1}}
    records = []
    for exponent, eisenstein_prime in [(4, 17), (6, 5)]:
        constant = 57**exponent - 4**(exponent+1)
        factors = {int(k): int(v) for k, v in sp.factorint(constant).items()}
        assert factors == expected[exponent]
        assert all(is_prime_trial(k) for k in factors)
        assert constant % eisenstein_prime == 0 and constant % eisenstein_prime**2 != 0
        euler = pow(2, (eisenstein_prime-1)//2, eisenstein_prime)
        assert euler == (1 if exponent == 4 else eisenstein_prime-1)
        records.append({"exponent": exponent, "constant": constant,
                        "factorization": factors, "Eisenstein_prime": eisenstein_prime,
                        "Euler_criterion_2_at_Eisenstein_prime": euler})
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    certificate = {
        "status": "PASS",
        "source_commit": SOURCE_COMMIT,
        "source_sha256": sha256(PAPER.read_bytes()).hexdigest(),
        "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "mobius_group": enumerate_mobius(),
        "square_gap_rows": square_gaps(),
        "prime_and_fixtures": check_point_and_fixtures(),
        "Chebotarev_field_input": eisenstein_data(),
        "scope": [
            "All twelve rational automorphisms of the six finite contact roots are enumerated.",
            "Ten nontrivial branches have no rational slope at X=1,A=P for every odd shift B>=3.",
            "The involution fails on each displayed unbounded progression of odd shifts.",
            "Infinitely many obstructing primes outside every finite set follow from the manuscript, not a finite search.",
            "No statement about arbitrary rational square rescalings, other contact systems, or a variable lower bound is certified.",
        ],
    }
    text = json.dumps(certificate, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    print("PASS: 12 automorphisms; 20 uniform square gaps; 2 exact inert-prime progressions; 2 Eisenstein field inputs.")


if __name__ == "__main__":
    main()
