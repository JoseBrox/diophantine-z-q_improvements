#!/usr/bin/env python3
"""Verify vertical trace algebra and the exact sequential-unit obstruction."""
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
TRACE = 'negative_results/papers/pole_parameters/vertical_and_fixed_slope_20261117_v70.tex'
CURVES = 'negative_results/papers/pole_parameters/curves_and_abelian_families_20261117_v69.tex'
UNITS = 'negative_results/papers/quartic/sequential_unit_detector_obstruction_20261117_v70.tex'
TP = 'negative_results/computation/actual_trace_vertical_v70'
UP = 'negative_results/computation/sequential_units_v70'
HALF = 'negative_results/papers/elliptic_charts/half_scalar_helper_20261117_v70.tex'
HP = 'negative_results/computation/half_scalar_helper_v70'
ARITHMETIC = 'papers/pole_parameters/actual_trace_arithmetic_20261117_v70.tex'
AP = 'computation/pole_parameters/actual_trace_arithmetic_v70'
CONTRIBUTORS_HASH = 'bec5e749954eb50b1206e43bc7b27462419ac135762f820a201e528b222b3285'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads((ROOT/path).read_text())


def run(arguments):
    result = subprocess.run([sys.executable, '-B', *map(str, arguments)],
                            cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout


def main(output):
    checks = [(TP, ['--manuscript', ROOT/TRACE]), (UP, []),
              (HP, ['--manuscript', ROOT/HALF]), (AP, ['--manuscript', ROOT/ARITHMETIC])]
    with tempfile.TemporaryDirectory(prefix='diophantine-v70-') as directory:
        for i, (package, arguments) in enumerate(checks):
            target = Path(directory)/f'certificate-{i}.json'
            run([ROOT/package/'check.py', *arguments, '--output', target])
            assert target.read_bytes() == (ROOT/package/'certificate.json').read_bytes(), package
        half_result = Path(directory)/'half-independent.json'
        run([ROOT/HP/'check_independent.py', '--certificate', ROOT/HP/'certificate.json',
             '--output', half_result])
        assert half_result.read_bytes() == (ROOT/HP/'independent_certificate.json').read_bytes()
        arithmetic_source = Path(directory)/'arithmetic-source'
        arithmetic_source.mkdir()
        for name in ('check.py', 'certificate.json'):
            (arithmetic_source/name).write_bytes((ROOT/AP/name).read_bytes())
        (arithmetic_source/Path(ARITHMETIC).name).write_bytes((ROOT/ARITHMETIC).read_bytes())
        arithmetic_result = Path(directory)/'arithmetic-independent.json'
        run([ROOT/AP/'check_independent.py', '--source', arithmetic_source, '--output', arithmetic_result])
        assert arithmetic_result.read_bytes() == (ROOT/AP/'independent_certificate.json').read_bytes()
    trace = read(TP+'/certificate.json')
    assert trace['status'] == 'PASS'
    assert trace['source_sha256'] == digest(ROOT/TRACE)
    assert trace['checker_sha256'] == digest(ROOT/TP/'check.py')
    assert trace['collision_slopes'] == 35 and trace['minimum_distinct_roots'] == 9
    assert len(trace['affine_contact_derivatives']) == 4
    review = read(TP+'/independent_review.json')
    assert review['status'] == 'PASS' and review['manuscript_sha256'] == digest(ROOT/TRACE)
    assert review['depends_on_frozen_v69_sha256'] == digest(ROOT/CURVES)
    assert review['review_sha256'] == digest(ROOT/TP/'independent_review.md')
    assert review['checker_replay']['checker_sha256'] == digest(ROOT/TP/'check.py')
    assert review['checker_replay']['certificate_sha256'] == digest(ROOT/TP/'certificate.json')
    provenance = read(TP+'/provenance.json')
    assert provenance['manuscript_sha256'] == digest(ROOT/TRACE)
    assert provenance['checker_sha256'] == digest(ROOT/TP/'check.py')
    for item in provenance['internal_sources']:
        assert digest(ROOT/item['path']) == item['sha256'], item['path']

    units = read(UP+'/certificate.json')
    assert units['status'] == 'PASS'
    assert units['checker_sha256'] == digest(ROOT/UP/'check.py')
    assert units['factor_model_sha256'] == digest(ROOT/UP/'factor_model.json')
    totals = units['totals_all_five_s']
    assert totals['sequential_choices'] == 4664
    assert totals['distinct_s_basis_pairs'] == 3166
    assert totals['globally_distinct_final_bases'] == 2834
    assert len(units['survivors']) == 2
    for survivor in units['survivors']:
        contradiction = survivor['factor_contradiction']
        assert contradiction['all_quadratic_test_assignments_excluded']
        assert contradiction['raw_weight_for_every_test_forced_by_detector1'][1] == 3
        for mismatch in contradiction['detector0_mixed_factor_mismatches']:
            assert mismatch['comparison_row_exponent'][1] == 0
            assert mismatch['raw_row_exponent'][1] == 6
    unit_review = read(UP+'/independent_review.json')
    assert unit_review['status'] == 'PASS'
    assert unit_review['manuscript_sha256'] == digest(ROOT/UNITS)
    assert unit_review['review_sha256'] == digest(ROOT/UP/'independent_review.md')
    assert unit_review['independent_arithmetic_sha256'] == digest(ROOT/UP/'independent_arithmetic.json')
    original_math = (ROOT/UNITS).read_text().replace(
        r'\begin{thebibliography}{9}\raggedright', r'\begin{thebibliography}{9}')
    assert hashlib.sha256(original_math.encode()).hexdigest() == unit_review['reviewed_mathematical_text_sha256']
    independent = read(UP+'/independent_arithmetic.json')
    assert independent['status'] == 'PASS' and independent['distinct_bases'] == 2834
    assert independent['manuscript_sha256'] == digest(ROOT/UNITS)
    assert independent['factor_model_sha256'] == digest(ROOT/UP/'factor_model.json')
    for a, b in zip(independent['counts'], units['counts_by_s']):
        assert (a['s'], a['ordered'], a['bases'], a['survivors']) == (
            b['s'], b['sequential_choices'], b['distinct_bases_for_s'], b['single_comparison_survivors'])
    for a, b in zip(independent['survivors'], units['survivors']):
        assert a['s'] == b['s']
        assert a['basis'] == sorted([[0, 0], *b['unit_basis'].values()])
        expected = sorted([[s['powers'][0], s['powers'][1], s['comparison_weight'],
                            s['row_exponents'][0], s['row_exponents'][1]]
                           for s in b['comparison_states']])
        assert a['states'] == expected
    manifest = read(UP+'/MANIFEST.json')
    assert manifest['proof'] == UNITS and manifest['proof_sha256'] == digest(ROOT/UNITS)
    for name, expected in manifest['files'].items():
        path = ROOT/UP/name
        assert path.stat().st_size == expected['bytes'] and digest(path) == expected['sha256'], name
    model = read(UP+'/factor_model.json')
    assert model['source_table_sha256'] == digest(ROOT/'computation/quartic/search194_v69/source195.json')
    ledger = read(UP+'/runs.json')
    assert ledger['models'] == ledger['unsat'] == 30
    assert ledger['sat'] == ledger['unknown'] == 0
    assert len(ledger['runs']) == 30
    for result in ledger['runs']:
        assert result['status'] == 'unsat' and result['integer_weights_unbounded']
        assert result['nominal_coordinates'] == 194
    # Authenticate every recorded model without running an optional SMT solver.
    run([ROOT/UP/'generate_models.py', '--source-package', ROOT/'computation/quartic/search194_v69'])

    half = read(HP+'/certificate.json')
    assert half['status'] == 'PASS' and half['manuscript_sha256'] == digest(ROOT/HALF)
    assert half['checker_sha256'] == digest(ROOT/HP/'check.py')
    interface = half['one_component_quadratic_interface']
    assert interface['coordinates'] == 21 and interface['degree_two_monomials'] == 253
    assert interface['evaluation_rank'] == 236 and interface['known_relation_rank'] == 17
    assert interface['quadratic_relation_dimension'] == 17
    assert interface['prime'] == 1009 and interface['nonzero_minor_determinant_mod_prime'] == 514
    half_independent = read(HP+'/independent_certificate.json')
    assert half_independent['status'] == 'PASS'
    assert half_independent['source_certificate_sha256'] == digest(ROOT/HP/'certificate.json')
    assert half_independent['checker_sha256'] == digest(ROOT/HP/'check_independent.py')
    half_review = read(HP+'/independent_review.json')
    assert half_review['status'] == 'PASS' and half_review['manuscript_sha256'] == digest(ROOT/HALF)
    assert half_review['review_sha256'] == digest(ROOT/HP/'independent_review.md')
    assert half_review['independent_certificate_sha256'] == digest(ROOT/HP/'independent_certificate.json')
    half_provenance = read(HP+'/provenance.json')
    assert half_provenance['proof'] == HALF and half_provenance['manuscript_sha256'] == digest(ROOT/HALF)
    for path, expected in half_provenance['source_sha256'].items():
        assert digest(ROOT/path) == expected, path
    for name, expected in half_provenance['files'].items():
        assert digest(ROOT/HP/name) == expected, name

    arithmetic = read(AP+'/certificate.json')
    assert arithmetic['status'] == 'PASS' and arithmetic['manuscript_sha256'] == digest(ROOT/ARITHMETIC)
    assert arithmetic['checker_sha256'] == digest(ROOT/AP/'check.py')
    genera = dict(u_curve=24, t_quotient=224, t_twist=225, z_curve=449)
    assert arithmetic['genera'] == genera
    assert arithmetic['good_reduction_certificate']['prime'] == 101
    assert arithmetic['good_reduction_certificate']['u_degree'] == 50
    assert arithmetic['good_reduction_certificate']['t_degree'] == 450
    assert arithmetic['good_reduction_certificate']['t_constant_residue'] != 0
    polynomials = arithmetic['integer_polynomials_ascending']
    assert {k: len(v)-1 for k, v in polynomials.items()} == dict(N=24, D=24, A_physical=9, B_physical=8)
    assert arithmetic['actual_inputs']['tests'] == ['c', 'c', 'd', 'd', '0', '0']
    local = arithmetic['actual_local_example']
    assert local['contact_prime'] == 17 and local['obstruction_prime'] == 31
    assert [local[k] for k in ('u_mod_31', 'V_mod_31', 'w_mod_31', 'C_mod_31')] == [9, 22, 19, 11]
    arithmetic_independent = read(AP+'/independent_certificate.json')
    assert arithmetic_independent['status'] == 'PASS' and arithmetic_independent['genera'] == genera
    assert arithmetic_independent['checker_sha256'] == digest(ROOT/AP/'check_independent.py')
    assert arithmetic_independent['author_checker_sha256'] == digest(ROOT/AP/'check.py')
    assert arithmetic_independent['author_certificate_sha256'] == digest(ROOT/AP/'certificate.json')
    assert arithmetic_independent['manuscript_sha256_if_present'] == digest(ROOT/ARITHMETIC)
    arithmetic_review = read(AP+'/independent_review.json')
    assert arithmetic_review['status'] == 'PASS' and arithmetic_review['manuscript_sha256'] == digest(ROOT/ARITHMETIC)
    assert arithmetic_review['review_sha256'] == digest(ROOT/AP/'independent_review.md')
    assert arithmetic_review['independent_certificate_sha256'] == digest(ROOT/AP/'independent_certificate.json')
    arithmetic_provenance = read(AP+'/provenance.json')
    assert arithmetic_provenance['manuscript_sha256'] == digest(ROOT/ARITHMETIC)
    for item in arithmetic_provenance['internal_sources']:
        assert digest(ROOT/item['path']) == item['sha256'], item['path']
    original_arithmetic = (ROOT/ARITHMETIC).read_text().replace(
        r'\begin{aligned}', r'\begin{split}', 1).replace(r'\end{aligned}', r'\end{split}', 1)
    assert hashlib.sha256(original_arithmetic.encode()).hexdigest() == arithmetic_review['reviewed_mathematical_text_sha256']

    criteria = read('data/criteria_20261117_v70.json')
    assert criteria['current_construction_records'] == 'data/results_20261117_v68.json'
    assert criteria['unchanged_counts'] == dict(general=25, ordinary_abc=11,
        general_quartic=195, ordinary_abc_quartic=68, explicit_quartic=229)
    for key in ('new_defining_polynomial_count', 'targets_21_and_9_proved',
                'number_field_counterexample_established', 'all_number_fields_definition_established',
                'arithmetic_foundations_complete_independent_audit'):
        assert criteria[key] is False, key
    catalog = {item['id']: item for item in read('negative_results/data/results.json')['theorems']}
    for field in ('actual_trace_obstruction', 'quartic_unit_obstruction', 'scalar_helper_obstruction'):
        item = criteria[field]
        assert catalog[item['id']] == item
    theorem = criteria['actual_trace_obstruction']
    assert theorem['general_vertical_unit_lambda_plus_one_required']
    assert theorem['derivative_prepared_abelian_families_constant_with_fixed_root']
    assert theorem['general_all_nine_point_roles_free']
    assert not theorem['individual_rational_witnesses_excluded']
    assert not theorem['unrestricted_derivative_root_and_slope_variation_excluded']
    assert not criteria['quartic_unit_obstruction']['global_quartic_variable_lower_bound']
    arithmetic_record = criteria['actual_trace_arithmetic']
    assert arithmetic_record['general_fixed_tuple_weight_curve_genus_bound'] == 36
    assert arithmetic_record['physical_lift_equation_degree'] == 9
    assert arithmetic_record['exact_genera'] == genera
    assert arithmetic_record['all_original_guards_required']
    assert not arithmetic_record['fixture']['shift_sufficient_for_definition_asserted']
    assert not arithmetic_record['local_example']['full_preparation']
    assert not arithmetic_record['admissible_global_rational_witness_found']
    assert not arithmetic_record['global_realization_proved']
    builds = read('data/audits/tex_build_20261117_v70.json')['papers']
    assert {b['paper'] for b in builds} == {TRACE, UNITS, HALF, ARITHMETIC}
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
    assert 'docs/results_20261117_v70.md' in readme

    report = dict(schema='diophantine-exact-verification/v70', status='PASS',
        python=platform.python_version(), current_records=criteria['current_construction_records'],
        source_sha256={p: digest(ROOT/p) for p in (TRACE, UNITS, HALF, ARITHMETIC)},
        certificate_sha256={p+'/certificate.json': digest(ROOT/p/'certificate.json') for p in (TP, UP, HP, AP)},
        independent_mathematical_reviews_pinned=True,
        exact_affine_contact_types=4, collision_slopes=35,
        sequential_unit_bases=2834, surviving_unit_bases=2,
        surviving_bases_excluded_by_integer_certificate=True,
        supplementary_model_hashes_reproduced=30, SMT_needed_for_proof=False,
        scalar_half_helper_quadratic_identity_dimension=17,
        scalar_half_helper_minor_determinant_mod1009=514,
        actual_trace_integer_polynomials_independently_reconstructed=4,
        actual_trace_exact_genera=genera, actual_trace_weight_genus_bound=36,
        actual_trace_physical_lift_degree=9, actual_global_witness_found=False,
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
