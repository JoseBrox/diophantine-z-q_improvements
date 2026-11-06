#!/usr/bin/env python3
"""Exact finite checks for the numerical inequalities in precision52.tex.

These checks verify only elementary integer identities and inequalities.
They do not certify the external arithmetic inputs of the construction.
"""
from fractions import Fraction
import json


def main():
    checks = {
        'safe_constant_21': 5**6 * 7**13 < 15**13,
        'constant_14_is_too_small': 5**6 > 2**13,
        'new_threshold_implies_old_threshold': 21**13 > 20**4,
        'log2_3_exceeds_three_halves': 3**2 > 2**3,
        'log2_21_below_five': 21 < 2**5,
        'source_log2_H_bound': 4783227 > 0,
    }
    threshold = Fraction(13, 2) * (5 + 4783227)
    anchor_bound = 1 + Fraction(3, 2) * (2**25 - 1)
    checks['threshold_exponent_exact'] = threshold == 31091008
    checks['anchor_exponent_exact'] = anchor_bound == Fraction(100663295, 2)
    checks['new_anchor_exceeds_threshold'] = anchor_bound > threshold
    weights = {m: [10*m-5, 10*m-8, 2*m-1] for m in (1,16,52)}
    checks['weights_exact'] = weights == {
        1: [5,2,1], 16: [155,152,31], 52: [515,512,103]}
    checks['tail_valuation_bound'] = 3*19044 >= 52
    checks['anchor_fourth_power'] = 4*2**26 == 2**28
    if not all(checks.values()):
        raise AssertionError(checks)
    print(json.dumps({
        'status': 'PASS',
        'scope': 'Exact elementary numerical checks only; external arithmetic '
                 'hypotheses are not independently certified.',
        'checks': checks,
        'finite_anchor_exponent': int(threshold),
        'semilocal_anchor_log2_lower_bound': str(anchor_bound),
        'detector_weight_exponents': weights,
    }, indent=2))


if __name__ == '__main__':
    main()
