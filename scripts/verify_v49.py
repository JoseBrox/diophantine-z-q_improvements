#!/usr/bin/env python3
"""Reconstruct the complete 71-variable quartic and both point-pair certificates."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = 'computation/quartic/abc71_v49'


def run(script, *arguments):
    process = subprocess.run(
        [sys.executable, '-B', str(ROOT / script), *map(str, arguments)],
        cwd=ROOT, text=True, capture_output=True)
    if process.returncode:
        raise ValueError(script + ' failed:\n' + process.stdout[-6000:]
                         + process.stderr[-6000:])


def compare(produced, stored):
    if produced.read_bytes() != stored.read_bytes():
        raise ValueError('Reconstruction differs: ' + str(stored))
    return {'path': str(stored.relative_to(ROOT)),
            'sha256': hashlib.sha256(produced.read_bytes()).hexdigest()}


def main(output):
    import sympy
    if sympy.__version__ != '1.14.0':
        raise ValueError('Use SymPy 1.14.0.')
    checks = []
    with tempfile.TemporaryDirectory(prefix='diophantine-v49-') as directory:
        temporary = Path(directory)
        for script, name in [('pair-check.py', 'pair-certificate.json'),
                             ('independent-pair-check.py', 'independent-pair-verification.json')]:
            produced = temporary / name
            run(PACKAGE + '/' + script, '--output', produced)
            checks.append({'name': script, 'status': 'PASS',
                           'files': [compare(produced, ROOT / PACKAGE / name)]})
            print(script + ': PASS', flush=True)
        rebuilt = temporary / 'abc71'
        run(PACKAGE + '/build.py', '--output', rebuilt)
        files = [compare(rebuilt / name, ROOT / PACKAGE / name) for name in
                 ('quadratic-family.json', 'polynomial-family.json',
                  'construction-report.json')]
        basis = ROOT / PACKAGE / 'basis-transformation.json'
        shutil.copyfile(basis, rebuilt / basis.name)
        files.append(compare(rebuilt / basis.name, basis))
        independent = rebuilt / 'independent-verification.json'
        run(PACKAGE + '/check.py', '--tables', rebuilt, '--output', independent)
        files.append(compare(independent, ROOT / PACKAGE / independent.name))
        checks.append({'name': 'complete-abc71', 'status': 'PASS', 'files': files})
        print('complete-abc71: PASS', flush=True)
    report = {
        'schema': 'diophantine-exact-verification/v49',
        'status': 'PASS', 'python': platform.python_version(),
        'sympy': sympy.__version__, 'checks': checks,
        'total_variable_counts': {'general': 25, 'explicit_general': 27,
            'weak_abc': 13, 'quartic': 195, 'explicit_quartic': 257, 'abc_quartic': 71},
        'new_variable_reduction': True,
        'abc_quartic': {'variables': 71, 'degree': 4, 'quadratic_rows': 59,
            'monomials': 1187, 'parameter_separated_terms': 1190, 'content': 1,
            'exact_coefficient_height_for_fixed_odd_B_at_least_81': 'B^2+1',
            'largest_fixed_coefficient': 3554,
            'input_comparison': 'beta=X', 'reference_translator': 'R0',
            'retained_rational_trace_coordinates': 0,
            'scaled_physical_trace': 'Tr(a)=X^2*Tr(x(U-V))',
            'additional_nonzero_guard': False},
        'construction_records': 'data/results_20261116_v49.json',
        'negative_results_catalog': 'negative_results/data/results.json',
        'scope': 'Complete literal quadratic source, automatic reference units, '
                 'physical product recovery, universal variable-difference '
                 'identities and exhaustive finite pair fibers including '
                 'two-torsion differences, invertible row transformations, '
                 'independent full quartic expansion and coefficient profiles. '
                 'The zero-input finite fixture is only an algebraic consistency '
                 'check, not a sufficient defining parameter. The manuscript '
                 'proves soundness and completeness under ordinary rational abc '
                 'and its retained arithmetic premises. Uniform actual '
                 'prescribed-trace realization for 21/9 remains unproved.',
        'external_arithmetic_foundation_audited': False,
        'non_author_review': False,
    }
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    main(parser.parse_args().report)
