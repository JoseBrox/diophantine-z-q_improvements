#!/usr/bin/env python3
"""Reproduce the complete 68-variable quartic and derivative-fiber certificates."""
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
PACKAGE = 'computation/quartic/abc68_v65'
GENUS = 'negative_results/computation/derivative_trace_genus_v65'
PAPERS = [
    'papers/quartic_existence/quartic_abc68_20261117_v65.tex',
    'negative_results/papers/pole_parameters/derivative_trace_genus_20261117_v65.tex',
]
CONTRIBUTORS_HASH = 'bec5e749954eb50b1206e43bc7b27462419ac135762f820a201e528b222b3285'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(script, *arguments):
    result = subprocess.run([sys.executable, '-B', str(ROOT / script),
                             *(str(x) for x in arguments)], cwd=ROOT,
                            capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)


def main(output):
    with tempfile.TemporaryDirectory(prefix='diophantine-v65-') as directory:
        temporary = Path(directory)
        rebuilt = temporary / 'quartic68'
        run(PACKAGE + '/build.py', '--output', rebuilt)
        tables = ['quadratic-family.json', 'polynomial-family.json',
                  'construction-report.json', 'basis-transformation.json']
        for name in tables:
            assert (rebuilt / name).read_bytes() == (ROOT / PACKAGE / name).read_bytes(), name
        certificates = [
            (PACKAGE + '/check.py', 'independent-verification.json',
             ['--tables', rebuilt]),
            (PACKAGE + '/chart-check.py', 'chart-certificate.json', []),
            (PACKAGE + '/universal-chart-check.py', 'universal-chart-certificate.json', []),
            (GENUS + '/check.py', 'certificate.json', ['--source', ROOT / PAPERS[1]]),
        ]
        receipts = []
        for index, (script, certificate, arguments) in enumerate(certificates):
            target = temporary / f'certificate-{index}.json'
            run(script, *arguments, '--output', target)
            retained = ROOT / Path(script).parent / certificate
            assert target.read_bytes() == retained.read_bytes(), script
            result = json.loads(target.read_text())
            assert result['status'] == 'PASS'
            receipts.append(result)
    exact, chart, universal, genus = receipts
    assert exact['variables'] == 68 and exact['quadraticRows'] == 56
    assert exact['degree'] == 4 and exact['contentForEveryIntegerB'] == 1
    assert exact['ordinaryMonomialsForEveryIntegerBAtLeast81'] == 1078
    assert exact['parameterSeparatedTerms'] == 1081
    assert exact['largestFixedCoefficient'] == 3554
    assert exact['exactHeightForEveryIntegerBAtLeast81'] == 'B^2+1'
    assert exact['constantPivotRow'] == 37
    assert exact['zeroInputFixture']['all56LiteralAndTransformedRowsVanish']
    assert not exact['zeroInputFixture']['arithmeticHeightThresholdClaimed']
    assert chart['identities']['identity_count'] == 6
    finite = chart['finite_fields']['totals']
    assert finite == dict(coefficient_fibers=68, solutions=12960,
                         tangent_pairs=812, zero_ordinate_pairs=1556,
                         zero_abscissa_torsion_differences=880,
                         nonzero_abscissa_torsion_differences=744)
    assert universal['checker_sha256'] == digest(ROOT / PACKAGE / 'universal-chart-check.py')
    assert universal['field_chart_rows'] == 4
    assert universal['rational_chart_coordinates'] == 13
    assert universal['rational_chart_rows'] == 9
    assert universal['zero_input_rows_and_gap']
    assert genus['source_sha256'] == digest(ROOT / PAPERS[1])
    assert genus['checker_sha256'] == digest(ROOT / GENUS / 'check.py')
    assert len(genus['contacts_checked']) == 18
    assert genus['minimum_simple_branch_points'] == 18
    assert genus['riemann_hurwitz_genus_lower_bound'] == 8
    assert not genus['global_actual_trace_realization_proved']
    assert not genus['actual_trace_criterion_disproved']

    current = json.loads((ROOT / 'data/results_20261117_v65.json').read_text())
    previous = json.loads((ROOT / 'data/results_20261117_v63.json').read_text())
    now = {row['id']: row for row in current['current_constructions']}
    before = {row['id']: row for row in previous['current_constructions']}
    assert {key: row['variables'] for key, row in now.items()} == dict(
        general25=25, quartic195=195, explicit27=27, explicit_quartic229=229,
        weak13=13, abc13=13, abc_quartic68=68, ordinary_abc11=11)
    for key in before.keys() - {'abc_quartic71'}:
        assert now[key] == before[key], key
    q = now['abc_quartic68']
    assert q['variables'] == 68 and q['quadratic_rows'] == 56
    assert q['proof'] == PAPERS[0] and q['data'] == PACKAGE
    assert q['monomials'] == 1078 and q['parameter_separated_terms'] == 1081
    assert q['paired_field_coordinates'] == 6
    assert q['product_helper_field_coordinates'] == 2
    assert q['retained_rational_trace_coordinates'] == 1
    assert not q['parameter_effective'] and not q['additional_nonzero_guard']
    assert current['new_variable_reduction']
    assert not current['new_degree_improvement'] and not current['new_coefficient_improvement']
    assert not current['arithmetic_foundations_complete_independent_audit']
    assert not current['trace_conic_realization']['proved']
    assert not current['new_eleven_source']['actual_nine_variable_realization_proved']
    assert not current['number_fields']['counterexample_established']
    assert not current['number_fields']['all_number_fields_theorem_established']
    criteria = json.loads((ROOT / current['single_derivative_trace_criterion']).read_text())
    assert not criteria['general_target_21_proved']
    assert not criteria['single_derivative_trace']['nine_variable_definition_established']
    catalog = {row['id']: row for row in json.loads(
        (ROOT / 'negative_results/data/results.json').read_text())['theorems']}
    assert len(current['new_negative_results']) == 1
    negative = current['new_negative_results'][0]
    assert negative == catalog['derivative_actual_trace_genus']
    assert negative['proof'] == PAPERS[1] and negative['data'] == GENUS
    assert negative['minimum_geometric_genus'] == 8
    assert not negative['actual_trace_realization_disproved']

    builds = json.loads((ROOT / 'data/audits/tex_build_20261117_v65.json').read_text())
    assert {row['paper'] for row in builds['papers']} == set(PAPERS)
    for row in builds['papers']:
        assert row['returncode'] == 0 and row['warnings'] == []
        assert row['source_sha256'] == digest(ROOT / row['paper'])
        assert row['all_rendered_pages_reviewed'] and row['pages'] > 0
    readme = (ROOT / 'README.md').read_text()
    section = re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)', readme)
    assert section and hashlib.sha256(section.group().encode()).hexdigest() == CONTRIBUTORS_HASH
    historical_guide = (ROOT / 'docs/results_20261117_v65.md').read_text()
    assert 'data/results_20261117_v65.json' in historical_guide
    assert 'docs/results_20261117_v65.md' in readme
    assert '**68**' in historical_guide
    assert re.search(r'1,078\s+coordinate monomials', historical_guide)
    assert r'\(' not in readme and r'\[' not in readme

    report = dict(schema='diophantine-exact-verification/v65', status='PASS',
                  python=platform.python_version(),
                  current_records='data/results_20261117_v65.json',
                  retained_records='data/results_20261117_v63.json',
                  source_sha256={path: digest(ROOT / path) for path in PAPERS},
                  complete_quartic=dict(variables=68, quadratic_rows=56, degree=4,
                      monomials=1078, parameter_separated_terms=1081, integer_content=1,
                      coefficient_height='B^2+1', sufficient_shift_effective=False,
                      ordinary_abc_required=True, additional_guards=0,
                      all_tangent_and_finite_torsion_differences_covered=True,
                      explicit_zero_input_transfer=True),
                  independent_table_sha256=dict(quadratic=exact['quadraticSha256'],
                                                polynomial=exact['polynomialSha256']),
                  independent_chart_finite_evidence=finite,
                  derivative_genus=dict(simple_branch_contacts=18, genus_lower_bound=8,
                      global_realization_disproved=False),
                  other_current_records_unchanged=True,
                  targets_21_and_9_proved=False,
                  all_number_fields_definition_established=False,
                  number_field_counterexample_established=False,
                  inherited_arithmetic_foundations_independently_audited=False,
                  contribution_and_citation_section_sha256=CONTRIBUTORS_HASH)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    main(parser.parse_args().report)
