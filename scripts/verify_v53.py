#!/usr/bin/env python3
"""Verify reweighted detectors, the square criterion and fixed-fiber certificates."""
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
CONTRIBUTORS_HASH = '7c4e19ff00bd3f87f97db5ba836cea716e72fa8b583756c1a4fd7c5b5a075214'
PACKAGES = (
    ('computation/pole_parameters/reweighted_detectors_v53', 'check.py'),
    ('computation/pole_parameters/native_squares_v53', 'check.py'),
    ('negative_results/computation/fixed_flat_fibers_v53', 'generate.py'),
)
PAPERS = (
    'papers/pole_parameters/reweighted_elliptic_detectors_20261116_v53.tex',
    'papers/pole_parameters/native_square_criterion_20261116_v53.tex',
    'negative_results/papers/pole_parameters/fixed_flat_fibers_20261116_v53.tex',
)


def run(arguments):
    result = subprocess.run([sys.executable, '-B', *map(str, arguments)],
                            cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise ValueError(result.stdout + result.stderr)
    return result.stdout


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(output):
    certificates = {}
    source_hashes = {}
    with tempfile.TemporaryDirectory(prefix='diophantine-v53-') as directory:
        for index, (relative, script) in enumerate(PACKAGES):
            package = ROOT / relative
            generated = Path(directory) / f'certificate-{index}.json'
            run([package / script, '--output', generated])
            original = package / 'certificate.json'
            if generated.read_bytes() != original.read_bytes():
                raise ValueError(f'Reconstructed certificate differs: {relative}')
            certificates[str(original.relative_to(ROOT))] = digest(generated)
            for name in ('check.py', 'generate.py'):
                path = package / name
                if path.is_file():
                    source_hashes[str(path.relative_to(ROOT))] = digest(path)
            if index == 2:
                run([package / 'check.py', '--certificate', generated, '--repo', ROOT])

    source = json.loads((ROOT / PACKAGES[0][0] / 'certificate.json').read_text())
    square = json.loads((ROOT / PACKAGES[1][0] / 'certificate.json').read_text())
    fibers = json.loads((ROOT / PACKAGES[2][0] / 'certificate.json').read_text())
    assert source['local_native_product_criterion_checks'] == 648
    assert source['negative_odd_pole_cases'] == 432
    assert source['counts'] == {'general': 25, 'conditional': 13, 'include_input': True}
    assert source['actual_uniform_rational_realization_proved'] is False
    assert source['numerical_determinant_degree_bound_transferred'] is False
    assert square['prescribed_coordinate_j1728_identity'] is True
    assert square['safe_outer_parameter_integer_order_checks'] == 784
    assert square['reference_product_exact_square'] is True
    assert len(square['actual_multiplication_examples']) == 3
    assert [(r['input'], r['comparison'], r['simultaneous_cover_genus'])
            for r in fibers['records']] == [
                (1, 'original', 236), (1, 'symmetric', 236),
                (2, 'original', 332), (2, 'symmetric', 332)]

    current = json.loads((ROOT / 'data/results_20261116_v53.json').read_text())
    previous = json.loads((ROOT / 'data/results_20261116_v52.json').read_text())
    if current['current_constructions'] != previous['current_constructions']:
        raise ValueError('The new auxiliary theorems must not change the established records.')
    assert current['new_variable_reduction'] is False
    assert current['new_coefficient_improvement'] is False
    assert current['native_square_realization']['proved'] is False
    assert current['native_square_realization']['targets'] == [21, 9]
    assert current['native_square_realization']['all_prime_local_solubility_claimed'] is False
    assert current['adaptive_complements']['actual_uniform_rational_realization_proved'] is False
    assert all(not theorem['new_variable_bound'] for theorem in current['new_auxiliary_theorems'])
    readme = (ROOT / 'README.md').read_text()
    match = re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)', readme)
    if not match or hashlib.sha256(match.group().encode()).hexdigest() != CONTRIBUTORS_HASH:
        raise ValueError('The user contribution and citation section changed.')
    if r'\(' in readme or r'\[' in readme:
        raise ValueError('The main README contains unsupported math delimiters.')
    for relative in PAPERS:
        source_hashes[relative] = digest(ROOT / relative)
    fixture = 'computation/pole_parameters/native_trace_fixture_v47/build-fixture.py'
    source_hashes[fixture] = digest(ROOT / fixture)

    report = {
        'schema': 'diophantine-exact-verification/v53',
        'status': 'PASS',
        'python': platform.python_version(),
        'certificate_sha256': certificates,
        'source_sha256': source_hashes,
        'construction_records_unchanged_from': 'data/results_20261116_v52.json',
        'current_records': 'data/results_20261116_v53.json',
        'contribution_and_citation_section_sha256': CONTRIBUTORS_HASH,
        'established_general_counts': [25, 13],
        'abc_quartic_variables': 71,
        'new_source_counts': [25, 13],
        'conditional_realization_targets': [21, 9],
        'actual_uniform_rational_realization_proved': False,
        'new_defining_variable_count': False,
        'numeric_degree_bound_for_changed_sources_assigned': False,
        'fixed_fiber_single_cover_genera': [59, 83],
        'fixed_fiber_simultaneous_cover_genera': [236, 332],
        'fixed_fiber_finite_rational_points_excluded': False,
        'external_arithmetic_foundation_audited': False,
        'scope': ('Exact reweighting and native-square identities, specified local models, '
                  'actual symmetry examples, and independently verified good-reduction '
                  'coefficient and Bezout certificates for the stated fixed fibers. '
                  'Universal source transfers and the conditional finite-algebra reduction '
                  'are manuscript theorems under retained premises. No uniform rational '
                  'realization, 21/9 defining bound or new numerical degree bound is asserted.'),
    }
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    main(parser.parse_args().report)
