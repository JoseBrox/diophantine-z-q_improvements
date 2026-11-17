#!/usr/bin/env python3
"""Independent exact checks for the eleven-coordinate derivative source.

The proof audit is in derivative_source_independent_audit_v59.md.  This
standard-library checker does not import the source author's checker, use
symbolic differentiation, or purport to test abc or prime-pattern existence.
"""
from fractions import Fraction as Q
from functools import reduce
from math import gcd
from pathlib import Path
import hashlib
import json
import argparse

BASE = Path(__file__).resolve().parent
SHIFTS = tuple(range(-8, 0)) + tuple(range(1, 9))

def product(xs):
    return reduce(lambda a, b: a*b, xs, Q(1))

def pp(p, e):
    return Q(p**e) if e >= 0 else Q(1, p**(-e))

def vp(q, p):
    q = Q(q)
    if q == 0:
        return None
    n, d, result = abs(q.numerator), q.denominator, 0
    while n % p == 0:
        n //= p
        result += 1
    while d % p == 0:
        d //= p
        result -= 1
    return result

def detector(u, cs):
    ds = [c*c/(1+u*c*c) for c in cs]
    return product(1+d*d/u for d in ds)

def original_u(a, z):
    """Use F_a/F=sum 2(a+c)/((a+c)^2-z^2), not differentiation."""
    den = sum((2*(a+c)/((a+c)**2-z*z) for c in SHIFTS), Q(0))
    return -32*a/den

def squared_u(a, z):
    """Evaluate G/G_A by its eight quadratic factors in A=a^2."""
    A, Z = a*a, z*z
    factors = [(A+j*j-Z)**2-4*j*j*A for j in range(1, 9)]
    logarithmic_derivative = sum(
        (2*(A-j*j-Z)/factor for j, factor in zip(range(1, 9), factors)), Q(0))
    return -16/logarithmic_derivative

input_cases = 0
for B in (3, 81, 1001, 1000000001):
    for numerator in range(-31, 32):
        for denominator in range(1, 24):
            if gcd(numerator, denominator) != 1:
                continue
            beta_num = numerator*numerator+B*denominator*denominator
            beta_den = denominator*denominator
            assert gcd(beta_num, beta_den) == 1
            assert beta_num >= max(numerator*numerator, denominator*denominator)
            assert beta_num >= B*beta_den
            input_cases += 1

quotient_cases = 0
for M in (Q(3), Q(7, 2), Q(19, 3), Q(81, 7)):
    a = M**3
    for offset in (Q(9), Q(31, 2), Q(109, 3)):
        z = a+offset
        u = original_u(a, z)
        assert u == squared_u(a, z)
        assert u > 0
        quotient_cases += 1

# These tests include numerator and denominator primes of M.  The limit
# u/z^2=1 has sufficient local precision even at the dyadic place.
local_square_cases = 0
for p in (2, 3, 7, 43):
    for vM in (-2, 0, 2):
        a = (3*pp(p, vM))**3
        z = pp(p, -40)
        u = original_u(a, z)
        assert u == squared_u(a, z)
        assert vp(u, p) == -80
        precision = vp(u/(z*z)-1, p)
        assert precision is None or precision >= 10
        w = u/(1+u)**2
        assert vp(w, p) == 80
        local_square_cases += 1

balanced_cases = fresh_trace_cases = negative_trace_cases = 0
for p in (3, 7, 43):
    for nu in (-7, -3, -1, 1, 3, 7):
        u = 2*pp(p, nu)
        for exponent in range(-6, 7):
            c = 2*pp(p, exponent)
            d = c*c/(1+u*c*c)
            assert vp(d, p) == max(2*exponent, -nu)
            if nu > 0:
                assert (vp(d, p) > 0) == (exponent > 0)
            else:
                assert vp(d*d/u, p) >= -3*nu
            balanced_cases += 1
        for exponent in (-6, -1, 0, 1, 6):
            opposite = [pp(p, exponent), Q(0), pp(p, -exponent), Q(1), Q(2), pp(p, 2)]
            if nu > 0:
                successful = [pp(p, nu+1)]*4+[Q(0), pp(p, nu+2)]
                W1, W2 = detector(u, successful), detector(u, opposite)
                V = 1/W1+1/W2
                assert vp(V, p) == 0
                assert vp(4*u/((1+u)**2*V*V), p) == nu
                fresh_trace_cases += 1
            else:
                first = [pp(p, -8), pp(p, 3), Q(0), Q(1), pp(p, -3), pp(p, 1)]
                W1, W2 = detector(u, first), detector(u, opposite)
                assert vp(W1-1, p) >= 1
                assert vp(W2-1, p) >= 1
                V = 1/W1+1/W2
                assert vp(V, p) == 0
                assert vp(4*u/((1+u)**2*V*V), p) == -nu
                negative_trace_cases += 1

# At valuation zero the new denominator 1+u can vanish to any order;
# its contribution is still even, as required by square-denominator
# completeness.  No new congruence is needed at these primes.
unit_denominator_cases = 0
for p in (3, 7, 43):
    for depth in range(1, 9):
        u = Q(p**depth-1)
        assert vp(u, p) == 0
        assert vp(u/(1+u)**2, p) == -2*depth
        unit_denominator_cases += 1

kappa, eps = Q(1001, 1000), Q(1, 100)
alpha = 4/kappa-3
height_denominator = 6-5*kappa
Qheight = (2*kappa-1)/height_denominator
gamma, C = (16-6-3*eps)/2, 4+eps
absorbed = Qheight*(C+1/(2*alpha))
margin = gamma-absorbed
assert (alpha, height_denominator, Qheight) == (Q(997,1001), Q(199,200), Q(1002,995))
assert absorbed == Q(225373347,49600750)
assert margin == Q(87545567,198403000) > 0
assert 4**3*2 == 128 and 1+6+1+2+1 == 11

source = BASE.parents[2]/'papers/conditional_few_variables/derivative_detector11_20261117_v59.tex'
certificate = {
    'status': 'PASS',
    'scope': 'Independent exact algebra/local fixtures and constants; full arithmetic proof is audited separately.',
    'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'uniform_input_height_cases': input_cases,
    'independent_log_derivative_quotient_cases': quotient_cases,
    'local_leading_square_cases': local_square_cases,
    'balanced_valuation_cases': balanced_cases,
    'fresh_positive_odd_trace_cases': fresh_trace_cases,
    'new_negative_odd_trace_cases': negative_trace_cases,
    'valuation_zero_denominator_cases': unit_denominator_cases,
    'height_constants': {'alpha': str(alpha), 'Q': str(Qheight), 'gamma': str(gamma),
                        'C': str(C), 'absorbed': str(absorbed), 'margin': str(margin)},
    'finite_algebra_rank': 128,
    'coordinates': {'input': 1, 'point_coordinates': 6, 'slope': 1,
                    'intrinsic_pole_parameters': 2, 'encoder': 1, 'total': 11},
    'external_theorems_not_computationally_proved': [
        'ordinary rational abc and its homogeneous squarefree-form consequence',
        'elliptic group, formal logarithmic comparison, trace height, and point-chart theorems',
        'Sun simultaneous prime-pattern theorem with compatible reduction orders',
        'intrinsic Burungale realization and parameter density',
        'one-coordinate guarded finite-algebra encoder']
}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,default=BASE/'source_lemmas_certificate.json')
target=parser.parse_args().output
target.write_text(json.dumps(certificate, indent=2)+'\n')
print(json.dumps({'status': 'PASS', 'certificate': str(target),
                  'height_margin': str(margin), 'total_variables': 11}, indent=2))
