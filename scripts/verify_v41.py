#!/usr/bin/env python3
"""Reproduce the local pole and automatic-conic obstruction certificates."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = [
    ('shared-parameter-local-solubility', 'shared_parameter_local_v41', 'verification.json'),
    ('all-rational-conic-chain-coefficients', 'conic_chain_v41', 'certificate.json'),
    ('automatic-conic-global-obstructions', 'automatic_conic_v41', 'verification.json'),
]


def main(output):
    import sympy
    if sympy.__version__ != '1.14.0':
        raise ValueError('Use SymPy 1.14.0.')
    checks = []
    with tempfile.TemporaryDirectory(prefix='diophantine-v41-') as directory:
        temporary = Path(directory)
        for name, package, certificate in PACKAGES:
            source = ROOT / 'computation/pole_parameters' / package
            produced = temporary / (package + '.json')
            process = subprocess.run(
                [sys.executable, '-B', str(source / 'check.py'), '--output', str(produced)],
                cwd=ROOT, capture_output=True, text=True)
            if process.returncode:
                raise ValueError(name + ' failed:\n' + process.stdout[-6000:]
                                 + process.stderr[-6000:])
            stored = source / certificate
            if produced.read_bytes() != stored.read_bytes():
                raise ValueError('Certificate reconstruction differs: ' + str(stored))
            checks.append({
                'name': name, 'status': 'PASS',
                'certificate': str(stored.relative_to(ROOT)),
                'sha256': hashlib.sha256(produced.read_bytes()).hexdigest(),
            })
            print(name + ': PASS', flush=True)
    report = {
        'schema': 'diophantine-pole-verification/v41', 'status': 'PASS',
        'python': platform.python_version(), 'sympy': sympy.__version__,
        'checks': checks, 'new_variable_reduction': False,
        'construction_records': 'data/results_20261115_v40.json',
        'scope': 'Exact polynomial identities, native pole-guard audit, finite local '
                 'certificates, and independently computed Tunnell coefficients. '
                 'The accompanying proofs establish the universal local and '
                 'obstruction statements. No simultaneous rational realization '
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
