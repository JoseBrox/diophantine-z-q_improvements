#!/usr/bin/env python3
"""Reconstruct fixed-fiber, K3, rational-section, and mixed-sign certificates."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def run(*arguments):
    process = subprocess.run([sys.executable, '-B', *map(str, arguments)],
                             cwd=ROOT, text=True, capture_output=True)
    if process.returncode:
        raise ValueError('Verification failed:\n' + process.stdout[-6000:]
                         + process.stderr[-6000:])


def identical(produced, stored):
    if produced.read_bytes() != stored.read_bytes():
        raise ValueError('Certificate reconstruction differs: ' + str(stored))
    return hashlib.sha256(produced.read_bytes()).hexdigest()


def main(output):
    import sympy
    if sympy.__version__ != '1.14.0':
        raise ValueError('Use SymPy 1.14.0.')
    checks = []
    with tempfile.TemporaryDirectory(prefix='diophantine-v42-') as directory:
        temporary = Path(directory)
        source = ROOT / 'computation/pole_parameters/fixed_fiber_guards_v42'
        produced = temporary / 'fixed_fiber_guards.json'
        run(source / 'check.py', '--output', produced)
        stored = source / 'verification.json'
        checks.append({'name': 'native-fixed-fiber-guards', 'status': 'PASS',
                       'certificate': str(stored.relative_to(ROOT)),
                       'sha256': identical(produced, stored)})
        print('Native fixed-fiber guards: PASS', flush=True)

        source = ROOT / 'negative_results/computation/mixed_sign_v42'
        produced = temporary / 'mixed_sign' / 'certificate.json'
        run(source / 'build.py', '--output', produced.parent)
        run(source / 'check.py', '--certificate', produced)
        stored = source / 'certificate.json'
        checks.append({'name': 'mixed-reference-signs', 'status': 'PASS',
                       'certificate': str(stored.relative_to(ROOT)),
                       'sha256': identical(produced, stored)})
        print('Mixed reference signs, independent coordinates: PASS', flush=True)

        source = ROOT / 'negative_results/computation/fixed_input_k3_v42'
        produced = temporary / 'fixed_input_k3.json'
        run(source / 'check.py', '--output', produced)
        stored = source / 'verification.json'
        checks.append({'name': 'fixed-input-k3-geometry', 'status': 'PASS',
                       'certificate': str(stored.relative_to(ROOT)),
                       'sha256': identical(produced, stored)})
        print('Fixed-input K3 branch and resolution identities: PASS', flush=True)

        source = ROOT / 'negative_results/computation/rational_sections_v42'
        produced = temporary / 'rational_sections.json'
        run(source / 'check.py', '--output', produced)
        stored = source / 'verification.json'
        checks.append({'name': 'rational-section-classification', 'status': 'PASS',
                       'certificate': str(stored.relative_to(ROOT)),
                       'sha256': identical(produced, stored)})
        print('Rational-section maps, twists, and fixed points: PASS', flush=True)

    report = {
        'schema': 'diophantine-research-verification/v42', 'status': 'PASS',
        'python': platform.python_version(), 'sympy': sympy.__version__,
        'checks': checks, 'new_variable_reduction': False,
        'construction_records': 'data/results_20261115_v40.json',
        'scope': 'Exact native square-extraction and scalar-dependency audits, '
                 'elliptic identities and rational odd-multiple examples, '
                 'and independently checked finite-field order and '
                 'mixed-sign certificates, and exact branch and resolution '
                 'identities for the fixed-input K3 models, and rational-section '
                 'maps, twists and fixed points. The manuscripts prove the '
                 'infinite statements. No simultaneous rational realization '
                 'or smaller defining polynomial is asserted.',
        'external_arithmetic_foundation_audited': False,
    }
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    main(parser.parse_args().report)
