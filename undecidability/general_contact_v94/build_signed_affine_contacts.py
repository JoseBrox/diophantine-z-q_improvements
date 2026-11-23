#!/usr/bin/env python3
"""Compose shared affine contacts with the signed-source positivity theorem."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SIGNED = ROOT / 'undecidability/source_repair_v93/build_signed_positivity.py'


def build(m):
    spec = importlib.util.spec_from_file_location('signed_source_transformer', SIGNED)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    predecessor = HERE / f'affine_contact_m{m}_quadrics.json'
    old = json.loads(predecessor.read_bytes())
    assert (old['variables'], len(old['residuals'])) == {
        163: (1048, 908), 179: (1228, 1064)}[m]
    table = module.build(predecessor)
    table['signed_binomial_positivity_predecessor'] = str(predecessor.relative_to(ROOT))
    table['signed_affine_composition_proof'] = 'undecidability/general_contact_v94/affine_contact_progressions.tex'
    table['signed_affine_savings_from_corrected_ceiling'] = {'coordinates': 31, 'quadratic_rows': 17}
    certificate = {
        'interface_coordinates': m,
        'variables': table['variables'],
        'quadratic_rows': len(table['residuals']),
        'quartic_degree': 4,
        'coefficient_parameters': table['parameters'],
        'predecessor': str(predecessor.relative_to(ROOT)),
        'predecessor_sha256': hashlib.sha256(predecessor.read_bytes()).hexdigest(),
        'corrected_ceiling_predecessor': table['affine_contact_predecessor'],
        'corrected_ceiling_predecessor_sha256': table['affine_contact_predecessor_sha256'],
        'coordinate_saving_from_affine': 5,
        'quadratic_row_saving_from_affine': 1,
        'coordinate_saving_from_corrected_ceiling': 31,
        'quadratic_row_saving_from_corrected_ceiling': 17,
        'removed_coordinates': table['signed_binomial_positivity_removed_coordinates'],
        'removed_rows': table['signed_binomial_positivity_removed_rows'],
        'added_coordinate': 's_inverse',
        'added_row': 'jones1980.s.nonzero',
        'source_coding_theorem': table['source_coding_theorem'],
        'source_universality_hypothesis': None,
        'source_universality_verified': True,
        'source_coding_theorem_independently_reproved': False,
        'arithmetic_hypotheses_unchanged': True,
        'unconditional_undecidability_claim': False,
        'proofs': [table['signed_affine_composition_proof'],
                   table['signed_binomial_positivity_proof']],
        'verification_scope': 'Every coefficient transformation, private positivity supports, retained guards, integer coefficient domains, support, counts and hashes; quantified source positivity and arithmetic completeness are proved separately.'}
    return table, certificate


def main():
    for m in (163, 179):
        table, certificate = build(m)
        path = HERE / f'signed_affine_contact_m{m}_quadrics.json'
        path.write_text(json.dumps(table, sort_keys=True, separators=(',', ':')) + '\n')
        certificate['table_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        path.with_name(f'signed_affine_contact_m{m}_certificate.json').write_text(
            json.dumps(certificate, sort_keys=True, indent=2) + '\n')
        print(json.dumps({'m': m, 'variables': table['variables'],
                          'rows': len(table['residuals']), 'sha256': certificate['table_sha256']}))


if __name__ == '__main__':
    main()
