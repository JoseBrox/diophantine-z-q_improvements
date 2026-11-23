#!/usr/bin/env python3
"""Verify the short Pell power source and its complete thirteen-input tables."""
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
        ('power_lemmas', 'pell_power_v97/verify_power_lemmas.py'),
        ('abc_complete_table', 'pell_power_v97/verify_power_abc.py'),
        ('general_complete_table', 'pell_power_v97/verify_power_general.py')]}
    ledger = json.loads((FOLDER / 'results.json').read_text())
    records = {r['id']: r for r in ledger['records']}
    assert len(records) == len(ledger['records'])
    counts = {}
    for m, n, q in [(163, 979, 829), (56, 704, 595)]:
        record = records[f'pell-power-quartic-{m}']
        path = FOLDER / record['table']
        table = json.loads(path.read_bytes())
        cert = json.loads((FOLDER / record['certificate']).read_bytes())
        assert record['variables'] == table['variables'] == cert['variables'] == n
        assert record['quadratic_rows'] == len(table['residuals']) == cert['quadratic_rows'] == q
        assert record['table_sha256'] == cert['table_sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
        assert record['outer_coordinates'] == table['outer_coordinates']
        assert record['outer_quadratic_rows'] == table['outer_residuals']
        assert record['integer_certificates'] == table['integer_blocks'] == 13
        assert record['integer_predicates_added'] == 2
        assert all(name in table['ordinary_integer_inputs'] for name in ('power_delta', 'power_alpha'))
        assert 'o' not in table['variable_names']
        assert not any(name.startswith('ceiling_power_') for name in table['variable_names'])
        assert record['degree'] == table['sum_of_squares_degree'] == 4
        assert record['instance_tail'] == 'x > 32*z for fixed positive integer z'
        assert record['source_universality_hypothesis'] is None
        assert table['source_coding_theorem_independently_reproved'] is False
        assert table['unconditional_undecidability_claim'] is False
        assert (FOLDER / record['proof']).with_suffix('.pdf').is_file()
        counts[str(m)] = {'variables': n, 'quadratic_rows': q, 'table_sha256': record['table_sha256']}
    assert records['halftrace-quartic-179']['variables'] == 1147
    assert not any('adaptive' in key for key in records)
    result = {'schema': 'zq-undecidability-verification/v97', 'status': 'PASS',
              'new_quartics': counts, 'specified_quartic_unchanged': 1147,
              'checks_passed': list(checks), 'local_source_equivalence_proved': True,
              'retained_arithmetic_interfaces': True,
              'fixed_general_parameter_may_be_increased': True,
              'external_coding_theorem': 'Jones (1980), Theorem 2',
              'quartic_target_263_established': False,
              'adaptive_contact_candidate_promoted': False,
              'scope': 'Complete source and certificate coefficients, all removed supports and unchanged rows, independently expanded new integer blocks, global-sum and fixed-offset changes, guards, parameter rings, counts, hashes and registry. Quantified source and finite-family proofs are in the manuscript.'}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
