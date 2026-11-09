#!/usr/bin/env python3
"""Exact finite audit accompanying the general Frey-denominator proof."""
from fractions import Fraction
from math import gcd
from pathlib import Path
import json


def v2(n):
    return (n & -n).bit_length()-1


cases = 0
max_cancellation = 0
for exponent in (2, 4, 6, 8, 10, 12):
    for A in range(1, 129):
        for B in range(1, 129):
            if gcd(A, B) != 1:
                continue
            a, b = A**exponent, B**exponent
            # Invariants derived from the Weierstrass coefficients
            # a1=a3=a6=0, a2=b-a, a4=-a*b.
            b2, b4, b6, b8 = 4*(b-a), -2*a*b, 0, -a*a*b*b
            c4 = b2*b2-24*b4
            discriminant = -b2*b2*b8-8*b4**3-27*b6*b6+9*b2*b4*b6
            assert c4 == 16*(a*a+a*b+b*b)
            assert discriminant == 16*a*a*b*b*(a+b)**2
            numerator = 256*(a*a+a*b+b*b)**3
            denominator = a*a*b*b*(a+b)**2
            cancellation = gcd(numerator, denominator)
            assert cancellation == 2**min(8, v2(denominator))
            j = Fraction(c4**3, discriminant)
            assert j == Fraction(numerator, denominator)
            assert j.denominator == denominator//cancellation
            H = max(A, B)
            assert 256*j.denominator >= H**(4*exponent)
            assert max(j.numerator, j.denominator) <= 6912*H**(6*exponent)
            # Integer version of log den(j) >= 2h(j)/3 - constants.
            assert j.denominator**3 * 256**3 * 6912**2 >= \
                   max(j.numerator, j.denominator)**2
            cases += 1
            max_cancellation = max(max_cancellation, cancellation)

report = {
    'status': 'PASS',
    'primitive_positive_pairs_checked_per_exponent_bound': 128,
    'even_exponents': [2, 4, 6, 8, 10, 12],
    'exact_cases': cases,
    'largest_cancellation_observed': max_cancellation,
    'invariants_independently_derived': True,
    'exact_two_adic_cancellation_checked': True,
    'height_majorants_checked_as_integer_inequalities': True,
    'general_statement': 'den(j)>=H^(4d)/256 and h(j)<=6d*log(H)+log(6912)',
    'scope': 'Finite verification complements the all-input elementary proof. No abc hypothesis or elliptic-rank calculation is used.',
}
out = Path(__file__).with_name('frey-denominator-certificate.json')
out.write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
