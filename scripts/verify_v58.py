#!/usr/bin/env python3
"""Verify signed height data, optimal criteria, safe classes and scoped obstructions."""
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
CONTRIBUTORS_HASH = 'bec5e749954eb50b1206e43bc7b27462419ac135762f820a201e528b222b3285'
JOBS = (
    ('computation/pole_parameters/sharp_single_cover_v58', 'check.py', 'certificate.json'),
    ('computation/pole_parameters/sharp_single_cover_v58', 'check_criteria.py', 'criteria_certificate.json'),
    ('computation/pole_parameters/sharp_single_cover_v58', 'independent_criteria.py', 'independent_criteria_certificate.json'),
    ('computation/pole_parameters/small_trace_classes_v58', 'check.py', 'certificate.json'),
    ('computation/pole_parameters/small_trace_classes_v58', 'check_rank.py', 'rank_certificate.json'),
    ('computation/pole_parameters/small_trace_classes_v58', 'independent_rank.py', 'independent_rank_certificate.json'),
    ('negative_results/computation/actual_multiplication_surface_v58', 'check.py', 'certificate.json'),
    ('negative_results/computation/two_square_height_v58', 'check.py', 'certificate.json'),
)
PAPERS = (
    'papers/elliptic_heights/signed_mixed_power_height_20261117_v58.tex',
    'papers/pole_parameters/small_trace_classes_20261117_v58.tex',
    'negative_results/papers/rational_fibers/actual_multiplication_surface_20261117_v58.tex',
    'negative_results/papers/contact_heights/two_square_height_20261117_v58.tex',
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(output):
    hashes, certificates, results = {}, {}, []
    with tempfile.TemporaryDirectory(prefix='diophantine-v58-') as temporary:
        for i, (relative, script, certificate) in enumerate(JOBS):
            package = ROOT/relative
            generated = Path(temporary)/f'certificate-{i}.json'
            run = subprocess.run([sys.executable, '-B', str(package/script),
                                  '--output', str(generated)], cwd=ROOT,
                                 capture_output=True, text=True)
            if run.returncode:
                raise ValueError(run.stdout+run.stderr)
            original = package/certificate
            if original.read_bytes() != generated.read_bytes():
                raise ValueError(f'Certificate differs: {relative}/{certificate}')
            results.append(json.loads(generated.read_text()))
            hashes[str((package/script).relative_to(ROOT))] = digest(package/script)
            certificates[str(original.relative_to(ROOT))] = digest(generated)
    height, criteria, independent, classes, rank, independent_rank, ramification, two_squares = results
    assert all(item['status'] == 'PASS' for item in results)
    assert height['total_exact_fixtures'] == 3133
    assert criteria['ordinary_abc_minimum_argument_degrees'] == {'k0':48, 'k2':60}
    assert independent['ordinary_abc_minima'] == {'fixed_class':48, 'support_budget_two':60}
    expected = [48,48,48,96,60,72,80,168]
    assert [row['argument_degree'] for row in criteria['rows']] == expected
    independent_rows = {(row['kappa'], row['support_budget'], row['e'], row['d']):row
                        for row in independent['rows']}
    assert len(independent_rows) == 10
    for a in criteria['rows']:
        b = independent_rows[(a['kappa'], a['support_degree'], a['e'], a['d'])]
        assert a['argument_degree'] == b['degree']
        assert (a['kappa'], a['e'], a['d'], a['q'], a['contraction']) == (
            b['kappa'], b['e'], b['d'], b['q'], b['contraction'])
    # The independent audit also checks the two admissible equal-degree ties.
    admissible_ties = {(row['kappa'], row['support_degree'], tie['e'], tie['d'])
                      for row in criteria['rows'] for tie in row['all_same_degree_pairs']
                      if tie.get('admissible')}
    assert set(independent_rows) == admissible_ties
    assert rank['scope']['positive_rank_proved']
    assert not rank['scope']['actual_prescribed_trace_realization_proved']
    assert not independent_rank['scope']['actual_prescribed_detector_trace_matching_proved']
    assert [(r['n'], r['degree'], r['leading_coefficient'])
            for r in rank['primitive_data']] == [(8,15,1),(10,24,5),(12,35,3)]
    assert [(r['n'], r['denominator_square_root_degree'],
             r['denominator_square_root_leading_coefficient'])
            for r in independent_rank['rows']] == [(8,15,1),(10,24,5),(12,35,3)]
    assert all(r['matches_independent_division_polynomial_array']
               for r in independent_rank['rows'])
    coefficient_file = ROOT/'computation/pole_parameters/small_trace_classes_v58/rank_coefficients.json'
    assert digest(coefficient_file) == independent_rank['author_coefficient_data_sha256']
    hashes[str(coefficient_file.relative_to(ROOT))] = digest(coefficient_file)
    assert ramification['F_degree'] == 6 and ramification['F_separable']
    assert not ramification['individual_rational_witness_nonexistence_claimed']
    assert two_squares['unbounded_family_proved_for_all_powers_of_two']
    assert not two_squares['actual_inner_form_or_full_detector_counterexample_claimed']
    current = json.loads((ROOT/'data/results_20261117_v58.json').read_text())
    previous = json.loads((ROOT/'data/results_20261117_v57.json').read_text())
    assert current['current_constructions'] == previous['current_constructions']
    assert not current['new_variable_reduction']
    assert not current['native_square_realization']['proved']
    assert not current['single_cover_realization']['proved']
    assert not current['trace_conic_realization']['proved']
    assert not current['variable_squareclass_realization']['proved']
    assert current['sharp_single_cover_criterion']['ordinary_argument_degrees'] == [48,60]
    assert current['trace_conic_realization']['smallest_cubic_block'] == {
        'radicand':'V^3+(2-w)*V^2+4*w', 'total_degree':3,
        'monomials':4, 'coefficient_height':4}
    assert current['trace_conic_realization']['smallest_cubic_rank']['positive_rank_proved']
    assert not current['trace_conic_realization']['smallest_cubic_rank']['actual_trace_matching_proved']
    readme = (ROOT/'README.md').read_text()
    match = re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)', readme)
    assert match and hashlib.sha256(match.group().encode()).hexdigest() == CONTRIBUTORS_HASH
    assert r'\(' not in readme and r'\[' not in readme
    for relative in PAPERS:
        hashes[relative] = digest(ROOT/relative)
    report = {
        'schema':'diophantine-exact-verification/v58', 'status':'PASS',
        'python':platform.python_version(), 'certificate_sha256':certificates,
        'source_sha256':hashes, 'current_records':'data/results_20261117_v58.json',
        'construction_records_unchanged_from':'data/results_20261117_v57.json',
        'contribution_and_citation_section_sha256':CONTRIBUTORS_HASH,
        'established_general_counts':[25,13], 'abc_quartic_variables':71,
        'signed_mixed_power_exact_fixtures':height['total_exact_fixtures'],
        'optimal_single_cover_argument_degrees':expected,
        'ordinary_abc_argument_degrees':[48,60],
        'independent_integer_inequality_optimization_check':True,
        'small_trace_class_block':current['trace_conic_realization']['smallest_cubic_block'],
        'smallest_trace_cubic_positive_rank_range':'Every rational 0<w<=1/4',
        'smallest_trace_cubic_independent_group_law_check':True,
        'actual_full_surface_rational_identity_excluded':True,
        'individual_rational_witness_nonexistence_claimed':False,
        'two_square_counterexample_scope':'Unrestricted inner value, powers of two; not a full detector counterexample.',
        'actual_uniform_rational_realization_proved':False,
        'new_defining_variable_count':False,
        'new_full_defining_degree_or_coefficient_bound':False,
        'external_arithmetic_foundation_audited':False,
        'scope':('Exact normalization inequalities, independent finite parameter optimization, '
                 'trace-class polynomial identities, independently verified torsion exclusions, '
                 'contact data and explicit two-square '
                 'counterfamilies. Universal height and geometric proofs are in the manuscripts. '
                 'No global actual-trace realization or 21/9 defining bound is certified.'),
    }
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    main(parser.parse_args().report)
