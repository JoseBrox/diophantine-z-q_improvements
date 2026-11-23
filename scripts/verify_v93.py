#!/usr/bin/env python3
"""Verify corrected Jones sources, shared abc contacts, and paired spectra."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT/'undecidability'


def check(relative):
    output = subprocess.run([sys.executable, '-B', str(FOLDER/relative)],
                            cwd=ROOT, check=True, text=True, capture_output=True).stdout
    result = json.loads(output)
    assert result['status'].lower() == 'pass'
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--report', type=Path)
    args = ap.parse_args()
    checks = {name: check(path) for name, path in [
        ('ceiling_power', 'verify_ceiling_power.py'),
        ('fixed_contacts', 'joint_detector_v93/verify_abc_fixed_offsets.py'),
        ('corrected_source', 'source_repair_v93/verify_corrected_source.py'),
        ('paired_spectra', 'alternative_v93/check_paired_spectral.py')]}
    ledger = json.loads((FOLDER/'results.json').read_text())
    records = {r['id']: r for r in ledger['records']}
    assert len(records) == len(ledger['records'])
    assert ledger['global_minimum_claimed'] is False
    assert ledger['inherited_arithmetic_premises_independently_proved'] is False
    quartics = {}
    for key, n, q in [('corrected-ceiling-quartic-163', 1074, 924),
                      ('corrected-ceiling-quartic-179', 1254, 1080),
                      ('corrected-fixed_offsets-quartic-56', 786, 685)]:
        r = records[key]
        path = FOLDER/r['table']
        table = json.loads(path.read_bytes())
        cert = json.loads((FOLDER/r['certificate']).read_text())
        assert r['variables'] == table['variables'] == cert['variables'] == n
        assert r['quadratic_rows'] == len(table['residuals']) == cert['quadratic_rows'] == q
        assert r['table_sha256'] == cert['table_sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
        assert r['degree'] == table['sum_of_squares_degree'] == 4
        assert r['source_universality_hypothesis'] is table['source_universality_hypothesis'] is None
        assert table['source_universality_verified'] is True
        assert table['source_coding_theorem_independently_reproved'] is False
        assert table['unconditional_undecidability_claim'] is False
        assert r['integer_certificates'] == 12 and r['integer_predicates_discarded'] == 0
        assert (FOLDER/r['proof']).with_suffix('.pdf').is_file()
        quartics[key] = {'variables': n, 'quadratic_rows': q}
    degree_certificate = json.loads((FOLDER/'alternative_v93/certificate.json').read_text())
    degree_records = {}
    for group, prefix in [('finite_wrapper', 'finite-wrapper'),
                          ('common_numerator', 'common-numerator'),
                          ('shared_integer', 'shared-integer')]:
        for route, entry in degree_certificate['degree_ledgers'][group]['routes'].items():
            key = f'paired-spectral-{prefix}-{route}'
            r = records[key]
            assert r['variables'] == entry['variables']
            assert int(r['degree_upper_bound']) == int(entry['final_degree_bound'])
            assert r['degree_strictly_less_than_power2'] == entry['final_degree_strict_power2']
            assert int(r['degree_upper_bound']) < 2**r['degree_strictly_less_than_power2']
            assert r['retains_project_arithmetic_premises'] is True
            degree_records[key] = {'variables': r['variables'],
                                   'degree_strict_power2': r['degree_strictly_less_than_power2']}
    result = {'schema': 'zq-undecidability-verification/v93', 'status': 'PASS',
              'corrected_quartics': quartics, 'degree_improvements': degree_records,
              'external_coding_theorem': 'Jones (1980), Theorem 2',
              'independent_reproof_of_coding_theorem': False,
              'old_U_em_proved': False, 'retained_arithmetic_interfaces': True,
              'independent_checks_passed': list(checks),
              'scope': 'Exact coefficient replacements and reconstruction, all contact substitutions and guards, full source-degree ledgers, nilpotent and excluded-character examples, hashes and registry. General proofs are in the manuscripts; external arithmetic is retained.'}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
