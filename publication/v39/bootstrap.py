#!/usr/bin/env python3
"""Restore the hash-bound v38 source update and bind native verification."""
from pathlib import Path,PurePosixPath
import argparse,base64,hashlib,json,lzma,os,platform,subprocess,sys,urllib.request
ROOT=Path(__file__).resolve().parents[2]
PAYLOAD_SHA='360e17fb26bcf6cf2cfdc0a43bd9e964d103661e2bc9d6ffaa18c98f864acd0a'
PARTS=12

def need(ok,msg):
 if not ok: raise RuntimeError(msg)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def run(*args,cwd=ROOT):subprocess.run([sys.executable,'-B',*args],cwd=cwd,check=True)
def load():
 raw=base64.b64decode(''.join((ROOT/f'publication/v39/part-{i:02d}.b64').read_text().strip() for i in range(1,PARTS+1)),validate=True)
 need(sha(raw)==PAYLOAD_SHA,'Source transport SHA-256 mismatch')
 return json.loads(lzma.decompress(raw))
def verify(records):
 for n,v in records.items():
  b=(ROOT/n).read_bytes();need(len(b)==v['bytes'] and sha(b)==v['sha256'],'Reconstruction mismatch: '+n)
def manifest():
 run('scripts/update_manifest.py')
 f=ROOT/'MANIFEST.json';d=json.loads(f.read_text())
 # This historical source log is an input, not a disposable build log.
 n='sources/h10_quartic198/circuits/elimination-search.log'
 b=(ROOT/n).read_bytes()
 d['files']=[r for r in d['files'] if r['path']!=n]
 d['files'].append(dict(path=n,bytes=len(b),sha256=sha(b)))
 d['files'].sort(key=lambda r:r['path'])
 f.write_text(json.dumps(d,indent=2)+'\n')
def prepare():
 p=load()
 # Copy frozen parent inputs before changing any publication documentation.
 for dest,src in p['copy'].items():
  f=ROOT/dest;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes((ROOT/src).read_bytes())
 for group in ['fetch','historical']:
  for dest,spec in p[group].items():
   if os.environ.get('LOCAL_SOURCE_MIRROR'):
    raw=(Path(os.environ['LOCAL_SOURCE_MIRROR'])/dest).read_bytes()
   elif group=='historical':
    subprocess.run(['git','fetch','origin',spec['ref']],cwd=ROOT,check=True)
    raw=subprocess.check_output(['git','show',spec['ref']+':'+spec['path']],cwd=ROOT)
   else:
    with urllib.request.urlopen(spec['url'],timeout=60) as response:raw=response.read()
   need(sha(raw)==spec['sha256'],'Pinned source mismatch: '+dest)
   f=ROOT/dest;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(raw)
 for n,t in p['text'].items():
  q=PurePosixPath(n);need(not q.is_absolute() and '..' not in q.parts and q.parts[0] not in ('.git','.github'),'Unsafe source member')
  f=ROOT/n;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(t,encoding='utf-8')
 d=json.loads((ROOT/'data/results.json').read_text());d.update(p['results_update']);(ROOT/'data/results.json').write_text(json.dumps(d,indent=2)+'\n')
 arch=ROOT/'sources/h10_quartic198'
 run('verify.py',cwd=arch)
 run('circuits/balance_affine200.py',cwd=arch)
 run('circuits/check_balanced200.py',cwd=arch)
 run('computation/quartic/abc78_v34/build.py')
 run('computation/quartic/laurent_recovery_v38/build.py')
 run('computation/quartic/laurent_recovery_v38/build_explicit.py')
 verify(p['regenerate']);verify(p['archive'])
 manifest()
 print('Authenticated every restored source and all reconstructed polynomial tables.')
def finalize(args):
 need(sys.version_info[:2]==(3,12),'Native Python 3.12 required')
 report=json.loads(Path(args.report).read_text());need(report.get('status')=='PASS' and report.get('suite_count')==8 and report.get('legacy_stages')==126 and report.get('native_python312') is True,'Incomplete native verification')
 p=load();verify(p['archive']);verify(p['regenerate'])
 receipt={'schema':'recovered-v38-native-publication/v39','status':'PASS','source_commit':os.environ['GITHUB_SHA'],'workflow_run':os.environ['GITHUB_RUN_ID'],'python':platform.python_version(),'source_transport_sha256':PAYLOAD_SHA,'verification':report,'archived_editable_files':89,'archive_origin_record_additional':True,'original_pdf_redistributed':False,'independent_mathematical_review':False,'scope':'Native verification of the complete v38 source update; no new 233-variable claim. Arithmetic inputs remain explicit.'}
 (ROOT/'data/audits/integration_20261115_v39.json').write_text(json.dumps(receipt,indent=2)+'\n')
 manifest()
 final=json.loads((ROOT/'MANIFEST.json').read_text());final['files']=[r for r in final['files'] if not r['path'].startswith('publication/v39/') and r['path']!='.github/workflows/publication-v39.yml']
 w=(ROOT/'publication/v39/final-verify.yml').read_bytes()
 for r in final['files']:
  if r['path']=='.github/workflows/verify.yml':r.update(bytes=len(w),sha256=sha(w))
 (ROOT/'publication/v39/final-MANIFEST.json').write_text(json.dumps(final,indent=2)+'\n')
 manifest()
 for r in json.loads((ROOT/'MANIFEST.json').read_text())['files']:
  b=(ROOT/r['path']).read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'Publication manifest: '+r['path'])
 print('Native eight-suite verification bound; clean final manifest prepared.')
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('mode',choices=['prepare','finalize']);ap.add_argument('--report');a=ap.parse_args()
 if a.mode=='prepare':prepare()
 else:finalize(a)
