#!/usr/bin/env python3
"""Verify aggregate contact spacing and both complete affine substitutions."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'undecidability'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    raw = subprocess.run([sys.executable, '-B', str(FOLDER /
                         'aggregate_spacing_v100/verify_aggregate_spacing.py')],
                         cwd=ROOT, check=True, text=True, capture_output=True).stdout
    check = json.loads(raw)
    assert len(check['tables']) == 2
    assert all(item['status'] == 'PASS' for item in check['tables'])
    assert check['local_fixtures']['lucas_exact_modular_fixtures'] == 75
    assert check['local_fixtures']['index_difference_fixtures'] == 120
    ledger = json.loads((FOLDER / 'results.json').read_text())
    records = {r['id']: r for r in ledger['records']}
    assert len(records) == len(ledger['records'])
    counts = {}
    for m, n, q, blocks in [(163, 971, 826, 13), (179, 1145, 996, 11)]:
        record = records[f'aggregate-spacing-quartic-{m}']
        path = FOLDER / record['table']
        table = json.loads(path.read_bytes())
        cert = json.loads((FOLDER / record['certificate']).read_bytes())
        old = records[record['predecessor_record']]
        assert record['variables'] == table['variables'] == cert['variables'] == n
        assert record['quadratic_rows'] == len(table['residuals']) == cert['quadratic_rows'] == q
        assert record['table_sha256'] == cert['table_sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
        assert record['outer_coordinates'] == table['outer_coordinates']
        assert record['outer_quadratic_rows'] == table['outer_residuals']
        assert record['integer_certificates'] == table['integer_blocks'] == blocks
        assert record['coordinates_saved_in_this_step'] == old['variables'] - n == 1
        assert record['quadratic_rows_saved_in_this_step'] == old['quadratic_rows'] - q == 0
        assert record['degree'] == table['sum_of_squares_degree'] == 4
        assert record['contact_spacing_fixed_before_prime_selection'] is True
        assert record['maximum_contact_block_index'] == 15
        assert 'contact_common_spacing' not in table['variable_names']
        assert record['source_universality_hypothesis'] is None
        assert table['source_coding_theorem_independently_reproved'] is False
        assert record['unconditional_undecidability_claim'] is False
        assert (FOLDER / record['proof']).with_suffix('.pdf').is_file()
        counts[str(m)] = {'variables': n, 'quadratic_rows': q, 'table_sha256': record['table_sha256']}
    assert records['product-quartic-56']['variables'] == 696
    result = {'schema': 'zq-undecidability-verification/v100', 'status': 'PASS',
              'new_quartics': counts, 'abc_quartic_unchanged': 696,
              'fixed_aggregate_spacing': True, 'no_new_supplier_hypothesis': True,
              'retained_arithmetic_interfaces': True,
              'external_coding_theorem': 'Jones (1980), Theorem 2',
              'quartic_target_263_established': False,
              'scope': 'Complete affine coefficient substitutions, all unchanged rows, guards, support, degree, exact Lucas modular fixtures, fixed index separation, metadata, hashes and registry. The manuscript proves ordered arithmetic completeness.'}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
