#!/usr/bin/env python3
"""Reproduce the cumulative v23--v27 checks, separately from the legacy suite."""
from pathlib import Path
import argparse,hashlib,json,os,platform,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def main():
 if not __debug__:raise SystemExit('Run without -O.')
 ap=argparse.ArgumentParser();ap.add_argument('--authenticate-sources',action='store_true');ap.add_argument('--report',type=Path,default=ROOT/'data/audits/verification_20261114_v27.json');a=ap.parse_args()
 commands=[['scripts/verify_v25.py']+(['--authenticate-sources'] if a.authenticate_sources else []),
 ['computation/quartic/abc79_v27/build.py'],['computation/quartic/abc79_v27/check_reference.py'],['computation/quartic/abc79_v27/check.py'],
 ['computation/quartic/pole81_v27/build.py'],['computation/quartic/compressed_reference_v27/build.py'],['computation/quartic/compressed_reference_v27/check.py'],
 ['computation/quartic/reciprocal204_v27/build.py'],['computation/quartic/reciprocal204_v27/check.py'],['computation/quartic/reciprocal204_v27/check_arithmetic.py']]
 records=[];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONOPTIMIZE='0')
 for cmd in commands:
  print('Checking:',' '.join(cmd),flush=True);r=subprocess.run([sys.executable,'-B',*cmd],cwd=ROOT,text=True,capture_output=True,env=env)
  if r.returncode:print(r.stdout);print(r.stderr,file=sys.stderr);raise SystemExit('FAILED: '+' '.join(cmd))
  records.append(dict(command=cmd,status='PASS',stdout_sha256=hashlib.sha256(r.stdout.encode()).hexdigest()))
 report=dict(schema='cumulative-exact-verification/v27',date='2026-11-14',status='PASS',python_version=platform.python_version(),top_level_commands=len(commands),commands=records,
 current_total_variables={'general':25,'explicit_general':27,'abc_general':13,'quartic':204,'explicit_quartic':260,'abc_quartic':79},
 current_quartic_rows={'204':186,'260':232,'79':71,'lower_coefficient_abc81':73},
 current_quartic_monomials={'204':3046,'260':3704,'79':1139,'lower_coefficient_abc81':929},
 prior_elliptic_pair_examples=702,finite_algebra_examples=13,native_general_sources_authenticated=a.authenticate_sources,
 legacy_full_verifier_run_by_this_script=False,independent_non_author_review=False,
 scope='Exact row and coefficient reconstructions, exceptional reference-chart certificates, finite-algebra bounds, rational identities, finite examples and negative controls. Infinite arithmetic premises and complete non-author acceptance are not certified by these checks.')
 a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
