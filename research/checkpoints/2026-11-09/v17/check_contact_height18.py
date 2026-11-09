#!/usr/bin/env python3
"""Exact arithmetic certificate for the five-contact exponent-eighteen bound.

This checks the finite constants. The modular realization, Belyi height
theorem, and isogeny theorem remain mathematical inputs proved or cited
in the accompanying paper.
"""
from argparse import ArgumentParser
from fractions import Fraction
from hashlib import sha256
from math import factorial, isqrt, prod
from pathlib import Path
import json


def primes_up_to(n):
    sieve = bytearray(b'\x01') * (n + 1)
    sieve[:2] = b'\x00\x00'
    for p in range(2, isqrt(n) + 1):
        if sieve[p]:
            sieve[p*p:n+1:p] = b'\x00' * ((n-p*p)//p + 1)
    result = [p for p in range(2, n+1) if sieve[p]]
    # Independent trial division validates every sieve entry, including
    # composite entries, so the entire prime product is determined.
    trial = [m for m in range(2, n+1)
             if all(m % p for p in range(2, isqrt(m)+1))]
    assert result == trial
    return result


def exp_partial(x, order):
    x = Fraction(x)
    return sum((x**j / factorial(j) for j in range(order+1)), Fraction())


def rational_record(x):
    return {'numerator': x.numerator, 'denominator': x.denominator}


def integer_digest(n):
    return sha256(n.to_bytes((n.bit_length()+7)//8, 'big')).hexdigest()


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).with_name('contact-height18-certificate.json'))
    args = parser.parse_args()
    primes = primes_up_to(76176)
    base = prod(primes)
    bound = (1 << 110) * 210**1800 * base**18 + 128
    assert base < 1 << 109445
    assert bound < 1 << 1984521
    assert 111 + 1800*8 + 18*109445 == 1984521
    assert 25 + 14*6 == 109
    assert 300*6 == 1800 and 3*6 == 18
    assert 4608 < 1 << 14 and 13000000 < 1 << 24

    exponential_checks = []
    for x, order, target in [(Fraction(8), 24, 2304),
                              (Fraction(2), 6, 7),
                              (Fraction(17, 24), 8, 2)]:
        partial = exp_partial(x, order)
        assert partial > target
        exponential_checks.append({
            'argument': rational_record(x), 'series_order': order,
            'target': target, 'partial_sum': rational_record(partial),
            'strictly_greater': True})

    v_ratio = (Fraction(4, 16) + Fraction(32, 16**2)
               + Fraction(7, 2*16**3) + Fraction(50, 16**4))
    assert 0 < v_ratio < 1
    result = {
        'status': 'PASS',
        'scope': 'Exact finite constants only; the arithmetic realization and height theorems are separate mathematical inputs.',
        'prime_cutoff': 76176,
        'prime_count': len(primes),
        'last_prime': primes[-1],
        'prime_product_bit_length': base.bit_length(),
        'prime_product_strict_log2_upper_bound': 109445,
        'prime_product_sha256_big_endian': integer_digest(base),
        'height_constant_formula': '2^110 * 210^1800 * B_*^18 + 128',
        'height_constant_bit_length': bound.bit_length(),
        'height_constant_strict_log2_upper_bound': 1984521,
        'height_constant_sha256_big_endian': integer_digest(bound),
        'isogeny_correction_ratio_upper_bound_at_T16': rational_record(v_ratio),
        'exponential_series_certificates': exponential_checks,
        'uniform_height_exponent': 18,
        'amplified_height_exponent': '18/r'
    }
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: result[key] for key in
                     ['status', 'prime_count', 'prime_product_bit_length',
                      'height_constant_bit_length', 'uniform_height_exponent']}))


if __name__ == '__main__':
    main()
