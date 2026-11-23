#!/usr/bin/env python3
"""Reproduce local detector and point-role algebra certificates with scoped records."""
import argparse
import hashlib
import json
import platform
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = [
    'papers/quartic/revised_detector_factors_20261117_v66.tex',
    'negative_results/papers/integer_labels/point_role_restrictions_20261117_v66.tex',
]
PACKAGES = [
    'computation/quartic/local_detector_factors_v66',
    'negative_results/computation/point_roles_v66',
]
CONTRIBUTORS_HASH = '7c4e19ff00bd3f87f97db5ba836cea716e72fa8b583756c1a4fd7c5b5a075214'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(output):
    certificates = []
    with tempfile.TemporaryDirectory(prefix='diophantine-v66-') as directory:
        temporary = Path(directory)
        for i, package in enumerate(PACKAGES):
            target = temporary / f'certificate-{i}.json'
            result = subprocess.run([sys.executable, '-B', str(ROOT / package / 'check.py'),
                '--output', str(target)], cwd=ROOT, capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError(result.stdout + result.stderr)
            retained = ROOT / package / 'certificate.json'
            assert target.read_bytes() == retained.read_bytes(), package
            certificate = json.loads(target.read_text())
            assert certificate['status'] == 'PASS'
            assert certificate['checker_sha256'] == digest(ROOT / package / 'check.py')
            certificates.append(certificate)
    factors, points = certificates
    assert factors['source_sha256'] == digest(ROOT / PAPERS[0])
    assert factors['residue_period_complete'] == 8
    assert len(factors['residue_partitions']) == 16
    assert len(factors['strict_thresholds']) == 7
    assert len(factors['selected_contact_bounds']) == 5
    assert factors['zero_test_terms_may_be_omitted']
    assert factors['alternating_pairing_arithmetic_passes']
    assert not factors['new_polynomial_or_variable_count_proved']
    conics = points['conic_and_resultants']
    assert conics['universal_quadratic_resultant_identity']
    assert conics['actual_degree_drop_identities']
    assert conics['fully_generic_total_degree_two_relation']
    for stratum, degree in [('quadratic_in_b', 8), ('linear_in_b', 6), ('constant_in_b', 4)]:
        certificate = conics['resultant_degree_certificates'][stratum]
        assert certificate['degree_in_a_n_together'] == degree
        assert certificate['degree_in_t'] == 4
    assert points['scalar_contacts_and_forced_prime']['scalar_product_squarefree_over_Q']
    assert points['shifted_Lucas']['exact_integer_cases'] == 282
    assert points['shifted_Lucas']['matrix_power_independently_matches_recurrence']
    assert points['shifted_Lucas']['universal_matrix_identity_mod_a_minus_1_squared']

    criteria = json.loads((ROOT / 'data/criteria_20261117_v66.json').read_text())
    assert criteria['current_construction_records'] == 'data/results_20261117_v65.json'
    assert criteria['unchanged_counts'] == dict(general=25, ordinary_abc=11,
        general_quartic=195, ordinary_abc_quartic=68, explicit_quartic=229)
    for key in ('new_defining_polynomial_count', 'targets_21_and_9_proved',
                'number_field_counterexample_established', 'all_number_fields_definition_established',
                'arithmetic_foundations_complete_independent_audit'):
        assert criteria[key] is False, key
    catalog = {item['id']: item for item in json.loads(
        (ROOT / 'negative_results/data/results.json').read_text())['theorems']}
    assert criteria['point_role_restrictions'] == catalog['quadratic_point_role_restrictions']
    assert not criteria['point_role_restrictions']['arbitrary_numerator_index_families_excluded']
    assert not criteria['shifted_Lucas_coupling']['joint_prime_trace_scale_and_real_realization']
    assert not criteria['local_detector_factors']['complete_new_quadratic_table']

    audit = json.loads((ROOT / 'data/audits/point_roles_independent_review_20261117_v66.json').read_text())
    assert audit['status'] == 'PASS'
    assert audit['published_manuscript_sha256'] == digest(ROOT / PAPERS[1])
    assert all(audit['manual_checks'].values())
    for source, source_hash in audit['source_sha256'].items():
        assert digest(ROOT / source.removeprefix('repo/')) == source_hash
    assert audit['checker_rerun']['sha256'] == digest(ROOT / PACKAGES[1] / 'check.py')
    assert audit['checker_rerun']['output_sha256'] == digest(ROOT / PACKAGES[1] / 'certificate.json')

    builds = json.loads((ROOT / 'data/audits/tex_build_20261117_v66.json').read_text())
    assert {row['paper'] for row in builds['papers']} == set(PAPERS)
    for row in builds['papers']:
        assert row['returncode'] == 0 and row['warnings'] == []
        assert row['source_sha256'] == digest(ROOT / row['paper'])
        assert row['pages'] > 0 and row['all_rendered_pages_reviewed']
    readme = (ROOT / 'README.md').read_text()
    section = re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)', readme)
    assert section and hashlib.sha256(section.group().encode()).hexdigest() == CONTRIBUTORS_HASH
    assert 'docs/results_20261117_v66.md' in readme
    historical_guide = (ROOT / 'docs/results_20261117_v66.md').read_text()
    assert 'data/results_20261117_v65.json' in historical_guide
    assert r'\(' not in readme and r'\[' not in readme

    report = dict(schema='diophantine-exact-verification/v66', status='PASS',
        python=platform.python_version(),
        current_records=criteria['current_construction_records'],
        criteria='data/criteria_20261117_v66.json',
        source_sha256={paper: digest(ROOT / paper) for paper in PAPERS},
        certificate_sha256={package: digest(ROOT / package / 'certificate.json') for package in PACKAGES},
        local_arithmetic=dict(all_odd_depths=True, finite_residue_partitions=16,
            exact_thresholds=7, selected_factors=5, complete_quadratic_table=False),
        point_role_algebra=dict(generic_quadratic_relation=True,
            resultant_parameter_degree_bounds=[8,6,4], Lucas_integer_specializations=282,
            independent_matrix_evaluation=True),
        construction_records_unchanged=True, targets_21_and_9_proved=False,
        shifted_coupling_joint_realization_proved=False,
        arithmetic_foundations_independently_audited=False,
        contribution_and_citation_section_sha256=CONTRIBUTORS_HASH)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    main(parser.parse_args().report)
