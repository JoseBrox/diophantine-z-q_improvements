#!/usr/bin/env python3
"""Independent complete audit of eleven-block general/specification CRT tables.

No builder is imported. The exact checks certify the coefficient operation,
including all surviving cross-block uses of the deleted contact weights.
Arithmetic soundness/completeness and the signed Pell theorem are separately
proved in the accompanying paper and its contact-family section.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PREFIXES = ('integer.o.', 'global.o.', 'scalar_norm.o.', 'detector_trace.o.')


def named(row, names):
    return sorted((term['coefficient'], tuple(sorted(names[j-1] for j in term['monomial'])))
                  for term in row['terms'])


def verify(m):
    predecessor = ROOT / f'undecidability/general_contact_v94/signed_affine_contact_m{m}_quadrics.json'
    path = HERE / f'pell_crt_m{m}_quadrics.json'
    certificate_path = HERE / f'pell_crt_m{m}_certificate.json'
    old, new, certificate = [json.loads(p.read_bytes()) for p in (predecessor, path, certificate_path)]
    assert certificate['table_sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert certificate['predecessor_sha256'] == hashlib.sha256(predecessor.read_bytes()).hexdigest()
    names = old['variable_names']
    deleted = {name for name in names if name == 'o' or name.startswith('int_o_')}
    assert len(deleted) == {163: 61, 179: 76}[m]
    assert new['variable_names'] == [name for name in names if name not in deleted] + ['CF']
    assert len(new['variable_names']) == len(set(new['variable_names'])) == new['variables']
    assert set(names)-set(new['variable_names']) == deleted
    assert set(new['variable_names'])-set(names) == {'CF'}
    oldrows = {row['name']: row for row in old['residuals']}
    newrows = {row['name']: row for row in new['residuals']}
    assert len(oldrows) == len(old['residuals']) and len(newrows) == len(new['residuals'])
    private_rows = {name for name in oldrows if name.startswith(PREFIXES)}
    census = Counter('.'.join(name.split('.')[:2]) for name in private_rows)
    assert census == {'integer.o': {163: 46, 179: 59}[m], 'global.o': 4,
                      'scalar_norm.o': 1, 'detector_trace.o': 1}
    removed_rows = private_rows | {'jones1980.I.definition'}
    assert list(newrows) == [name for name in oldrows if name not in removed_rows
                            and name != 'jones1980.H.definition'] + [
                                'jones1980.CF.definition', 'jones1980.H.definition']
    assert named(oldrows['jones1980.I.definition'], names) == [('-1', ('F', 'o')), ('-1', ('d',)), ('1', ('I',))]
    assert named(oldrows['jones1980.H.definition'], names) == [('-1', ()), ('-1', ('c', 'j')), ('-2', ('r',)), ('1', ('H',))]
    assert named(newrows['jones1980.CF.definition'], new['variable_names']) == [('-1', ('F', 'c')), ('1', ('CF',))]
    h_expected = [('-1', ('c',)), ('-2', ('F2', 'r')), ('-1', ('F2',)),
                  ('1', ('F2', 'c')), ('-1', ('CF', 'j')), ('1', ('H',))]
    assert named(newrows['jones1980.H.definition'], new['variable_names']) == sorted(h_expected)
    last = 1 if m == 163 else 2
    cross_names = {f'integer.i.balanced.detector{last}.poleInput.definition',
                   f'integer.i.shared.inverse{last}', f'integer.i.shared.gate{last}'}
    weights = {f'int_o_{j}' for j in ((153,) if m == 163 else (154, 155))}
    weights.add('int_o_last_contact_weight')
    cross_found, dropped_terms, unchanged_rows = set(), 0, 0
    for name, row in oldrows.items():
        uses = {names[j-1] for term in row['terms'] for j in term['monomial']} & deleted
        if name in removed_rows or name == 'jones1980.H.definition':
            continue
        if uses:
            assert name in cross_names and uses == weights
            cross_found.add(name)
            retained = []
            for term in row['terms']:
                factors = {names[j-1] for j in term['monomial']}
                if factors & deleted:
                    assert factors & deleted <= weights
                    assert len(factors & weights) == 1
                    dropped_terms += 1
                else:
                    retained.append(term)
            assert named({'terms': retained}, names) == named(newrows[name], new['variable_names']), name
        else:
            assert named(row, names) == named(newrows[name], new['variable_names']), name
            unchanged_rows += 1
    assert cross_found == cross_names
    assert dropped_terms == (6 if m == 163 else 9)
    expected_counts = {163: (983, 855), 179: (1148, 998)}[m]
    assert (new['variables'], len(new['residuals'])) == expected_counts
    assert (certificate['variables'], certificate['quadratic_rows']) == expected_counts
    assert old['variables']-new['variables'] == len(deleted)-1
    assert len(old['residuals'])-len(new['residuals']) == len(private_rows)
    assert new['integer_blocks'] == 11
    assert new['global_contact_weights'] == (22 if m == 163 else 33)
    assert new['ordinary_integer_inputs'] == ['b', 'g', 't', 'm', 'w', 's', 'h', 'c', 'gamma', 'j']
    assert new['affine_contact_active_indices'] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11]
    assert new['affine_contact_blocks'] == new['ordinary_integer_inputs']+['i']
    assert not any(weight in new['global_contact_sum_elimination'] for weight in weights)
    assert new['outer_coordinates'] == old['outer_coordinates']
    assert new['outer_residuals'] == old['outer_residuals']
    # The common gauge's nonzero and square guards survive literally.
    for guard in ('integer.b.unit.c_inverse', 'integer.b.unit.c_inverse_square'):
        assert named(oldrows[guard], names) == named(newrows[guard], new['variable_names'])
    assert named(oldrows['jones1980.s.nonzero'], names) == named(newrows['jones1980.s.nonzero'], new['variable_names'])
    assert named(oldrows['jones1980.F2.definition'], names) == named(newrows['jones1980.F2.definition'], new['variable_names'])
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
    assert new['source_universality_hypothesis'] is None
    assert new['source_coding_theorem_independently_reproved'] is False
    assert new['unconditional_undecidability_claim'] is False
    return {'status': 'PASS', 'm': m, 'variables': new['variables'],
            'quadratic_rows': len(new['residuals']),
            'private_coordinates_deleted_including_o': len(deleted),
            'private_rows_deleted': len(private_rows),
            'shared_contact_sum_rows_checked': len(cross_found),
            'deleted_weight_terms_checked': dropped_terms,
            'unchanged_rows_checked': unchanged_rows,
            'retained_integer_blocks': 11,
            'retained_contact_weights': new['global_contact_weights'],
            'table_sha256': certificate['table_sha256']}


if __name__ == '__main__':
    print(json.dumps([verify(m) for m in (163, 179)], sort_keys=True, indent=2))
