#!/usr/bin/env python3
"""Read-only reproduction of the 196/258 reductions and supplied 198 archive."""
from pathlib import Path
import argparse,hashlib,json,os,platform,shutil,subprocess,sys,tempfile,time
ROOT=Path(__file__).resolve().parents[1]
def require(ok,message):
 if not ok:raise ValueError(message)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--report',type=Path);a=ap.parse_args();reports=[]
 import sympy
 require(sympy.__version__=='1.14.0','Use SymPy 1.14.0')
 with tempfile.TemporaryDirectory(prefix='diophantine-v38-') as name:
  tmp=Path(name)
  for filename,label in [('check.py','laurent196'),('check_explicit.py','explicit258')]:
   dst=tmp/(label+'.json');start=time.monotonic();script=ROOT/'computation/quartic/laurent_recovery_v38'/filename
   p=subprocess.run([sys.executable,'-B',str(script),'--output',str(dst)],cwd=ROOT,capture_output=True,text=True)
   require(p.returncode==0,label+' failed:\n'+p.stdout[-5000:]+p.stderr[-5000:]);r=json.loads(dst.read_text());require(r.get('status')=='PASS',label)
   saved=ROOT/'data/audits'/('laurent196_20261115_v38.json' if label=='laurent196' else 'explicit258_20261115_v38.json')
   require(dst.read_bytes()==saved.read_bytes(),'Stored receipt differs: '+label)
   reports.append(dict(name=label,status='PASS',seconds=round(time.monotonic()-start,3),receipt_sha256=digest(dst)));print(label+': PASS',flush=True)
  shutil.copytree(ROOT/'sources/h10_quartic198',tmp/'archive',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
  start=time.monotonic();p=subprocess.run([sys.executable,'-B','verify.py'],cwd=tmp/'archive',capture_output=True,text=True)
  require(p.returncode==0,'Original 198 archive checks failed:\n'+p.stdout[-8000:]+p.stderr[-8000:]);require(sum(line.startswith('PASS ') for line in p.stdout.splitlines())==13 and 'All algebraic checks passed.' in p.stdout,'Check original verifier completion: '+p.stdout[-3000:])
  reports.append(dict(name='supplied-198-archive',status='PASS',commands=13,seconds=round(time.monotonic()-start,3),stdout_sha256=hashlib.sha256(p.stdout.encode()).hexdigest()));print('Supplied 198 archive: PASS (13 commands)',flush=True)
 report=dict(schema='quartic-recovery-integration/v38',status='PASS',python=platform.python_version(),sympy=sympy.__version__,checks=reports,number_of_new_corruption_tests=13,current_quartic_counts=dict(inherited=196,fully_specified=258),abc78_verified_by_this_script=False,general_counts=[25,13],recovery_233='not supported by the supplied archives; no claim',native_python312=sys.version_info[:2]==(3,12),external_arithmetic_review=False,independent_mathematical_review=False,scope='Read-only exact algebra and supplied archive reconstruction; parent arithmetic premises remain explicit.')
 if a.report:a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
