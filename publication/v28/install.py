#!/usr/bin/env python3
"""Authenticate the v28 source transport and bind native verification receipts."""
import hashlib, io, json, os, platform, shutil, subprocess, sys, tarfile
from pathlib import Path, PurePosixPath
ROOT=Path(__file__).resolve().parents[2]
STAGE=ROOT/'publication/v28'
EXPECTED='4a05daf63ff7e7da3f0609a7c35ebbb4f4558614f06df1002864eefd920752fc'
def dump(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2)+'\n')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def install():
    raw=b''.join((STAGE/f'part-{i:02d}.bin').read_bytes() for i in range(1,6))
    if hashlib.sha256(raw).hexdigest()!=EXPECTED:raise SystemExit('Source archive hash mismatch')
    with tarfile.open(fileobj=io.BytesIO(raw),mode='r:xz') as tf:
        members=tf.getmembers()
        if len(members)!=14:raise SystemExit('Unexpected source member count')
        for item in members:
            p=PurePosixPath(item.name)
            if not item.isfile() or p.is_absolute() or '..' in p.parts or '.git' in p.parts or '.github' in p.parts:
                raise SystemExit('Unsafe source member: '+item.name)
            target=ROOT/item.name
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(tf.extractfile(item).read())
    data=json.loads((ROOT/'data/results.json').read_text())
    data.update(json.loads((STAGE/'results-pointer.json').read_text()))
    dump(ROOT/'data/results.json',data)
    print('Authenticated and installed fourteen source and publication files.')
def expected():
    records=json.loads((STAGE/'expected.json').read_text())
    for path,row in records.items():
        p=ROOT/path
        if p.stat().st_size!=row['bytes'] or digest(p)!=row['sha256']:
            raise SystemExit('Reconstructed bytes differ: '+path)
    print('All seven reconstructed publication records match the local exact checks.')
def record():
    reports={name:json.loads(Path('/tmp/'+name+'.json').read_text()) for name in ('v28','retained-v27','legacy')}
    if any(r.get('status')!='PASS' for r in reports.values()):raise SystemExit('Verification receipt not PASS')
    if len(reports['legacy'].get('stages',[]))!=126:raise SystemExit('Expected 126 legacy stages')
    for name,report in reports.items():dump(ROOT/f'data/audits/native_{name}_20261114_v28.json',report)
    dump(ROOT/'data/audits/integration_20261114_v28.json',dict(
        schema='general-degree-native-integration/v28',status='PASS',
        source_commit=os.environ['GITHUB_SHA'],workflow_run=os.environ['GITHUB_RUN_ID'],
        python=platform.python_version(),platform=platform.platform(),
        legacy_stages=126,earlier_cumulative_commands=reports['retained-v27']['top_level_commands'],
        v28_pinned_inputs=reports['v28']['pinned_inputs'],v28_reconstructed_specifications=reports['v28']['reconstructed_specifications'],
        source_transport_sha256=EXPECTED,independent_mathematical_review=False,
        scope='Native exact reconstruction and publication-byte checks. Infinite arithmetic premises remain assumptions; no new PDF is published.'))
    subprocess.run([sys.executable,'-B',str(ROOT/'scripts/update_manifest.py')],check=True,cwd=ROOT)
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    manifest['files']=[r for r in manifest['files'] if not r['path'].startswith('publication/v28/') and r['path']!='.github/workflows/publication-v28.yml']
    workflow=(STAGE/'final-verify.yml').read_bytes()
    for row in manifest['files']:
        if row['path']=='.github/workflows/verify.yml':row.update(bytes=len(workflow),sha256=hashlib.sha256(workflow).hexdigest())
    dump(STAGE/'final_MANIFEST.json',manifest)
    subprocess.run([sys.executable,'-B',str(ROOT/'scripts/update_manifest.py')],check=True,cwd=ROOT)
    print('Bound native receipts and prepared the clean final manifest; no workflow definitions were changed.')
if __name__=='__main__':
    {'install':install,'expected':expected,'record':record}[sys.argv[1]]()
