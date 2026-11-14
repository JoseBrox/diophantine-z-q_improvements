#!/usr/bin/env python3
"""Check the published v27 bytes, then reproduce new tables in an isolated copy.

The byte-pinned legacy suite remains a separate command. This wrapper leaves the
published tree unchanged, including machine-dependent execution receipts.
"""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()
def main() -> None:
    if not __debug__: raise SystemExit('Run without -O.')
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--report',type=Path)
    args=ap.parse_args()
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    for item in manifest['files']:
        p=ROOT/item['path']
        if not p.is_file() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']:
            raise SystemExit('Publication byte mismatch: '+item['path'])
    with tempfile.TemporaryDirectory(prefix='zinq-v27-check-') as folder:
        work=Path(folder)/'repo'
        shutil.copytree(ROOT,work,ignore=shutil.ignore_patterns('.git','__pycache__','.verification','.tex-build'))
        before={p.relative_to(work).as_posix():sha(p) for p in work.rglob('*') if p.is_file()}
        receipt=Path(folder)/'verification.json'
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONOPTIMIZE='0')
        subprocess.run([sys.executable,'-B',str(work/'scripts/verify_v27.py'),
                        '--authenticate-sources','--report',str(receipt)],cwd=work,env=env,check=True)
        runtime_receipts={
            'data/audits/verification_20261113_v24.json',
            'data/audits/verification_20261113_v25.json',
        }
        checked=0
        for rel,digest in before.items():
            if rel in runtime_receipts: continue
            if not (work/rel).is_file() or sha(work/rel)!=digest:
                raise SystemExit('Reconstruction differs from published bytes: '+rel)
            checked+=1
        report=json.loads(receipt.read_text())
        report.update(publication_manifest_files_checked=len(manifest['files']),
                      unchanged_published_files_compared=checked,
                      execution_receipt_comparison_exceptions=sorted(runtime_receipts),
                      isolated_reconstruction=True,
                      scope=report['scope']+' All published tables and non-runtime records were byte-compared after isolated reconstruction; the original tree was not modified.')
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
