#!/usr/bin/env python3
"""Reconstruct the scalar, reference, norm-map, and obstruction certificates."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = (
    ('square-complement-baseline',
     'computation/pole_parameters/square_complement_baseline_v43',
     'check.py', 'verification.json'),
    ('scaled-reference-and-height',
     'computation/elliptic_charts/scaled_reference_v43',
     'check.py', 'verification.json'),
    ('doubled-source-norm-map',
     'computation/pole_parameters/doubled_source_congruent_twists_v43',
     'verify.py', 'certificate.json'),
    ('actual-square-complement-neighborhoods',
     'negative_results/computation/actual_square_complement_v43',
     'check.py', 'verification.json'),
    ('square-complement-normalization',
     'negative_results/computation/square_complement_normalization_v43',
     'check.py', 'verification.json'),
    ('shared-reference-test-obstructions',
     'negative_results/computation/shared_reference_tests_v43',
     'check.py', 'verification.json'),
    ('fixed-class-synchronization',
     'negative_results/computation/fixed_class_synchronization_v43',
     'verify.py', 'certificate.json'),
)


def main(output):
    import sympy
    if sympy.__version__ != '1.14.0':
        raise ValueError('Use SymPy 1.14.0.')
    checks = []
    with tempfile.TemporaryDirectory(prefix='diophantine-v43-') as directory:
        temporary = Path(directory)
        for name, package, script, certificate in PACKAGES:
            source = ROOT / package
            produced = temporary / (name + '.json')
            process = subprocess.run(
                [sys.executable, '-B', str(source / script),
                 '--output', str(produced)],
                cwd=ROOT, text=True, capture_output=True)
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
        'schema': 'diophantine-research-verification/v43',
        'status': 'PASS', 'python': platform.python_version(),
        'sympy': sympy.__version__, 'checks': checks,
        'new_variable_reduction': False,
        'construction_records': 'data/results_20261115_v40.json',
        'research_records': 'data/research_results_20261116_v43.json',
        'scope': 'Exact source bindings, scalar identities and valuation cases, '
                 'quadratic chart and height identities with the nonzero guard, '
                 'norm maps, rational normalization counterexamples, '
                 'finite-field and Hensel-lifting certificates, branch data, '
                 'quotient maps, and geometric invariant identities. '
                 'The manuscripts prove the infinite statements. '
                 'Neither a common rational detector fiber nor a smaller '
                 'complete defining polynomial is asserted.',
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
