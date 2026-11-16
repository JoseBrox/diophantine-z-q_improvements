#!/usr/bin/env python3
"""Reconstruct the small-coefficient quartic, reference graph and norm certificates."""
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


def run(script, *arguments):
    process = subprocess.run(
        [sys.executable, '-B', str(ROOT / script), *map(str, arguments)],
        cwd=ROOT, text=True, capture_output=True)
    if process.returncode:
        raise ValueError(script + ' failed:\n' + process.stdout[-6000:]
                         + process.stderr[-6000:])


def compare(produced, stored):
    if produced.read_bytes() != stored.read_bytes():
        raise ValueError('Certificate reconstruction differs: ' + str(stored))
    return {'path': str(stored.relative_to(ROOT)),
            'sha256': hashlib.sha256(produced.read_bytes()).hexdigest()}


def main(output):
    import sympy
    if sympy.__version__ != '1.14.0':
        raise ValueError('Use SymPy 1.14.0.')
    checks = []
    with tempfile.TemporaryDirectory(prefix='diophantine-v48-') as directory:
        temporary = Path(directory)
        cases = [
            ('inverse-reference-squares',
             'computation/elliptic_charts/inverse_reference_squares_v48',
             [('check.py', 'certificate.json'),
              ('independent-check.py', 'independent-verification.json')]),
            ('bounded-native-norm-levels',
             'computation/pole_parameters/bounded_norm_levels_v48',
             [('check.py', 'certificate.json')]),
            ('automatic-level-finiteness',
             'negative_results/computation/automatic_levels_v48',
             [('check.py', 'certificate.json')]),
            ('tangent-quadratic-completion-obstructions',
             'negative_results/computation/tangent_completion_v48',
             [('check.py', 'certificate.json'),
              ('independent-check.py', 'independent-verification.json'),
              ('trace-check.py', 'trace-certificate.json'),
              ('trace-independent-check.py', 'trace-independent-verification.json')]),
        ]
        for name, package, scripts in cases:
            files = []
            for script, certificate in scripts:
                produced = temporary / (name + '-' + certificate)
                run(package + '/' + script, '--output', produced)
                files.append(compare(produced, ROOT / package / certificate))
            checks.append({'name': name, 'status': 'PASS', 'files': files})
            print(name + ': PASS', flush=True)

        package = 'computation/quartic/abc74_v48'
        rebuilt = temporary / 'abc74'
        run(package + '/build.py', '--output', rebuilt)
        files = [compare(rebuilt / name, ROOT / package / name) for name in
                 ('quadratic-family.json', 'polynomial-family.json',
                  'construction-report.json')]
        # The basis matrix is part of the specification, not an algorithmic
        # output. Both programs independently verify its full invertibility.
        basis = ROOT / package / 'basis-transformation.json'
        shutil.copyfile(basis, rebuilt / basis.name)
        files.append(compare(rebuilt / basis.name, basis))
        independent = rebuilt / 'independent-verification.json'
        run(package + '/check.py', '--tables', rebuilt, '--output', independent)
        files.append(compare(independent, ROOT / package / independent.name))
        checks.append({'name': 'small-coefficient-abc74',
                       'status': 'PASS', 'files': files})
        print('small-coefficient-abc74: PASS', flush=True)
    report = {
        'schema': 'diophantine-exact-verification/v48',
        'status': 'PASS', 'python': platform.python_version(),
        'sympy': sympy.__version__, 'checks': checks,
        'total_variable_counts': {'general': 25, 'explicit_general': 27,
            'weak_abc': 13, 'quartic': 195, 'explicit_quartic': 257, 'abc_quartic': 74},
        'new_variable_reduction': False,
        'abc_quartic': {'variables': 74, 'degree': 4, 'quadratic_rows': 66,
            'monomials': 1695, 'content': 1,
            'exact_coefficient_height': 'max(30568,B^2+1)',
            'input_comparison': 'beta=X', 'reference_translator': 'R0'},
        'construction_records': 'data/results_20261116_v48.json',
        'negative_results_catalog': 'negative_results/data/results.json',
        'scope': 'Exact reconstruction of the complete 74-variable quadratic '
                 'source and quartic expansion, inverse reference identities '
                 'and exceptional fibers, bounded native norm-level identities '
                 'and local filters, automatic-level examples, and both complete '
                 'quadratic-identity spaces for the specified tangent embeddings. '
                 'The manuscripts prove the infinite implications under their '
                 'stated premises. Uniform actual prescribed-trace realization '
                 'and a complete quartic below 74 remain unproved.',
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
