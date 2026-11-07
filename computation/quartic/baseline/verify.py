#!/usr/bin/env python3
"""Verify the complete finite baseline chain. Requires Python3.10+ and Node18+."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    assert sys.version_info >= (3,10), 'Python3.10 or later is required'
    node=shutil.which('node')
    assert node, 'Node.js18 or later is required for the independent source replay'
    node_version=subprocess.check_output([node,'--version'],text=True).strip()
    assert int(node_version.lstrip('v').split('.')[0])>=18
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    for item in manifest['files']:
        assert sha(ROOT/item['path'])==item['sha256'],item['path']
    steps=[]
    # All outputs go to an isolated temporary copy. The distributed inputs
    # and their manifest remain unchanged under repeated verification.
    with tempfile.TemporaryDirectory(prefix='quartic-baseline-',dir=ROOT.parent) as tmp:
        work=Path(tmp)/'baseline'
        shutil.copytree(ROOT,work,ignore=shutil.ignore_patterns('__pycache__','verification.json'))
        for name in ('check_source_system.py','check_primary_domain.py','check_local_correction.py'):
            result=subprocess.run([sys.executable,str(work/name)],capture_output=True,text=True)
            if result.returncode:
                sys.stderr.write(result.stderr)
                raise AssertionError(name+' failed')
            data=json.loads(result.stdout)
            assert data['status']=='PASS'
            steps.append({'checker':name,'totalVariables':data['totalVariables'],'status':'PASS'})
            print(name+': PASS',flush=True)
        final=work/'data/system474/residuals.json'
        assert sha(final)=='9bd49b7542507f32e06cbc424cf223ec2b5226826b980876c7f0750edfa0e09c'
    result={'status':'PASS','python':sys.version.split()[0],'node':node_version,
            'manifestFilesVerified':len(manifest['files']),'steps':steps,
            'finalBaselineSha256':'9bd49b7542507f32e06cbc424cf223ec2b5226826b980876c7f0750edfa0e09c',
            'scope':'Independent source-builder replay, all raw gate identities, every elimination and substitution, guarded point-domain changes, and complete coefficient tables. The arithmetic inputs and rational nonzero-domain lemmas are proved or stated separately in the quartic paper.'}
    (ROOT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
