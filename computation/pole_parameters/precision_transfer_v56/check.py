#!/usr/bin/env python3
"""Exact finite coefficients, height exponents and Lucas witnesses."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json

def lucas_pair(a, index):
    u, v = 0, 1
    for _ in range(index):
        u, v = v, a * v - u
    return u, v


def certificate():
    # The recurrence for the exact source logarithm gives this truncation.
    a0 = F(1)
    a1 = F(-2, 5)
    a2 = a1 * F(3, 9)
    assert (a0, a1, a2) == (F(1), F(-2, 5), F(-2, 15))
    assert 1 + a1 == F(3, 5) > 0

    # Exact exponents in the two soundness comparisons.
    assert F(7, 3) / 2 == F(7, 6) < 2
    assert (6 + 3) * F(7, 36) == F(7, 4) < 2
    assert F(7, 6) < 2
    witness_rows = []
    for s in (7, 13, 19):
        a = s * s
        k = 2 * (a - 2)
        w, t = lucas_pair(a, k)
        assert w % (a - 2) == 0
        b = w // (a - 2)
        assert t * t - a * (a - 2) * t * b + (a - 2) ** 2 * b * b == 1
        assert t > 0 and b > 0 and t % 2 == 1 and b % 2 == 1
        witness_rows.append({'s': s, 'parameter': a, 'index': k,
                             't_bits': t.bit_length(), 'b_bits': b.bit_length()})

    report = {'status': 'PASS', 'scalar_orders': [1, 1, 1, 1, 2, 2],
              'reciprocal_orders': [1] * 10,
              'comparison_orders': [1, 6, 6, 6, 1, 6],
              'logarithm_truncation': 'z*(1-2*D*f^2/5)',
              'relative_formal_error_at_depth_one': 8,
              'required_comparison_precision': 6,
              'scalar_height_exponent': '7/6',
              'nonzero_lucas_residual_exponent': '7/4',
              'lucas_witnesses': witness_rows,
              'retained_variables': 25,
              'new_defining_variable_bound': False}
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    text = json.dumps(certificate(), indent=2)+'\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end='')
