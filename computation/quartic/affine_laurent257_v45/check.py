#!/usr/bin/env python3
"""Independently verify the 257-variable quartic directly from its pinned source.

This checker imports neither the producer nor any Laurent conversion routine.
It checks every source-to-final residual identity using SymPy expressions and
the full sum-of-squares expansion using SymPy's sparse polynomial ring. All
support, primitivity and height assertions are uniform in integer N >= 1.
"""
import argparse
import hashlib
import json
from functools import reduce
from math import gcd
from pathlib import Path

import sympy as sp
from sympy.polys.domains import ZZ
from sympy.polys.rings import ring


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PINNED_SOURCE = 'computation/quartic/laurent_recovery_v38/family258/balanced-quadratic.json'
PINNED_SHA256 = 'ad8204d383210613590b3daa8031dc43113d50b0d26e84d067971cac5f37fe4c'
CONSTANT_HEIGHT = 484991541504995159662206970923766531374664106904986910720
PACKAGE_FILES = (
    'transformation.json', 'quadratic-family.json',
    'polynomial-family.json', 'construction-report.json',
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE/'independent-verification.json')
    args = parser.parse_args()
    blobs = {name: (HERE/name).read_bytes() for name in PACKAGE_FILES}
    certificate, final, advertised, construction = (
        json.loads(blobs[name]) for name in PACKAGE_FILES
    )
    assert certificate['source'] == PINNED_SOURCE
    assert certificate['source_sha256'] == PINNED_SHA256
    source_blob = (ROOT/PINNED_SOURCE).read_bytes()
    assert hashlib.sha256(source_blob).hexdigest() == PINNED_SHA256
    source = json.loads(source_blob)
    assert source['variables'] == 258 and len(source['residuals']) == 230
    assert final['variables'] == advertised['variables'] == 257
    assert len(final['residuals']) == 229
    assert source['inputCoordinate'] == final['inputCoordinate'] == advertised['inputCoordinate'] == 1
    assert source['fixedParameter'] == final['fixedParameter'] == advertised['fixedParameter']
    assert source['fixedParameter']['quantified'] is False
    assert source['fixedParameter']['domain'] == 'C=149^N, N>=1'
    assert final['coordinates'] == advertised['coordinates']
    assert [c['id'] for c in source['coordinates']] == list(range(1, 259))
    assert [c['id'] for c in final['coordinates']] == list(range(1, 258))
    assert final['coordinates'][0]['name'] == 'input'

    laurent = certificate['laurent']
    scaling = certificate['parameter_scaling']
    rename = {int(i): j for i, j in laurent['old_to_new'].items()}
    assert set(rename) == set(range(1, 259))-{157}
    assert set(rename.values()) == set(range(1, 258))
    assert rename[1] == 1 and rename[155] == 155 and rename[156] == 156
    assert laurent['deleted_coordinates'] == [157]
    assert laurent['base_units'] == ['w1']
    assert laurent['powers'] == {'155': [-1], '156': [1], '157': [2]}
    assert certificate['unit_guard'] == {'old_ids': [155, 156], 'equation': 'q1*w1=1'}
    assert certificate['deleted_power'] == {'old_id': 157, 'value': 'w1²'}
    assert certificate['input_fixed'] is True
    for old, new in rename.items():
        assert final['coordinates'][new-1]['parent_id'] == old
        assert final['coordinates'][new-1]['name'] == source['coordinates'][old-1]['name']

    laurent_weights = {}
    for i, powers in laurent['weights'].items():
        assert len(powers) == 1 and isinstance(powers[0], int)
        laurent_weights[int(i)] = powers[0]
    assert set(laurent_weights) <= set(range(1, 259))-{155, 156, 157}
    C_weights = {int(i): power for i, power in scaling['weights'].items()}
    assert all(1 <= i <= 257 and isinstance(power, int) for i, power in C_weights.items())
    assert laurent_weights.get(1, 0) == 0
    assert all(C_weights.get(i, 0) == 0 for i in (1, 155, 156))

    C, w = sp.symbols('C w', nonzero=True)
    z = {i: sp.Symbol(f'z{i}') for i in range(1, 258)}
    y = {i: sp.Symbol(f'y{i}') for i in range(1, 259)}

    def expression(terms, coordinates):
        return sp.Add(*(
            sp.Rational(t['coefficient'])*C**t['parameterPower']*
            sp.Mul(*(coordinates[i] for i in t['monomial']))
            for t in terms
        ))

    # Check the entire affine map explicitly. Its inverse is triangular:
    # y116=x116-x155, y138=x138-2*x116+x155, y139=x139-x117.
    affine = certificate['affine_substitutions']
    assert set(affine) == {'116', '138', '139'}
    expected_affine = {116: y[116]+y[155], 138: y[138]+2*y[116]+y[155], 139: y[139]+y[117]}
    for i, expected in expected_affine.items():
        assert sp.expand(expression(affine[str(i)], y)-expected) == 0
    assert 1 not in expected_affine

    final_units = dict(z)
    final_units[155], final_units[156] = 1/w, w
    centered = {}
    unit_powers = {155: -1, 156: 1, 157: 2}
    for i in range(1, 259):
        if i in unit_powers:
            centered[i] = w**unit_powers[i]
        else:
            j = rename[i]
            centered[i] = w**laurent_weights.get(i, 0)*C**C_weights.get(j, 0)*z[j]
    original_coordinates = dict(centered)
    for i, terms in affine.items():
        original_coordinates[int(i)] = expression(terms, centered)
    assert original_coordinates[1] == z[1]

    source_rows = {r['id']: r for r in source['residuals']}
    final_rows = {r['id']: r for r in final['residuals']}
    assert len(source_rows) == 230 and len(final_rows) == 229
    assert len({r['name'] for r in source_rows.values()}) == 230
    assert len({r['name'] for r in final_rows.values()}) == 229
    affine_clears = {r['name']: r['multiplyByParameterPower'] for r in certificate['affine_rows']}
    assert len(affine_clears) == len(certificate['affine_rows']) == 230
    assert set(affine_clears) == {r['name'] for r in source_rows.values()}
    assert all(p == 0 for p in affine_clears.values())
    assert set(scaling['row_shifts']) == {r['name'] for r in final_rows.values()}
    assert all(isinstance(p, int) for p in scaling['row_shifts'].values())

    links = laurent['rows']
    assert len(links) == 229
    assert {r['target_row'] for r in links} == set(final_rows)
    assert len({r['source_row'] for r in links}) == 229
    deleted_names = laurent['deleted_rows']
    assert deleted_names == ['detector1.inverseWeightSquared.definition']
    deleted_rows = [r for r in source_rows.values() if r['name'] in deleted_names]
    assert len(deleted_rows) == 1
    assert {r['source_row'] for r in links} | {r['id'] for r in deleted_rows} == set(source_rows)
    assert expression(deleted_rows[0]['terms'], y) == y[156]**2-y[157]
    guard_name = 'detector1.inverseWeight.definition'
    source_guard = next(r for r in source_rows.values() if r['name'] == guard_name)
    final_guard = next(r for r in final_rows.values() if r['name'] == guard_name)
    assert expression(source_guard['terms'], y) == 1-y[155]*y[156]
    assert expression(final_guard['terms'], z) == 1-z[155]*z[156]

    checked_row_names = []
    for link in links:
        old, new = source_rows[link['source_row']], final_rows[link['target_row']]
        assert old['name'] == new['name']
        assert len(link['division_exponents']) == 1
        w_power = link['division_exponents'][0]
        assert isinstance(w_power, int)
        primitive_multiplier = sp.Rational(link['primitive_multiplier'])
        assert primitive_multiplier != 0
        C_power = affine_clears[old['name']]-scaling['row_shifts'][new['name']]
        transformed = expression(old['terms'], original_coordinates)*C**C_power*w**(-w_power)*primitive_multiplier
        assert sp.expand(transformed-expression(new['terms'], final_units)) == 0, old['name']
        checked_row_names.append(old['name'])
    for row in deleted_rows:
        assert sp.expand(expression(row['terms'], original_coordinates)) == 0

    # Independent full expansion in 258 polynomial indeterminates (C and z1,...,z257).
    polynomial_ring = ring(','.join(['C']+[f'z{i}' for i in range(1, 258)]), ZZ)[0]

    def polynomial(terms):
        coefficients = {}
        for term in terms:
            coefficient = sp.Rational(term['coefficient'])
            assert coefficient.q == 1 and coefficient != 0
            power = term['parameterPower']
            assert isinstance(power, int) and power >= 0
            monomial = term['monomial']
            assert monomial == sorted(monomial)
            assert all(isinstance(i, int) and 1 <= i <= 257 for i in monomial)
            powers = [0]*258
            powers[0] = power
            for i in monomial:
                powers[i] += 1
            powers = tuple(powers)
            assert powers not in coefficients
            coefficients[powers] = int(coefficient)
        return polynomial_ring.from_dict(coefficients)

    expanded = polynomial_ring.zero
    primitivity_receipts = []
    linear_coefficients = []
    for row in final_rows.values():
        residual = polynomial(row['terms'])
        assert residual and max(sum(p[1:]) for p in residual) <= 2
        assert all(p[0] in (0, 1) for p in residual)
        ordinary = set()
        by_power = {0: [], 1: []}
        for powers, coefficient in residual.items():
            assert powers[1:] not in ordinary, 'mixed-C coefficient in one residual'
            ordinary.add(powers[1:])
            by_power[powers[0]].append(abs(int(coefficient)))
            if powers[0] == 1:
                linear_coefficients.append(abs(int(coefficient)))
        g0, g1 = (reduce(gcd, by_power[e], 0) for e in (0, 1))
        assert gcd(g0, 149*g1) == 1, row['name']
        primitivity_receipts.append({'name': row['name'], 'g0': g0, 'g1': g1})
        expanded += residual**2
    assert max(linear_coefficients) == 149
    target = polynomial(advertised['terms'])
    assert expanded == target
    assert len(target) == 3684
    assert max(p[0] for p in target) == 2
    assert max(sum(p[1:]) for p in target) == advertised['degree'] == 4
    assert {i for p in target for i in range(1, 258) if p[i]} == set(range(1, 258))

    profiles = {}
    for powers, coefficient in target.items():
        profiles.setdefault(powers[1:], [0, 0, 0])[powers[0]] = int(coefficient)
    assert len(profiles) == 3679
    assert profiles[(4,)+(0,)*256] == [1, 0, 0]

    def monomial_key(indices):
        result = [0]*257
        for i in indices:
            result[i-1] += 1
        return tuple(result)

    def value(profile, at):
        return profile[0]+at*(profile[1]+at*profile[2])

    def monotonicity_certificate(profile, at, strict):
        initial = value(profile, at)
        derivative = profile[1]+2*at*profile[2]
        assert profile[2] >= 0 and derivative >= 0
        assert initial > 0 if strict else initial >= 0

    for profile in profiles.values():
        leading = next(c for c in reversed(profile) if c)
        sign = 1 if leading > 0 else -1
        monotonicity_certificate([sign*c for c in profile], 149, True)
    # Positive value, nonnegative first derivative and nonnegative second
    # derivative prove each signed coefficient remains positive for C>=149.

    constant_monomial = [82, 86, 86, 131]
    power_monomial = [166, 166]
    assert profiles[monomial_key(constant_monomial)] == [CONSTANT_HEIGHT, 0, 0]
    leader = [0, 0, 149**2]
    assert profiles[monomial_key(power_monomial)] == leader
    small_heights = []
    for N in range(1, 13):
        actual = max(abs(value(profile, 149**N)) for profile in profiles.values())
        assert actual == CONSTANT_HEIGHT
        small_heights.append({'N': N, 'height': str(actual)})
    for profile in profiles.values():
        for sign in (-1, 1):
            difference = [leader[i]+sign*profile[i] for i in range(3)]
            monotonicity_certificate(difference, 149**13, False)
    assert 149**26 < CONSTANT_HEIGHT < 149**28

    for key, expected in {
        'source_sha256': PINNED_SHA256, 'variables': 257, 'input_coordinate': 1,
        'quadratic_rows': 229, 'degree': 4, 'integer_content': 1,
        'ordinary_monomials': 3679, 'parameter_separated_terms': 3684,
        'coefficient_parameter_degree': 2, 'maximum_C_coefficient_in_quadratic_rows': 149,
        'height_crossover_N': 13,
        'coefficient_height': 'max(484991541504995159662206970923766531374664106904986910720,149^(2N+2))',
    }.items():
        assert construction[key] == expected, key
    assert construction['defining_threshold_effective'] is True
    assert construction['effective_sufficient_N'] == 9682
    assert construction['explicit_height_at_N9682'] == '149^19366'

    # Certify a stable input snapshot.
    assert (ROOT/PINNED_SOURCE).read_bytes() == source_blob
    assert all((HERE/name).read_bytes() == blob for name, blob in blobs.items())
    receipt = {
        'schema': 'affine-Laurent-quartic257-independent-verification/v45',
        'status': 'PASS',
        'independent_engine': 'SymPy expressions and sparse polynomial ring; no producer, optimizer, or Laurent-converter imports.',
        'source': PINNED_SOURCE,
        'source_sha256': PINNED_SHA256,
        'package_sha256': {name: hashlib.sha256(blob).hexdigest() for name, blob in blobs.items()},
        'source_rows': 230, 'retained_rows': 229,
        'source_to_final_residual_identities': len(checked_row_names),
        'deleted_power_identities': 1,
        'deleted_coordinate': 157,
        'affine_map_triangular_with_diagonal_one': True,
        'literal_source_and_final_unit_guard': '1-z155*z156',
        'unit_parameter_weights_zero': [155, 156],
        'input_coordinate_fixed': True,
        'all_source_rows_accounted_for': True,
        'zero_set_equivalence': 'Input-preserving rational bijection for every fixed nonzero rational C. The retained unit guard justifies all Laurent divisions.',
        'variables': 257, 'quadratic_rows': 229,
        'primitive_rows_for_every_integer_N_at_least_1': 229,
        'row_primitivity_proof': 'Each residual has distinct ordinary monomials and gcd(g0,149*g1)=1, so gcd(g0,149^N*g1)=1 for every N>=1.',
        'row_primitivity_certificates': primitivity_receipts,
        'full_sum_of_squares_expansion_equal': True,
        'degree': 4, 'integer_content': 1,
        'input_fourth_coefficient': 1,
        'all_257_variables_occur': True,
        'ordinary_monomials_for_every_integer_N_at_least_1': 3679,
        'parameter_separated_terms': 3684,
        'coefficient_parameter_degree': 2,
        'maximum_C_coefficient_in_quadratic_rows': 149,
        'support_proof': 'Every coefficient has a sign with positive value and nonnegative first and second derivatives at C=149; it remains nonzero for every real C>=149.',
        'coefficient_height_for_every_integer_N_at_least_1': 'max(484991541504995159662206970923766531374664106904986910720,149^(2N+2))',
        'constant_height_monomial': constant_monomial,
        'power_height_monomial': power_monomial,
        'small_N_exact_heights': small_heights,
        'power_height_for_all_N_at_least': 13,
        'height_proof': 'For every coefficient f, both 149^2*C^2+f and 149^2*C^2-f have nonnegative value and first and second derivatives at C=149^13; both are nonnegative thereafter.',
        'strict_crossover': '149^26 < 484991541504995159662206970923766531374664106904986910720 < 149^28',
        'effective_sufficient_N_inherited': 9682,
        'height_at_effective_N9682': '149^19366',
        'scope': 'Exact algebraic equivalence and coefficient assertions. The inherited arithmetic premises and sufficient fixed-parameter threshold are unchanged, not independently certified here. No optimizer optimality claim.',
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps({key: value for key, value in receipt.items() if key not in ('row_primitivity_certificates', 'package_sha256')}, indent=2))


if __name__ == '__main__':
    main()
