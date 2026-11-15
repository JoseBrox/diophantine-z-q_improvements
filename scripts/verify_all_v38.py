#!/usr/bin/env python3
"""Run all eight verification suites and record precisely the runtime used.

Use Python 3.12 for the native release check. On Python 3.13 this script
uses a byte-identical executable copy of the repository's existing legacy
serialization wrapper only for the inherited suites. It never changes the
source checkout. Reports and complete logs go outside the repository.
"""
from pathlib import Path
import argparse,hashlib,json,platform,shutil,subprocess,sys,tempfile,time
ROOT=Path(__file__).resolve().parents[1]
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();out=args.output.resolve()
 if out==ROOT or ROOT in out.parents:raise SystemExit('Reports must be outside the source checkout.')
 out.mkdir(parents=True,exist_ok=True);record=dict(status='RUNNING',python=platform.python_version(),native_python312=sys.version_info[:2]==(3,12),compatibility_wrapper_used=sys.version_info[:2]==(3,13),suites=[],source_root=str(ROOT),remote_publication_confirmed=False,post_push_ci_confirmed=False,external_arithmetic_review=False)
 def save(): (out/'verification.json').write_text(json.dumps(record,indent=2)+'\n')
 with tempfile.TemporaryDirectory(prefix='zinq-compat-') as tmp:
  runtime=sys.executable
  if sys.version_info[:2]==(3,13):
   wrapper=Path(tmp)/'python313_legacy_compat.py';shutil.copyfile(ROOT/'scripts/python313_legacy_compat.py',wrapper);wrapper.chmod(0o755);runtime=str(wrapper);record['compatibility_wrapper_sha256']=hashlib.sha256(wrapper.read_bytes()).hexdigest()
  elif sys.version_info[:2]!=(3,12):raise SystemExit('Use Python 3.12 or the disclosed 3.13 compatibility path.')
  jobs=[('v38',[sys.executable,'-B','scripts/verify_v38.py','--report',str(out/'v38.json')]),('v34',[sys.executable,'-B','scripts/verify_v34.py','--report',str(out/'v34.json')]),('v33',[runtime,'-B','scripts/verify_v33.py','--report',str(out/'v33.json')]),('v30',[runtime,'-B','scripts/verify_v30.py','--report',str(out/'v30.json')]),('v29',[runtime,'-B','computation/pole_parameters/joint_realization_v29/check.py']),('v28',[runtime,'-B','scripts/verify_v28.py','--report',str(out/'v28.json')]),('v27',[runtime,'-B','scripts/verify_release_v27.py','--report',str(out/'v27.json')]),('legacy',[runtime,'-B','scripts/verify.py','--full','--receipt',str(out/'legacy.json')])]
  save()
  for name,cmd in jobs:
   print('Running '+name,flush=True);start=time.monotonic()
   with (out/(name+'.log')).open('w') as log:p=subprocess.run(cmd,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
   row=dict(name=name,returncode=p.returncode,seconds=round(time.monotonic()-start,3),status='PASS' if p.returncode==0 else 'FAIL',log_sha256=hashlib.sha256((out/(name+'.log')).read_bytes()).hexdigest());record['suites'].append(row);save()
   if p.returncode:record['status']='FAIL';save();raise SystemExit(name+' failed; see '+str(out/(name+'.log')))
  old=json.loads((out/'legacy.json').read_text());record.update(status='PASS',legacy_stages=len(old['stages']),suite_count=len(jobs),scope='Exact reproduction and finite checks. Serialization compatibility is disclosed; no native GitHub CI or remote publication is implied.');save();print('PASS: eight suites; '+str(len(old['stages']))+' legacy stages',flush=True)
if __name__=='__main__':main()
