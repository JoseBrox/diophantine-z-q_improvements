#!/usr/bin/env python3
"""Check the half-trace guard absorption and all current quartic records."""
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
    raw = subprocess.run([sys.executable, '-B', str(FOLDER / 'pell_halftrace_v96/verify_halftrace.py')],
                         cwd=ROOT, check=True, text=True, capture_output=True).stdout
    checked = json.loads(raw)
    assert checked['status'].lower() == 'pass'
    quotient_raw = subprocess.run(
        [sys.executable, '-B', str(FOLDER / 'joint_research_v94/verify_quotient_merging.py')],
        cwd=ROOT, check=True, text=True, capture_output=True).stdout
    assert json.loads(quotient_raw)['status'].lower() == 'pass'
    ledger = json.loads((FOLDER / 'results.json').read_text())
    records = {r['id']: r for r in ledger['records']}
    assert len(records) == len(ledger['records'])
    counts = {}
    for m, n, q in [(163, 982, 854), (179, 1147, 997), (56, 733, 642)]:
        r = records[f'halftrace-quartic-{m}']
        path = FOLDER / r['table']
        table = json.loads(path.read_bytes())
        cert = json.loads((FOLDER / r['certificate']).read_bytes())
        assert r['variables'] == table['variables'] == cert['variables'] == n
        assert r['quadratic_rows'] == len(table['residuals']) == cert['quadratic_rows'] == q
        assert r['table_sha256'] == cert['table_sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
        assert r['outer_coordinates'] == table['outer_coordinates']
        assert r['outer_quadratic_rows'] == table['outer_residuals']
        assert r['integer_certificates'] == table['integer_blocks'] == 11
        assert 's_inverse' not in table['variable_names']
        assert 'jones1980.s.nonzero' not in {row['name'] for row in table['residuals']}
        assert r['degree'] == table['sum_of_squares_degree'] == 4
        assert table['source_universality_hypothesis'] is None
        assert table['source_coding_theorem_independently_reproved'] is False
        assert table['unconditional_undecidability_claim'] is False
        assert (FOLDER / r['proof']).with_suffix('.pdf').is_file()
        counts[str(m)] = {'variables': n, 'quadratic_rows': q,
                          'table_sha256': r['table_sha256']}
    result = {'schema': 'zq-undecidability-verification/v96', 'status': 'PASS',
              'quartics': counts, 'local_equivalence_unconditional': True,
              'undecidability_retains_arithmetic_interfaces': True,
              'external_coding_theorem': 'Jones (1980), Theorem 2',
              'quotient_checkpoint_exact_checks': 'PASS',
              'quartic_target_263_established': False,
              'scope': 'All new coefficient rows and private supports, deleted inverse guard, polynomial identities, signed fixtures, counts, degree, hashes and current registry. The manuscript proves the quantified source equivalence.'}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
