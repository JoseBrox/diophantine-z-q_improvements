#!/usr/bin/env python3
"""Verify the exact-square research checkpoint without changing result records."""
from pathlib import Path
from importlib.metadata import version
import argparse
import hashlib
import json
import os
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
PACKAGE=ROOT/'computation/actual_square_v83'


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    assert version('sympy')=='1.14.0'
    assert version('passagemath-pari')=='10.8.14'
    manifest=read(PACKAGE/'manifest.json')
    actual={str(p.relative_to(PACKAGE)) for p in PACKAGE.rglob('*')
            if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts}
    assert actual==set(manifest['files'])
    for name,h in manifest['files'].items():
        assert sha(PACKAGE/name)==h,name
    for name,h in manifest['retained_source_pins'].items():
        assert sha(ROOT/name)==h,name
    review=read(PACKAGE/'manual_review.json')
    assert review['status']=='PASS within the stated scope'
    assert review['new_defining_variable_count'] is False
    assert review['actual_detector_counterexample_claimed'] is False
    for name,h in review['reviewed_sha256'].items():
        assert sha(PACKAGE/name)==h,name
    stages=[]
    for script,certificate in manifest['arithmetic_checks']:
        result=subprocess.run([sys.executable,'-B',str(PACKAGE/script)],cwd=ROOT,
            env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True)
        if result.returncode:
            raise RuntimeError(script+'\n'+result.stdout+result.stderr)
        if certificate:
            assert json.loads(result.stdout)==read(PACKAGE/certificate),script
        stages.append({'script':script,'status':'PASS'})
        print(script+': PASS',flush=True)
    for name,h in manifest['files'].items():
        assert sha(PACKAGE/name)==h,'Verification modified '+name
    records=read(ROOT/'data/results_20261120_v82.json')
    counts={r['id']:r['variables'] for r in records['current_constructions']}
    assert counts['general25']==25 and counts['quartic163']==163 and counts['quartic179']==179
    assert records['unchanged_variable_counts']['ordinary_abc_unrestricted_degree']==11
    assert records['unchanged_variable_counts']['ordinary_abc_quartic']==56
    report={'schema':'actual-square-research-verification/v83','status':'PASS',
        'stages':stages,'raw_scalar_square_identity_verified':True,
        'actual_trace_square_realization_proved':False,
        'new_defining_variable_count':False,
        'counterexamples_are_prepared_scalar_data':True,
        'current_results_record_unchanged':True,
        'scope':'Exact algebra, algebraic rank bounds, full Kummer classes, and source pins. '
                'The all-prime and approximation arguments are manually reviewed; '
                'no actual elliptic trace counterexample or global rational realization is inferred.'}
    output=json.dumps(report,indent=2)+'\n'
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(output)
    print(output)


if __name__=='__main__':
    main()
