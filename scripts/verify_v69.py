#!/usr/bin/env python3
"""Reproduce the power-shift and actual-trace algebra, audits and search scope."""
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
POWER = 'papers/number_fields/power_shifts_and_finite_exceptions_20261117_v69.tex'
TRACE = 'negative_results/papers/pole_parameters/curves_and_abelian_families_20261117_v69.tex'
POWER_PACKAGE = 'computation/number_fields/power_shifts_v69'
TRACE_PACKAGE = 'negative_results/computation/actual_trace_curves_v69'
SEARCH = 'computation/quartic/search194_v69'
SUN = 'docs/audits/sun_v2_20261117_v69'
CONTRIBUTORS_HASH = '7c4e19ff00bd3f87f97db5ba836cea716e72fa8b583756c1a4fd7c5b5a075214'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads((ROOT/path).read_text())


def main(output):
    checks = [
        (POWER_PACKAGE, 'check.py', 'check_certificate.json', ['--manuscript', str(ROOT/POWER)]),
        (TRACE_PACKAGE, 'check.py', 'certificate.json', ['--manuscript', str(ROOT/TRACE)]),
        (SEARCH, 'check_model.py', 'model_certificate.json', []),
        (SEARCH, 'check_projection.py', 'projection_certificate.json', []),
    ]
    certificates = []
    with tempfile.TemporaryDirectory(prefix='diophantine-v69-') as directory:
        for index, (package, checker, retained, arguments) in enumerate(checks):
            target = Path(directory)/f'certificate-{index}.json'
            process = subprocess.run([sys.executable, '-B', str(ROOT/package/checker),
                *arguments, '--output', str(target)], cwd=ROOT, capture_output=True, text=True)
            if process.returncode:
                raise RuntimeError(process.stdout+process.stderr)
            assert target.read_bytes() == (ROOT/package/retained).read_bytes(), retained
            certificate = json.loads(target.read_text())
            assert certificate['status'] == 'PASS'
            certificates.append(certificate)
    power, trace, model, projection = certificates
    assert power['source_sha256']['check.py'] == digest(ROOT/POWER_PACKAGE/'check.py')
    assert power['source_sha256'][Path(POWER).name] == digest(ROOT/POWER)
    assert len(power['power_shift_examples']) == 3
    assert [x['exponent'] for x in power['power_shift_examples']] == [2, 3, 5]
    assert len(power['four_contact_boundary_examples']) == 6
    assert trace['source_sha256'] == digest(ROOT/TRACE)
    assert trace['checker_sha256'] == digest(ROOT/TRACE_PACKAGE/'check.py')
    assert len(trace['contacts_and_infinity']['contacts']) == 18
    assert trace['contacts_and_infinity']['rational_infinity_ordinates'] == [-2, 2]
    assert trace['balanced_boundary_checks']['exact_Laurent_cases'] == 200
    assert len(trace['general_contacts']['contacts']) == 10
    assert trace['general_contacts']['scalar_second_summand_has_exact_R_power_five']
    assert trace['general_contacts']['first_cover_genus_bound_from_Riemann_Hurwitz'] == 4
    review = read(TRACE_PACKAGE+'/independent_review.json')
    assert review['status'] == 'PASS' and review['manuscript_sha256'] == digest(ROOT/TRACE)
    assert review['review_sha256'] == digest(ROOT/TRACE_PACKAGE/'independent_review.md')
    assert review['independent_arithmetic_sha256'] == digest(ROOT/TRACE_PACKAGE/'independent_arithmetic.json')
    assert review['native_guard_sha256'] == digest(ROOT/review['native_guard_file'])
    provenance = read(TRACE_PACKAGE+'/provenance.json')
    for path, expected in provenance['internal_source_sha256'].items():
        assert digest(ROOT/path) == expected, path
    arithmetic = read(TRACE_PACKAGE+'/independent_arithmetic.json')
    assert arithmetic['point_counts_mod17'] == {'9': 20, '13': 16}
    assert arithmetic['first_contact_derivatives'] == [x['R_derivative'] for x in trace['general_contacts']['contacts']]
    assert model['reference_change_rank'] == 8 and len(model['models']) == 3
    assert projection['unit_bases'] == 32 and projection['incompatible_pairs'] == 128
    assert projection['real_coordinate_weights_already_excluded']
    assert not projection['integer_weight_parity_needed']
    for name, expected in projection['input_model_sha256'].items():
        assert digest(ROOT/SEARCH/'models'/(name+'.json')) == expected
    for item in read(SEARCH+'/MANIFEST.json')['files']:
        path = ROOT/SEARCH/item['path']
        assert path.stat().st_size == item['bytes'] and digest(path) == item['sha256'], item['path']
    for result in read(SEARCH+'/rerun.json')['results']:
        assert result['status'] == 'unsat' and result['nominal_coordinates'] == 194
        assert result['integer_weights_unbounded'] and result['extra_unit_candidates'] == 32

    audit = read(SUN+'/audit.json')
    manifest = read(SUN+'/publication_manifest.json')
    assert manifest['audit_sha256'] == digest(ROOT/SUN/'audit.json')
    for name, expected in manifest['source_sha256'].items():
        if name == Path(POWER).name:
            path = ROOT/POWER
        elif name in ('check.py', 'check_certificate.json'):
            path = ROOT/POWER_PACKAGE/name
        else:
            path = ROOT/SUN/name
        assert digest(path) == expected, name
    power_review = read(SUN+'/independent_power_shift_review.json')
    assert power_review['status'] == 'PASS' and power_review['sha256'] == digest(ROOT/POWER)
    assert audit['counts']['sun_v2_without_extra_abc']['total'] == 27
    assert audit['counts']['sun_v2_ordinary_abc']['total'] == 17
    assert len(audit['arithmetic_suppliers_not_recursively_certified']) == 5
    assert audit['sun_scoped_refinements']['odd_chart_deletion']['generic_branch_rank_new'] == 2**24

    criteria = read('data/criteria_20261117_v69.json')
    assert criteria['current_construction_records'] == 'data/results_20261117_v68.json'
    assert criteria['unchanged_counts'] == dict(general=25, ordinary_abc=11,
        general_quartic=195, ordinary_abc_quartic=68, explicit_quartic=229)
    for key in ('new_defining_polynomial_count', 'targets_21_and_9_proved',
                'number_field_counterexample_established', 'all_number_fields_definition_established',
                'arithmetic_foundations_complete_independent_audit'):
        assert criteria[key] is False, key
    theorem = criteria['power_shift_theorem']
    assert theorem['ring_total_coordinates'] == 'd*N'
    assert theorem['ring_single_equation_degree_bound'] == '2*d*D'
    assert theorem['square_shift_extra_coordinates'] == 0
    catalog = {x['id']: x for x in read('negative_results/data/results.json')['theorems']}
    assert catalog['actual_trace_curves_and_abelian_families'] == criteria['actual_trace_obstruction']
    builds = read('data/audits/tex_build_20261117_v69.json')['papers']
    assert {x['paper'] for x in builds} == {POWER, TRACE}
    for build in builds:
        assert build['source_sha256'] == digest(ROOT/build['paper'])
        assert build['returncode'] == 0 and build['warnings'] == []
        assert build['pages'] > 0 and build['all_rendered_pages_reviewed']
    readme = (ROOT/'README.md').read_text()
    section = re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)', readme)
    assert section and hashlib.sha256(section.group().encode()).hexdigest() == CONTRIBUTORS_HASH
    for name in ('README.md', 'negative_results/README.md'):
        text = (ROOT/name).read_text()
        assert '$' not in text and r'\operatorname' not in text, name
    assert 'docs/results_20261117_v69.md' in readme
    record_link = re.search(r'\[results JSON\]\((data/results_[^)]*\.json)\)', readme)
    assert record_link
    latest = read(record_link.group(1))
    assert not latest['targets_21_and_9_proved']
    assert not latest['arithmetic_foundations_complete_independent_audit']

    report = dict(schema='diophantine-exact-verification/v69', status='PASS',
        python=platform.python_version(), current_records=criteria['current_construction_records'],
        source_sha256={p: digest(ROOT/p) for p in (POWER, TRACE)},
        certificate_sha256={p+'/'+c: digest(ROOT/p/c) for p, _, c, _ in checks},
        independent_mathematical_reviews_pinned=True, split_prime_avoidance_examples=3,
        derivative_contacts=18, general_contacts=10, Laurent_regression_cases=200,
        quartic_search_support_models=3, independent_two_factor_cases=128,
        global_variable_lower_bound_asserted=False, new_defining_count=False,
        targets_21_and_9_proved=False, all_number_fields_definition_established=False,
        arithmetic_foundations_independently_audited=False,
        contribution_and_citation_section_sha256=CONTRIBUTORS_HASH)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    main(parser.parse_args().report)
