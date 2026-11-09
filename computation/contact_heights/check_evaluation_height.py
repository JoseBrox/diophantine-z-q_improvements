#!/usr/bin/env python3
"""Exact constants and identities for the differential-evaluation height bound.

The geometric evaluation theorem is proved in the accompanying paper.
This script verifies the rational elliptic-family identities and all
finite numerical comparisons used to make its five-contact consequence
explicit. It does not replace the geometric or modular input proofs.
"""
from argparse import ArgumentParser
from fractions import Fraction
from hashlib import sha256
from math import factorial, isqrt, prod
from pathlib import Path
import json


def primes_up_to(n):
    marked = bytearray(b'\x01') * (n+1)
    marked[:2] = b'\x00\x00'
    for p in range(2, isqrt(n)+1):
        if marked[p]:
            marked[p*p:n+1:p] = b'\x00' * ((n-p*p)//p+1)
    result = [p for p in range(2, n+1) if marked[p]]
    trial = [m for m in range(2, n+1)
             if all(m % q for q in range(2, isqrt(m)+1))]
    assert result == trial
    return result


def poly_add(a, b):
    c = [0] * max(len(a), len(b))
    for i, x in enumerate(a):
        c[i] += x
    for i, x in enumerate(b):
        c[i] += x
    while len(c) > 1 and c[-1] == 0:
        c.pop()
    return tuple(c)


def poly_mul(a, b):
    c = [0] * (len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return poly_add(c, ())


def poly_scale(a, c):
    return poly_add(tuple(c*x for x in a), ())


def exp_partial(x, order):
    x = Fraction(x)
    return sum((x**j/factorial(j) for j in range(order+1)), Fraction())


def rational_record(x):
    return {'numerator': x.numerator, 'denominator': x.denominator}


def digest_integer(n):
    return sha256(n.to_bytes((n.bit_length()+7)//8, 'big')).hexdigest()


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).with_name('evaluation-height-certificate.json'))
    args = parser.parse_args()

    # E_t: y^2=x^3+a*x+b, with a=-3t/(t-1), b=-2t/(t-1).
    t, denominator, a_num, b_num = (0, 1), (-1, 1), (0, -3), (0, -2)
    a_cubed = poly_mul(poly_mul(a_num, a_num), a_num)
    b_squared = poly_mul(b_num, b_num)
    cubic_sum_num = poly_add(poly_scale(a_cubed, 4),
                            poly_scale(poly_mul(b_squared, denominator), 27))
    assert cubic_sum_num == (0, 0, -108)
    assert poly_scale(cubic_sum_num, -16) == (0, 0, 1728)
    assert poly_scale(a_cubed, 4) == poly_mul(t, cubic_sum_num)

    primes = primes_up_to(76176)
    base = prod(primes)
    d0 = 4608 * 210**300
    assert d0*d0 < base and 144 < base
    assert d0 < 1 << 2413
    assert base < 1 << 109445
    assert 109445 < 1 << 17
    assert base >= 6 and d0 > 912 and d0 > 128
    constant_integer_upper = 19*d0*base**3*109445
    assert constant_integer_upper < 1 << 330770
    assert 5 + 2413 + 3*109445 + 17 == 330770
    assert 330770+1 == 330771 < 330789
    assert Fraction(7, 2)/4 == Fraction(7, 8)

    exp_certificates = []
    for argument, order, target in [(Fraction(8), 24, 2304),
                                    (Fraction(3), 8, 14),
                                    (Fraction(3, 2), 8, 4)]:
        partial = exp_partial(argument, order)
        assert partial > target
        exp_certificates.append({
            'argument': rational_record(argument),
            'series_order': order,
            'target': target,
            'partial_sum': rational_record(partial),
            'strictly_greater': True
        })
    # For exp(1), the tail beginning with 1/9! has all subsequent
    # term ratios at most1/10. Thus this is a rigorous rational upper bound.
    e_upper = exp_partial(Fraction(1), 8) + Fraction(1, factorial(9))/Fraction(9, 10)
    assert 2 < e_upper < 3

    result = {
        'status': 'PASS',
        'scope': 'Exact identities and constants; evaluation, finite-duality, and modular realization statements are proved in the accompanying paper.',
        'elliptic_family': {
            'a': '-3*t/(t-1)', 'b': '-2*t/(t-1)',
            'discriminant': '1728*t^2/(t-1)^3',
            'j_invariant': '1728*t',
            'symbolic_identities': 'PASS'
        },
        'prime_cutoff': 76176,
        'prime_count': len(primes),
        'last_prime': primes[-1],
        'prime_product_bit_length': base.bit_length(),
        'prime_product_sha256_big_endian': digest_integer(base),
        'D0_formula': '4608 * 210^300',
        'D0_bit_length': d0.bit_length(),
        'D0_squared_strictly_less_than_prime_product': True,
        '144_strictly_less_than_prime_product': True,
        'modular_jacobian_bound': 'd_H/2*(log(12)+log(N)+2*log(d_H))+g_H*log(2/sqrt(pi))',
        'vertical_different_bound_for_p_greater_than_3': 'The different contains N in each torsion-point field and every intermediate field.',
        'contact_bound': {
            'exact_constant_formula': '19*D0*B_*^3*log B_*',
            'logarithmic_height_exponent': 3,
            'additional_log_factor_exponent': 1,
            'constant_strict_log2_upper_bound': 330770,
            'integer_constant_upper_bound_bit_length': constant_integer_upper.bit_length(),
            'integer_constant_upper_bound_sha256_big_endian': digest_integer(constant_integer_upper),
            'pure_power_exponent': '7/2',
            'stronger_pure_power_constant_strict_log2_upper_bound': 330771,
            'pure_power_constant_strict_log2_upper_bound': 330789,
            'four_block_exponent': '7/8'
        },
        'exponential_series_certificates': exp_certificates,
        'rational_upper_bound_for_e': rational_record(e_upper)
    }
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({
        'status': result['status'],
        'prime_count': len(primes),
        'prime_product_bits': base.bit_length(),
        'D0_bits': d0.bit_length(),
        'integer_constant_upper_bits': constant_integer_upper.bit_length(),
        'pure_power_exponent': '7/2',
        'pure_power_constant_log2_bound': 330789
    }))


if __name__ == '__main__':
    main()
