#!/usr/bin/env python3
"""Audit signed positivity, affine contacts, and their complete compositions."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'undecidability'


def check(path):
    raw = subprocess.run([sys.executable, '-B', str(FOLDER / path)],
                         cwd=ROOT, check=True, text=True, capture_output=True).stdout
    result = json.loads(raw)
    results = result if isinstance(result, list) else [result]
    assert all(r['status'].lower() == 'pass' for r in results)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    checks = {name: check(path) for name, path in [
        ('signed_source', 'source_repair_v93/verify_signed_positivity.py'),
        ('affine_contacts', 'general_contact_v94/verify_affine_contacts.py'),
        ('signed_affine_composition', 'general_contact_v94/verify_signed_affine_contacts.py')]}
    records = {r['id']: r for r in json.loads((FOLDER / 'results.json').read_text())['records']}
    counts = {}
    for key, n, q in [('signed-affine-quartic-163', 1043, 907),
                      ('signed-affine-quartic-179', 1223, 1063),
                      ('signed-fixed_offsets-quartic-56', 781, 684)]:
        record = records[key]
        path = FOLDER / record['table']
        table = json.loads(path.read_bytes())
        certificate = json.loads((FOLDER / record['certificate']).read_bytes())
        assert record['variables'] == table['variables'] == certificate['variables'] == n
        assert record['quadratic_rows'] == len(table['residuals']) == certificate['quadratic_rows'] == q
        assert record['table_sha256'] == certificate['table_sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
        assert record['outer_coordinates'] == table['outer_coordinates']
        assert record['outer_quadratic_rows'] == table['outer_residuals']
        assert record['degree'] == table['sum_of_squares_degree'] == 4
        assert record['integer_certificates'] == table['integer_blocks'] == 12
        assert record['integer_predicates_discarded'] == 0
        assert table['source_universality_hypothesis'] is None
        assert table['source_coding_theorem_independently_reproved'] is False
        assert table['unconditional_undecidability_claim'] is False
        assert table['M_recovery'] == 'sr'
        assert table['a_recovery'] == '(U+1)*sr'
        assert (FOLDER / record['proof']).with_suffix('.pdf').is_file()
        counts[key] = {'variables': n, 'quadratic_rows': q}
    result = {'schema': 'zq-undecidability-verification/v94', 'status': 'PASS',
              'quartics': counts, 'independent_checks_passed': list(checks),
              'source_coding_theorem': 'Jones (1980), Theorem 2',
              'independent_coding_reproof': False, 'retained_arithmetic_interfaces': True,
              'scope': 'All coefficient substitutions, omitted-row identities, private positivity occurrences, guards, disjoint composition supports, hashes, counts, registry and source qualifications. The manuscripts prove the general signed and arithmetic assertions.'}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
