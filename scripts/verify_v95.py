#!/usr/bin/env python3
"""Verify the one-quotient Pell source, eleven-block tables, and barriers."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'undecidability'


def run(relative):
    raw = subprocess.run([sys.executable, '-B', str(FOLDER / relative)],
                         cwd=ROOT, check=True, text=True, capture_output=True).stdout
    result = json.loads(raw)
    items = result if isinstance(result, list) else [result]
    assert all(item['status'].lower() == 'pass' for item in items)
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--report', type=Path)
    args = ap.parse_args()
    checks = {name: run(path) for name, path in [
        ('general_crt', 'pell_crt_v95/verify_crt_general.py'),
        ('abc_crt', 'pell_crt_v95/verify_crt_abc.py'),
        ('y_congruence', 'pell_crt_v95/verify_y_congruence.py'),
        ('compression_barriers', 'joint_research_v94/verify_compression_barriers.py')]}
    ledger = json.loads((FOLDER / 'results.json').read_text())
    records = {r['id']: r for r in ledger['records']}
    counts = {}
    for m, n, q in [(163, 983, 855), (179, 1148, 998), (56, 734, 643)]:
        r = records[f'pell-crt-quartic-{m}']
        path = FOLDER / r['table']
        table = json.loads(path.read_bytes())
        certificate = json.loads((FOLDER / r['certificate']).read_bytes())
        assert r['variables'] == table['variables'] == certificate['variables'] == n
        assert r['quadratic_rows'] == len(table['residuals']) == certificate['quadratic_rows'] == q
        assert r['table_sha256'] == certificate['table_sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
        assert r['integer_certificates'] == table['integer_blocks'] == 11
        assert r['integer_predicates_discarded'] == 1
        assert 'o' not in table['variable_names']
        assert not any(name.startswith('int_o_') for name in table['variable_names'])
        assert ('CF' if m != 56 else 'pell_crt_cF') in table['variable_names']
        assert r['degree'] == table['sum_of_squares_degree'] == 4
        assert r['source_universality_hypothesis'] is table['source_universality_hypothesis'] is None
        assert table['source_coding_theorem_independently_reproved'] is False
        assert table['unconditional_undecidability_claim'] is False
        assert (FOLDER / r['proof']).with_suffix('.pdf').is_file()
        counts[str(m)] = {'variables': n, 'quadratic_rows': q}
    result = {'schema': 'zq-undecidability-verification/v95', 'status': 'PASS',
              'quartics': counts, 'integer_certificates': 11,
              'checks_passed': list(checks), 'retained_arithmetic_interfaces': True,
              'external_coding_theorem': 'Jones (1980), Theorem 2',
              'scope': 'Exact complete coefficient audits, private supports and global-sum substitutions, retained guards, source identities, counts, hashes and registry. Quantified Pell, finite-family, and method-boundary statements are proved in the manuscripts; finite examples are supplementary.'}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
