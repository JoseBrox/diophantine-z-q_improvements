#!/usr/bin/env python3
"""Verify signed first-Pell projection and complete sign-square deletion."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'undecidability'


def read_check(name):
    raw = subprocess.run([sys.executable, '-B', str(FOLDER /
                         'pell_signed_branch_v101' / name)],
                         cwd=ROOT, check=True, text=True, capture_output=True).stdout
    result = json.loads(raw)
    entries = result if isinstance(result, list) else [result]
    assert all(e['status'] == 'PASS' for e in entries)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    read_check('verify_signed_branch_lemmas.py')
    assert len(read_check('verify_signed_branch.py')) == 2
    ledger = json.loads((FOLDER / 'results.json').read_text())
    records = {r['id']: r for r in ledger['records']}
    assert len(records) == len(ledger['records'])
    counts = {}
    for m, n, q in [(163, 970, 825), (56, 695, 590)]:
        record = records[f'signed-branch-quartic-{m}']
        path = FOLDER / record['table']
        table = json.loads(path.read_bytes())
        cert = json.loads((FOLDER / record['certificate']).read_bytes())
        old = records[record['predecessor_record']]
        assert record['variables'] == table['variables'] == cert['variables'] == n
        assert record['quadratic_rows'] == len(table['residuals']) == cert['quadratic_rows'] == q
        assert record['table_sha256'] == cert['table_sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
        assert record['outer_coordinates'] == table['outer_coordinates'] == 76
        assert record['outer_quadratic_rows'] == table['outer_residuals'] == 52
        assert record['integer_certificates'] == table['integer_blocks'] == 13
        assert record['coordinates_saved_in_this_step'] == old['variables'] - n == 1
        assert record['quadratic_rows_saved_in_this_step'] == old['quadratic_rows'] - q == 1
        assert record['degree'] == table['sum_of_squares_degree'] == 4
        assert record['first_Pell_sign_square_deleted'] is True
        assert record['positive_source_witnesses_reconstructed'] is True
        assert 'pell_d_positive_square' not in table['variable_names']
        assert cert['pell_signed_branch_same_auxiliary_lift_claim'] is False
        assert record['source_universality_hypothesis'] is None
        assert table['source_coding_theorem_independently_reproved'] is False
        assert record['unconditional_undecidability_claim'] is False
        assert (FOLDER / record['proof']).with_suffix('.pdf').is_file()
        counts[str(m)] = {'variables': n, 'quadratic_rows': q, 'table_sha256': record['table_sha256']}
    assert records['aggregate-spacing-quartic-179']['variables'] == 1145
    result = {'schema': 'zq-undecidability-verification/v101', 'status': 'PASS',
              'new_quartics': counts, 'specified_quartic_unchanged': 1145,
              'projection_equivalence_only': True, 'same_signed_auxiliary_lift_claim': False,
              'retained_arithmetic_interfaces': True,
              'external_coding_theorem': 'Jones (1980), Theorem 2',
              'quartic_target_263_established': False,
              'scope': 'Exact zero-s divisibility, signed recurrences, alternating sums and bound fixtures, full removed-coordinate occurrence audit, every unchanged row, degree, current/historical sign metadata, counts, hashes and registry. The manuscript proves quantified coding projection.'}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
