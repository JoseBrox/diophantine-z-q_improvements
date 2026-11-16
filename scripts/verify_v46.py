#!/usr/bin/env python3
"""Reconstruct the 74-variable quartic and finite-complement certificates."""
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
    with tempfile.TemporaryDirectory(prefix='diophantine-v46-') as directory:
        temporary = Path(directory)
        package = 'computation/quartic/abc74_v46'
        tables = temporary / 'abc74'
        run(package + '/build.py', '--output', tables)
        names = ('quadratic-family.json', 'polynomial-family.json',
                 'construction-report.json')
        files = [compare(tables / name, ROOT / package / name) for name in names]
        produced = temporary / 'abc74-independent.json'
        run(package + '/check.py', '--output', produced)
        files.append(compare(produced, ROOT / package / 'independent-verification.json'))
        checks.append({'name': 'weighted-product-abc74', 'status': 'PASS', 'files': files})
        print('weighted-product-abc74: PASS', flush=True)
        package = 'computation/pole_parameters/finite_classes_v46'
        produced = temporary / 'finite-complement-classes.json'
        run(package + '/check.py', '--output', produced)
        checks.append({'name': 'finite-complement-classes', 'status': 'PASS',
                       'certificate': compare(produced, ROOT / package / 'certificate.json')})
        print('finite-complement-classes: PASS', flush=True)
    report = {
        'schema': 'diophantine-exact-verification/v46',
        'status': 'PASS', 'python': platform.python_version(),
        'sympy': sympy.__version__, 'checks': checks,
        'total_variable_counts': {'general': 25, 'explicit_general': 27,
            'weak_abc': 13, 'quartic': 195, 'explicit_quartic': 257, 'abc_quartic': 74},
        'new_variable_reduction': True,
        'construction_records': 'data/results_20261116_v46.json',
        'negative_results_catalog': 'negative_results/data/results.json',
        'scope': 'Complete quadratic reconstruction, exact quartic expansion, uniform '
                 'coefficient height and support, weighted point and trace identities, '
                 'zero-weight exclusion certificates and zero-input specialization; '
                 'finite-complement algebra, parity and prepared coefficient family. '
                 'The manuscripts prove the arithmetic implications under their stated '
                 'premises. Actual common rational fibers and finite-class native '
                 'complement realization remain unproved.',
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
