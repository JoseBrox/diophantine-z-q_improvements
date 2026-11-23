#!/usr/bin/env python3
"""Reconstruct the 193-coordinate quartic, exact transfers and improved heights."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = 'computation/quartic/seven_units193_v74'
PREVIOUS = 'computation/quartic/cleared_comparisons194_v73'
PAPER = 'papers/quartic/quartic193_20261117_v74.tex'
CONTRIBUTORS_HASH = '7c4e19ff00bd3f87f97db5ba836cea716e72fa8b583756c1a4fd7c5b5a075214'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def run(directory, *args):
    result = subprocess.run([sys.executable, '-B', *args], cwd=directory,
                            capture_output=True, text=True)
    if result.returncode:
        print(result.stdout[-3000:], file=sys.stderr)
        print(result.stderr[-6000:], file=sys.stderr)
        raise AssertionError(args)


def verify(output=None):
    package = ROOT / PACKAGE
    manifest = read(package / 'manifest.json')
    for name, checksum in manifest.items():
        assert digest(package / name) == checksum, name
    original_files = {}
    for variant in ['primitive', 'fewer_monomials', 'compact', 'compact_fewer_monomials']:
        for path in (package / variant).glob('*.json'):
            original_files[str(path.relative_to(package))] = path.read_bytes()
    for name in ['support-certificate.json', 'arithmetic-certificate.json', 'transfer-certificate.json']:
        original_files[name] = (package / name).read_bytes()
    with tempfile.TemporaryDirectory(prefix='quartic193-v74-') as temporary:
        base = Path(temporary)
        copied = base / 'seven_units193_v74'
        shutil.copytree(package, copied)
        shutil.copytree(ROOT / PREVIOUS, base / 'cleared_comparisons194_v73')
        run(copied, 'build.py')
        run(copied, 'verify_height.py')
        run(copied, 'check_support.py', '--output', 'support-certificate.json')
        run(copied, 'check_arithmetic.py')
        for variant, option in [('primitive', ['--primitive-reference']), ('fewer_monomials', [])]:
            run(copied, 'check.py', '--folder', variant, *option,
                '--output', variant + '/independent-verification.json')
        run(copied, 'build_scaled.py')
        run(copied, 'check_scaled.py')
        run(copied, 'check_transfer.py')
        for name, raw in original_files.items():
            assert (copied / name).read_bytes() == raw, name
    variants = []
    expected = [('compact', 2770, 2775, 6), ('compact_fewer_monomials', 2626, 2631, 13)]
    for variant, monomials, terms, crossover in expected:
        report = read(package / variant / 'independent-verification.json')
        assert report['status'] == 'PASS' and report['variables'] == 193
        assert report['quadratic_rows'] == 167 and report['degree'] == 4
        assert report['content'] == 1 and report['every_coordinate_occurs']
        assert report['all_parameter_pullbacks_exact'] and report['input_unchanged']
        assert report['all_rows_primitive_for_C_149_power_N']
        assert report['changed_noninput_coordinates'] == 12
        assert report['quartic_parameter_degree'] == 2
        assert report['coordinate_monomials_for_all_N_ge_1'] == monomials
        assert report['parameter_separated_terms'] == terms
        assert report['exact_height']['coefficient_crossover_N'] == crossover
        assert report['exact_height']['crossover_is_not_defining_threshold']
        variants.append({'basis': variant, 'monomials': monomials,
                         'parameter_separated_terms': terms,
                         'height': report['exact_height']['formula'],
                         'quartic_sha256': digest(package / variant / 'polynomial-family.json')})
    for variant in ['primitive', 'fewer_monomials']:
        r = read(package / variant / 'independent-verification.json')
        assert r['explicit_physical_component_rows'] == r['retained_source_rows'] == 81
        assert r['normalized_quadratic_rows'] == 167 and r['literal_unit_guards'] == 5
        assert r['all_row_pullbacks_exact'] and r['independent_sum_of_squares_expansion']
    transfer = read(package / 'transfer-certificate.json')
    assert transfer['status'] == 'PASS' and transfer['bijection_on_entire_rational_zero_set']
    assert transfer['input_coordinate_fixed'] and transfer['new_arithmetic_assumptions'] == []
    assert transfer['same_sufficient_parameter_threshold_as_v73']
    assert not transfer['sufficient_numerical_defining_threshold_known']
    for variant in transfer['variants']:
        assert variant['physical_rows_identical_to_v73'] == 162
        assert variant['factor_assignments_unchanged']
    arithmetic = read(package / 'arithmetic-certificate.json')
    assert arithmetic['status'] == 'PASS' and len(arithmetic['factor_table']) == 10
    assert arithmetic['homogeneous_lucas_identity']
    review = read(package / 'independent_review.json')
    assert review['status'] == 'PASS'
    assert review['unit_chart']['all_zero_strata_excluded_by_literal_unit_equations']
    assert review['unit_chart']['total_coordinates_including_input'] == 193
    assert review['unit_chart']['total_quadratic_rows'] == 167
    assert review['v73_transfer']['correct_old_coordinate_map_power'] == 'new_weight - old_weight'
    assert review['v73_transfer']['transfer_receipt_matches_stored_report']
    for name, checksum in review['sha256'].items():
        assert digest(ROOT / name) == checksum, name
    for reviewed, expected_variant in zip(review['exact_coefficient_reconstruction']['variants'], expected):
        assert reviewed['variant'] == expected_variant[0]
        assert reviewed['coordinate_support'] == expected_variant[1]
        assert reviewed['parameter_separated_terms'] == expected_variant[2]
        assert reviewed['independent_squared_row_expansion']
    records = read(ROOT / 'data/results_20261117_v74.json')
    previous_records = read(ROOT / 'data/results_20261117_v73.json')
    previous = {x['id']: x for x in previous_records['current_constructions']}
    current = {x['id']: x for x in records['current_constructions']}
    prior = previous.pop('quartic194')
    new = current.pop('quartic193')
    assert current == previous
    assert records['superseded_constructions']['quartic194'] == prior
    assert new['variables'] == 193 and new['quadratic_rows'] == 167
    assert new['proof'] == PAPER and new['data'] == PACKAGE
    assert not new['parameter_effective']
    for field in ['targets_21_and_9_proved', 'all_number_fields_definition_established',
                  'number_field_counterexample_established',
                  'arithmetic_foundations_complete_independent_audit']:
        assert records[field] is False, field
    build = read(ROOT / 'data/audits/tex_build_20261117_v74.json')['papers']
    assert len(build) == 1
    assert build[0]['paper'] == PAPER and build[0]['source_sha256'] == digest(ROOT / PAPER)
    assert build[0]['returncode'] == 0 and build[0]['warnings'] == []
    assert build[0]['pages'] > 0 and build[0]['all_rendered_pages_reviewed']
    readme = (ROOT / 'README.md').read_text()
    section = re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)', readme)
    assert section and hashlib.sha256(section.group().encode()).hexdigest() == CONTRIBUTORS_HASH
    historical_guide = (ROOT / 'docs/results_20261117_v74.md').read_text()
    for value in ['193 total variables', '2,770', '2,626']:
        assert value in historical_guide
    assert 'docs/results_20261117_v74.md' in readme
    link = re.search(r'\[historical results JSON\]\((data/results_20261117_v75\.json)\)', readme)
    assert link
    latest = read(ROOT / link.group(1))
    assert next(r for r in latest['current_constructions'] if r['id'] == 'quartic193') == new
    for name in ['README.md', PACKAGE + '/README.md', 'docs/results_20261117_v74.md']:
        text = (ROOT / name).read_text()
        assert '$' not in text and r'\operatorname' not in text, name
    report = {
        'schema': 'diophantine-exact-verification/v74', 'status': 'PASS',
        'python': platform.python_version(), 'total_variables': 193,
        'quadratic_rows': 167, 'degree': 4, 'integer_content': 1,
        'physical_component_rows_unchanged': 162, 'unit_coordinates': 7,
        'unit_equations': 5, 'parameter_rescaled_coordinates': 12,
        'quartic_parameter_degree': 2, 'variants': variants,
        'manuscript_sha256': digest(ROOT / PAPER),
        'independent_new_claims_review': 'PASS',
        'complete_integer_family_under_retained_premises': True,
        'sufficient_defining_parameter_effective': False,
        'global_21_or_9_realization_proved': False,
        'arithmetic_foundations_complete_independent_audit': False,
    }
    if output:
        Path(output).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report')
    verify(parser.parse_args().report)
