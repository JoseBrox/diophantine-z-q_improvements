#!/usr/bin/env python3
"""Finite exact checks for the scoped input-only weight counterexample.

The global existence assertion is proved in the manuscript, not by this
finite computation. Only the standard library is used.
"""
from argparse import ArgumentParser
from fractions import Fraction as Q
from math import comb, gcd, isqrt
from pathlib import Path
import hashlib
import json


def mul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return c


def ev(a, x):
    r = 0
    for c in reversed(a):
        r = r * x + c
    return r


def vp_int(a, p):
    assert a != 0
    a = abs(a)
    v = 0
    while a % p == 0:
        a //= p
        v += 1
    return v


def vp(x, p):
    x = Q(x)
    return vp_int(x.numerator, p) - vp_int(x.denominator, p)


def mod_q(x, modulus):
    x = Q(x)
    assert gcd(x.denominator, modulus) == 1
    return x.numerator * pow(x.denominator, -1, modulus) % modulus


def crt(residues, moduli):
    x, modulus = 0, 1
    for r, n in zip(residues, moduli):
        x += modulus * ((r - x) * pow(modulus, -1, n) % n)
        modulus *= n
        x %= modulus
    return x


def primes_to(n):
    return [p for p in range(2, n + 1)
            if all(p % a for a in range(2, isqrt(p) + 1))]


def logarithm_coefficients(d, maximum_r):
    return [(4 * r + 1,
             Q((-1) ** r * comb(2 * r, r) * d ** (2 * r), 4 * r + 1))
            for r in range(maximum_r + 1)]


def formal_value(coefficients, z, degree_bound=None):
    return sum((c * z ** j for j, c in coefficients
                if degree_bound is None or j <= degree_bound), Q(0))


parser = ArgumentParser()
parser.add_argument('--output', type=Path)
args = parser.parse_args()
base = Path(__file__).resolve().parent

F = [1]
for a in (1, 3, 5, 9):
    F = mul(F, [-a * a, 0, 56 * 56])
assert len(F) == 9 and F[-1] == 56 ** 8
assert all(F[i] == 0 for i in (1, 3, 5, 7))
assert F[0] == (1 * 3 * 5 * 9) ** 2
for x in range(-12, 13):
    direct = 1
    for a in (1, 3, 5, 9):
        direct *= (56 * x) ** 2 - a * a
    assert ev(F, x) == direct
    if x:
        assert 16 * direct > 50

fixed_residue_cases = 0
for x in range(56):
    f = ev(F, x)
    assert f % 8 == 1
    assert f % 7 != 0 and (16 * f) % 7 in {1, 2, 4}
    assert (1 + 16 * f) % 7 != 0
    fixed_residue_cases += 1

denominator_cases = 0
for p in primes_to(211):
    if p in (2, 7):
        continue
    x = Q(2) + Q(1, p)
    u = 16 * ev(F, x)
    assert vp(u, p) == -8
    assert vp(u, 2) == 4 and mod_q(u / 16, 8) == 1
    assert vp(u, 7) == 0 and mod_q(u, 7) in {1, 2, 4}
    assert u > 50
    denominator_cases += 1

progression_cases = 0
for q in (11, 17, 19):
    for a in range(4):
        for b in range(4):
            for c in range(2):
                common = 2 ** a * 7 ** b * q ** c * 5
                for initial_depth in range(1, 9):
                    delta = initial_depth % 2
                    r = crt([1, 1, q ** delta], [8, 7, q ** (delta + 1)])
                    assert r > 0 and vp_int(r, q) == delta
                    h = common * common * r
                    assert vp_int(h, 2) % 2 == 0
                    assert (h // 2 ** vp_int(h, 2)) % 8 == 1
                    assert vp_int(h, 7) % 2 == 0
                    assert (h // 7 ** vp_int(h, 7)) % 7 in {1, 2, 4}
                    assert (initial_depth + vp_int(r, q)) % 2 == 0
                    progression_cases += 1

fixed_depth_cases = 0
for T in range(1, 33):
    k = 8 * T - 7
    assert k > 0 and k % 2 == 1 and 8 * T - k == 7
    for e_P in (4, 5, 8):
        for v_h in range(0, 22, 2):
            margin = 8 * T * (e_P + v_h) - k * (4 + v_h)
            assert margin >= 28 + 7 * v_h > 0
            assert k * (4 + v_h) % 2 == 0
            assert 2 + k * (4 + v_h) >= 6
            if v_h > 2:
                assert 8 * T * (e_P + v_h) - k * (v_h - 2) > 0
            fixed_depth_cases += 1

negative_odd_cases = 0
for nu in range(-51, 0, 2):
    for val_c in range(-24, 25):
        val_D = max(2 * val_c, -nu)
        assert 2 * val_D - nu >= -3 * nu > 0
        assert -nu > 0
        negative_odd_cases += 1

# Direct finite formal logarithm/truncation calculations, independent of
# the abstract composition proof. z_H=p^e and d=5 are local fixtures;
# they are not asserted to be global rational elliptic points.
local_maps = 0
local_residues = 0
local_distance_checks = 0
d = 5
N = 3
coefficients = logarithm_coefficients(d, N + 2)
for p in (2, 3, 5, 7):
    e = 2 if p == 2 else 1
    modulus = p ** N
    scale = p ** e
    # All omitted logarithm terms have valuation >=e+N.
    for r in range(N + 3, 64):
        j = 4 * r + 1
        assert j * e - vp_int(j, p) >= e + N
    L = [mod_q(formal_value(coefficients, scale * u) / scale, modulus)
         for u in range(modulus)]
    assert sorted(L) == list(range(modulus))
    inverse_L = {v: i for i, v in enumerate(L)}
    assert gcd(L[1], p) == 1
    for T in (1, 4, 5, 9, 13):
        lam = [mod_q(formal_value(coefficients, scale * u, T) / scale,
                     modulus) for u in range(modulus)]
        assert sorted(lam) == list(range(modulus))
        inv_lam_H = pow(lam[1], -1, modulus)
        phi = [lam[inverse_L[m * L[1] % modulus]] * inv_lam_H % modulus
               for m in range(modulus)]
        assert sorted(phi) == list(range(modulus))
        for m in range(modulus):
            for valuation in range(N):
                next_m = (m + p ** valuation) % modulus
                diff = (phi[next_m] - phi[m]) % modulus
                assert diff and vp_int(diff, p) == valuation
                local_distance_checks += 1
        local_maps += 1
        local_residues += modulus

source = Path(__file__).resolve().parents[3] / 'negative_results/papers/pole_parameters/input_only_weight_false_witnesses_20261117_v61.tex'
certificate = {
    'status': 'PASS',
    'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest()
        if source.exists() else None,
    'F_coefficients_ascending': F,
    'fixed_residue_cases': fixed_residue_cases,
    'rational_denominator_cases': denominator_cases,
    'compatible_index_progression_cases': progression_cases,
    'fixed_depth_inequality_cases': fixed_depth_cases,
    'negative_odd_weight_cases': negative_odd_cases,
    'finite_local_index_bijections': local_maps,
    'local_residues_checked': local_residues,
    'local_isometry_checks': local_distance_checks,
    'global_rational_witnesses_computed': False,
    'global_claim_depends_on_manuscript_proof_and_intrinsic_theorem': True,
    'scope': 'the stated amplified index block plus the explicit input-only weight',
    'all_two_point_sources_excluded': False,
    'new_defining_variable_bound_claimed': False,
}
destination = args.output or base / 'certificate.json'
destination.write_text(json.dumps(certificate, indent=2) + '\n')
print(json.dumps(certificate, indent=2))
