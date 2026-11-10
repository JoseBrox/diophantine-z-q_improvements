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
    # Logarithmic amplification retains the quadratic contact exponent.
    logarithmic_height_bits = 221432
    logarithmic_shift = 101
    assert 221231+2*100 < logarithmic_height_bits
    assert 4 < logarithmic_shift**2
    # exp(7/10)>2 certifies log(2)<7/10 without floating arithmetic.
    taylor07 = sum((q(7, 10)**k/q(prod(range(1, k+1))) for k in range(6)), q(0))
    assert taylor07 > 2
    local_order = 3
    L = 20483
    forced_exponent = 2*L+1
    forced_minimum = ell**forced_exponent
    forced_binary_exponent = forced_minimum.bit_length()-1
    assert L % 2 == 1 and forced_exponent == 40967
    assert forced_binary_exponent == 664420
    assert forced_minimum > 1 << forced_binary_exponent
    assert forced_minimum > 120*(1 << common_height_bits)
    # Scalar tail absorption is unchanged.
    assert q(99**2, 2) > q(9, 4)*100+340
    assert 100-1 > q(9, 4)
    # Delta!=0 implies B^(1/3)<9K(102+5log(B)/6)^2.
    assert 4**3*10 < 9**3
    delta_binary_bound = 664417
    assert (1 << (delta_binary_bound-3*logarithmic_height_bits))*12**6 > 9**3*(1224+7*delta_binary_bound)**6
    assert forced_minimum-1 >= 1 << delta_binary_bound
    # Keep c separate in |N*c|<=2exp(h(beta))*B*c.
    input_order = 1
    constant = 224000
    assert 102**2 < 1 << 14
    assert 102*(logarithmic_height_bits+3+14) < 101*constant
    assert q(103, 101) < 2
    h_beta_coefficient = q(2)
    taylor4 = sum((q(4**k, prod(range(1, k+1))) for k in range(4)), q(0))
    assert taylor4 > 16
    assert q(1, 4)-q(1, 16) > 0
    linear_coefficient = h_beta_coefficient*(q(1, 120)+q(1, 4))
    assert linear_coefficient == q(31, 60) < 1
    c_floor = 10**6
    assert forced_minimum > c_floor
    assert constant+linear_coefficient*c_floor < c_floor-4
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
        'ten_contact_height_exponent': '1 with a quadratic logarithmic factor',
        'ten_contact_logarithmic_constant': '2^221432',
        'ten_contact_logarithmic_shift': 101,
        'comparison_Lucas_residual_order': local_order,
        'comparison_input_residual_order': input_order,
        'comparison_orders': [1]*11+[3]*3+[1,3],
        'scalar_orders': [1]*4+[3]*2,
        'rho_additive_height_constant_upper_bound': 128,
        'effective_sum_additive_constant': 82,
        'effective_common_height_additive_constant': 340,
        'defining_parameter_L': L,
        'forced_index_exponent': forced_exponent,
        'forced_index_binary_lower_exponent': forced_binary_exponent,
        'nonzero_Lucas_residual_binary_upper_exponent': delta_binary_bound,
        'input_log_height_constant_upper_bound': str(constant),
        'input_h_beta_and_log_c_coefficient': str(h_beta_coefficient),
        'input_linear_c_coefficient': str(linear_coefficient),
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
