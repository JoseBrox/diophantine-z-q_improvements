#!/usr/bin/env python3
"""Check the single actual-trace criterion without asserting its realization."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = 'computation/pole_parameters/single_trace_v64'
PAPERS = [
    'papers/pole_parameters/single_trace_derivative_criterion_20261117_v64.tex',
    'negative_results/papers/pole_parameters/cofinite_mobius_coupling_obstruction_20261117_v64.tex',
]
SOURCE_COMMIT = 'f70057ffce6b8318a79a7e3648779067fd98c2e3'
CONTRIBUTORS_HASH = 'bec5e749954eb50b1206e43bc7b27462419ac135762f820a201e528b222b3285'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(output):
    with tempfile.TemporaryDirectory(prefix='diophantine-v64-') as directory:
        target = Path(directory) / 'certificate.json'
        result = subprocess.run([sys.executable, '-B', str(ROOT / PACKAGE / 'check.py'),
                                 '--output', str(target)], cwd=ROOT,
                                capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)
        assert target.read_bytes() == (ROOT / PACKAGE / 'certificate.json').read_bytes()
        certificate = json.loads(target.read_text())
    assert certificate['status'] == 'PASS'
    assert certificate['derivative_source_commit'] == SOURCE_COMMIT
    assert certificate['checker_sha256'] == digest(ROOT / PACKAGE / 'check.py')
    assert certificate['cleared_trace_identity']
    assert certificate['reference_trace_radicand'] == 4
    assert certificate['point_algebra_relation_signs'] == [1, 1, 1, -1, -1, 1]
    assert certificate['comparison_test_signs'] == [1, 1, 1, 1, -1, -1]
    assert certificate['balanced_test_and_product_invariant']
    assert not certificate['uniform_actual_trace_realization_proved']

    criteria = json.loads((ROOT / 'data/criteria_20261117_v64.json').read_text())
    target = criteria['single_derivative_trace']
    assert target['proof'] == PAPERS[0] and target['data'] == PACKAGE
    assert target['source_commit'] == SOURCE_COMMIT
    assert target['conditional_total_variables'] == 9
    assert target['finite_algebra_rank'] == 128
    assert target['radicand'] == 'V^2+w*(2-V)'
    assert target['positive_tail_realization_sufficient']
    assert target['additional_variables_for_finite_completion'] == 0
    assert target['all_denominator_and_whole_character_guards_verified']
    assert target['terminal_zero_allowed']
    for key in ['uniform_actual_trace_realization_proved',
                'cofinite_actual_trace_realization_proved',
                'all_prime_local_solubility_proved',
                'nine_variable_definition_established',
                'general_21_transfer_of_derivative_height_proved']:
        assert not target[key]
    assert not criteria['new_defining_variable_bound']
    assert not criteria['general_target_21_proved']
    negative = criteria['cofinite_coupling']
    assert negative['proof'] == PAPERS[1]
    assert negative['exact_root_prescription'] == 'A=[n]P at X=n'
    assert negative['infinite_positive_input_progression']
    assert negative['finite_input_repairs_excluded']
    assert negative['common_input_progression_after_coefficient_refinement']
    assert not negative['all_fixed_coefficient_shifts_excluded']
    assert not negative['all_nine_variable_sources_excluded']
    catalog = json.loads((ROOT / 'negative_results/data/results.json').read_text())
    assert next(row for row in catalog['theorems'] if row['id'] == negative['id']) == negative

    current = json.loads((ROOT / criteria['current_construction_records']).read_text())
    counts = {row['id']: row['variables'] for row in current['current_constructions']}
    assert counts == dict(general25=25, quartic195=195, explicit27=27,
                          explicit_quartic229=229, weak13=13, abc13=13,
                          abc_quartic71=71, ordinary_abc11=11)
    assert not current['trace_conic_realization']['proved']
    assert not current['number_fields']['all_number_fields_theorem_established']

    builds = json.loads((ROOT / 'data/audits/tex_build_20261117_v64.json').read_text())
    assert {row['paper'] for row in builds['papers']} == set(PAPERS)
    for row in builds['papers']:
        assert row['returncode'] == 0 and row['warnings'] == []
        assert row['source_sha256'] == digest(ROOT / row['paper'])
        assert row['all_rendered_pages_reviewed'] and row['pages'] > 0
    readme = (ROOT / 'README.md').read_text()
    section = re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)', readme)
    assert section and hashlib.sha256(section.group().encode()).hexdigest() == CONTRIBUTORS_HASH
    assert 'data/criteria_20261117_v64.json' in readme
    assert 'data/results_20261117_v63.json' in readme

    report = dict(schema='diophantine-criteria-verification/v64', status='PASS',
                  python=platform.python_version(), derivative_source_commit=SOURCE_COMMIT,
                  source_sha256={path: digest(ROOT / path) for path in PAPERS},
                  exact_trace_and_sign_identities_verified=True,
                  point_algebra_relations_checked=6,
                  sound_source_conditional_count=9,
                  finite_completion_additional_coordinates=0,
                  uniform_actual_trace_realization_proved=False,
                  cofinite_actual_trace_realization_proved=False,
                  new_defining_variable_count_proved=False,
                  current_defining_counts=counts,
                  cofinite_coupling_scope=negative['scope'],
                  all_fixed_shifts_obstructed=False,
                  contribution_and_citation_section_sha256=CONTRIBUTORS_HASH)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    main(parser.parse_args().report)
