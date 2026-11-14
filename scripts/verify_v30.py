#!/usr/bin/env python3
"""Authenticate v30 source files and reconstruct all new exact certificates.

Does not alter the checkout. Legacy suites are separate commands.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
REL=Path('computation/few_variables/subalgebra_norms_v30')
POLE=Path('computation/pole_parameters/common_twists_v30')

def require(ok,message):
    if not ok:raise AssertionError(message)

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def run(*args):
    proc=subprocess.run([sys.executable,'-B',*map(str,args)],cwd=ROOT,text=True,capture_output=True,
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    if proc.returncode:sys.stderr.write(proc.stdout[-8000:]+proc.stderr[-8000:]);raise SystemExit('Failed command: '+' '.join(map(str,args)))

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--report',type=Path);a=ap.parse_args()
    import sympy
    require(sympy.__version__=='1.14.0','Use the pinned SymPy 1.14.0')
    inputs=json.loads((ROOT/REL/'inputs.json').read_text())
    for row in inputs['files']:
        p=ROOT/row['path'];require(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'Input mismatch: '+row['path'])
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    for row in manifest['files']:
        p=ROOT/row['path'];require(p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'Manifest mismatch: '+row['path'])
    with tempfile.TemporaryDirectory(prefix='zinq-v30-') as tmp:
        t=Path(tmp);specs=t/'specifications';cert=t/'certificate.json';pole=t/'pole.json'
        run(ROOT/REL/'build.py','--output',specs)
        run(ROOT/REL/'check.py','--directory',specs,'--output',cert)
        for p in specs.glob('*.json'):require(p.read_bytes()==(ROOT/REL/'specifications'/p.name).read_bytes(),'Specification mismatch: '+p.name)
        require(cert.read_bytes()==(ROOT/REL/'verification.json').read_bytes(),'Independent algebra certificate mismatch')
        run(ROOT/POLE/'check.py','--output',pole)
        require(pole.read_bytes()==(ROOT/POLE/'verification.json').read_bytes(),'Pole application certificate mismatch')
        algebra=json.loads(cert.read_text());twists=json.loads(pole.read_text())
        # Parameter tests are separate finite checks of degree uniformity.
        def load(name,path):
            spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
        producer=load('v30_producer',ROOT/REL/'build.py');checker=load('v30_checker',ROOT/REL/'check.py')
        parameter_checks=[]
        for name,parameters in [('general25',(5,101)),('explicit27',(5,20485)),('weak13',(5,101)),('abc13',(5,101))]:
            baseline=json.loads((specs/(name+'.json')).read_text())['bounds']['degree_bound']
            for parameter in parameters:
                src=producer.make_source(name,parameter);spec=producer.compile_specification(src);checker.verify_spec(src,spec)
                require(spec['bounds']['degree_bound']==baseline,'Parameter degree changed')
                parameter_checks.append(dict(name=name,parameter=parameter,degree_bound=baseline))
    report=dict(schema='subalgebra-norm-release-verification/v30',status='PASS',python=platform.python_version(),sympy=sympy.__version__,
        base_remote_commit=inputs['source_commit'],pinned_inputs=len(inputs['files']),manifest_files=len(manifest['files']),
        reconstructed_specifications=5,algebra_certificate_byte_identical=True,pole_certificate_byte_identical=True,
        small_finite_algebra_examples=len(algebra['finite_algebra_checks']['examples']),
        deliberate_algebra_mutations=len(algebra['mutation_controls']),prepared_pole_pairs=len(twists['prepared_examples']),
        additional_parameter_examples=parameter_checks,global_variable_count_improvement=False,
        legacy_suite_run_by_this_script=False,earlier_cumulative_suite_run_by_this_script=False,
        independent_mathematical_review=False,scope='Exact reproducibility and stated finite algebra checks. No production determinant expansion, external arithmetic proof audit or remote GitHub CI is claimed by this receipt.')
    if a.report:a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
