#!/usr/bin/env python3
"""Authenticate and independently reconstruct the v28 degree specifications.

No files in the published checkout are modified. The historical verification
suites are separate commands and are not silently counted as run here.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[1]
REL=Path('computation/few_variables/unit_norm_v28')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    if not __debug__:raise SystemExit('Run without -O.')
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--report',type=Path)
    args=ap.parse_args()
    inputs=json.loads((ROOT/REL/'inputs.json').read_text())
    for row in inputs['files']:
        path=ROOT/row['path']
        if path.stat().st_size!=row['bytes'] or digest(path)!=row['sha256']:
            raise SystemExit('Pinned source mismatch: '+row['path'])
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    for row in manifest['files']:
        path=ROOT/row['path']
        if not path.is_file() or path.stat().st_size!=row['bytes'] or digest(path)!=row['sha256']:
            raise SystemExit('Publication byte mismatch: '+row['path'])
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONOPTIMIZE='0')
    with tempfile.TemporaryDirectory(prefix='zinq-v28-') as tmp:
        directory=Path(tmp)/'specifications';receipt=Path(tmp)/'verification.json'
        subprocess.run([sys.executable,'-B',str(ROOT/REL/'build.py'),'--output',str(directory)],check=True,cwd=ROOT,env=env)
        subprocess.run([sys.executable,'-B',str(ROOT/REL/'check.py'),'--directory',str(directory),'--output',str(receipt)],check=True,cwd=ROOT,env=env)
        outputs=list(directory.glob('*.json'))
        for path in outputs:
            if path.read_bytes()!=(ROOT/REL/'specifications'/path.name).read_bytes():
                raise SystemExit('Reconstructed specification differs: '+path.name)
        if receipt.read_bytes()!=(ROOT/REL/'verification.json').read_bytes():
            raise SystemExit('Independent verification certificate differs from published bytes')
        checks=json.loads(receipt.read_text())
    report=dict(schema='unit-norm-release-verification/v28',status='PASS',
        pinned_inputs=len(inputs['files']),publication_manifest_files=len(manifest['files']),
        reconstructed_specifications=len(outputs),independent_verification_byte_identical=True,
        full_recipe_examples=len(checks['full_recipe_examples']['examples']),
        finite_field_reconstructions=sum(len(c['finite_field_reconstructions']) for c in checks['constructions']),
        degree_corruption_controls=len(checks['negative_controls']),
        other_corruption_controls=['point multiplication','pole ordinate scaling','nonseparating element','omitted scalar norm guard'],
        native_source_sha256={r['name']:r['canonical_source_sha256'] for r in checks['constructions']},
        legacy_suite_run_by_this_script=False,earlier_cumulative_suite_run_by_this_script=False,
        independent_mathematical_review=False,
        scope='Exact formula, factor, degree and coefficient-norm checks, plus explicitly finite examples. Infinite arithmetic premises and full-unit completeness remain mathematical arguments, not computational certificates.')
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
