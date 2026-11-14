#!/usr/bin/env python3
"""Run the consolidated exact checks; not a proof of inherited arithmetic inputs."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    if not __debug__:
        raise SystemExit('Run without -O: the exact checkers use assertions.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--authenticate-sources', action='store_true',
                        help='Require and authenticate the four native inputs in the full checkout.')
    parser.add_argument('--report', type=Path,
                        default=ROOT/'data/audits/verification_20261113_v25.json')
    args = parser.parse_args()
    commands = [
        ['computation/sun_pr30_audit/check.py', '--output', 'data/audits/sun_pr30_20261113.json'],
        ['scripts/verify_v24.py'] + (['--authenticate-sources'] if args.authenticate_sources else []),
        ['computation/quartic/abc81_v25/build.py'],
        ['computation/quartic/abc81_v25/check.py'],
        ['computation/quartic/abc81_v25/check_examples.py'],
        ['computation/quartic/additive212_v25/build.py'],
        ['computation/quartic/additive212_v25/check.py'],
    ]
    env = dict(os.environ, PYTHONOPTIMIZE='0', PYTHONDONTWRITEBYTECODE='1')
    records = []
    for command in commands:
        print('Checking:', ' '.join(command), flush=True)
        result = subprocess.run([sys.executable, '-B', *command], cwd=ROOT,
                                text=True, capture_output=True, env=env)
        if result.returncode:
            print(result.stdout, end='')
            print(result.stderr, file=sys.stderr)
            raise SystemExit(f'FAILED: {command}')
        records.append({'command': command, 'status': 'PASS',
                        'stdout_sha256': hashlib.sha256(result.stdout.encode()).hexdigest()})
    def read(path: str):
        return json.loads((ROOT/path).read_text())
    abc = read('computation/quartic/abc81_v25/independent-verification.json')
    q212 = read('computation/quartic/additive212_v25/independent-verification.json')
    examples = read('computation/quartic/abc81_v25/elliptic-example-verification.json')
    report = {
        'schema': 'consolidated-exact-verification/v25', 'date': '2026-11-13', 'status': 'PASS',
        'python_version': platform.python_version(), 'sympy_version': abc['sympyVersion'],
        'commands': records, 'top_level_commands': len(records),
        'abc81_exact_stages': abc['stageCount'], 'additive212_exact_stages': q212['stageCount'],
        'v23_exact_stages': 25, 'finite_algebra_examples': 13,
        'elliptic_ordered_pair_examples': examples['orderedPointPairs'],
        'elliptic_regular_ratio_examples': examples['regularRatioChecks'],
        'quartic_rows_checked': {'predecessor214': 188, 'new212': 186, 'new81': 73},
        'quartic_monomials_checked': {'predecessor214': 2919, 'new212': 2908, 'new81': 941},
        'native_general_sources_authenticated': args.authenticate_sources,
        'legacy_full_verifier_run_by_this_script': False,
        'independent_non_author_review': False,
        'scope': 'Exact algebra and coefficient reconstruction, degree/norm bounds, bounded exact examples and negative controls. The arithmetic proofs and their inherited premises remain separate. This script does not publish to GitHub.'
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
