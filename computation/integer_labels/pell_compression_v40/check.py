#!/usr/bin/env python3
"""Exact finite checks for integral Lucas labels and local approximants.

The proof of the unbounded assertions is in the companion manuscript.
This verifier uses only Python's standard library and no imported producer.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from math import isqrt
from pathlib import Path


def add(*polys):
    result = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            result[monomial] = result.get(monomial, 0) + coefficient
    return {m: c for m, c in result.items() if c}


def scale(poly, coefficient):
    return {m: c * coefficient for m, c in poly.items() if c * coefficient}


def mul(left, right):
    result = {}
    for m, a in left.items():
        for n, b in right.items():
            exponent = tuple(x + y for x, y in zip(m, n))
            result[exponent] = result.get(exponent, 0) + a * b
    return {m: c for m, c in result.items() if c}


def square(poly):
    return mul(poly, poly)


def lucas(a, j):
    previous, current = 0, 1
    for _ in range(j):
        previous, current = current, a * current - previous
    return previous


def norm(a, t, w):
    return t * t - a * t * w + w * w


def matrix_mul(left, right, modulus):
    return tuple(
        sum(left[2*i+k] * right[2*k+j] for k in range(2)) % modulus
        for i in range(2) for j in range(2)
    )


def matrix_order(a, modulus):
    matrix = (a % modulus, -1 % modulus, 1 % modulus, 0)
    identity = (1 % modulus, 0, 0, 1 % modulus)
    current = identity
    for order in range(1, modulus**4 + 1):
        current = matrix_mul(current, matrix, modulus)
        if current == identity:
            return order
    raise AssertionError('A matrix in a finite group must have finite order')


def run():
    # Symbolic parametrization, in independent indeterminates (a,s).
    one = {(0, 0): 1}
    a = {(1, 0): 1}
    s = {(0, 1): 1}
    s2 = square(s)
    denominator = add(s2, scale(mul(a, s), -1), one)
    numerator_t = add(s2, scale(one, -1))
    numerator_w = mul(s, add(mul(a, s), scale(one, -2)))
    assert add(square(numerator_t),
               scale(mul(a, mul(numerator_t, numerator_w)), -1),
               square(numerator_w), scale(square(denominator), -1)) == {}

    # Discriminant equation, in indeterminates (a,n,z).
    one3 = {(0, 0, 0): 1}
    av = {(1, 0, 0): 1}
    nv = {(0, 1, 0): 1}
    zv = {(0, 0, 1): 1}
    tv = add(mul(add(av, scale(one3, -2)), nv), one3)
    rhs = add(mul(add(square(av), scale(one3, -4)), square(tv)), scale(one3, 4))
    expected = {
        (4, 2, 0): 1, (3, 2, 0): -4, (1, 2, 0): 16,
        (0, 2, 0): -16, (3, 1, 0): 2, (2, 1, 0): -4,
        (1, 1, 0): -8, (0, 1, 0): 16, (2, 0, 0): 1,
    }
    assert rhs == expected
    polynomial = add(square(zv), scale(rhs, -1))
    assert max(map(sum, polynomial)) == 6
    assert max(map(abs, polynomial.values())) == 16
    assert polynomial[(0, 0, 2)] == 1

    # Clear-denominator local identity at a=5, in the indeterminate s.
    s5 = {(1,): 1}
    one5 = {(0,): 1}
    d5 = add(square(s5), scale(s5, -5), one5)
    left = scale(add(square(s5), scale(one5, -1), scale(d5, -4)), 3)
    right = add(scale(one5, 85), scale(square(add(scale(s5, 3), scale(one5, -10))), -1))
    assert left == right

    positive_witnesses = []
    sharp_witnesses = []
    for avalue in list(range(-30, -2)) + list(range(5, 31)):
        c = abs(avalue - 2)
        t = -lucas(avalue, c - 1)
        w = -lucas(avalue, c - 2)
        assert (t - 1) % (avalue - 2) == 0
        n = (t - 1) // (avalue - 2)
        assert n != 0 and norm(avalue, t, w) == 1
        assert abs(t) == lucas(abs(avalue), c - 1)
        assert abs(t) >= (abs(avalue) - 1)**(c - 2)
        sharp_witnesses.append({'a': avalue, 'n': n, 't': t, 'w': w})
        if avalue > 0:
            t = lucas(avalue, c + 1)
            w = lucas(avalue, c)
            assert (t - 1) % c == 0
            n = (t - 1) // c
            assert n > 0 and norm(avalue, t, w) == 1
            if avalue % 6 == 1:
                assert n % 2 == w % 2 == 1
            positive_witnesses.append({'a': avalue, 'n': n, 't': t, 'w': w})

    # Enumeration uses discriminant squarehood, independently of recurrence.
    rectangle_solutions = []
    a_values = list(range(-20, -2)) + list(range(5, 21))
    for avalue in a_values:
        c = abs(avalue - 2)
        bound = lucas(abs(avalue), c - 1)
        for n in range(-5000, 5001):
            if n == 0:
                continue
            t = (avalue - 2) * n + 1
            disc = (avalue * avalue - 4) * t * t + 4
            z = isqrt(disc)
            if z * z != disc:
                continue
            assert (avalue * t + z) % 2 == 0
            w = (avalue * t + z) // 2
            assert norm(avalue, t, w) == 1
            assert abs(t) >= bound
            if avalue >= 5 and n > 0:
                assert t >= lucas(avalue, c + 1)
            rectangle_solutions.append({'a': avalue, 'n': n, 't': t, 'w': w})

    # Excluded low-parameter cases actually occur.
    excluded = [{'a': 3, 'n': -2, 't': -1, 'w': 0},
                {'a': 4, 'n': -1, 't': -1, 'w': 0}]
    for item in excluded:
        assert item['t'] == (item['a'] - 2) * item['n'] + 1
        assert norm(item['a'], item['t'], item['w']) == 1

    progression_checks = []
    for avalue, modulus in [(5, 2), (7, 6), (8, 5), (13, 6)]:
        c = avalue - 2
        order = matrix_order(avalue, c * modulus)
        period = c * order
        n0 = (lucas(avalue, c + 1) - 1) // c
        w0 = lucas(avalue, c)
        for k in range(3):
            index = c + 1 + k * period
            t = lucas(avalue, index)
            w = lucas(avalue, index - 1)
            assert (t - 1) % c == 0
            n = (t - 1) // c
            assert n > 0 and norm(avalue, t, w) == 1
            assert (n - n0) % modulus == 0
            assert (w - w0) % modulus == 0
        progression_checks.append({'a': avalue, 'modulus': modulus,
                                   'matrix_order': order, 'period': period})

    approximants = []
    q = 3
    modulus = 19
    for r in range(1, 13):
        assert (q * q - 85) % modulus == 0
        svalue = ((10 + q) * pow(3, -1, modulus)) % modulus + modulus
        denominator = svalue * svalue - 5 * svalue + 1
        t = Fraction(svalue * svalue - 1, denominator)
        w = Fraction(svalue * (5 * svalue - 2), denominator)
        n = (t - 1) / 3
        assert norm(5, t, w) == 1
        assert 0 < n < 1
        assert (n - 1).denominator % 19 != 0
        assert (n - 1).numerator % modulus == 0
        approximants.append({'r': r, 's': svalue, 'n': str(n),
                             't': str(t), 'w': str(w)})
        correction = -((q * q - 85) // modulus) * pow(2 * q, -1, 19) % 19
        q += correction * modulus
        modulus *= 19
    assert isqrt(340)**2 != 340

    return {
        'schema': 'pell-label-compression-check/v40',
        'symbolic_identities': ['norm-conic parametrization', 'discriminant expansion',
                                'local congruence identity'],
        'finite_square_polynomial': {'degree': 6, 'coefficient_height': 16,
                                    'integer_content': 1, 'monomials': len(polynomial)},
        'sharp_witnesses': sharp_witnesses,
        'positive_witnesses': positive_witnesses,
        'exhaustive_rectangle': {'a_values': a_values, 'n_min': -5000, 'n_max': 5000,
                                'excluded_n': 0, 'solutions': rectangle_solutions},
        'excluded_low_parameters': excluded,
        'progression_checks': progression_checks,
        'local_approximants': approximants,
        'scope': 'Finite exact checks of formulas and edge cases. Infinite bounds and '
                 'existence are proved in the companion manuscript. No new defining-polynomial '
                 'variable count and no external arithmetic theorem are certified.',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('certificate.json'))
    args = parser.parse_args()
    report = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': 'passed',
                      'rectangle_solution_count': len(report['exhaustive_rectangle']['solutions']),
                      'local_approximation_orders': [1, 12],
                      'certificate_sha256': hashlib.sha256(args.output.read_bytes()).hexdigest()},
                     sort_keys=True))
