#!/usr/bin/env python3
"""Reconstruct the 195- and 257-variable quartics and exact certificates."""
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
    with tempfile.TemporaryDirectory(prefix='diophantine-v45-') as directory:
        temporary = Path(directory)
        for count in (195, 257):
            package = f'computation/quartic/affine_laurent{count}_v45'
            tables = temporary / f'quartic{count}'
            run(package + '/build.py', '--output', tables)
            names = ('quadratic-family.json', 'polynomial-family.json',
                     'construction-report.json')
            files = [compare(tables / name, ROOT / package / name) for name in names]
            produced = temporary / f'quartic{count}-independent.json'
            run(package + '/check.py', '--output', produced)
            files.append(compare(produced, ROOT / package / 'independent-verification.json'))
            name = f'affine-Laurent-quartic{count}'
            checks.append({'name': name, 'status': 'PASS', 'files': files})
            print(name + ': PASS', flush=True)
        for name, package in (
                ('native-complement-guards', 'computation/pole_parameters/guarded_complements_v45'),
                ('mixed-power-height', 'computation/elliptic_heights/mixed_power_v45')):
            produced = temporary / (name + '.json')
            run(package + '/check.py', '--output', produced)
            checks.append({'name': name, 'status': 'PASS',
                           'certificate': compare(produced, ROOT / package / 'certificate.json')})
            print(name + ': PASS', flush=True)
    report = {
        'schema': 'diophantine-exact-verification/v45',
        'status': 'PASS', 'python': platform.python_version(),
        'sympy': sympy.__version__, 'checks': checks,
        'total_variable_counts': {'general': 25, 'explicit_general': 27,
            'weak_abc': 13, 'quartic': 195, 'explicit_quartic': 257, 'abc_quartic': 76},
        'new_variable_reduction': True,
        'construction_records': 'data/results_20261116_v45.json',
        'negative_results_catalog': 'negative_results/data/results.json',
        'scope': 'Exact input-preserving source transformations, complete quartic expansion, '
                 'uniform coefficient height and support, native complement character identities '
                 'and free-input preparation examples, and mixed-power symbolic valuation cases. '
                 'The manuscripts prove the infinite statements. No native common rational '
                 'fiber or square-complement realization is asserted.',
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
