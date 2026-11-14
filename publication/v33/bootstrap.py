#!/usr/bin/env python3
"""Authenticate the cumulative source transport and bind native release evidence."""
from __future__ import annotations
import argparse,base64,hashlib,json,lzma,os,platform,subprocess,sys
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parents[2]
PAYLOAD_SHA='bf6fe0cec8478b3a150c27542fbfe509d7c7567e6a1db10938897cfa77cf257e'
QDIR='computation/quartic/shifted200_v33'
RDIR='computation/pole_parameters/reflection_v33'
PUBLISHER='.github/workflows/publication-v33.yml'

def require(ok,msg):
    if not ok:raise SystemExit(msg)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def run(*args):subprocess.run([sys.executable,'-B',*map(str,args)],cwd=ROOT,check=True)
def verify_manifest(manifest,clean=False):
    for item in manifest['files']:
        p=ROOT/item['path']
        if clean and item['path']=='.github/workflows/verify.yml':p=ROOT/'publication/v33/final-verify.yml'
        raw=p.read_bytes();require(len(raw)==item['bytes'] and sha(raw)==item['sha256'],'Manifest mismatch: '+item['path'])
def prepare():
    encoded=''.join((ROOT/f'publication/v33/part-{i:02d}.b64').read_text().strip() for i in range(1,9))
    raw=base64.b64decode(encoded,validate=True);require(sha(raw)==PAYLOAD_SHA,'Transport hash mismatch')
    files=json.loads(lzma.decompress(raw));require(len(files)==35,'Unexpected source count')
    for name,text in files.items():
        p=PurePosixPath(name);require(not p.is_absolute() and '..' not in p.parts and p.parts[0]!='.git' and isinstance(text,str),'Unsafe transport member')
        require(not name.startswith('.github/'),'The runner must not change workflow definitions')
        target=ROOT/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text,encoding='utf-8')
    run('computation/few_variables/subalgebra_norms_v30/build.py')
    run('computation/few_variables/subalgebra_norms_v30/check.py','--output','computation/few_variables/subalgebra_norms_v30/verification.json')
    run('computation/pole_parameters/common_twists_v30/check.py','--output','computation/pole_parameters/common_twists_v30/verification.json')
    run(QDIR+'/build.py');run(QDIR+'/check.py');run(QDIR+'/check_normalization.py','--output',QDIR+'/normalization.json')
    run(QDIR+'/balance.py');run(QDIR+'/check_balance.py')
    run(RDIR+'/reflection_uniform11.py','--output',RDIR+'/uniform11.json')
    run(RDIR+'/reflection_lifts.py','--output',RDIR+'/lifts19.json')
    expected=json.loads((ROOT/'publication/v33/expected-generated.json').read_text())
    require(len(expected)==17,'Generated output count')
    for name,record in expected.items():
        raw=(ROOT/name).read_bytes();require(len(raw)==record['bytes'] and sha(raw)==record['sha256'],'Reconstruction mismatch: '+name)
    p=ROOT/'data/results.json';data=json.loads(p.read_text())
    data.update(current_results_reference='data/results_20261115_v33.json',current_results_guide='docs/results_20261115_v33.md')
    p.write_text(json.dumps(data,indent=2)+'\n')
    run('scripts/update_manifest.py');verify_manifest(json.loads((ROOT/'MANIFEST.json').read_text()))
    print('Authenticated 35 source files and regenerated 17 exact output files.')
def finalize(args):
    require(sys.version_info[:2]==(3,12),'Native Python 3.12 required')
    import sympy
    require(sympy.__version__=='1.14.0','Pinned SymPy required')
    reports={name:json.loads(Path(getattr(args,name)).read_text()) for name in ['v33','v30','v28','v27','legacy']}
    for name,report in reports.items():require(report.get('status')=='PASS',name+' did not pass')
    require(len(reports['legacy']['stages'])==126,'Expected all 126 legacy stages')
    require(reports['v27']['top_level_commands']==10,'Expected 10 earlier cumulative commands')
    require(reports['v30']['reconstructed_specifications']==5,'Expected five v30 specifications')
    require(reports['v33']['old_scalar_shift_rejected'] and reports['v33']['monomials']==3221,'Corrected scalar verification missing')
    receipt=dict(schema='native-cumulative-publication/v33',status='PASS',source_commit=os.environ['GITHUB_SHA'],workflow_run=os.environ['GITHUB_RUN_ID'],python=platform.python_version(),sympy=sympy.__version__,
        legacy_stages=126,earlier_cumulative_commands=10,v30_reconstructed_specifications=5,
        quartic_variables=200,quartic_rows=186,quartic_monomials=3221,old_scalar_shift_rejected=True,
        all_fixed_positive_parameter_coefficients_checked=True,source_transport_sha256=PAYLOAD_SHA,
        report_sha256={name:sha(Path(getattr(args,name)).read_bytes()) for name in reports},
        external_arithmetic_independently_audited=False,independent_mathematical_review=False,
        scope='Native exact source reconstruction and all retained verification suites. The 200-variable projection theorem retains explicitly stated arithmetic inputs. Previous v32 scalar-shift tables are superseded. New proofs are TeX-only; this receipt does not assert independent mathematical acceptance.')
    (ROOT/'data/audits/integration_20261115_v33.json').write_text(json.dumps(receipt,indent=2)+'\n')
    for name in reports:
        (ROOT/f'data/audits/native_{name}_20261115_v33.json').write_bytes(Path(getattr(args,name)).read_bytes())
    run('scripts/update_manifest.py')
    final=json.loads((ROOT/'MANIFEST.json').read_text())
    final['files']=[r for r in final['files'] if not r['path'].startswith('publication/v33/') and r['path']!=PUBLISHER]
    verify_raw=(ROOT/'publication/v33/final-verify.yml').read_bytes()
    for r in final['files']:
        if r['path']=='.github/workflows/verify.yml':r.update(bytes=len(verify_raw),sha256=sha(verify_raw))
    verify_manifest(final,True)
    (ROOT/'publication/v33/final-MANIFEST.json').write_text(json.dumps(final,indent=2)+'\n')
    run('scripts/update_manifest.py');verify_manifest(json.loads((ROOT/'MANIFEST.json').read_text()))
    print('Native integration bound; clean manifest entries:',len(final['files']))
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('mode',choices=['prepare','finalize'])
    for name in ['v33','v30','v28','v27','legacy']:ap.add_argument('--'+name)
    args=ap.parse_args()
    if args.mode=='prepare':prepare()
    else:
        require(all(getattr(args,n) for n in ['v33','v30','v28','v27','legacy']),'All receipts required');finalize(args)
if __name__=='__main__':main()
