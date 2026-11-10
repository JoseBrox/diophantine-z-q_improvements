#!/usr/bin/env python3
"""Exact constants for the effective twenty-seven-variable construction.

The checks use integer and Fraction arithmetic. They certify the finite
exceptional set and strict bounds used by the paper, not the inherited
modular realization, pole realization, or prime-pattern input.
"""
from fractions import Fraction
from itertools import combinations
from math import isqrt, prod
from pathlib import Path
import argparse
import json


def prime_divisors(n):
    n = abs(n)
    assert n > 0
    factors = []
    p = 2
    while p*p <= n:
        if n % p == 0:
            factors.append(p)
            while n % p == 0:
                n //= p
        p = 3 if p == 2 else p+2
    if n > 1:
        factors.append(n)
    return factors


def trial_prime(n):
    return n > 1 and all(n % d for d in range(2, isqrt(n)+1))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).with_name('effective27-constants-certificate.json'))
    args = parser.parse_args()
    q = Fraction
    theta = [q(0), q(-1, 2), q(-1), q(1, 2399), q(-32, 407)]
    blocks = [[q(s)+x for s in (4*j+2, 4*j+4) for x in theta]
              for j in range(3)]
    poles = [q(-1), q(-2), q(-3)]
    values = sum(blocks, [])+poles
    assert len(values) == len(set(values)) == 33
    assert all(x > 0 for x in sum(blocks, []))
    exceptional = set()
    for value in values+[a-b for a, b in combinations(values, 2)]:
        assert value
        for integer in (abs(value.numerator), value.denominator):
            exceptional.update(p for p in prime_divisors(integer) if p > 76176)
    expected = [149027, 272011, 1875611, 3828397, 3982747]
    assert sorted(exceptional) == expected
    assert all(trial_prime(p) for p in expected)
    exceptional_product = prod(expected)
    assert exceptional_product.bit_length() == 100
    assert exceptional_product < 1 << 100
    ell = 76249
    assert trial_prime(ell) and ell not in exceptional
    assert 1 << 16 < ell < 1 << 17
    # The source certificate makes ell a forced scalar prime and excludes
    # ell from the original five-contact radical M_5(beta).
    # The latter is independently checked by fourth-power residue enumeration.
    beta_residues = {(216*pow(x, 4, ell)+450459) % ell for x in range(ell)}
    finite_roots = {0, 1, 2401, (-343*pow(32, -1, ell)) % ell}
    assert beta_residues.isdisjoint(finite_roots)
    # Negative ell-adic beta valuations are multiples of4, so the infinity
    # contact has even valuation as well.
    base_height_bits = 221234
    common_height_bits = 221470
    exponent = q(7, 3)
    # H*E^(7/3) <2^(221467+1/3); adding log35<4 is still <Hbar.
    assert q(base_height_bits)+100*exponent < common_height_bits-1
    assert 35 < 1 << 6
    # Using log35<6 instead of its sharper value still leaves ample margin.
    assert 6 < 1 << (common_height_bits-1)
    # Fixed additive rho-height constant: the logarithm is bounded by
    # bit lengths and log2<1, giving114<128.
    product_height_constant = 2*2402*375*3
    assert product_height_constant == 5404500
    rho_constant_bound = (3*product_height_constant.bit_length()
                          +2*(34).bit_length()+ell.bit_length()
                          +(102**2).bit_length()+2)
    assert rho_constant_bound == 114 and rho_constant_bound < 128
    # The effective sum-height constant is80+log7<82. Certify e^2>7
    # by a finite positive Taylor sum.
    factorial = 1
    taylor2 = q(1)
    for k in range(1, 6):
        factorial *= k
        taylor2 += q(2**k, factorial)
    assert taylor2 > 7
    # Main profile and the explicit odd coefficient parameter.
    local_order = 3
    L = 125001
    forced_exponent = 2*L+1
    assert L >= 3 and L % 2 == 1 and forced_exponent == 250003
    forced_binary_exponent = 16*forced_exponent
    assert forced_binary_exponent == 4000048
    # ell^(2L+1)>120*Hbar follows just from ell>2^16.
    assert forced_binary_exponent > common_height_bits+7
    assert 120 < 1 << 7
    # Tail <=(9/4)c+340 is <(c-1)^2/2 for c>=100.
    # The difference has positive derivative there; its value is checked.
    assert q(99**2, 2) > q(9, 4)*100+340
    assert 100-1 > q(9, 4)
    residual_exponent = exponent/(2*local_order)
    assert residual_exponent == q(7, 18)
    assert 5*residual_exponent == q(35, 18) < 2
    # Delta!=0 implies B <=4^18 *10^7 *Hbar^18 <2^3986520.
    assert 10**7 < 1 << 24
    delta_binary_bound = 36+24+18*common_height_bits
    assert delta_binary_bound == 3986520
    assert forced_binary_exponent > delta_binary_bound+1
    # Input residual: log B <181205+(7/22)h(beta).
    constant = q(9, 11)*(common_height_bits+2+2*residual_exponent)
    assert constant == 181205
    h_beta_coefficient = q(9, 11)*residual_exponent
    assert h_beta_coefficient == q(7, 22)
    # h(beta)<=c/120; c>=10^6 makes this upper bound below c-4.
    c_floor = 10**6
    assert 1 << 20 > c_floor
    assert forced_binary_exponent > 20
    assert constant+h_beta_coefficient*q(c_floor, 120) < c_floor-4
    assert h_beta_coefficient/120 < 1
    # Prime-cluster inequality needed for the all-linear scalar converse.
    # For u>=25, sqrt(u)<=u/5 and1<u/10, so u+1+2sqrt(u)<3u/2.
    assert q(1)+q(1, 10)+q(2, 5) == q(3, 2)
    report = {
        'status': 'PASS',
        'scope': 'Exact finite exceptions, residue checks and sufficient effective threshold. Arithmetic source hypotheses and the finite-algebra compilation are established separately.',
        'contact_blocks': [[str(x) for x in block] for block in blocks],
        'poles': list(map(str, poles)),
        'extra_exceptional_primes': expected,
        'extra_exceptional_product': str(exceptional_product),
        'extra_exceptional_product_bit_length': exceptional_product.bit_length(),
        'forced_prime': ell,
        'forced_prime_outside_exceptional_set': True,
        'forced_prime_excluded_from_five_contact_radical': True,
        'beta_residues_checked': ell,
        'base_height_constant': '2^221234',
        'common_height_constant': '2^221470',
        'base_height_exponent': '7/3',
        'ten_contact_height_exponent': '7/6',
        'comparison_residual_order': local_order,
        'rho_additive_height_constant_upper_bound': 128,
        'effective_sum_additive_constant': 82,
        'effective_common_height_additive_constant': 340,
        'defining_parameter_L': L,
        'forced_index_exponent': forced_exponent,
        'forced_index_binary_lower_exponent': forced_binary_exponent,
        'nonzero_Lucas_residual_binary_upper_exponent': delta_binary_bound,
        'input_log_height_constant_upper_bound': str(constant),
        'input_h_beta_coefficient': str(h_beta_coefficient),
        'counts': {'point_coordinate_pairs': 9, 'comparison_slope': 1,
                   'pole_parameter_pairs': 3, 'input': 1,
                   'retained_coordinates': 26, 'separating_coordinate': 1,
                   'total_coordinates': 27, 'quartic_roots': 9,
                   'quadratic_roots': 3, 'finite_algebra_rank': 2**21},
        'degree_and_coefficients': 'Specified and checked by the source builder; no expanded monomial count is asserted here.'
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: report[key] for key in ('status', 'extra_exceptional_primes',
          'defining_parameter_L', 'forced_index_binary_lower_exponent',
          'nonzero_Lucas_residual_binary_upper_exponent')}))


if __name__ == '__main__':
    main()
