#!/usr/bin/env python3
"""Reproduce the exact 11-variable, degree-234157441 source certificates."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[1]
PACKAGE='computation/few_variables/derivative11_v63'
JOBS=(('check_algebra.py','algebra_certificate.json'),
      ('check_completeness.py','completeness_certificate.json'),
      ('check_native.py','native_certificate.json'),
      ('check_specification.py','specification_certificate.json'))

def main(output):
    reports=[]; hashes={}
    with tempfile.TemporaryDirectory(prefix='derivative11-v63-') as tmp:
        for i,(script,cert) in enumerate(JOBS):
            target=Path(tmp)/('certificate%d.json'%i)
            command=[sys.executable,'-B',str(ROOT/PACKAGE/script),'--output',str(target)]
            run=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
            if run.returncode:raise RuntimeError(run.stdout+run.stderr)
            if target.read_bytes()!=(ROOT/PACKAGE/cert).read_bytes():
                raise AssertionError('Certificate differs: '+cert)
            reports.append(json.loads(target.read_text()))
            hashes[PACKAGE+'/'+script]=hashlib.sha256((ROOT/PACKAGE/script).read_bytes()).hexdigest()
            hashes[PACKAGE+'/'+cert]=hashlib.sha256(target.read_bytes()).hexdigest()
    algebra,complete,native,spec=reports
    assert all(r['status']=='PASS' for r in reports)
    assert algebra['sun_prime_positions']==18
    assert algebra['height_parameters']['strict_margin']=='44272779/198801800'
    assert complete['odd_valuation_fixtures']==7296
    assert native['characters']==384 and native['guard_count']==35
    assert native['finite_rank']==spec['finite_rank']==128
    assert native['source_sha256']==spec['source_sha256']
    assert spec['degree_bound']==234157441 and spec['support_strict_power_of_two']==264
    assert spec['variables']==11 and spec['terminal_root_zero_allowed']
    assert spec['all_preceding_radicands_units'] and spec['corruption_controls_rejected']==2
    for rel in ('build_source.py','specification/source.json','specification/polynomial.json',
                'specification/subalgebra_parent.json','specification/construction.json'):
        hashes[PACKAGE+'/'+rel]=hashlib.sha256((ROOT/PACKAGE/rel).read_bytes()).hexdigest()
    paper='papers/conditional_few_variables/derivative_detector11_20261117_v63.tex'
    hashes[paper]=hashlib.sha256((ROOT/paper).read_bytes()).hexdigest()
    report=dict(schema='derivative11-exact-verification/v63',status='PASS',
        python=platform.python_version(),source_sha256=hashes,
        construction=dict(variables=11,degree_upper_bound=234157441,
            monomials_strict_power_two=264,integer_content=1,finite_rank=128,
            sufficient_shift_effective=False,ordinary_abc_required=True),
        actual_character_evaluations=384,all_source_denominators_independently_checked=True,
        targets_21_and_9_proved=False,external_foundations_independently_audited=False)
    if output:
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--report',type=Path)
    main(ap.parse_args().report)
