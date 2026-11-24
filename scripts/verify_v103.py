#!/usr/bin/env python3
"""Verify the shared-denominator quartics and the scoped source checkpoint."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'undecidability'


def run(relative):
    process = subprocess.run([sys.executable, '-B', str(FOLDER / relative)],
                             cwd=ROOT, check=True, capture_output=True, text=True)
    return json.loads(process.stdout)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    contact = run('quadratic_reduction_v103/verify_contact_denominator.py')
    frontier = run('source_frontier_v103/verify_source_frontier.py')
    assert len(contact['results']) == 2
    assert all(r['status'] == 'PASS' for r in contact['results'])
    assert frontier['integer_predicates_removed'] == 0
    assert frontier['new_polynomial_universal_source_compiled'] is False
    ledger = json.loads((FOLDER / 'results.json').read_text())
    records = {r['id']: r for r in ledger['records']}
    assert len(records) == len(ledger['records'])
    for m, n, q, count in ((163, 963, 818, 14), (179, 1140, 991, 12)):
        record = records[f'contact-denominator-quartic-{m}']
        predecessor = records[record['predecessor_record']]
        path = FOLDER / record['table']
        data = json.loads(path.read_text())
        certificate = json.loads((FOLDER / record['certificate']).read_text())
        assert record['variables'] == data['variables'] == certificate['variables'] == n
        assert record['quadratic_rows'] == len(data['residuals']) == certificate['quadratic_rows'] == q
        assert record['table_sha256'] == certificate['table_sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
        assert record['coordinates_saved_in_this_step'] == predecessor['variables'] - n == count - 9
        assert record['quadratic_rows_saved_in_this_step'] == predecessor['quadratic_rows'] - q == count - 9
        assert record['contact_denominator_contact_count'] == count
        assert record['integer_certificates'] == data['integer_blocks']
        assert record['degree'] == data['sum_of_squares_degree'] == 4
        assert record['source_universality_hypothesis'] is None
        assert record['unconditional_undecidability_claim'] is False
        assert (FOLDER / record['proof']).with_suffix('.pdf').is_file()
    result = {
        'schema': 'zq-undecidability-verification/v103', 'status': 'PASS',
        'new_quartics': contact['results'], 'abc_quartic_unchanged_at_this_stage': 695,
        'contact_zero_set_equivalence': 'bijective rational reconstruction',
        'integer_predicates_removed_by_source_checkpoint': 0,
        'retained_arithmetic_interfaces': True, 'quartic_target_263_established': False,
        'scope': 'Exact polynomial identities, all coefficient rows and guards, counts, degrees, hashes, registry, and scoped finite source-frontier checks. Inherited arithmetic premises and external coding theorem are not independently proved.'}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
