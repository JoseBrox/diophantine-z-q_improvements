#!/usr/bin/env python3
"""Reconstruct corrected 200-variable coefficients and the two local certificates.

No checkout is modified. Every generated certificate is byte-compared with the
publication. This is finite exact verification, not independent arithmetic review.
"""
from __future__ import annotations
import argparse,hashlib,json,os,platform,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
QDIR=Path('computation/quartic/shifted200_v33')
RDIR=Path('computation/pole_parameters/reflection_v33')

def require(ok,message):
    if not ok:raise AssertionError(message)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(*arguments):
    proc=subprocess.run([sys.executable,'-B',*map(str,arguments)],cwd=ROOT,text=True,capture_output=True,
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    if proc.returncode:
        raise RuntimeError(' '.join(map(str,arguments))+'\n'+proc.stdout[-6000:]+proc.stderr[-6000:])
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--report',type=Path);args=ap.parse_args()
    import sympy
    require(sympy.__version__=='1.14.0','Pinned SymPy version')
    pins=json.loads((ROOT/QDIR/'inputs.json').read_text())
    for row in pins['files']:
        p=ROOT/row['path'];require(p.stat().st_size==row['bytes'] and digest(p)==row['sha256'],'Source pin: '+row['path'])
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    for row in manifest['files']:
        p=ROOT/row['path'];require(p.is_file() and p.stat().st_size==row['bytes'] and digest(p)==row['sha256'],'Manifest: '+row['path'])
    with tempfile.TemporaryDirectory(prefix='zinq-v33-') as tmp:
        out=Path(tmp)
        run(ROOT/QDIR/'build.py','--output',out)
        run(ROOT/QDIR/'check.py','--quadratic',out/'quadratic-family.json','--output',out/'verification.json')
        run(ROOT/QDIR/'check_normalization.py','--output',out/'normalization.json')
        run(ROOT/QDIR/'balance.py','--source',out/'quadratic-family.json','--output',out)
        run(ROOT/QDIR/'check_balance.py','--directory',out,'--output',out/'balanced-verification.json')
        for p in out.glob('*.json'):
            require(p.read_bytes()==(ROOT/QDIR/p.name).read_bytes(),'Reconstructed file mismatch: '+p.name)
        for code,certificate in [('reflection_uniform11.py','uniform11.json'),('reflection_lifts.py','lifts19.json')]:
            run(ROOT/RDIR/code,'--output',out/certificate)
            require((out/certificate).read_bytes()==(ROOT/RDIR/certificate).read_bytes(),'Reflection certificate: '+certificate)
        coeff=json.loads((out/'verification.json').read_text())
        norm=json.loads((out/'normalization.json').read_text())
        balanced=json.loads((out/'balanced-verification.json').read_text())
        for value in (coeff,norm,balanced):require(value['status']=='PASS','Missing PASS status')
    result={'schema':'corrected200-release-verification/v33','status':'PASS','python':platform.python_version(),'sympy':sympy.__version__,
      'manifest_files':len(manifest['files']),'source_pins':len(pins['files']),
      'variables':200,'quadratic_rows':186,'degree':4,'integer_content':1,'monomials':3221,
      'old_scalar_shift_rejected':norm['old_shift_rejected'],'complete_coefficient_reconstruction':True,
      'exact_all_positive_parameter_height_verified':True,'reflection_certificates_byte_identical':True,
      'independent_mathematical_review':False,'legacy_suite_run_by_this_script':False,
      'scope':'Exact changed and retained quadratic rows, every expanded coefficient, physical scalar normalization, balanced coefficient envelope and support, finite identities and obstruction tables. Arithmetic premises and universal arguments require their separate mathematical proofs.'}
    text=json.dumps(result,indent=2)+'\n'
    if args.report:args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(text)
    print(text)
if __name__=='__main__':main()
