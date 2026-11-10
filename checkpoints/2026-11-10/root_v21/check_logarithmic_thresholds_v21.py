#!/usr/bin/env python3
"""Exact numerical thresholds from the quadratic logarithmic height estimate.

The checker certifies finite inequalities, not the retained modular,
elliptic, pole-realization or prime-pattern assumptions. The analytic
inequalities and their use in soundness are proved in the companion papers.
"""
from fractions import Fraction as Q
from hashlib import sha256
from math import factorial
from pathlib import Path
import argparse
import json


def exp_lower(x, n):
    return sum((x**j / factorial(j) for j in range(n+1)), Q(0))


def integer_record(n):
    raw = n.to_bytes((n.bit_length()+7)//8, 'big')
    return {'binary_digits': n.bit_length(), 'sha256_big_endian': sha256(raw).hexdigest()}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path,
                    default=Path(__file__).with_name('logarithmic-thresholds-v21-certificate.json'))
    args = ap.parse_args()

    # Strict, rational certificates for every logarithm bound used below.
    assert exp_lower(Q(7, 10), 5) > 2
    assert exp_lower(Q(2), 5) > 7
    assert exp_lower(Q(4), 6) > 35
    assert exp_lower(Q(3), 4) > 14
    assert 2029147 < 2**21
    assert 221231+2*21 == 221273
    assert 221231+2*100 == 221431
    # Adding the height-change constants is absorbed in the next power of2.
    assert 2 < 22**2
    assert 4 < 101**2

    tq = 331969
    q_left = 2**(2*tq-3*221274)*15**6
    q_right = 13**3*(345+7*tq)**6
    assert q_left > q_right
    assert 5**3*14 < 13**3
    nq = 9682
    lq = (19*(2*nq-1))//8+1
    cq = 149**lq
    assert lq == 45988
    assert cq-1 >= 2**tq
    assert cq > 40*2**221234
    assert cq > 4640000
    assert 5290 < 2**13
    assert 23*221287 < 22*232000
    assert Q(12, 11) < 2
    quartic_height = 149**(4*nq+2)+1
    assert quartic_height.bit_length() == 279599
    assert 4*nq+2 == 38730 and 2*nq+1 == 19365

    tf = 664417
    f_left = 2**(tf-3*221432)*12**6
    f_right = 9**3*(1224+7*tf)**6
    assert f_left > f_right
    assert 4**3*10 < 9**3
    lf = 20483
    cf = 76249**(2*lf+1)
    assert lf >= 3 and lf % 2 == 1
    assert cf-1 >= 2**tf
    assert cf > 120*2**221470
    assert cf > 10**6
    assert 102**2 < 2**14
    assert 102*221449 < 101*224000
    assert Q(103, 101) < 2
    assert Q(31, 60)*10**6 + 224000 < 10**6-4
    # The same scalar tail absorption as the complete source proof.
    assert Q(99**2, 2) > Q(9, 4)*100+340
    assert 99 > Q(9, 4)

    report = {
        'status': 'PASS',
        'scope': 'Exact rational and integer numerical inequalities; the logarithmic contact-height and defining-projection proofs are separate.',
        'base_contact_height_constant_log2_strict_upper_bound': 221231,
        'log2_strict_rational_upper_bound': '7/10',
        'log2_bound_exponential_taylor_sum': str(exp_lower(Q(7, 10), 5)),
        'quartic': {
            'contact_constant_power_of_two': 221274,
            'contact_logarithmic_shift': 22,
            'index_upper_bound_binary_exponent_if_Lucas_residual_nonzero': tq,
            'index_threshold_integer_left': str(q_left),
            'index_threshold_integer_right': str(q_right),
            'sufficient_N': nq, 'forced_index_depth': lq,
            'forced_index_minimum': integer_record(cq),
            'parameter': '149^19365', 'coefficient_height': '149^38730+1',
            'coefficient_height_record': integer_record(quartic_height),
            'input_logarithmic_constant_upper_bound': 232000,
        },
        'few_variables': {
            'contact_constant_power_of_two': 221432,
            'contact_logarithmic_shift': 101,
            'index_upper_bound_binary_exponent_if_Lucas_residual_nonzero': tf,
            'index_threshold_integer_left': str(f_left),
            'index_threshold_integer_right': str(f_right),
            'sufficient_odd_L': lf, 'forced_index_depth': 2*lf+1,
            'forced_index_minimum': integer_record(cf),
            'input_logarithmic_constant_upper_bound': 224000,
        },
        'minimality_claimed': False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'quartic_N': nq,
                     'quartic_coefficient_binary_digits': quartic_height.bit_length(),
                     'few_variable_L': lf}, indent=2))


if __name__ == '__main__':
    main()
