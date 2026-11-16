#!/usr/bin/env python3
"""Exact checks for the square-complement normalization obstruction.

The infinite-family/local-field proof is in the companion TeX manuscript.
This standard-library program checks identities and exact rational fixtures.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from math import gcd, isqrt
from pathlib import Path


def valuation(x: F, p: int) -> int | None:
    if not x:
        return None
    a, b = abs(x.numerator), x.denominator
    v = 0
    while a % p == 0:
        a //= p
        v += 1
    while b % p == 0:
        b //= p
        v -= 1
    return v


def unit_residue(x: F, p: int, modulus: int) -> int:
    v = valuation(x, p)
    assert v is not None
    u = x / F(p) ** v
    return (u.numerator * pow(u.denominator, -1, modulus)) % modulus


def is_local_square(x: F, p: int) -> bool:
    v = valuation(x, p)
    if v is None:
        return True
    if v % 2:
        return False
    if p == 2:
        return unit_residue(x, 2, 8) == 1
    return pow(unit_residue(x, p, p), (p - 1) // 2, p) == 1


def p_add(a, b):
    c = dict(a)
    for m, v in b.items():
        c[m] = c.get(m, 0) + v
    return {m: v for m, v in c.items() if v}


def p_scale(a, c):
    return {m: v * c for m, v in a.items() if v * c}


def p_mul(a, b):
    c = {}
    for m, u in a.items():
        for n, v in b.items():
            t = tuple(x + y for x, y in zip(m, n))
            c[t] = c.get(t, 0) + u * v
    return {m: v for m, v in c.items() if v}


def run():
    one, x = {(0,): 1}, {(1,): 1}
    plus = p_add(p_scale(one, 17), x)
    minus = p_add(p_scale(one, 17), p_scale(x, -1))
    norm_lhs = p_scale(p_add(p_scale(p_mul(plus, plus), 17),
                             p_scale(x, -1156)), 17)
    norm_rhs = p_scale(p_mul(minus, minus), 289)
    assert norm_lhs == norm_rhs

    # X=tau^2 and D are independent indeterminates.
    X, Dp = {(1, 0): 1}, {(0, 1): 1}
    den, en = p_add(X, p_scale(Dp, 3)), p_add(X, p_scale(Dp, -1))
    factor1 = p_add(den, p_scale(en, -1))
    factor2 = p_add(den, p_scale(en, 3))
    assert factor1 == p_scale(Dp, 4)
    assert factor2 == p_scale(X, 4)
    assert p_mul(Dp, p_mul(factor1, factor2)) == {(1, 2): 16}

    assert all(409 % d for d in range(2, isqrt(409) + 1))
    assert [409 % m for m in (8, 3, 17)] == [1, 1, 1]
    assert 204 == 2**2 * 3 * 17
    assert 408 == 2**3 * 3 * 17
    assert 2448 == 6 * 408 and 409 % 408 == 1
    assert gcd(409, 2448) == 1
    assert 409**3 > 204**2

    D = F(17 * 409)
    tau_values = [F(1), F(2), F(-1), F(1, 409), F(409)]
    fixtures = []
    for n in range(2, 10):
        P = 409 ** (2 * n - 1)
        b = F(204**2, P)
        B = 1156 * b / (17 + b) ** 2
        c = 17 * (17 - b) / (17 + b)
        t, tnew = F(204, 409**n), F(408 * 409**(n - 1), P + 2448)
        assert b == 409 * t**2 and B == 409 * tnew**2
        assert 0 < b < 1 and 0 < B < 17
        assert b.denominator == P
        assert B == F(408**2 * P, (P + 2448)**2)
        assert B.denominator == (P + 2448)**2
        assert c == F(17 * (P - 2448), P + 2448) and c > 0
        assert 17 * (17 - B) == c**2
        vb = [valuation(b, p) for p in (2, 3, 17, 409)]
        vB = [valuation(B, p) for p in (2, 3, 17, 409)]
        assert vb == [4, 2, 2, 1 - 2*n]
        assert vB == [6, 2, 2, 2*n - 1]
        assert all(is_local_square(a, p) for a in (b, B) for p in (2, 3, 17))
        for tau in tau_values:
            den = tau**2 + 3*D
            e = (tau**2 - D) / den
            p = -4*D*tau / den
            assert valuation(e, 409) == 0
            assert p**2 == D*(1-e)*(1+3*e)
            A = e*c**2
            s, q = c, c**2*p
            assert q and s**2 - A and s**2 + 3*A
            assert q**2 == D*(s**2-A)*(s**2+3*A)
        fixtures.append({
            'n': n, 'before_valuations_2_3_17_409': vb,
            'after_valuations_2_3_17_409': vB,
            'reduced_square_denominator': True,
            'nonzero_rational_witnesses_verified': len(tau_values),
        })

    # Exhaustive integer valuation alternatives; symbolic proof is in the note.
    cases = 0
    for n in range(2, 20):
        for r in range(-30, 31):
            w = 1 + 2*min(2*r, 1 - 2*n)
            assert w % 2
            if r <= -n:
                assert w == 1 + 4*r
            else:
                assert r >= 1-n and w == 3 - 4*n
            cases += 1

    # Independent actual-rational check of the local valuation formulas,
    # including the zero conic parameter and zero s.
    local_checks = 0
    for n in (2, 3, 5):
        b = F(204**2, 409**(2*n-1))
        C = 17*(17-b)
        for tau in [F(0)] + [F(409)**r for r in range(-3, 4)]:
            e = (tau*tau-D)/(tau*tau+3*D)
            A = e*C
            assert valuation(e, 409) == 0
            assert valuation(A, 409) == 1-2*n
            for s in [F(0)] + [F(409)**r for r in range(-7, 4)]:
                rad = D*(s*s-A)*(s*s+3*A)
                assert rad and valuation(rad, 409) % 2
                assert not is_local_square(rad, 409)
                local_checks += 1

    n, tau = 2, F(1)
    P = 409**(2*n-1)
    b = F(204**2, P)
    B = 1156*b/(17+b)**2
    c = F(17*(P-2448), P+2448)
    e = (tau*tau-D)/(tau*tau+3*D)
    p = -4*D*tau/(tau*tau+3*D)
    assert e == F(-1738, 5215) and p == F(-6953, 5215)
    return {
        'status': 'PASS',
        'date': '2026-11-16',
        'scope': 'Exact identities and fixtures for an isolated pole-predicate obstruction; universal proof in companion manuscript; no full-source counterexample.',
        'polynomial_identity_checks': ['square complement', 'first-conic factors', 'first-conic ordinate'],
        'family_fixtures': fixtures,
        'integer_valuation_grid_cases': cases,
        'actual_rational_local_checks': local_checks,
        'explicit_first_fixture': {k: str(v) for k, v in {
            'b': b, 'Phi_b': B, 'D': D, 'tau': tau, 'e': e,
            'first_conic_p': p, 'second_s': c, 'second_q': c*c*p,
        }.items()},
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).with_name('verification.json'))
    args = parser.parse_args()
    result = run()
    result['checker_sha256'] = sha256(Path(__file__).read_bytes()).hexdigest()
    root = Path(__file__).resolve().parents[3]
    proof = 'negative_results/papers/pole_parameters/square_complement_normalization_20261116_v43.tex'
    result['proof_note_sha256'] = sha256((root/proof).read_bytes()).hexdigest()
    result['proof_note'] = proof
    sources = ['papers/finite_algebra/unit_norm_20261114_v28.tex',
               'papers/pole_parameters/common_parameter_guard_reduction_20261116_v42.tex',
               'papers/pole_parameters/shared_parameter_local_solubility_20261115_v41.tex']
    result['source_sha256'] = {path: sha256((root/path).read_bytes()).hexdigest() for path in sources}
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'certificate': str(args.output),
                      'family_fixtures': len(result['family_fixtures']),
                      'rational_local_checks': result['actual_rational_local_checks']}))
