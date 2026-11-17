#!/usr/bin/env python3
"""Reproduce the full auxiliary-point eleven-coordinate construction."""
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
PACKAGE = 'computation/few_variables/full_auxiliary11_v71'
PAPER = 'papers/conditional_few_variables/full_auxiliary11_20261117_v71.tex'
CONTRIBUTORS_HASH = 'bec5e749954eb50b1206e43bc7b27462419ac135762f820a201e528b222b3285'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(arguments):
    result = subprocess.run([sys.executable, '-B', *map(str, arguments)],
                            cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)


def main(report_path):
    package = ROOT / PACKAGE
    with tempfile.TemporaryDirectory(prefix='diophantine-v71-') as directory:
        target = Path(directory) / 'specification'
        run([package/'build_source.py', '--repo', ROOT, '--name',
             'ordinary_abc11_full_auxiliary', '--parameter', '3', '--output', target])
        for name in ('source.json', 'subalgebra_parent.json', 'polynomial.json',
                     'construction.json'):
            assert (target/name).read_bytes() == (package/'specification'/name).read_bytes(), name
        certificate = Path(directory)/'independent.json'
        run([package/'check.py', '--repo', ROOT, '--specification', target,
             '--output', certificate])
        assert certificate.read_bytes() == (package/'specification/independent_certificate.json').read_bytes()
    checked = json.loads((package/'specification/independent_certificate.json').read_text())
    construction = json.loads((package/'specification/construction.json').read_text())
    assert checked['status'] == 'PASS'
    assert checked['degree_bound'] == 232094337
    assert checked['coefficient_log2_l1_bound'] == 487256960
    assert checked['characters'] == 384 and checked['corruption_controls_rejected'] == 2
    assert not checked['nine_coordinate_completeness_claimed']
    assert construction['nodes'] == 1990 and construction['guards'] == 32
    assert checked['universal_point_algebra']['auxiliary_stage_degrees'] == [6, 9]
    assert checked['elementary_point_bounds']['coefficient_l1'] == [30, 22]
    assert checked['elementary_point_bounds']['basis_scales'] == [1, 16, 16, 80]
    assert 1 + 128*(1526992 + 286244 + 1) == 232094337

    records = json.loads((ROOT/'data/results_20261117_v71.json').read_text())
    current = {item['id']: item for item in records['current_constructions']}
    ordinary = current['ordinary_abc11']
    assert ordinary['variables'] == 11 and int(ordinary['degree_upper_bound']) == 232094337
    assert ordinary['proof'] == PAPER and ordinary['auxiliary_indices_half_integral']
    assert ordinary['source_integer_arithmetic_nodes'] == 1990
    assert ordinary['recorded_guard_numerators'] == 32
    assert ordinary['retained_subalgebra_norm_factors'] == 38
    assert ordinary['finite_algebra_rank'] == 128 and ordinary['terminal_zero_allowed']
    previous = json.loads((ROOT/'data/results_20261117_v68.json').read_text())
    old = {item['id']: item for item in previous['current_constructions']}
    for name, item in current.items():
        if name != 'ordinary_abc11':
            assert item == old[name], name
    assert int(ordinary['degree_upper_bound']) < int(old['ordinary_abc11']['degree_upper_bound'])
    for key in ('new_variable_reduction', 'targets_21_and_9_proved',
                'number_field_counterexample_established', 'all_number_fields_definition_established',
                'arithmetic_foundations_complete_independent_audit'):
        assert records[key] is False, key

    review = json.loads((package/'independent_review.json').read_text())
    assert review['status'] == 'PASS' and review['manuscript_sha256'] == digest(ROOT/PAPER)
    assert review['review_sha256'] == digest(package/'independent_review.md')
    assert review['certificate_sha256'] == digest(package/'specification/independent_certificate.json')
    assert review['checker_sha256'] == digest(package/'check.py')
    assert review['producer_sha256'] == digest(package/'build_source.py')
    builds = json.loads((ROOT/'data/audits/tex_build_20261117_v71.json').read_text())['papers']
    assert len(builds) == 1
    build = builds[0]
    assert build['paper'] == PAPER and build['source_sha256'] == digest(ROOT/PAPER)
    assert build['returncode'] == 0 and build['warnings'] == []
    assert build['pages'] == 4 and build['all_rendered_pages_reviewed']
    readme = (ROOT/'README.md').read_text()
    section = re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)', readme)
    assert section and hashlib.sha256(section.group().encode()).hexdigest() == CONTRIBUTORS_HASH
    for name in ('README.md', 'negative_results/README.md', PACKAGE+'/README.md'):
        text = (ROOT/name).read_text()
        assert '$' not in text and r'\operatorname' not in text, name
    assert '232,094,337' in readme and '234,157,441' not in readme
    record_link = re.search(r'\[results JSON\]\((data/results_[^)]*\.json)\)', readme)
    assert record_link
    latest = json.loads((ROOT/record_link.group(1)).read_text())
    latest_11 = next(row for row in latest['current_constructions']
                     if row['id'] == 'ordinary_abc11')
    assert latest_11 == ordinary
    assert 'docs/results_20261117_v71.md' in readme
    report = dict(schema='diophantine-exact-verification/v71', status='PASS',
        python=platform.python_version(), current_records='data/results_20261117_v71.json',
        manuscript_sha256=digest(ROOT/PAPER), coefficient_fixture_parameter=3,
        polynomial_specification_sha256=digest(package/'specification/polynomial.json'),
        native_source_sha256=digest(package/'specification/source.json'),
        degree_upper_bound=232094337, total_variables=11, point_characters_checked=384,
        complete_integer_family_under_retained_premises=True,
        global_nine_variable_realization_proved=False,
        arithmetic_foundations_complete_independent_audit=False)
    if report_path:
        Path(report_path).write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report')
    main(parser.parse_args().report)
