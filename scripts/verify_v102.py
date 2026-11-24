#!/usr/bin/env python3
"""Verify contact endpoint reuse and the scoped c-integrality obstruction."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'undecidability'


def run(name):
    raw = subprocess.run([sys.executable, '-B', str(FOLDER / name)],
                         cwd=ROOT, check=True, text=True, capture_output=True).stdout
    return json.loads(raw)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    endpoint = run('contact_endpoint_v102/verify_contact_endpoint.py')
    assert len(endpoint['tables']) == 2
    assert all(e['status'] == 'PASS' for e in endpoint['tables'])
    obstruction = run('c_integrality_checkpoint_v102/verify_c_obstruction.py')
    assert obstruction['status'] == 'PASS'
    assert obstruction['full_source_counterexample_claim'] is False
    assert obstruction['c_integer_predicate_removed'] is False
    assert obstruction['variable_saving_claim'] == 0
    ledger = json.loads((FOLDER / 'results.json').read_text())
    records = {r['id']: r for r in ledger['records']}
    assert len(records) == len(ledger['records'])
    counts = {}
    for m, n, q, blocks in [(163, 968, 823, 13), (179, 1143, 994, 11)]:
        record = records[f'contact-endpoint-quartic-{m}']
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
        assert record['coordinates_saved_in_this_step'] == old['variables'] - n == 2
        assert record['quadratic_rows_saved_in_this_step'] == old['quadratic_rows'] - q == 2
        assert record['degree'] == table['sum_of_squares_degree'] == 4
        assert record['contact_endpoint_reused_at_index'] == 16
        assert record['guarded_contact_rechart_coordinates'] == 4
        assert record['source_universality_hypothesis'] is None
        assert table['source_coding_theorem_independently_reproved'] is False
        assert record['unconditional_undecidability_claim'] is False
        assert (FOLDER / record['proof']).with_suffix('.pdf').is_file()
        counts[str(m)] = {'variables': n, 'quadratic_rows': q, 'table_sha256': record['table_sha256']}
    assert records['signed-branch-quartic-56']['variables'] == 695
    assert any(x['id'] == 'nonintegral_c_three_Pell_subsystem'
               for x in ledger['proved_obstructions'])
    result = {'schema': 'zq-undecidability-verification/v102', 'status': 'PASS',
              'new_quartics': counts, 'abc_quartic_unchanged': 695,
              'exact_guarded_zero_set_equivalence': True,
              'c_predicate_retained': True, 'full_source_c_question_open': True,
              'retained_arithmetic_interfaces': True,
              'quartic_target_263_established': False,
              'scope': 'Four-coordinate Laurent rechart, two affine eliminations, two omitted-row identities, all changed/unchanged coefficients and guards, counts, degree, hashes, registry, exact nonintegral norm-subsystem counterfamily and scoped local Hensel fixtures.'}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
