#!/usr/bin/env python3
"""Reproduce the current finite algebra and quartic certificates in temporary files."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(script, *arguments):
    process = subprocess.run([sys.executable, '-B', str(ROOT / script), *map(str, arguments)],
                             cwd=ROOT, capture_output=True, text=True)
    require(process.returncode == 0,
            script + ' failed:\n' + process.stdout[-6000:] + process.stderr[-6000:])
    return process.stdout


def compare(produced, stored):
    require(produced.read_bytes() == stored.read_bytes(),
            'Reconstruction differs: ' + str(stored.relative_to(ROOT)))
    return {'path': str(stored.relative_to(ROOT)), 'sha256': sha256(produced)}


def main(report_path):
    import sympy
    require(sympy.__version__ == '1.14.0', 'Use SymPy 1.14.0.')
    checks = []
    with tempfile.TemporaryDirectory(prefix='diophantine-v40-') as directory:
        temporary = Path(directory)

        for label, relative in [
            ('integral-pell-labels', 'computation/integer_labels/pell_compression_v40'),
            ('three-coordinate-reference', 'computation/elliptic_charts/three_coordinate_v40'),
        ]:
            output = temporary / (label + '.json')
            run(relative + '/check.py', '--output', output)
            checks.append({'name': label, 'status': 'PASS',
                           'certificate': compare(output, ROOT / relative / 'certificate.json')})
            print(label + ': PASS', flush=True)

        relative = 'computation/few_variables/terminal_root_v40'
        output = temporary / 'terminal-specifications'
        run(relative + '/build.py', '--output', output)
        files = [compare(p, ROOT / relative / 'specifications' / p.name)
                 for p in sorted(output.glob('*.json'))]
        require(len(files) == 5, 'Four terminal-root specifications and their bounds.')
        receipt = temporary / 'terminal-verification.json'
        run(relative + '/check.py', '--specifications', output, '--output', receipt)
        files.append(compare(receipt, ROOT / relative / 'verification.json'))
        checks.append({'name': 'terminal-root-descent', 'status': 'PASS', 'files': files})
        print('terminal-root-descent: PASS', flush=True)

        relative = 'computation/quartic/abc78_reduced_v40'
        output = temporary / 'abc78'
        run(relative + '/build.py', '--output', output)
        files = [compare(p, ROOT / relative / p.name) for p in sorted(output.glob('*.json'))]
        require(len(files) == 3, 'Three abc78 construction tables.')
        receipt = temporary / 'abc78-verification.json'
        run(relative + '/check.py', '--output', receipt)
        files.append(compare(receipt, ROOT / relative / 'independent-verification.json'))
        checks.append({'name': 'paired-ratio-abc78', 'status': 'PASS', 'files': files})
        print('paired-ratio-abc78: PASS', flush=True)

        relative = 'computation/quartic/paired_redundancy196_v40'
        output = temporary / 'quartic196'
        run(relative + '/build.py', '--output', output)
        files = [compare(p, ROOT / relative / p.name) for p in sorted(output.glob('*.json'))]
        require(len(files) == 5, 'Five quartic196 construction tables.')
        run(relative + '/check.py', '--directory', output, '--write-certificate')
        files.append(compare(output / 'certificate.json', ROOT / relative / 'certificate.json'))
        checks.append({'name': 'paired-ratio-quartic196', 'status': 'PASS', 'files': files})
        print('paired-ratio-quartic196: PASS', flush=True)

        relative = 'computation/quartic/abc78_balanced_v40'
        output = temporary / 'primitive-abc78'
        run(relative + '/build.py', '--output', output)
        files = [compare(p, ROOT / relative / p.name) for p in sorted(output.glob('*.json'))]
        require(len(files) == 3, 'Three primitive-basis abc78 tables.')
        run(relative + '/check.py', '--output', output)
        files.append(compare(output / 'independent-verification.json',
                             ROOT / relative / 'independent-verification.json'))
        files.append({'path': relative + '/basis-certificate.json',
                      'sha256': sha256(ROOT / relative / 'basis-certificate.json')})
        checks.append({'name': 'primitive-basis-abc78', 'status': 'PASS', 'files': files})
        print('primitive-basis-abc78: PASS', flush=True)

        relative = 'computation/quartic/primitive_basis196_v40'
        output = temporary / 'primitive-quartic196'
        run(relative + '/build.py', '--output', output)
        files = [compare(p, ROOT / relative / p.name) for p in sorted(output.glob('*.json'))]
        require(len(files) == 3, 'Three primitive-basis quartic196 tables.')
        run(relative + '/check.py', '--directory', output, '--write-certificate')
        files.append(compare(output / 'certificate.json', ROOT / relative / 'certificate.json'))
        files.append({'path': relative + '/transform.json',
                      'sha256': sha256(ROOT / relative / 'transform.json')})
        checks.append({'name': 'primitive-basis-quartic196', 'status': 'PASS', 'files': files})
        print('primitive-basis-quartic196: PASS', flush=True)

    report = {
        'schema': 'diophantine-exact-verification/v40',
        'status': 'PASS', 'python': platform.python_version(), 'sympy': sympy.__version__,
        'checks': checks,
        'total_variable_counts': {'general': 25, 'explicit_general': 27,
                                 'weak_abc': 13, 'quartic': 196,
                                 'explicit_quartic': 258, 'abc_quartic': 78},
        'new_variable_reduction': False,
        'external_arithmetic_premises_certified': False,
        'scope': 'Exact source bindings, independent coefficient reconstruction, '
                 'finite-algebra examples and proof certificates. The accompanying '
                 'papers prove the infinite algebraic implications. Arithmetic '
                 'realization and height premises remain explicitly inherited.',
    }
    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    main(parser.parse_args().report)
