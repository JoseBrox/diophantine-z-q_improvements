#!/usr/bin/env python3
"""Reconstruct norm, prescribed-trace, reference-cover and obstruction certificates."""
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
    with tempfile.TemporaryDirectory(prefix='diophantine-v47-') as directory:
        temporary = Path(directory)
        cases = [
            ('norm-compatible-scalar', 'computation/pole_parameters/norm_scalar_v47',
             [('check.py', 'certificate.json'),
              ('independent-check.py', 'independent-verification.json')]),
            ('reference-covers', 'computation/elliptic_charts/reference_covers_v47',
             [('check.py', 'certificate.json'),
              ('independent_check.py', 'independent-verification.json')]),
            ('signed-finite-class-obstruction',
             'negative_results/computation/finite_nonsquare_classes_v47',
             [('check.py', 'certificate.json')]),
        ]
        for name, package, scripts in cases:
            files = []
            for script, certificate in scripts:
                produced = temporary / (name + '-' + certificate)
                run(package + '/' + script, '--output', produced)
                files.append(compare(produced, ROOT / package / certificate))
            checks.append({'name': name, 'status': 'PASS', 'files': files})
            print(name + ': PASS', flush=True)

        package = 'computation/pole_parameters/native_trace_fixture_v47'
        fixture = temporary / 'fixture.json'
        scaling = temporary / 'scaling.json'
        run(package + '/build-fixture.py', '--output', fixture)
        run(package + '/build-scaling.py', '--fixture', fixture, '--output', scaling)
        files = [compare(fixture, ROOT / package / 'fixture.json'),
                 compare(scaling, ROOT / package / 'scaling.json')]
        for script, certificate in [('check.py', 'verification.json'),
                                    ('independent-check.py', 'independent-verification.json')]:
            produced = temporary / certificate
            run(package + '/' + script, '--fixture', fixture,
                '--scaling', scaling, '--output', produced)
            files.append(compare(produced, ROOT / package / certificate))
        checks.append({'name': 'actual-prescribed-trace-fixture',
                       'status': 'PASS', 'files': files})
        print('actual-prescribed-trace-fixture: PASS', flush=True)
    report = {
        'schema': 'diophantine-exact-verification/v47',
        'status': 'PASS', 'python': platform.python_version(),
        'sympy': sympy.__version__, 'checks': checks,
        'total_variable_counts': {'general': 25, 'explicit_general': 27,
            'weak_abc': 13, 'quartic': 195, 'explicit_quartic': 257, 'abc_quartic': 74},
        'new_variable_reduction': False,
        'construction_records': 'data/results_20261116_v47.json',
        'negative_results_catalog': 'negative_results/data/results.json',
        'scope': 'Exact norm-scalar algebra and local preparation; actual two-block '
                 'prescribed traces and all 128 complement guards for inputs -1 and 1 '
                 'at B=3 with fixed S-unit rescaling; universal reference-cover and '
                 'paired trace identities; finite-class obstruction certificates. '
                 'The manuscripts prove the infinite implications under their stated '
                 'premises. Uniform prescribed-trace realization and a complete '
                 'quartic saving remain unproved.',
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
