#!/usr/bin/env python3
"""Exact constants and pole identity for the uniform complement guard.

The inequalities for arbitrary real point characters are proved in the
companion manuscript.  This checker verifies their integer constants, the
two contact sums, the polynomial identity, and the source census/bindings.
It neither searches for nor certifies a rational complement-square lift.
"""
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SHIFTS = {
    7: (-7, -6, -4, 1, 3, 5, 8),
    9: (-10, -8, -5, 1, 2, 3, 4, 6, 7),
}


def add(*polys):
    out = {}
    for poly in polys:
        for powers, coefficient in poly.items():
            out[powers] = out.get(powers, 0) + coefficient
    return {powers: coefficient for powers, coefficient in out.items() if coefficient}


def scale(poly, scalar):
    return {powers: scalar*coefficient for powers, coefficient in poly.items() if scalar*coefficient}


def mul(left, right):
    out = {}
    for (a, b), coefficient in left.items():
        for (c, d), other in right.items():
            powers = (a+c, b+d)
            out[powers] = out.get(powers, 0) + coefficient*other
    return {powers: coefficient for powers, coefficient in out.items() if coefficient}


def power(poly, exponent):
    result = {(0, 0): 1}
    for _ in range(exponent):
        result = mul(result, poly)
    return result


def pole_identity():
    # Variables d and t=c^2.  Reduction by t=1-d is explicit.
    one, d, t = {(0, 0): 1}, {(1, 0): 1}, {(0, 1): 1}
    dp1 = add(d, one)
    dm1 = add(d, scale(one, -1))
    omd = add(one, scale(d, -1))
    pole = add(mul(mul(d, power(dp1, 2)), power(t, 2)),
               scale(mul(mul(d, power(dm1, 2)), power(omd, 2)), -1))
    ordinate_square = power(scale(mul(d, omd), 2), 2)
    factorization = mul(mul(d, power(dp1, 2)),
                        mul(add(t, scale(omd, -1)), add(t, omd)))
    assert add(pole, scale(ordinate_square, -1), scale(factorization, -1)) == {}
    reduced = {}
    for (i, j), coefficient in pole.items():
        reduced = add(reduced, scale(mul(power(d, i), power(omd, j)), coefficient))
    assert reduced == ordinate_square
    return {
        'verified_by': 'independent integer coefficient convolution in d and t=c^2',
        'universal_identity': 'P_d(1,c)-[2d(1-d)]^2=d(d+1)^2[c^2-(1-d)][c^2+(1-d)]',
        'specialization': 'c^2=1-d implies P_d(1,c)=[2d(1-d)]^2',
        'nonzero_ordinate_hypothesis': 'd(1-d) != 0',
    }


def source_bindings():
    sources = {}
    for contacts, subdirectory in [(9, 'specification'), (7, 'seven_contact')]:
        relative = f'computation/few_variables/even_valuation11_v75/{subdirectory}/source.json'
        path = REPO/relative
        source = json.loads(path.read_text())
        assert source['contact_count'] == contacts
        assert source['balancing'] == 'C/(1+u*C) for four abscissa tests; C^2/(1+u*C^2) for two comparisons'
        assert source['total_external_variables'] == 11
        assert source['retained_base_count'] == 10
        blocks = source['finite_blocks']
        assert [block['degree'] for block in blocks] == [4, 4, 4, 2]
        assert [block['kind'] for block in blocks] == ['point_block']*3+['pole']
        labels = [label for _, label in source['guard_descriptions']]
        assert all(f'balanced{i}.denominator norm' in labels for i in range(6))
        assert all(label in labels for label in [
            'height.M', 'height.nonzero signed argument', 'contact.G', 'contact.H',
            'contact.u', 'contact.one_plus_u', 'detector.product norm',
            'detector.trace numerator', 'intrinsic.input'])
        sources[str(contacts)] = {
            'source': relative, 'source_sha256': sha256(path.read_bytes()).hexdigest(),
            'point_rank': 4**3, 'rank_after_one_quadratic': 4**3*2,
            'old_retained_base_coordinates': 10,
            'new_retained_base_coordinates': 10-2,
            'shared_encoder_coordinates': 1,
            'new_total_coordinates': 10-2+1,
            'role_of_check': 'Checks metadata, guards and census of the previously audited source; no new coefficient source is compiled.',
        }
    return sources


def reference_normalizer():
    one, u = {(0, 0): 1}, {(1, 0): 1}
    plus = add(scale(one, 4), scale(u, 7))
    minus = add(scale(one, 4), scale(u, -7))
    assert add(power(plus, 2), scale(u, -112), scale(power(minus, 2), -1)) == {}
    upper = Q(280, 1369)*Q(251, 250)**12
    assert 0 < upper < Q(294, 1369) < 1
    return {
        'definition': 'w_star=16u/(4+7u)^2; eta_star=28w_star/V^2',
        'new_guard': '4+7u != 0',
        'old_one_plus_u_guard_retained': True,
        'detector_u_D_W_V_unchanged': True,
        'reference_identity_verified': '(4+7u)^2-112u=(4-7u)^2',
        'reference_trace': 2,
        'reference_comparison_domain': 'u>=10 on the chosen real completeness domain',
        'reference_trace_is_actual_guarded_value': False,
        'eta_star_exact_strict_upper_bound': str(upper),
        'eta_star_simplified_strict_upper_bound': str(Q(294, 1369)),
        'valuation_transfer_proved_in_manuscript': True,
        'native_source_count': 11,
        'native_completeness_requires': 'ordinary rational abc and the retained source arithmetic premises',
        'finite_complement_count': 9,
        'global_complement_square_proved': False,
        'new_source_compiled': False,
        'new_degree_bound_claimed': False,
    }


def main():
    contact_bounds = {}
    for count, shifts in SHIFTS.items():
        assert len(shifts) == len(set(shifts)) == count
        assert sum(shifts) == 0 and max(shifts) < 10
        harmonic_sum = sum((Q(1, 10-c) for c in shifts), Q(0))
        lower_bound = 2*count/harmonic_sum
        assert lower_bound > 10
        contact_bounds[str(count)] = {
            'shifts': list(shifts), 'sum_reciprocal_gaps_at_offset_10': str(harmonic_sum),
            'strict_u_lower_bound': str(lower_bound), 'strict_bound_exceeds_10': True,
            'hypotheses': ['a > max(abs(c))', 'z > a+10'],
        }
    margin = 21*250**12-20*251**12
    assert margin == 1108398992054805009292439980 and margin > 0
    upper = Q(70, 121)*Q(251, 250)**12
    simple_upper = Q(147, 242)
    assert 0 < upper < simple_upper < 1
    report = {
        'schema': 'uniform-complement-guard/v77', 'status': 'PASS',
        'continuous_inequalities_proved_in_manuscript': True,
        'real_abscissa_bound': 'x >= -(3+sqrt(2)) > -5 at either real embedding',
        'u_hypothesis': 'u >= 10, used only as a completeness choice',
        'slot_product_upper_bound': '(1+4/u^3)^6',
        'trace_lower_bound': '2/(1+4/u^3)^6',
        'eta_strict_upper_bound': str(upper),
        'eta_simplified_strict_upper_bound': str(simple_upper),
        'integer_margin_21_times_250_pow12_minus_20_times_251_pow12': margin,
        'physical_contact_bounds': contact_bounds,
        'native_pole_identity': pole_identity(),
        'source_bindings': source_bindings(),
        'reference_normalizer_variant': reference_normalizer(),
        'selected_rational_square_searched_for': False,
        'selected_rational_square_proved': False,
        'nine_variable_completeness_proved': False,
        'new_polynomial_degree_claimed': False,
    }
    (HERE/'certificate.json').write_text(json.dumps(report, indent=2)+'\n')
    print('PASS: exact uniform and reference-normalizer bounds, both harmonic contact sums, native specialization, source census and guards.')


if __name__ == '__main__':
    main()
