#!/usr/bin/env python3
"""Independent integer certificates for two fixed-prime scalar normalizations.

No producer module or computer-algebra package is imported. Trial division,
modular exponentiation, and exact integer inequalities are used throughout.
The infinite valuation cases are proved in the accompanying mathematical note;
this script checks their constants and the boundary cases used in that proof.
"""
from fractions import Fraction
from math import isqrt
from pathlib import Path
import json


def is_prime_by_trial_division(n):
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def residues(beta_constant, beta_coefficient, prime):
    targets = [Fraction(0), Fraction(1), Fraction(2401),
               Fraction(-343, 32), Fraction(1, 2)]
    values = []
    for theta in targets:
        quotient = (theta - beta_constant) / beta_coefficient
        values.append(quotient.numerator * pow(quotient.denominator, -1, prime) % prime)
    return values


def check_29():
    ell, k, m, height_exponent = 76249, 137715, 20, 2093448
    assert is_prime_by_trial_division(ell)
    assert ell > 76176 and ell % 24 == 1 and ell % 17 == 4
    values = residues(450459, 216, ell)
    assert values == [32862, 32509, 24048, 904, 70810]
    tests = [pow(value, (ell - 1) // 4, ell) for value in values]
    assert all(value != 1 for value in tests)
    assert k % 20 == 15
    q = k // 20
    left_minimum = 2 * k + 1 - 20 * q
    right_minimum = 1 - 2 * k + 60 * (q + 1)
    assert left_minimum == right_minimum == k + 16
    forced_depth = (m - 1) * (k + 16) + 1
    assert forced_depth == 2616890
    assert ell > 2 ** 16
    lower_binary_exponent = 16 * forced_depth
    required_binary_exponent = 20 * (height_exponent + 6)
    assert lower_binary_exponent > required_binary_exponent
    assert 102 ** 2 < 17 ** 4
    return {
        'prime': ell,
        'trial_division_bound': isqrt(ell),
        'quartic_nonresidue_arguments': values,
        'quartic_power_tests': tests,
        'normalization_exponent': k,
        'minimum_odd_valuation': k + 16,
        'scalar_test_order': m,
        'forced_index_depth': forced_depth,
        'strict_binary_index_lower_exponent': lower_binary_exponent,
        'required_binary_index_exponent': required_binary_exponent,
        'binary_exponent_margin': lower_binary_exponent - required_binary_exponent,
        'constant_real_bound': '102^2 / 17^4 < 1',
    }


def check_quartic():
    ell, n, height_exponent = 80989, 27464, 2093448
    assert is_prime_by_trial_division(ell)
    assert ell > 76176 and ell % 17 == 1
    values = residues(2504, 51, ell)
    tests = [pow(value, (ell - 1) // 2, ell) for value in values]
    assert all(value == ell - 1 for value in tests)
    minimum_valuation = 2 * n - 1
    forced_depth = 187 * minimum_valuation // 8 + 1
    assert minimum_valuation == 54927 and forced_depth == 1283919
    assert pow(ell, 4096) > 1 << 66787
    required_binary_exponent = 10 * (height_exponent + 7)
    margin = 66787 * forced_depth - 4096 * required_binary_exponent
    assert margin == 1181453 and margin > 0
    return {
        'prime': ell,
        'trial_division_bound': isqrt(ell),
        'quadratic_nonresidue_arguments': values,
        'quadratic_power_tests': tests,
        'normalization_parameter': n,
        'minimum_odd_valuation': minimum_valuation,
        'forced_index_depth': forced_depth,
        'certified_log2_prime_lower_bound': '66787/4096',
        'required_binary_index_exponent': required_binary_exponent,
        'cleared_integer_margin': margin,
        'scope': 'Numerical and scalar-normalization check; full quartic domain review is separate.',
    }


def main():
    result = {
        'arithmetic': 'exact integers and fractions',
        'independent_of_construction_builder': True,
        'coordinate_29': check_29(),
        'quartic': check_quartic(),
        'status': 'all asserted exact checks passed',
    }
    target = Path(__file__).with_name('forced_prime_independent_certificate_20261108_v8.json')
    target.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
