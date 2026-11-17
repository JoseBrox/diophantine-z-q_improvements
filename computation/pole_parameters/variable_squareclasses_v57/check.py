#!/usr/bin/env python3
"""Exact height budgets for point-dependent native square classes."""
import argparse
import json
from fractions import Fraction as Q
from pathlib import Path


def constants(kappa, e, d=None):
    alpha, gamma = Q(e)/kappa-3, Q(8)/kappa-6
    if d is None:
        return alpha, gamma
    epsilon = d-kappa*(Q(d, 2)+2)
    if min(alpha, gamma, epsilon) <= 0:
        return None
    height_coefficient = ((4+kappa)*d-6*kappa)/((2-kappa)*d-4*kappa)
    return height_coefficient/(alpha*gamma)


def main(output):
    two, single = [], []
    cases = [(Q(36, 35), 6, Q(251, 250), 14, 8),
             (Q(16, 15), 8, Q(16, 15), 24, 8),
             (Q(121, 100), 14, Q(121, 100), 64, 12)]
    for two_kappa, two_e, kappa, e, d in cases:
        alpha, gamma = constants(two_kappa, two_e)
        contraction = Q(5)/(alpha*gamma)
        assert 0 < contraction < 1
        for lower_e in range(2, two_e, 2):
            lower_alpha, _ = constants(two_kappa, lower_e)
            assert lower_alpha*gamma <= 5
        two.append({'kappa':str(two_kappa), 'e':two_e,
                    'alpha_gamma':str(alpha*gamma),
                    'contraction':str(contraction),
                    'class_degrees':[2, 2]})
        q = constants(kappa, e, d)
        assert q is not None and 0 < Q(5, 2)*q < 1
        budget = e*d
        admissible = []
        # Every positive even pair with a smaller product lies in this box.
        for trial_d in range(2, budget//2+1, 2):
            for trial_e in range(2, budget//trial_d+1, 2):
                trial_q = constants(kappa, trial_e, trial_d)
                if trial_q is not None and Q(5, 2)*trial_q < 1:
                    admissible.append((trial_e*trial_d, trial_e, trial_d))
        assert min(admissible) == (budget, e, d)
        single.append({'kappa':str(kappa), 'e':e, 'd':d,
                       'height_coefficient':str(q),
                       'contraction':str(Q(5, 2)*q),
                       'height_argument_total_degree':2*e*d,
                       'minimum_product_in_stated_even_power_criterion':budget,
                       'class_degree':2})

    for d in range(6, 114, 2):
        for e in range(4, 114//d+1, 2):
            if e*d < 112:
                q = constants(Q(1), e, d)
                assert q is None or Q(5, 2)*q >= 1

    report = {
        'status':'PASS',
        'varying_class':'(X^2+B)^2+Trace(x(A))^2',
        'optional_menu_of_forms':['1', '(X^2+B)^2+Trace(x(A))^2', '1+X^4'],
        'input_class_support_budget':'log r_S(1+X^4) <= 4h(X)+log2 <= 2 h(1:beta:T)+log2',
        'support_budget':'log r_S(delta) <= 2 h(1:beta:T) + log 2',
        'two_cover_rows':two, 'single_cover_rows':single,
        'conditional_retained_coordinates':9,
        'two_cover_finite_rank_per_menu_branch':256,
        'single_cover_finite_rank_per_menu_branch':128,
        'actual_uniform_rational_realization_proved':False,
        'new_nine_variable_defining_bound':False,
        'general_21_variable_transfer_proved':False,
        'ordinary_abc_minimum_two_cover_exponent_in_stated_criterion':6,
        'ordinary_abc_minimum_single_cover_argument_degree_in_stated_criterion':224,
        'scope':'Exact parameter inequalities and finite optimization within the stated height criterion. The universal support and soundness arguments are in the manuscript; no rational realization is certified.'
    }
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    main(parser.parse_args().output)
