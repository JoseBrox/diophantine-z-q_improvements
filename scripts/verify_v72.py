#!/usr/bin/env python3
"""Reproduce the full auxiliary general twenty-five-variable construction."""
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
PACKAGE = 'computation/few_variables/full_auxiliary25_v72'
PAPER = 'papers/few_variables25/full_auxiliary25_20261117_v72.tex'
CONTRIBUTORS_HASH = 'bec5e749954eb50b1206e43bc7b27462419ac135762f820a201e528b222b3285'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(arguments):
    result = subprocess.run([sys.executable, '-B', *map(str, arguments)],
                            cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)


def main(report_path):
    package = ROOT/PACKAGE
    with tempfile.TemporaryDirectory(prefix='diophantine-v72-') as directory:
        target = Path(directory)/'specification'
        run([package/'build_source.py', '--repo', ROOT, '--name', 'general25',
             '--parameter', '3', '--output', target])
        for name in ('source.json', 'subalgebra_parent.json', 'polynomial.json', 'construction.json'):
            assert (target/name).read_bytes() == (package/'specification'/name).read_bytes(), name
        certificate = Path(directory)/'independent.json'
        run([package/'check.py', '--repo', ROOT, '--specification', target, '--output', certificate])
        assert certificate.read_bytes() == (package/'specification/independent_certificate.json').read_bytes()
    checked = json.loads((package/'specification/independent_certificate.json').read_text())
    construction = json.loads((package/'specification/construction.json').read_text())
    assert checked['status'] == 'PASS' and checked['variables'] == 25
    assert checked['degree_bound'] == 4924857429000192
    assert construction['bounds']['coefficient_log2_l1_bound'] == 34765159307149312
    assert checked['native_character_evaluations'] == 72 and not checked['all_characters_exhausted']
    assert checked['corruption_controls_rejected'] == 2 and not checked['general21_realization_claimed']
    assert construction['nodes'] == 6169 and construction['guards'] == 101
    assert checked['point_algebra']['auxiliary_stage_degrees'] == [6, 9]
    assert 1048576*(4696539189 + 170852 + 1) == 4924857429000192

    records = json.loads((ROOT/'data/results_20261117_v72.json').read_text())
    current = {item['id']: item for item in records['current_constructions']}
    general = current['general25']
    assert general['variables'] == 25 and int(general['degree_upper_bound']) == 4924857429000192
    assert general['proof'] == PAPER and general['auxiliary_indices_half_integral']
    assert general['root_point_roles'] == 4 and general['auxiliary_point_roles'] == 5
    assert general['source_integer_arithmetic_nodes'] == 6169
    assert general['recorded_guard_numerators'] == 101
    assert general['retained_subalgebra_norm_factors'] == 128
    assert general['finite_algebra_rank'] == 1048576 and general['terminal_zero_allowed']
    previous = json.loads((ROOT/'data/results_20261117_v71.json').read_text())
    old = {item['id']: item for item in previous['current_constructions']}
    for name, item in current.items():
        if name != 'general25':
            assert item == old[name], name
    assert int(general['degree_upper_bound']) < int(old['general25']['degree_upper_bound'])
    for key in ('new_variable_reduction', 'targets_21_and_9_proved',
                'number_field_counterexample_established', 'all_number_fields_definition_established',
                'arithmetic_foundations_complete_independent_audit'):
        assert records[key] is False, key

    review = json.loads((package/'independent_review.json').read_text())
    for key, path in [('manuscript_sha256', ROOT/PAPER), ('review_sha256', package/'independent_review.md'),
                      ('certificate_sha256', package/'specification/independent_certificate.json'),
                      ('checker_sha256', package/'check.py'), ('producer_sha256', package/'build_source.py')]:
        assert review[key] == digest(path), key
    assert review['status'] == 'PASS' and not review['twenty_one_coordinate_completeness_proved']
    builds = json.loads((ROOT/'data/audits/tex_build_20261117_v72.json').read_text())['papers']
    assert len(builds) == 1
    build = builds[0]
    assert build['paper'] == PAPER and build['source_sha256'] == digest(ROOT/PAPER)
    assert build['returncode'] == 0 and build['warnings'] == []
    assert build['pages'] == 3 and build['all_rendered_pages_reviewed']
    readme = (ROOT/'README.md').read_text()
    section = re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)', readme)
    assert section and hashlib.sha256(section.group().encode()).hexdigest() == CONTRIBUTORS_HASH
    for name in ('README.md', 'negative_results/README.md', PACKAGE+'/README.md'):
        text = (ROOT/name).read_text()
        assert '$' not in text and r'\operatorname' not in text, name
    assert '4,924,857,429,000,192' in readme and '5,059,009,872,658,432' not in readme
    assert 'data/results_20261117_v72.json' in readme and 'docs/results_20261117_v72.md' in readme
    report = dict(schema='diophantine-exact-verification/v72', status='PASS',
        python=platform.python_version(), current_records='data/results_20261117_v72.json',
        manuscript_sha256=digest(ROOT/PAPER), coefficient_fixture_parameter=3,
        polynomial_specification_sha256=digest(package/'specification/polynomial.json'),
        native_source_sha256=digest(package/'specification/source.json'),
        degree_upper_bound=4924857429000192, total_variables=25, sampled_point_characters_checked=72,
        all_point_characters_exhausted=False, complete_integer_family_under_retained_premises=True,
        global_twenty_one_variable_realization_proved=False,
        arithmetic_foundations_complete_independent_audit=False)
    if report_path:
        Path(report_path).write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report')
    main(parser.parse_args().report)
