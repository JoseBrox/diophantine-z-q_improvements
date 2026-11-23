#!/usr/bin/env python3
"""Reproduce physical coordinate maps and exact Laurent support obstructions."""
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
PACKAGE = 'negative_results/computation/physical_detector_scaling_v67'
PAPER = 'negative_results/papers/quartic/physical_detector_scaling_20261117_v67.tex'
CONTRIBUTORS_HASH = '7c4e19ff00bd3f87f97db5ba836cea716e72fa8b583756c1a4fd7c5b5a075214'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(output):
    package = ROOT / PACKAGE
    commands = [
        ('check.py', 'certificate.json', []),
        ('check_mapping.py', 'mapping_certificate.json', ['--repo', str(ROOT)]),
        ('check_mapping_independent.py', 'mapping_independent_certificate.json',
         ['--repo', str(ROOT)]),
        ('check_support_independent.py', 'independent_audit.json',
         ['--package', str(package),
          '--source', str(ROOT / 'computation/quartic/affine_laurent195_v45/quadratic-family.json'),
          '--mapping-certificate', str(package / 'mapping_independent_certificate.json'),
          '--manuscript', str(ROOT / PAPER)]),
    ]
    certificates = []
    with tempfile.TemporaryDirectory(prefix='diophantine-v67-') as directory:
        for checker, retained, arguments in commands:
            target = Path(directory) / retained
            process = subprocess.run([sys.executable, '-B', str(package / checker),
                *arguments, '--output', str(target)], cwd=ROOT, capture_output=True, text=True)
            if process.returncode:
                raise RuntimeError(process.stdout + process.stderr)
            assert target.read_bytes() == (package / retained).read_bytes(), retained
            certificate = json.loads(target.read_text())
            assert certificate['status'] == 'PASS'
            if 'checker_sha256' in certificate:
                assert certificate['checker_sha256'] == digest(package / checker)
            for path, source_hash in certificate.get('input_sha256', {}).items():
                assert digest(ROOT / path) == source_hash
            certificates.append(certificate)

    support, selected, independent, audit = certificates
    assert support['source_table_rechecked']
    assert support['literal_reference_terms_checked'] == 2
    assert support['field_factor_terms_checked'] == 8
    assert support['full_square_multiplier_witnesses_checked'] == 3
    assert support['nonnegative_inequalities'] == 10
    assert support['physical_contact_directions'] == {'q0': [1, 0], 'q1': [1, 1]}
    assert support['model_sha256'] == digest(package / 'model.json')
    assert support['farkas_sha256'] == digest(package / 'farkas_certificate.json')
    for basis, rhs, bound in [('original', -12, 6), ('modified', -20, 2)]:
        result = support['results'][basis]
        assert result['exact_Farkas_contradiction'] == f'0 <= {rhs}'
        assert result['forced_row_weight_difference'] == 12
        assert result['constant_row_weight_bound'] == bound
        assert result['shared_special_factor_difference_excluded'] == [0, -3]

    assert selected['physical_weight_directions'] == {'first': [1, 0], 'second': [1, 1]}
    assert len(selected['physical_factor_output_maps']) == 20
    for record in selected['physical_factor_output_maps']:
        assert record['unit_exponent_in_u_v'] == [1, 2 * record['detector']]
        assert record['C_exponent'] == [1, 1, 1, 0, -1][record['factor']]
    assert independent['physical_contacts'] == {'q0': 'u', 'q1': 'u*v'}
    assert len(independent['source_coordinate_maps']) == 198
    assert independent['literal_consumer_rows_checked'] == 71
    assert len(independent['consumer_checks']) == 71
    assert independent['factor_parameter_powers'] == [1, 1, 1, 0, -1]
    assert independent['partial_product_parameter_powers'] == [3, 4, 3]
    assert audit['manuscript_sha256'] == digest(ROOT / PAPER)
    assert audit['full_mapping_certificate_sha256'] == digest(package / 'mapping_independent_certificate.json')
    assert audit['independent_mapping_checker_sha256'] == digest(package / 'check_mapping_independent.py')
    assert audit['independent_support_checker_sha256'] == digest(package / 'check_support_independent.py')
    assert audit['full_square_forcing_verified']
    assert audit['four_row_proof_independent_of_all_other_model_rows']
    assert audit['weight_components'] == 20 and audit['weighted_left_side'] == 'identically zero'
    assert audit['basis_results']['original']['weighted_rhs'] == -12
    assert audit['basis_results']['modified']['weighted_rhs'] == -20
    for path, source_hash in audit['package_sha256'].items():
        assert digest(package / path) == source_hash

    criteria = json.loads((ROOT / 'data/criteria_20261117_v67.json').read_text())
    assert criteria['current_construction_records'] == 'data/results_20261117_v65.json'
    assert criteria['unchanged_counts'] == dict(general=25, ordinary_abc=11,
        general_quartic=195, ordinary_abc_quartic=68, explicit_quartic=229)
    for key in ('new_defining_polynomial_count', 'targets_21_and_9_proved',
                'number_field_counterexample_established', 'all_number_fields_definition_established',
                'arithmetic_foundations_complete_independent_audit'):
        assert criteria[key] is False, key
    catalog = {item['id']: item for item in json.loads(
        (ROOT / 'negative_results/data/results.json').read_text())['theorems']}
    theorem = catalog['physical_detector_Laurent_scaling']
    assert criteria['physical_scaling_obstruction'] == theorem
    assert theorem['unbounded_real_weights']
    assert not theorem['general_variable_lower_bound']
    assert not theorem['arbitrary_factor_pairings_excluded']
    assert not theorem['row_combinations_excluded']

    builds = json.loads((ROOT / 'data/audits/tex_build_20261117_v67.json').read_text())
    assert len(builds['papers']) == 1
    build = builds['papers'][0]
    assert build['paper'] == PAPER and build['source_sha256'] == digest(ROOT / PAPER)
    assert build['returncode'] == 0 and build['warnings'] == []
    assert build['pages'] > 0 and build['all_rendered_pages_reviewed']
    readme = (ROOT / 'README.md').read_text()
    section = re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)', readme)
    assert section and hashlib.sha256(section.group().encode()).hexdigest() == CONTRIBUTORS_HASH
    assert 'docs/results_20261117_v67.md' in readme
    historical_guide = (ROOT / 'docs/results_20261117_v67.md').read_text()
    assert 'data/results_20261117_v65.json' in historical_guide
    assert r'\(' not in readme and r'\[' not in readme

    report = dict(schema='diophantine-exact-verification/v67', status='PASS',
        python=platform.python_version(), current_records=criteria['current_construction_records'],
        criteria='data/criteria_20261117_v67.json',
        source_sha256={PAPER: digest(ROOT / PAPER)},
        certificate_sha256={retained: digest(package / retained) for _, retained, _ in commands},
        checker_sha256={checker: digest(package / checker) for checker, _, _ in commands},
        source_coordinates_composed=198, literal_consumer_equations_checked=71,
        physical_factor_output_components_checked=20,
        physical_contacts={'q0': 'u', 'q1': 'u*v'},
        nonnegative_integer_inequalities=10, exact_Farkas_rhs=[-12, -20],
        bounded_search_used=False, general_variable_lower_bound=False,
        construction_records_unchanged=True, targets_21_and_9_proved=False,
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
