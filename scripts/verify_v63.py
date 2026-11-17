#!/usr/bin/env python3
"""Reproduce the current derivative, height and contact-obstruction certificates."""
from pathlib import Path
from fractions import Fraction
import argparse
import hashlib
import json
import platform
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PAPERS = [
    'papers/conditional_few_variables/derivative_detector11_20261117_v63.tex',
    'papers/effective_sums/elliptic_sum_heights_over_number_fields_20261117_v63.tex',
    'papers/number_fields/finite_exceptions_and_integrality_20261117_v63.tex',
    'negative_results/papers/pole_parameters/six_contact_mobius_obstruction_20261117_v63.tex',
    'negative_results/papers/number_fields/rank_stable_adjacent_contacts_20261117_v63.tex',
]
HEIGHT = 'computation/effective_sums/cyclic_number_fields_v63'
NEGATIVE = 'negative_results/computation/six_contact_mobius_v63'
CONTRIBUTORS_HASH = 'bec5e749954eb50b1206e43bc7b27462419ac135762f820a201e528b222b3285'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(script, *arguments):
    result = subprocess.run([sys.executable, '-B', str(ROOT / script),
                             *map(str, arguments)], cwd=ROOT,
                            capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)


def main(output):
    with tempfile.TemporaryDirectory(prefix='diophantine-v63-') as temporary:
        tmp = Path(temporary)
        run('scripts/verify_derivative11_v63.py', '--report', tmp / 'derivative.json')
        derivative = json.loads((tmp / 'derivative.json').read_text())
        certificates = {}
        for name, package in [('height', HEIGHT), ('coupling', NEGATIVE)]:
            target = tmp / (name + '.json')
            run(package + '/check.py', '--output', target)
            assert target.read_bytes() == (ROOT / package / 'certificate.json').read_bytes(), name
            certificates[name] = json.loads(target.read_text())
        independent_path = tmp / 'coupling-independent.json'
        run(NEGATIVE + '/check_independent.py', '--output', independent_path)
        assert independent_path.read_bytes() == (
            ROOT / NEGATIVE / 'independent_review_certificate.json').read_bytes()
        independent = json.loads(independent_path.read_text())
        chart_path = tmp / 'scaled-chart.json'
        chart_package = 'computation/elliptic_charts/scaled_single_point_audit_v63'
        run(chart_package + '/check.py', '--output', chart_path)
        assert chart_path.read_bytes() == (ROOT / chart_package / 'certificate.json').read_bytes()

    assert derivative['status'] == 'PASS'
    assert derivative['construction']['variables'] == 11
    assert derivative['construction']['degree_upper_bound'] == 234157441
    assert derivative['construction']['monomials_strict_power_two'] == 264
    assert derivative['construction']['finite_rank'] == 128
    assert derivative['actual_character_evaluations'] == 384
    assert derivative['all_source_denominators_independently_checked']
    assert not derivative['targets_21_and_9_proved']
    assert not derivative['external_foundations_independently_audited']
    alpha = Fraction(997, 1001)
    q = Fraction(501, 997)
    margin = Fraction(297, 200) - q * (Fraction(201, 100) + 1 / (2 * alpha))
    assert margin == Fraction(44272779, 198801800) > 0
    assert 1 + 128 * (1541062 + 288292 + 1) == 234157441 < 2**28

    height = certificates['height']
    assert height['status'] == 'PASS'
    assert height['source_sha256'] == digest(ROOT / PAPERS[1])
    assert height['X_coefficient_recursion_order'] == 18
    assert height['special_j1728_logarithm_verified']
    assert [r['r'] for r in height['subset_constants']] == list(range(1, 11))
    for row in height['subset_constants']:
        r = row['r']
        assert row['log_M_coefficient'] == (r - 1) * 2**(r - 1)

    coupling = certificates['coupling']
    assert coupling['status'] == 'PASS'
    assert coupling['source_sha256'] == digest(ROOT / PAPERS[3])
    assert coupling['checker_sha256'] == digest(ROOT / NEGATIVE / 'check.py')
    assert coupling['group']['ordered_image_triples'] == 120
    assert len(coupling['group']['automorphisms']) == 12
    assert len(coupling['uniform_gap_recurrence_certificates']) == 10
    fixtures = coupling['simultaneous_finite_menu']['fixtures']
    assert [row['exponent'] for row in fixtures] == [4, 5, 6, 7, 8, 10, 12, 16, 32]
    assert all(row['contact_valuation'] == 1 for row in fixtures)
    assert all(row['prime'] > 76176 for row in fixtures)
    assert independent['status'] == 'PASS'
    assert independent['source_sha256'] == coupling['source_sha256']
    assert independent['independent_one_step_recurrence_checks'] == 630
    assert len(independent['prime_fixtures']) == 9

    current = json.loads((ROOT / 'data/results_20261117_v63.json').read_text())
    previous = json.loads((ROOT / 'data/results_20261117_v62.json').read_text())
    now = {row['id']: row for row in current['current_constructions']}
    then = {row['id']: row for row in previous['current_constructions']}
    improved = now.pop('ordinary_abc11')
    earlier = then.pop('ordinary_abc11')
    assert now == then
    assert improved['variables'] == earlier['variables'] == 11
    assert int(improved['degree_upper_bound']) == 234157441 < int(earlier['degree_upper_bound'])
    assert improved['degree_power_two_strict'] == 28
    assert improved['monomials_strict_power_two'] == 264
    assert improved['proof'] == PAPERS[0]
    assert improved['terminal_zero_allowed'] and improved['subalgebra_norms']
    assert improved['source_integer_arithmetic_nodes'] == 2003
    assert not current['new_variable_reduction'] and current['new_degree_improvement']
    assert not current['new_coefficient_improvement']
    assert not current['arithmetic_foundations_complete_independent_audit']
    assert current['new_eleven_source']['k'] == 9
    assert current['new_eleven_source']['prime_positions'] == 18
    assert current['new_eleven_source']['height_margin'] == str(margin)
    assert not current['new_eleven_source']['actual_nine_variable_realization_proved']
    assert not current['native_square_realization']['proved']
    assert not current['trace_conic_realization']['proved']
    assert not current['number_fields']['counterexample_established']
    assert not current['number_fields']['all_number_fields_theorem_established']
    auxiliaries = {row['id']: row for row in current['new_auxiliary_theorems']}
    assert auxiliaries['cyclic_elliptic_sum_heights_all_number_fields']['proof'] == PAPERS[1]
    assert auxiliaries['finite_exception_integrality_criterion']['proof'] == PAPERS[2]
    catalog = {row['id']: row for row in json.loads(
        (ROOT / 'negative_results/data/results.json').read_text())['theorems']}
    for row in current['new_negative_results']:
        assert row == catalog[row['id']]
    assert {row['id'] for row in current['new_negative_results']} == {
        'six_contact_mobius_all_integer_powers', 'rank_stable_adjacent_contacts'}
    assert not catalog['six_contact_mobius_all_integer_powers']['all_nine_variable_sources_excluded']
    assert not catalog['rank_stable_adjacent_contacts']['number_field_counterexample']

    readme = (ROOT / 'README.md').read_text()
    section = re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)', readme)
    assert section and hashlib.sha256(section.group().encode()).hexdigest() == CONTRIBUTORS_HASH
    assert r'\(' not in readme and r'\[' not in readme
    assert (ROOT / 'data/results_20261117_v63.json').is_file()
    assert (ROOT / 'docs/results_20261117_v63.md').is_file()
    record_link = re.search(r'\[results JSON\]\((data/results_[^)]*\.json)\)', readme)
    assert record_link
    latest = json.loads((ROOT / record_link.group(1)).read_text())
    current_11 = next(row for row in latest['current_constructions']
                      if row['id'] == 'ordinary_abc11')
    assert current_11['variables'] == 11
    assert int(current_11['degree_upper_bound']) <= 234157441
    assert f"{int(current_11['degree_upper_bound']):,}" in readme and '**229**' in readme

    builds = json.loads((ROOT / 'data/audits/tex_build_20261117_v63.json').read_text())
    assert {row['paper'] for row in builds['papers']} == set(PAPERS)
    for row in builds['papers']:
        assert row['returncode'] == 0 and row['warnings'] == []
        assert row['source_sha256'] == digest(ROOT / row['paper'])
        assert row['all_rendered_pages_reviewed'] and row['pages'] > 0

    report = {
        'schema': 'diophantine-exact-verification/v63', 'status': 'PASS',
        'python': platform.python_version(),
        'current_records': 'data/results_20261117_v63.json',
        'retained_records': 'data/results_20261117_v62.json',
        'source_sha256': {path: digest(ROOT / path) for path in PAPERS},
        'derivative_source': derivative,
        'height_series_order': height['X_coefficient_recursion_order'],
        'coupling_symmetries': 12, 'coupling_prime_fixtures': len(fixtures),
        'independent_gap_controls': 630,
        'coupling_exponent_scope': 'Every integer e>=4; every fixed finite menu.',
        'field_transfer_lemmas': 'Proof-reviewed; no number-field definition claimed.',
        'all_current_variable_counts_unchanged': True,
        'targets_21_and_9_proved': False,
        'number_field_counterexample_established': False,
        'all_number_fields_definition_established': False,
        'arithmetic_foundations_independently_audited': False,
        'contribution_and_citation_section_sha256': CONTRIBUTORS_HASH,
    }
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    main(parser.parse_args().report)
