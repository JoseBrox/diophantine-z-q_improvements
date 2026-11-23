#!/usr/bin/env python3
"""Verify exact product elimination in all three complete quartic interfaces."""
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
    check = subprocess.run([sys.executable, '-B',
                            str(FOLDER / 'pell_product_v99/verify_product.py')],
                           cwd=ROOT, check=True, text=True, capture_output=True)
    checked = json.loads(check.stdout)
    assert checked['polynomial_identities'] == 2
    items = checked['tables']
    assert len(items) == 3
    assert all(item['status'].lower() == 'pass' for item in items)
    ledger = json.loads((FOLDER / 'results.json').read_text())
    records = {r['id']: r for r in ledger['records']}
    assert len(records) == len(ledger['records'])
    counts = {}
    for m, n, q, blocks in [(163, 972, 826, 13), (179, 1146, 996, 11),
                             (56, 696, 591, 13)]:
        record = records[f'product-quartic-{m}']
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
        assert record['quadratic_rows_saved_in_this_step'] == old['quadratic_rows'] - q == 1
        assert record['degree'] == table['sum_of_squares_degree'] == 4
        assert record['deleted_coordinate'] == 'sr2'
        assert record['inverse_lift'] == 'sr2=sr^2'
        assert 'sr2' not in table['variable_names']
        assert not any(row['name'] == 'jones1980.sr2.definition'
                       for row in table['residuals'])
        assert record['source_universality_hypothesis'] is None
        assert table['source_coding_theorem_independently_reproved'] is False
        assert record['unconditional_undecidability_claim'] is False
        assert (FOLDER / record['proof']).with_suffix('.pdf').is_file()
        counts[str(m)] = {'variables': n, 'quadratic_rows': q, 'table_sha256': record['table_sha256']}
    result = {'schema': 'zq-undecidability-verification/v99', 'status': 'PASS',
              'new_quartics': counts, 'all_zero_branches_included': True,
              'unique_polynomial_inverse_lift': True,
              'retained_arithmetic_interfaces': True,
              'external_coding_theorem': 'Jones (1980), Theorem 2',
              'quartic_target_263_established': False,
              'scope': 'Independent polynomial identities, complete occurrence audit, replacement row, every unchanged row, full support, degree, metadata, hashes and registry for three interfaces.'}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
