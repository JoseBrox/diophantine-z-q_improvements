#!/usr/bin/env python3
"""Verify the v56 auxiliary theorems without changing the established bounds."""
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
CONTRIBUTORS_HASH = '7c4e19ff00bd3f87f97db5ba836cea716e72fa8b583756c1a4fd7c5b5a075214'
PACKAGES = (
    'computation/pole_parameters/single_cover_v56',
    'computation/pole_parameters/intrinsic_pole_v56',
    'computation/pole_parameters/precision_transfer_v56',
    'negative_results/computation/order_three_v56',
)
PAPERS = (
    'papers/pole_parameters/single_cover_criterion_20261117_v56.tex',
    'papers/pole_parameters/intrinsic_pole_20261117_v56.tex',
    'papers/pole_parameters/precision_transfer_20261117_v56.tex',
    'negative_results/papers/pole_parameters/order_three_inert_obstruction_20261117_v56.tex',
    'negative_results/papers/pole_parameters/rational_detector_products_20261117_v56.tex',
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(output):
    hashes, certificates = {}, {}
    with tempfile.TemporaryDirectory(prefix='diophantine-v56-') as directory:
        for i, relative in enumerate(PACKAGES):
            package = ROOT/relative
            generated = Path(directory)/f'certificate-{i}.json'
            result = subprocess.run([sys.executable, '-B', str(package/'check.py'),
                                     '--output', str(generated)], cwd=ROOT,
                                    capture_output=True, text=True)
            if result.returncode:
                raise ValueError(result.stdout+result.stderr)
            original = package/'certificate.json'
            if original.read_bytes() != generated.read_bytes():
                raise ValueError(f'Certificate differs: {relative}')
            hashes[str((package/'check.py').relative_to(ROOT))] = digest(package/'check.py')
            certificates[str(original.relative_to(ROOT))] = digest(generated)

    values = [json.loads((ROOT/p/'certificate.json').read_text()) for p in PACKAGES]
    single, pole, precision, obstruction = values
    assert [r['soundness_coefficient'] for r in single['parameter_rows']] == [
        '10000/5187', '32/17', '40453083/21236816']
    assert [r['argument_total_degree_in_retained_coordinates']
            for r in single['parameter_rows']] == [96, 120, 384]
    assert single['reciprocal_trace_identity'] is True
    assert single['total_finite_algebra_rank'] == 128
    assert single['example_menu_compiled_factor_rank'] == 128
    assert single['example_menu_retained_coordinates'] == 9
    assert not single['actual_uniform_rational_realization_proved']
    assert not single['uniform_realization_with_menu_proved']
    assert not single['nine_variable_defining_bound_proved']
    assert (pole['total_degree'], pole['monomials'], pole['coefficient_height']) == (9, 12, 4)
    assert precision['reciprocal_orders'] == [1]*10
    assert precision['scalar_orders'] == [1, 1, 1, 1, 2, 2]
    assert precision['comparison_orders'] == [1, 6, 6, 6, 1, 6]
    assert precision['scalar_height_exponent'] == '7/6'
    assert precision['nonzero_lucas_residual_exponent'] == '7/4'
    assert precision['retained_variables'] == 25
    assert obstruction['prime'] == obstruction['covered_shift_residues'] == 81421
    assert len(obstruction['rows']) == 13
    assert obstruction['fixture']['contact_orders'] == [44771, 73604]
    assert not obstruction['other_couplings_excluded']

    independent = None
    if shutil.which('node'):
        path = ROOT/PACKAGES[-1]/'independent_check.mjs'
        result = subprocess.run(['node', str(path)], cwd=ROOT, capture_output=True, text=True)
        if result.returncode:
            raise ValueError(result.stdout+result.stderr)
        independent = json.loads(result.stdout)
        assert independent['status'] == 'PASS'
        assert independent['covered'] == 81421 and independent['rows'] == 13
        hashes[str(path.relative_to(ROOT))] = digest(path)
    fixture = ROOT/PACKAGES[-1]/'source_certificate.json'
    hashes[str(fixture.relative_to(ROOT))] = digest(fixture)

    current = json.loads((ROOT/'data/results_20261117_v56.json').read_text())
    previous = json.loads((ROOT/'data/results_20261116_v53.json').read_text())
    assert current['current_constructions'] == previous['current_constructions']
    assert not current['new_variable_reduction']
    assert not current['new_coefficient_improvement']
    assert not current['single_cover_realization']['proved']
    assert not current['native_square_realization']['proved']
    assert not current['native_square_realization']['menu_realization_proved']
    assert all(not t['new_variable_bound'] for t in current['new_auxiliary_theorems'])
    readme = (ROOT/'README.md').read_text()
    match = re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)', readme)
    assert match and hashlib.sha256(match.group().encode()).hexdigest() == CONTRIBUTORS_HASH
    assert r'\(' not in readme and r'\[' not in readme
    for relative in PAPERS:
        hashes[relative] = digest(ROOT/relative)
    report = {
        'schema':'diophantine-exact-verification/v56', 'status':'PASS',
        'python':platform.python_version(),
        'certificate_sha256':certificates, 'source_sha256':hashes,
        'independent_order_three_check':independent,
        'current_records':'data/results_20261117_v56.json',
        'construction_records_unchanged_from':'data/results_20261116_v53.json',
        'contribution_and_citation_section_sha256':CONTRIBUTORS_HASH,
        'established_general_counts':[25,13], 'abc_quartic_variables':71,
        'single_cover_target':9, 'two_cover_targets':[21,9],
        'height_argument_degrees':[96,120,384],
        'intrinsic_pole':{'degree':9,'monomials':12,'coefficient_height':4,
                          'free_coordinates':2},
        'actual_uniform_rational_realization_proved':False,
        'new_defining_variable_count':False,
        'new_full_defining_degree_or_coefficient_bound':False,
        'external_arithmetic_foundation_audited':False,
        'scope':('Exact height constants, finite-menu identities, intrinsic pole expansion, '
                 'formal coefficients and Lucas witnesses, and the independent finite '
                 'inert-prime obstruction certificate. Manuscripts supply the stated '
                 'universal implications under their explicit arithmetic premises. '
                 'No global rational realization or 21/9 defining bound is certified.'),
    }
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    main(parser.parse_args().report)
