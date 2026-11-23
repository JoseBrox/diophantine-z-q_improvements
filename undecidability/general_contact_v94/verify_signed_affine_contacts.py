#!/usr/bin/env python3
"""Independently audit the complete signed-affine composite coefficient tables.

No builder is imported. The affine and signed-source coefficient operations
have disjoint supports, as checked below, so their proved reconstructions
compose without a new source or arithmetic hypothesis.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
REMOVED_NAMES = {f'positive_{name}_{j}' for name in ('w', 's') for j in (1, 2, 3)}
REMOVED_ROWS = {'jones1980.positive.w', 'jones1980.positive.s'}


def named(row, names):
    return sorted((term['coefficient'], tuple(sorted(names[j-1] for j in term['monomial'])))
                  for term in row['terms'])


def verify(m):
    predecessor = HERE / f'affine_contact_m{m}_quadrics.json'
    path = HERE / f'signed_affine_contact_m{m}_quadrics.json'
    certificate_path = HERE / f'signed_affine_contact_m{m}_certificate.json'
    old, new, certificate = [json.loads(p.read_bytes()) for p in (predecessor, path, certificate_path)]
    assert new['signed_binomial_positivity_predecessor'] == str(predecessor.relative_to(ROOT))
    assert new['signed_binomial_positivity_predecessor_sha256'] == hashlib.sha256(predecessor.read_bytes()).hexdigest()
    assert certificate['predecessor_sha256'] == hashlib.sha256(predecessor.read_bytes()).hexdigest()
    assert certificate['table_sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
    original = ROOT / new['affine_contact_predecessor']
    assert new['affine_contact_predecessor_sha256'] == hashlib.sha256(original.read_bytes()).hexdigest()
    assert certificate['corrected_ceiling_predecessor_sha256'] == hashlib.sha256(original.read_bytes()).hexdigest()
    corrected = json.loads(original.read_bytes())
    expected = {163: (1043, 907), 179: (1223, 1063)}[m]
    assert (new['variables'], len(new['residuals'])) == expected
    assert (certificate['variables'], certificate['quadratic_rows']) == expected
    assert (corrected['variables']-new['variables'],
            len(corrected['residuals'])-len(new['residuals'])) == (31, 17)
    assert new['outer_coordinates'] == old['outer_coordinates']-5
    assert new['outer_residuals'] == old['outer_residuals']-1
    assert new['variable_names'] == [name for name in old['variable_names'] if name not in REMOVED_NAMES] + ['s_inverse']
    assert len(set(new['variable_names'])) == new['variables']
    assert set(old['variable_names'])-set(new['variable_names']) == REMOVED_NAMES
    assert set(new['variable_names'])-set(old['variable_names']) == {'s_inverse'}
    oldrows = {row['name']: row for row in old['residuals']}
    newrows = {row['name']: row for row in new['residuals']}
    assert len(newrows) == len(new['residuals'])
    assert list(newrows) == [name for name in oldrows if name not in REMOVED_ROWS] + ['jones1980.s.nonzero']
    for name in oldrows.keys()-REMOVED_ROWS:
        assert named(oldrows[name], old['variable_names']) == named(newrows[name], new['variable_names']), name
    for name in ('w', 's'):
        expected_terms = [('-2', ()), ('2', (name,))]
        for j in (1, 2, 3):
            coordinate = f'positive_{name}_{j}'
            expected_terms += [('-1', (coordinate,)), ('-1', (coordinate, coordinate))]
            occurrences = [row['name'] for row in old['residuals']
                           if any(old['variable_names'][i-1] == coordinate
                                  for term in row['terms'] for i in term['monomial'])]
            assert occurrences == [f'jones1980.positive.{name}']
        assert named(oldrows[f'jones1980.positive.{name}'], old['variable_names']) == sorted(expected_terms)
    assert named(newrows['jones1980.s.nonzero'], new['variable_names']) == [('-1', ()), ('1', ('s', 's_inverse'))]
    # Every affine change is in an integer-certificate coordinate. None touches
    # the source's two private positivity rows or the six deleted coordinates.
    assert not REMOVED_NAMES.intersection(new['affine_contact_substitution'])
    assert all(name.startswith('int_') for name in new['affine_contact_substitution'])
    assert all(name.startswith('integer.') for name in new['affine_contact_removed_rows'])
    parameters = tuple(map(sp.Symbol, new['parameters']))
    support = set()
    for row in new['residuals']:
        for term in row['terms']:
            assert len(term['monomial']) <= 2
            support.update(term['monomial'])
            coefficient = sp.sympify(term['coefficient'])
            assert coefficient.free_symbols <= set(parameters)
            assert sp.Poly(coefficient, *parameters, domain=sp.ZZ)
    assert support == set(range(1, new['variables']+1))
    assert max(len(term['monomial']) for row in new['residuals'] for term in row['terms']) == 2
    for key in ('affine_contact_savings', 'affine_contact_predecessor',
                'source_coding_theorem', 'source_coding_theorem_independently_reproved',
                'source_universality_hypothesis', 'source_universality_verified',
                'unconditional_undecidability_claim', 'pell_core_source_p_parameter',
                'M_recovery', 'a_recovery'):
        assert new[key] == old[key]
    assert new['pell_core_source_p_parameter'] == '2*w*s^2*r^2*n^6'
    assert new['M_recovery'] == 'sr'
    assert new['a_recovery'] == '(U+1)*sr'
    assert new['source_universality_hypothesis'] is None
    assert new['source_coding_theorem_independently_reproved'] is False
    assert new['unconditional_undecidability_claim'] is False
    return {'status': 'PASS', 'm': m, 'variables': new['variables'],
            'quadratic_rows': len(new['residuals']),
            'coordinate_saving_from_corrected_ceiling': 31,
            'quadratic_row_saving_from_corrected_ceiling': 17,
            'retained_rows_checked': len(newrows)-1,
            'disjoint_transformation_supports': True,
            'table_sha256': certificate['table_sha256']}


if __name__ == '__main__':
    print(json.dumps([verify(m) for m in (163, 179)], indent=2))
