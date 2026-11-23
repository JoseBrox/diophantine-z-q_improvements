#!/usr/bin/env python3
"""Reconstruct adaptive-level identities and the separate affine obstruction."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CONTRIBUTORS_HASH = '7c4e19ff00bd3f87f97db5ba836cea716e72fa8b583756c1a4fd7c5b5a075214'


def main(output):
    import sympy
    if sympy.__version__ != '1.14.0':
        raise ValueError('Use SymPy 1.14.0.')
    checks = []
    packages = (
        ('computation/pole_parameters/adaptive_levels_v50', 'certificate.json'),
        ('negative_results/computation/affine_coupling_v50', 'affine_coupling_certificate.json'),
    )
    with tempfile.TemporaryDirectory(prefix='diophantine-v50-') as directory:
        for index, (package, certificate) in enumerate(packages):
            generated = Path(directory) / str(index) / certificate
            run = subprocess.run([sys.executable, '-B', str(ROOT/package/'check.py'),
                                  '--output', str(generated)], cwd=ROOT,
                                 capture_output=True, text=True)
            if run.returncode:
                raise ValueError(package + ':\n' + run.stdout + run.stderr)
            stored = ROOT / package / certificate
            if generated.read_bytes() != stored.read_bytes():
                raise ValueError('Reconstruction differs: ' + str(stored))
            checks.append({'package':package, 'status':'PASS',
                           'certificate':str(stored.relative_to(ROOT)),
                           'sha256':hashlib.sha256(generated.read_bytes()).hexdigest()})
            print(package + ': PASS', flush=True)
    readme = (ROOT/'README.md').read_text()
    match = re.search(r'(?ms)^## Contributors and citation\n.*?(?=^## |\Z)', readme)
    if not match or hashlib.sha256(match.group().encode()).hexdigest() != CONTRIBUTORS_HASH:
        raise ValueError('The user contribution and citation section changed.')
    current = json.loads((ROOT/'data/results_20261116_v50.json').read_text())
    previous = json.loads((ROOT/'data/results_20261116_v49.json').read_text())
    if current['current_constructions'] != previous['current_constructions']:
        raise ValueError('This local extension must not change the construction records.')
    extension = current['adaptive_complements']
    assert extension['actual_uniform_rational_realization_proved'] is False
    assert extension['new_defining_variable_count'] is False
    assert extension['realization_targets'] == [21,9]
    report = {
        'schema':'diophantine-exact-verification/v50', 'status':'PASS',
        'python':platform.python_version(), 'sympy':sympy.__version__,
        'checks':checks, 'contribution_and_citation_section_sha256':CONTRIBUTORS_HASH,
        'construction_records_unchanged_from':'data/results_20261116_v49.json',
        'current_records':'data/results_20261116_v50.json',
        'established_general_counts':[25,13], 'abc_quartic_variables':71,
        'actual_uniform_rational_realization_proved':False,
        'new_defining_variable_count':False,
        'scope':'Exact universal identities and specified finite local examples, '
                'plus the exact counterexample to affine scalar coupling. '
                'The manuscripts prove the local and guard extensions and the '
                'source-specific infinite-family obstruction. The actual '
                'simultaneous prescribed-trace incidence remains unproved.',
        'external_arithmetic_foundation_audited':False,
    }
    if output:
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path)
    main(parser.parse_args().report)
