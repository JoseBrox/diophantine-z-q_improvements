#!/usr/bin/env python3
"""Independently bind the seven-unit presentation to the published v73 source.

This checker imports neither the construction module nor a solver.  It compares
all physical Laurent equations with the published 194-coordinate package and
checks the exact unit equations and input-preserving diagonal maps.
"""
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
PREVIOUS = HERE.parent / 'cleared_comparisons194_v73'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def physical_rows(path):
    answer = {}
    for row in read(path)['rows']:
        terms = defaultdict(Fraction)
        for term in row['terms']:
            key = (term['parameterPower'], tuple(term['monomial']),
                   tuple(term['unitPower']))
            terms[key] += Fraction(term['coefficient'])
        assert row['name'] not in answer
        answer[row['name']] = (row['group'], dict(terms))
    return answer


def verify():
    old_model = read(PREVIOUS / 'coordinate-model.json')
    new_model = read(HERE / 'coordinate-model.json')
    assert old_model['active'] == new_model['active']
    assert len(set(new_model['active'])) == 186
    for field in ['rows', 'quadratic_tests', 'linear_tests', 'factor_rows']:
        assert old_model[field] == new_model[field], field
    old_units = {int(k): tuple(v) for k, v in old_model['base_units'].items()}
    units = {int(k): tuple(v) for k, v in new_model['base_units'].items()}
    assert old_units.pop(78) == (-1, 0)
    assert old_units == units == {
        77: (1, 0), 90: (0, 1), 91: (0, -1), 92: (-1, -2),
        901: (0, -3), 902: (1, -1), 903: (-1, -1)}
    # v*v_inverse=1 forces v,v_inverse nonzero.  u*inverse_uv=v_inverse
    # forces u,inverse_uv nonzero.  The remaining three equations then
    # uniquely solve the remaining units; there is no additional component.
    expected_guards = {
        'unit.u': {(77, 903): 1, (91,): -1},
        'unit.v': {(): 1, (90, 91): -1},
        'unit.old_square': {(77, 92): 1, (91, 91): -1},
        'unit.v_inv_cube': {(90, 901): 1, (91, 91): -1},
        'unit.u_over_v': {(902,): 1, (77, 91): -1},
    }
    for terms in expected_guards.values():
        expansion = defaultdict(int)
        for monomial, coefficient in terms.items():
            exponent = tuple(sum(units[i][j] for i in monomial) for j in (0, 1))
            expansion[exponent] += coefficient
        assert not any(expansion.values())
    variants = []
    for variant in ['primitive', 'fewer_monomials']:
        old_path = PREVIOUS / variant / 'laurent-source.json'
        new_path = HERE / variant / 'laurent-source.json'
        old = physical_rows(old_path)
        new = physical_rows(new_path)
        assert old == new and len(new) == 162
        old_transform = read(PREVIOUS / variant / 'transformation.json')
        transform = read(HERE / variant / 'transformation.json')
        assert old_transform['factor_assignments'] == transform['factor_assignments']
        assert transform['weights']['1'] == old_transform['weights']['1'] == [0, 0]
        renumber = {int(k): v for k, v in transform['old_to_new'].items()}
        inverse = {v: k for k, v in renumber.items()}
        assert set(inverse) == set(range(1, 194)) and renumber[1] == 1
        assert 78 not in renumber
        rows = read(HERE / variant / 'quadratic-family.json')['residuals']
        found = {}
        for row in rows:
            if row['name'] not in expected_guards:
                continue
            terms = defaultdict(int)
            for term in row['terms']:
                assert term['parameterPower'] == 0
                terms[tuple(sorted(inverse[j] for j in term['monomial']))] += int(term['coefficient'])
            found[row['name']] = dict(terms)
        assert found == expected_guards
        assert len(rows) == len(new) + len(found) == 167
        # Every diagonal multiplier and every equation multiplier is a unit
        # on the common torus, and the inverse is obtained by negating powers.
        coordinate_map = {}
        for key, old_weight in old_transform['weights'].items():
            new_weight = transform['weights'][key]
            assert all(isinstance(e, int) for e in old_weight + new_weight)
            # physical x_i = u^old_weight * old_i = u^new_weight * new_i.
            coordinate_map[key] = [b-a for a,b in zip(old_weight, new_weight)]
        assert coordinate_map['1'] == [0, 0]
        variants.append({
            'basis': variant,
            'physical_rows_identical_to_v73': len(new),
            'factor_assignments_unchanged': True,
            'old_laurent_source_sha256': digest(old_path),
            'new_laurent_source_sha256': digest(new_path),
            'quadratic_table_sha256': digest(HERE / variant / 'quadratic-family.json'),
            'old_coordinate_equals_new_times_u_v_power': coordinate_map,
        })
    return {
        'schema': 'quartic193-input-preserving-transfer/v74',
        'status': 'PASS',
        'published_source_commit': 'ba18b9ffcf166856b4f2f921d560bb6497eec1ab',
        'previous_variables': 194,
        'variables': 193,
        'old_source_id_deleted': 78,
        'unit_coordinates': 7,
        'unit_equations': 5,
        'nonzero_unit_recovery': {
            '90': 'v', '91': '1/v', '77': 'u', '903': '1/(u*v)',
            '92': '1/(u*v^2)', '901': '1/v^3', '902': 'u/v',
        },
        'deleted_coordinate_recovery': 'old x78=1/u=x90*x903',
        'bijection_on_entire_rational_zero_set': True,
        'input_coordinate_fixed': True,
        'new_arithmetic_assumptions': [],
        'same_sufficient_parameter_threshold_as_v73': True,
        'sufficient_numerical_defining_threshold_known': False,
        'variants': variants,
        'scope': 'Exact transfer from v73. The external arithmetic premises of v73 are inherited, not independently reproved here.',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE / 'transfer-certificate.json')
    args = parser.parse_args()
    report = verify()
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print('PASS: all 162 physical rows agree with v73 in each basis; seven units, five exact guards, fixed input.')
