#!/usr/bin/env python3
"""Exact height coefficients and finite algebra census for the single-cover criterion."""
from fractions import Fraction as Q
from pathlib import Path
from math import comb
import argparse
import json
import sympy as S


def row(kappa, e, d, m=1):
    epsilon = d - kappa * Q(d + 4, 2)
    alpha = Q(e) / kappa - 3
    gamma = 8 / kappa - 6
    assert epsilon > 0 and alpha > 0 and gamma > 0
    constant = kappa * Q(3 * d + 2, 2) / epsilon + 2
    closed = ((4 + kappa) * d - 6 * kappa) / ((2 - kappa) * d - 4 * kappa)
    assert constant == closed
    coefficient = constant / (m * alpha * gamma)
    return dict(kappa=str(kappa), e=e, d=d, m=m,
                epsilon=str(epsilon), mixed_height_constant=str(constant),
                alpha=str(alpha), gamma=str(gamma),
                soundness_coefficient=str(coefficient),
                coefficient_below_two=coefficient < 2,
                argument_degree_in_beta_and_trace=e*d*m,
                argument_total_degree_in_retained_coordinates=2*e*d*m)


def certificate():
    A, B, w, k = S.symbols('A B w k')
    N = A*A-2*B*B
    g = 1+w
    Dg = g*g*N-2*g*A+1
    native = (1-2*A/(g*N)+1/(g*g*N))*(1+(1-A/N)/w)
    reciprocal = w*(g*N-A)/Dg
    assert S.cancel(native-reciprocal*(Dg/(w*g*N))**2) == 0
    assert S.cancel(reciprocal.subs({A:1, B:0})-1) == 0
    # Distinct positive menu entries have distinct nonzero roots on R != 0.
    y, R = S.symbols('y R')
    menu_poly = (y*y-R)*(y*y-2*R)
    assert S.discriminant(menu_poly, y) == 32*R**6
    parameters = ((Q(25, 24), 8, 6, Q(10000, 5187)),
                  (Q(16, 15), 10, 6, Q(32, 17)),
                  (Q(121, 100), 16, 12, Q(40453083, 21236816)))
    rows = []
    smaller_degree_checks = 0
    for kappa, e, d, expected in parameters:
        item = row(kappa, e, d)
        assert Q(item['soundness_coefficient']) == expected < 2
        degree = e*d
        # Outer amplification is dominated by e -> em, m -> 1.
        # Therefore the finite comparison below also covers m > 1.
        for ee in range(4, degree//6+1, 2):
            for dd in range(6, degree//ee+1, 2):
                if ee*dd >= degree or Q(ee)/kappa <= 3 or dd-kappa*Q(dd+4, 2) <= 0:
                    continue
                candidate = row(kappa, ee, dd)
                assert Q(candidate['soundness_coefficient']) >= 2
                smaller_degree_checks += 1
        item['minimal_argument_degree_within_stated_height_criterion'] = True
        rows.append(item)
    amplification_checks = 0
    for d in range(2, 18, 2):
        for m in range(1, 9):
            for j in range(d+1):
                assert comb(d, j) <= comb(d*m, j*m)
                amplification_checks += 1
    return {
        'schema': 'diophantine-single-cover-criterion/v56',
        'status': 'PASS',
        'parameter_rows': rows,
        'smaller_argument_degree_cases_checked': smaller_degree_checks,
        'binomial_amplification_coefficient_checks': amplification_checks,
        'point_algebra_rank': 4**3,
        'quadratic_adjunctions': 1,
        'total_finite_algebra_rank': 4**3*2,
        'retained_coordinates': {'input': 1, 'point_coordinates': 6,
                                 'free_parameter': 1, 'encoder': 1},
        'total_coordinates_under_realization': 1+6+1+1,
        'zero_free_parameter_allowed': True,
        'reciprocal_trace_identity': True,
        'reciprocal_reference_value': 1,
        'positive_exceptional_unit_menu_allowed': True,
        'example_squareclass_menu': [1, 2],
        'example_menu_polynomial_discriminant': '32*R^6',
        'example_menu_formal_product_algebra_rank': 64*4,
        'example_menu_compiled_factor_rank': 64*2,
        'menu_encoder': 'finite product of existing quadratic-branch encoders',
        'example_menu_retained_coordinates': 9,
        'uniform_realization_with_menu_proved': False,
        'conditional_soundness_proved': True,
        'actual_uniform_rational_realization_proved': False,
        'nine_variable_defining_bound_proved': False,
        'unconditional_twenty_one_transfer_proved': False,
        'full_determinant_degree_bound_assigned': False,
        'scope': ('Exact arithmetic of the stated height constants, the degree comparison '
                  'inside this mixed-power criterion, and the finite-algebra census. '
                  'The manuscript proves the height and soundness theorems under retained '
                  'hypotheses; no uniform rational realization is certified.')
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = certificate()
    text = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end='')
