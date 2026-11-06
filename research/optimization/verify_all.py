#!/usr/bin/env python3
"""Run the documented finite checks without changing the released package.

The resulting receipt certifies only these executions. It does not certify
the arithmetic theorem that the original source defines Z in Q.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PREFIX = Path('research/optimization')


def main():
    baseline = REPO / 'quartics/quartic-12504'
    expected = '7f5aa3117af82a0b323f0a4e74a18599204f5540408106d3ce99612b5ed830ca'
    actual = hashlib.sha256((baseline/'polynomial.expanded.txt').read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit('The released coefficient table does not match the pinned baseline.')
    jobs = [
        ('quartic-12493', [str(PREFIX/'quartic-anchor-packed/verify_anchor.py'),
                          str(PREFIX/'quartic-anchor-packed'), '--baseline', str(baseline)]),
        ('quartic-12465', [str(PREFIX/'quartic-anchor-packed-large/verify_anchor.py'),
                          str(PREFIX/'quartic-anchor-packed-large'), '--baseline', str(baseline)]),
        ('quartic-12449', [str(PREFIX/'verify_constant_quartic.py')]),
        ('square-root-identities', [str(PREFIX/'verification/check_square_root_compression.py')]),
        ('finite-fibre-inventory', [str(PREFIX/'verification/check_finite_fibre_inventory.py'),
                                  str(baseline/'source'), '--output',
                                  str(PREFIX/'verification/finite_fibre_inventory_verification.json')]),
        ('number-field-section', [str(PREFIX/'verification/check_base_change.py'),
                                  str(baseline), '--output',
                                  str(PREFIX/'verification/base_change_verification.json')]),
        ('circuit-855', [str(PREFIX/'verify_compact_polynomial.py')]),
        ('circuit-854', [str(PREFIX/'verify_compact_854.py')]),
        ('circuit-853-and-pole-guards', [str(PREFIX/'verify_compact_853.py')]),
    ]
    out = HERE/'verification'
    logs = out/'logs'
    logs.mkdir(parents=True, exist_ok=True)
    checks = []
    for label, args in jobs:
        command = [sys.executable, '-E', '-B', *args]
        result = subprocess.run(command, cwd=REPO, capture_output=True, text=True)
        log = logs/(label+'.txt')
        log.write_text(result.stdout + ('\nSTDERR:\n'+result.stderr if result.stderr else ''))
        entry = {'check': label, 'arguments': args, 'exit_code': result.returncode,
                 'status': 'PASS' if result.returncode == 0 else 'FAIL',
                 'log': str(log.relative_to(HERE)),
                 'log_sha256': hashlib.sha256(log.read_bytes()).hexdigest()}
        checks.append(entry)
        print(label+': '+entry['status'], flush=True)
        if result.returncode:
            break
    receipt = {
        'status': 'PASS' if len(checks) == len(jobs) and all(c['exit_code'] == 0 for c in checks) else 'FAIL',
        'baseline_revision': '28e87b1b62af0effd954605af7f70b2699dd5672',
        'baseline_coefficient_sha256': actual,
        'python_version': sys.version.split()[0],
        'checks': checks,
        'scope': 'Finite algebraic transformations, stated symbolic identities, inventories, and bounds. The 855 source-formula comparison includes sampled modular tests explicitly identified in its own receipt. No independent proof of the original arithmetic characterization or global minimality.',
        'verifier_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (out/'all-checks.json').write_text(json.dumps(receipt, indent=2)+'\n')
    raise SystemExit(0 if receipt['status'] == 'PASS' else 1)


if __name__ == '__main__':
    main()
