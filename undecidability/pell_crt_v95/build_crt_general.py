#!/usr/bin/env python3
"""Compile the one-quotient Pell source with eleven shared general certificates.

The old o-family is removed from the global contact sum. The three rows in
which that sum was substituted are audited explicitly. This is a transfer
through the eleven-family theorem, not a projection onto the old twelve-family
normalization.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(m):
    source = ROOT / f'undecidability/general_contact_v94/signed_affine_contact_m{m}_quadrics.json'
    old = json.loads(source.read_bytes())
    old_names = old['variable_names']
    removed = {name for name in old_names if name == 'o' or name.startswith('int_o_')}
    assert len(removed) == {163: 61, 179: 76}[m]
    weight_names = {f'int_o_{j}' for j in ({163: [153], 179: [154, 155]}[m])}
    weight_names.add('int_o_last_contact_weight')
    prefixes = ('integer.o.', 'global.o.', 'scalar_norm.o.', 'detector_trace.o.')
    private_rows = {row['name'] for row in old['residuals'] if row['name'].startswith(prefixes)}
    assert len(private_rows) == {163: 52, 179: 65}[m]
    dropped_rows = private_rows | {'jones1980.I.definition'}
    new_names = [name for name in old_names if name not in removed] + ['CF']
    new_ids = {name: i + 1 for i, name in enumerate(new_names)}
    new_rows, cross_changes = [], {}
    occurrence_audit = {name: [] for name in sorted(removed)}
    for row in old['residuals']:
        for name in {old_names[i-1] for term in row['terms'] for i in term['monomial']} & removed:
            occurrence_audit[name].append(row['name'])
        if row['name'] in dropped_rows or row['name'] == 'jones1980.H.definition':
            continue
        terms = []
        for term in row['terms']:
            names = [old_names[i-1] for i in term['monomial']]
            touched = set(names) & removed
            if touched:
                assert row['name'].startswith('integer.i.')
                assert touched <= weight_names
                cross_changes.setdefault(row['name'], []).append(
                    {'coefficient': term['coefficient'], 'monomial_names': names})
                continue
            terms.append({'coefficient': term['coefficient'],
                          'monomial': sorted(new_ids[name] for name in names)})
        new_rows.append({'name': row['name'], 'terms': terms})
    assert len(cross_changes) == 3
    expected_cross = {'integer.i.balanced.detector1.poleInput.definition',
                      'integer.i.shared.inverse1', 'integer.i.shared.gate1'} if m == 163 else {
                      'integer.i.balanced.detector2.poleInput.definition',
                      'integer.i.shared.inverse2', 'integer.i.shared.gate2'}
    assert set(cross_changes) == expected_cross

    def row(name, terms):
        return {'name': name, 'terms': [
            {'coefficient': str(coefficient),
             'monomial': sorted(new_ids[n] for n in factors)}
            for coefficient, factors in terms]}

    new_rows += [
        row('jones1980.CF.definition', [(1, ('CF',)), (-1, ('c', 'F'))]),
        row('jones1980.H.definition', [(1, ('H',)), (-1, ('c',)),
            (-2, ('r', 'F2')), (-1, ('F2',)), (1, ('c', 'F2')), (-1, ('CF', 'j'))])]
    new = copy.deepcopy(old)
    new.update(variable_names=new_names, variables=len(new_names), residuals=new_rows,
               integer_blocks=11,
               ordinary_integer_inputs=[name for name in old['ordinary_integer_inputs'] if name != 'o'],
               global_contact_weights={163: 22, 179: 33}[m])
    new['global_contact_sum_predecessor_expression'] = old['global_contact_sum_elimination']
    for name in sorted(weight_names, key=len, reverse=True):
        new['global_contact_sum_elimination'] = new['global_contact_sum_elimination'].replace(' - ' + name, '')
    assert not any(name in new['global_contact_sum_elimination'] for name in weight_names)
    new['affine_contact_original_blocks'] = old['affine_contact_blocks']
    new['affine_contact_blocks'] = [name for name in old['affine_contact_blocks'] if name != 'o']
    new['affine_contact_active_indices'] = [i for i, name in enumerate(old['affine_contact_blocks']) if name != 'o']
    new['pell_crt_predecessor'] = str(source.relative_to(ROOT))
    new['pell_crt_predecessor_sha256'] = sha(source)
    new['pell_crt_source_proof'] = 'undecidability/pell_crt_v95/one_quotient_pell.tex'
    new['pell_crt_interface_proof'] = 'undecidability/pell_crt_v95/contact_block_deletion.tex'
    new['pell_crt_quotient_register'] = 'j now stores the single integer J'
    new['pell_crt_bridge'] = 'CF=c*F; H=c+F2*(2*r+1-c)+CF*j; I is a rational root of the retained monic norm'
    new['pell_crt_removed_coordinates'] = sorted(removed)
    new['pell_crt_removed_rows'] = sorted(dropped_rows)
    new['pell_crt_replaced_row'] = 'jones1980.H.definition'
    new['pell_crt_added_coordinate'] = 'CF'
    new['pell_crt_deleted_contact_weights'] = sorted(weight_names)
    new['pell_crt_changed_cross_rows'] = cross_changes
    new['pell_crt_removed_occurrences'] = occurrence_audit
    new['pell_crt_projection_scope'] = 'Same universal instance set, through the proved one-quotient Pell certificate and the eleven-family integer interface. Not equality with the old twelve-family normalization.'
    new['pell_crt_positive_J_completeness'] = True
    new['pell_crt_retained_arithmetic_interfaces'] = True
    new['pell_crt_inherited_metadata_scope'] = 'Earlier savings and removed-coordinate maps describe their historical transformation stages. Current counts, active inputs, active contact weights and the CRT fields describe this complete table.'
    new['source_universality_verification_scope'] = 'Reduction through the one-quotient binomial certificate to the corrected Jones (1980) Theorem 2 source; its external coding theorem and all integer-interface premises are retained.'
    new['status'] = 'Proved quartic transfer with eleven integer certificates, conditional on the retained arithmetic interfaces and using the cited classical coding theorem.'
    new['pell_crt_savings'] = {'coordinates': old['variables'] - new['variables'],
                              'quadratic_rows': len(old['residuals']) - len(new_rows)}
    assert (new['variables'], len(new_rows)) == {163: (983, 855), 179: (1148, 998)}[m]
    assert new['outer_coordinates'] == old['outer_coordinates']
    assert new['outer_residuals'] == old['outer_residuals']
    support = {i for r in new_rows for t in r['terms'] for i in t['monomial']}
    assert support == set(range(1, new['variables'] + 1))
    assert max(len(t['monomial']) for r in new_rows for t in r['terms']) == 2
    certificate = {
        'schema': 'zq-pell-crt-general/v95', 'interface_coordinates': m,
        'variables': new['variables'], 'quadratic_rows': len(new_rows), 'degree': 4,
        'integer_certificates': 11, 'integer_predicates_removed': ['o'],
        'outer_coordinates': new['outer_coordinates'], 'outer_quadratic_rows': new['outer_residuals'],
        'predecessor': str(source.relative_to(ROOT)), 'predecessor_sha256': sha(source),
        'savings': new['pell_crt_savings'], 'private_rows_removed': sorted(private_rows),
        'source_rows_removed': ['jones1980.I.definition'],
        'source_rows_replaced': ['jones1980.H.definition'],
        'source_rows_added': ['jones1980.CF.definition'],
        'deleted_coordinate_occurrences': occurrence_audit,
        'deleted_contact_weights': sorted(weight_names),
        'global_contact_weights': new['global_contact_weights'],
        'changed_cross_rows': cross_changes,
        'source_universality_hypothesis': None,
        'source_coding_theorem_independently_reproved': False,
        'unconditional_undecidability_claim': False,
        'retained_arithmetic_interfaces': True,
        'source_proof': new['pell_crt_source_proof'], 'interface_proof': new['pell_crt_interface_proof'],
        'scope': 'Exact complete coefficients and support. Soundness reconstructs eleven integer blocks with their active global contact sum; completeness and the source projection are proved in the manuscripts.'}
    return new, certificate


def main():
    for m in (163, 179):
        table, certificate = build(m)
        path = HERE / f'pell_crt_m{m}_quadrics.json'
        path.write_text(json.dumps(table, sort_keys=True, separators=(',', ':')) + '\n')
        certificate['table_sha256'] = sha(path)
        path.with_name(f'pell_crt_m{m}_certificate.json').write_text(json.dumps(certificate, indent=2, sort_keys=True) + '\n')
        print(json.dumps({'m': m, 'variables': table['variables'],
                          'rows': len(table['residuals']), 'sha256': certificate['table_sha256']}))


if __name__ == '__main__':
    main()
