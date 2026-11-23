#!/usr/bin/env python3
"""Verify signed power recovery, the absorbed Pell bound and complete tables."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'undecidability'


def run(path):
    raw = subprocess.run([sys.executable, '-B', str(FOLDER / path)],
                         cwd=ROOT, check=True, text=True, capture_output=True).stdout
    result = json.loads(raw)
    items = result if isinstance(result, list) else [result]
    assert all(item['status'].lower() == 'pass' for item in items)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    checks = {name: run(path) for name, path in [
        ('signed_power_and_margin_lemmas', 'pell_signed_q_v98/verify_signed_q_lemmas.py'),
        ('complete_table_transformation', 'pell_signed_q_v98/verify_signed_q.py')]}
    ledger = json.loads((FOLDER / 'results.json').read_text())
    records = {r['id']: r for r in ledger['records']}
    assert len(records) == len(ledger['records'])
    counts = {}
    for m, n, q, saved in [(163, 973, 827, 6), (56, 697, 592, 7)]:
        record = records[f'signed-power-quartic-{m}']
        path = FOLDER / record['table']
        table = json.loads(path.read_bytes())
        cert = json.loads((FOLDER / record['certificate']).read_bytes())
        old = records[record['predecessor_record']]
        assert record['variables'] == table['variables'] == cert['variables'] == n
        assert record['quadratic_rows'] == len(table['residuals']) == cert['quadratic_rows'] == q
        assert record['table_sha256'] == cert['table_sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
        assert record['outer_coordinates'] == table['outer_coordinates'] == 78
        assert record['outer_quadratic_rows'] == table['outer_residuals'] == 54
        assert record['integer_certificates'] == table['integer_blocks'] == 13
        assert record['coordinates_saved_in_this_step'] == old['variables'] - n == saved
        assert record['quadratic_rows_saved_in_this_step'] == old['quadratic_rows'] - q
        assert record['added_integer_predicates_in_this_step'] == 0
        assert record['degree'] == table['sum_of_squares_degree'] == 4
        assert record['signed_power_recovery'] and record['absorbed_Pell_bound']
        assert record['abc_fourth_power_register_reused'] == (m == 56)
        assert not any(name.startswith(('power_positive_q_', 'power_positive_bound_'))
                       for name in table['variable_names'])
        assert ('power_b4' in table['variable_names']) == (m == 163)
        assert record['source_universality_hypothesis'] is None
        assert table['source_coding_theorem_independently_reproved'] is False
        assert table['unconditional_undecidability_claim'] is False
        assert (FOLDER / record['proof']).with_suffix('.pdf').is_file()
        counts[str(m)] = {'variables': n, 'quadratic_rows': q, 'table_sha256': record['table_sha256']}
    assert records['halftrace-quartic-179']['variables'] == 1147
    result = {'schema': 'zq-undecidability-verification/v98', 'status': 'PASS',
              'new_quartics': counts, 'specified_quartic_unchanged': 1147,
              'checks_passed': list(checks), 'local_source_equivalence_proved': True,
              'retained_arithmetic_interfaces': True,
              'external_coding_theorem': 'Jones (1980), Theorem 2',
              'quartic_target_263_established': False,
              'scope': 'Exact signed prefix and margin checks, all removed supports, strengthened eta row, reused abc fourth power, unchanged coefficients, complete counts, degree, hashes and registry. The manuscript proves the quantified arithmetic implications.'}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
