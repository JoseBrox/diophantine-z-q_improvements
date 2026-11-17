#!/usr/bin/env python3
"""Independent exact arithmetic for the uniform complement guard theorem.

Uses only integer polynomial arithmetic and fractions. It imports neither
the producer nor a computer algebra system. Universal inequalities and the
finite-algebra transfer are reviewed in independent_review.md.
"""
from fractions import Fraction
import json
from pathlib import Path


def add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] = result.get(monomial, 0) + coefficient
    return {m: c for m, c in result.items() if c}


def scale(polynomial, coefficient):
    return {m: coefficient*c for m, c in polynomial.items() if coefficient*c}


def multiply(left, right):
    result = {}
    for (a, b), x in left.items():
        for (c, d), y in right.items():
            monomial = (a+c, b+d)
            result[monomial] = result.get(monomial, 0) + x*y
    return {m: c for m, c in result.items() if c}


def power(polynomial, exponent):
    result = {(0, 0): 1}
    for _ in range(exponent):
        result = multiply(result, polynomial)
    return result


def rational(value):
    return {'numerator': value.numerator, 'denominator': value.denominator}


def main():
    # The curve parameters are 3-sqrt(2) and 3+sqrt(2).
    # Both are positive and less than 5, since 0<sqrt(2)<2.
    assert 0 < 2 < 2**2
    one = {(0, 0): 1}
    d = {(1, 0): 1}
    c = {(0, 1): 1}
    complement = add(one, scale(d, -1))
    c_squared = power(c, 2)
    native_at_v_one = add(
        multiply(multiply(d, power(add(d, one), 2)), power(c, 4)),
        scale(multiply(multiply(d, power(add(d, scale(one, -1)), 2)),
                       power(complement, 2)), -1))
    terminal = scale(multiply(d, complement), 2)
    residual = add(native_at_v_one, scale(power(terminal, 2), -1))
    factored = multiply(
        multiply(d, power(add(d, one), 2)),
        multiply(add(c_squared, scale(complement, -1)),
                 add(c_squared, complement)))
    assert residual == factored

    # Reuse the first indeterminate as u.  This reference identity is
    # polynomial, so no evaluation at the excluded normalizer is used.
    normalizer_plus = add(scale(one, 4), scale(d, 7))
    normalizer_minus = add(scale(one, 4), scale(d, -7))
    reference_residual = add(power(normalizer_plus, 2), scale(d, -112),
                             scale(power(normalizer_minus, 2), -1))
    assert reference_residual == {}

    contacts = {
        'seven': (-7, -6, -4, 1, 3, 5, 8),
        'nine': (-10, -8, -5, 1, 2, 3, 4, 6, 7),
    }
    harmonic = {}
    for name, shifts in contacts.items():
        assert len(set(shifts)) == len(shifts)
        assert all(10-shift > 0 for shift in shifts)
        reciprocal_sum = sum((Fraction(1, 10-shift) for shift in shifts),
                             Fraction(0))
        lower = 2*len(shifts)/reciprocal_sum
        assert lower > 10
        harmonic[name] = {
            'shifts': list(shifts),
            'sum_reciprocals': rational(reciprocal_sum),
            'strict_lower_bound_for_u': rational(lower),
        }
    assert harmonic['seven']['strict_lower_bound_for_u'] == rational(Fraction(1199520, 98251))
    assert harmonic['nine']['strict_lower_bound_for_u'] == rational(Fraction(15120, 1093))

    margin = 21*250**12-20*251**12
    assert margin == 1108398992054805009292439980 > 0
    exact_bound = Fraction(70, 121)*Fraction(251, 250)**12
    simple_bound = Fraction(147, 242)
    assert 0 < exact_bound < simple_bound < 1
    aligned_weight_endpoint = Fraction(16*10, (4+7*10)**2)
    assert aligned_weight_endpoint == Fraction(40, 1369)
    aligned_eta_bound = 7*aligned_weight_endpoint*Fraction(251, 250)**12
    assert 0 < aligned_eta_bound < Fraction(294, 1369) < 1

    # The expression bounding eta is decreasing for u>=10: both
    # u/(1+u)^2 and (1+4/u^3)^12 are positive and decreasing there.
    # The integer inequalities above certify its endpoint bound.
    result = {
        'schema': 'uniform-complement-guard-independent/v77',
        'status': 'PASS',
        'producer_imported': False,
        'cas_used': False,
        'native_polynomial_identity_verified': True,
        'polynomial_identity_terms': len(residual),
        'curve_abscissa_lower_bound': '-5',
        'physical_slope_offset': 10,
        'harmonic_bounds': harmonic,
        'eta_exact_upper_bound': rational(exact_bound),
        'eta_simple_strict_upper_bound': rational(simple_bound),
        'positive_integer_margin': margin,
        'aligned_normalizer': {
            'weight': '16*u/(4+7*u)^2',
            'new_guard': '4+7*u != 0',
            'old_guards_retained': True,
            'reference_square_identity_verified': True,
            'reference_identity': '(4+7u)^2-112u=(4-7u)^2',
            'weight_upper_bound_u_ge_10': rational(aligned_weight_endpoint),
            'eta_exact_upper_bound': rational(aligned_eta_bound),
            'eta_simple_strict_upper_bound': rational(Fraction(294, 1369)),
            'reference_comparison_domain': 'u>=10 on the chosen real completeness domain',
            'reference_value_is_actual_witness': False,
            'actual_global_square_realization_proved': False,
        },
        'finite_point_algebra_rank': 64,
        'finite_complement_algebra_rank': 128,
        'sound_source_variables': 9,
        'new_complete_variable_bound_proved': False,
        'global_complement_square_realization_proved': False,
        'scope': ('Exact coefficients and endpoint inequalities. Universal real '
                  'inequalities, local parity, and source transfer require the '
                  'accompanying proof and independent mathematical review.'),
    }
    output = Path(__file__).with_name('independent_certificate.json')
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
