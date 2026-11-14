#!/usr/bin/env python3
"""Reproduce the v24 algebraic checks, without claiming a foundational audit."""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--authenticate-sources', action='store_true',
                    help='Require the complete pinned native sources in this checkout.')
    args=ap.parse_args()
    few='computation/few_variables/triangular_elimination_v24'
    quartic='computation/quartic/balanced214_v24'
    commands=[
        [f'{few}/build.py']+(['--source-checkout',str(ROOT)] if args.authenticate_sources else []),
        [f'{few}/check_bounds.py'],[f'{few}/check_examples.py'],
        [f'{quartic}/build.py'],[f'{quartic}/check.py']]
    records=[]
    for command in commands:
        run=subprocess.run([sys.executable,*command],cwd=ROOT,text=True,capture_output=True)
        print(run.stdout,end='')
        if run.returncode:
            print(run.stderr,file=sys.stderr)
            raise SystemExit(f'Failed command: {command}')
        records.append(dict(command=command,status='PASS',
                            stdout_sha256=hashlib.sha256(run.stdout.encode()).hexdigest()))
    report=dict(schema='algebraic-improvements-verification/v24',date='2026-11-13',status='PASS',
        complete_checkout_sources_authenticated=args.authenticate_sources,
        repository_wide_verifier_run=False,non_author_review=False,
        exact_finite_algebra_examples=13,degree_and_norm_bound_constructions=4,
        quartic_rows_checked=188,quartic_coefficient_profiles_checked=2919,
        commands=records,
        scope='The new algebraic calculations only. Does not run the previous full suite, prove arithmetic foundations, or attest non-author independence.')
    output=ROOT/'data/audits/verification_20261113_v24.json'
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
