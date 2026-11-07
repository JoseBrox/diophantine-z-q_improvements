#!/usr/bin/env python3
"""Rebuild and independently verify the two preferred specifications.

Uses Python's standard library only. Frozen sources and specifications are
not overwritten; reconstructed files are compared in a temporary directory.
"""
from pathlib import Path
import gzip
import hashlib
import json
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
CASES = [
    ('finite', 29,
     '56f7685781adf0ed07cd3b2f6151110354998555dbf63a34fbea6d15edddc6a3',
     'aac8f38f50c6780bec58bcc7057b43a324270e4f7ad6d439151773f512227072'),
    ('semilocal', 31,
     'd62fb492a67271c8a3da695ea5d28a8af8e63480a5fe551a963a7e4299a37a5c',
     'ed3ee79fa33a7492b4c3990f34aacb1a39810b062378f17ec955905126a8a789'),
]


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def run(*args):
    result = subprocess.run([sys.executable, *map(str, args)], cwd=HERE,
                            text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stdout+'\n'+result.stderr)
    return result.stdout


def main():
    run(HERE/'verify_explicit_height_constant.py')
    run(HERE.parent/'verify_quadratic_height.py')
    run(HERE/'check_preferred_source.py')
    checked = []
    with tempfile.TemporaryDirectory(prefix='preferred-check-', dir=HERE) as directory:
        work = Path(directory)
        for anchor, total, source_sha, spec_sha in CASES:
            source = work/f'source-{total}.json.gz'
            output = work/f'polynomial-{total}'
            run(HERE/'build_preferred_source.py', '--anchor', anchor, '--output', source)
            raw = gzip.decompress(source.read_bytes())
            frozen_raw = gzip.decompress((HERE/f'source-{total}-preferred.json.gz').read_bytes())
            assert raw == frozen_raw and digest(raw) == source_sha
            run(HERE/'compile_source.py', source, '--output', output)
            spec_path = output/'polynomial-specification.json'
            spec_raw = spec_path.read_bytes()
            assert digest(spec_raw) == spec_sha
            assert spec_raw == (HERE/f'polynomial-{total}-preferred/polynomial-specification.json').read_bytes()
            run(HERE/'verify_specification.py', source, spec_path)
            receipt = json.loads((output/'verification.json').read_text())
            assert receipt['status'] == 'passed'
            checked.append({
                'total_variables': total,
                'source_rebuilt_identically': True,
                'specification_rebuilt_identically': True,
                'independent_coefficient_checker_passed': True,
                'source_sha256': source_sha,
                'specification_sha256': spec_sha,
                'degree_bound_power_of_two_exponent': receipt['degree_bound_power_of_two_exponent'],
                'coefficient_height_bound_double_power_of_two_exponent': receipt['coefficient_height_bound_double_power_of_two_exponent'],
            })
    run(HERE.parent/'verify_norm_height_obstruction.py')
    report = {
        'status': 'passed', 'cases': checked,
        'semantic_and_exact_arithmetic_checker_passed': True,
        'norm_height_obstruction_checker_passed': True,
        'external_software_dependencies': 'Python 3 standard library only',
        'scope': 'Reproduction and independent implementation checks; the named inherited arithmetic hypotheses remain separate mathematical inputs.',
        'reproducer_sha256': digest(Path(__file__).read_bytes()),
    }
    (HERE/'reproduction-verification.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
