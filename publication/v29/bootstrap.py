#!/usr/bin/env python3
"""Authenticate the v29 sources and bind native verification before publication."""
from __future__ import annotations
import argparse,base64,hashlib,json,lzma,os,platform,subprocess,sys
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parents[2]
SHA='33729eb9910610c70d8f1e5fc031842ff8f19b7384725a59842bbec996289405'
README_SHA='3beb0e59d6a1a1e4f0bbe396dd5c073870ca845206fe0195e0a41332f0a6a659'
CERT_SHA='ca1b34bd288099a6629dcfbcdd12daeaddaf2bfe8760fb0e1ee023c98940ec58'
CHECK='computation/pole_parameters/joint_realization_v29/check.py'
CERT='data/audits/joint_pole_realization_20261114_v29.json'
PUBLISHER='.github/workflows/publication-v29.yml'
EXPECTED={
 'papers/pole_parameters/joint_pole_realization_20261114_v29.tex',
 'papers/elliptic_charts/progression_density_20261114_v29.tex',
 CHECK,'computation/pole_parameters/joint_realization_v29/inputs.json',
 'computation/pole_parameters/joint_realization_v29/README.md',
 'docs/joint_pole_realization_20261114_v29.md',
 'publication/v29/final-verify.yml','publication/v29/readme-section.md'}
def require(ok,message):
 if not ok:raise SystemExit(message)
def digest(raw):return hashlib.sha256(raw).hexdigest()
def run(*args):subprocess.run([sys.executable,'-B',*args],cwd=ROOT,check=True)
def prepare():
 raw=base64.b64decode(''.join((ROOT/f'publication/v29/overlay-{i:02d}.b64').read_text().strip() for i in range(1,5)),validate=True)
 require(digest(raw)==SHA,'Source transport SHA-256 mismatch')
 files=json.loads(lzma.decompress(raw))
 require(set(files)==EXPECTED,'Unexpected source member list')
 for name,text in files.items():
  path=PurePosixPath(name)
  require(not path.is_absolute() and '..' not in path.parts and isinstance(text,str),'Unsafe source member')
  p=ROOT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
 p=ROOT/'README.md';text=p.read_text()
 heading='## Joint pole realization and reference-point restrictions in v29'
 if heading not in text:
  anchor='## General degree improvements in v28'
  require(text.count(anchor)==1,'README insertion anchor mismatch')
  text=text.replace(anchor,files['publication/v29/readme-section.md']+anchor,1)
 command='python -B '+CHECK
 if command not in text:
  anchor='python -m pip install sympy==1.14.0\n'
  require(text.count(anchor)==1,'README verification anchor mismatch')
  text=text.replace(anchor,anchor+command+'\n',1)
 require(digest(text.encode())==README_SHA,'Updated README SHA-256 mismatch')
 p.write_text(text)
 run(CHECK,'--output',CERT)
 require(digest((ROOT/CERT).read_bytes())==CERT_SHA,'Reconstructed certificate differs from the checked local certificate')
 run('scripts/update_manifest.py')
 print('Authenticated eight source files and independently rebuilt the exact v29 certificate.')
def verify_manifest(manifest,final=False):
 for row in manifest['files']:
  p=ROOT/row['path']
  if final and row['path']=='.github/workflows/verify.yml':p=ROOT/'publication/v29/final-verify.yml'
  raw=p.read_bytes()
  require(len(raw)==row['bytes'] and digest(raw)==row['sha256'],'Manifest mismatch: '+row['path'])
def finalize(args):
 require(sys.version_info[:2]==(3,12),'The integration receipt requires native Python 3.12')
 import sympy
 require(sympy.__version__=='1.14.0','Unexpected SymPy version')
 reports={key:json.loads(Path(path).read_text()) for key,path in [('v28',args.v28),('v27',args.v27),('legacy',args.legacy)]}
 for key,report in reports.items():require(report.get('status')=='PASS',key+' verification did not pass')
 require(len(reports['legacy']['stages'])==126,'Unexpected number of legacy stages')
 require(reports['v27']['top_level_commands']==10,'Unexpected cumulative command count')
 require(reports['v28']['reconstructed_specifications']==5,'Unexpected v28 specification count')
 run(CHECK)
 receipt={'schema':'joint-pole-native-integration/v29','status':'PASS','source_commit':os.environ['GITHUB_SHA'],'workflow_run':os.environ['GITHUB_RUN_ID'],'python':platform.python_version(),'sympy':sympy.__version__,'legacy_stages':126,'earlier_cumulative_commands':10,'v28_reconstructed_specifications':5,'symbolic_identities':14,'prepared_transfer_examples':9,'finite_algebra_examples':13,'elliptic_group_examples':81,'source_transport_sha256':SHA,'certificate_sha256':CERT_SHA,'report_sha256':{key:digest(Path(path).read_bytes()) for key,path in [('v28',args.v28),('v27',args.v27),('legacy',args.legacy)]},'global_variable_count_improvement':False,'independent_mathematical_review':False,'scope':'Native exact reconstruction and source-byte checks. Universal mathematical arguments are in the two TeX papers. External arithmetic inputs remain stated premises; no new global defining polynomial or smaller variable count is claimed.'}
 (ROOT/'data/audits/integration_20261114_v29.json').write_text(json.dumps(receipt,indent=2)+'\n')
 run('scripts/update_manifest.py')
 final=json.loads((ROOT/'MANIFEST.json').read_text())
 final['files']=[r for r in final['files'] if not r['path'].startswith('publication/v29/') and r['path']!=PUBLISHER]
 verify_bytes=(ROOT/'publication/v29/final-verify.yml').read_bytes()
 for row in final['files']:
  if row['path']=='.github/workflows/verify.yml':row.update(bytes=len(verify_bytes),sha256=digest(verify_bytes))
 require(len(final['files'])==774,'Unexpected clean publication file count')
 verify_manifest(final,final=True)
 (ROOT/'publication/v29/final-MANIFEST.json').write_text(json.dumps(final,indent=2)+'\n')
 run('scripts/update_manifest.py');verify_manifest(json.loads((ROOT/'MANIFEST.json').read_text()))
 print('Native receipt bound; all staged and all 774 clean publication files authenticated.')
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('mode',choices=['prepare','finalize']);ap.add_argument('--v28');ap.add_argument('--v27');ap.add_argument('--legacy');args=ap.parse_args()
 if args.mode=='prepare':prepare()
 else:
  require(all([args.v28,args.v27,args.legacy]),'All native reports are required');finalize(args)
if __name__=='__main__':main()
