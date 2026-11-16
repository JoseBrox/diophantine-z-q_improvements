#!/usr/bin/env python3
"""Reconstruct the 76-variable quartic, pole quadric and obstruction certificates."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
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
    with tempfile.TemporaryDirectory(prefix='diophantine-v44-') as directory:
        temporary = Path(directory)
        package = 'computation/quartic/abc76_v44'
        tables = temporary / 'abc76'
        run(package + '/build.py', '--output', tables)
        names = ('quadratic-family.json', 'polynomial-family.json',
                 'construction-report.json')
        files = [compare(tables / name, ROOT / package / name) for name in names]
        produced = temporary / 'abc76-independent.json'
        run(package + '/check.py', '--output', produced)
        files.append(compare(produced, ROOT / package / 'independent-verification.json'))
        checks.append({'name': 'abc76-complete-quartic', 'status': 'PASS',
                       'files': files})
        print('abc76-complete-quartic: PASS', flush=True)

        for name, package, certificate in (
                ('varying-input-quadric',
                 'computation/pole_parameters/varying_input_quadric_v44', 'certificate.json'),
                ('abelian-parameter-obstruction',
                 'negative_results/computation/abelian_parameter_v44', 'certificate.json'),
                ('fixed-argument-complement-ramification',
                 'negative_results/computation/fixed_argument_complement_v44', 'certificate.json'),
                ('duplicated-reference-signs',
                 'negative_results/computation/duplicated_sign_v44', 'verification.json')):
            produced = temporary / (name + '.json')
            run(package + '/check.py', '--output', produced)
            checks.append({'name': name, 'status': 'PASS',
                           'certificate': compare(produced, ROOT / package / certificate)})
            print(name + ': PASS', flush=True)

    report = {
        'schema': 'diophantine-exact-verification/v44',
        'status': 'PASS', 'python': platform.python_version(),
        'sympy': sympy.__version__, 'checks': checks,
        'total_variable_counts': {
            'general': 25, 'explicit_general': 27, 'weak_abc': 13,
            'quartic': 196, 'explicit_quartic': 258, 'abc_quartic': 76},
        'new_variable_reduction': True,
        'construction_records': 'data/results_20261116_v44.json',
        'negative_results_catalog': 'negative_results/data/results.json',
        'scope': 'Exact source-bound quadratic rows and independent quartic '
                 'expansion, coefficient-height profiles, the varying-input quadric '
                 'birational maps, pole rescaling, contact '
                 'identities, and separate obstruction certificates, including '
                 'fixed-argument complement ramification identities. The '
                 'manuscripts prove the infinite statements. No common rational '
                 'detector fiber or 24-variable construction is asserted.',
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
