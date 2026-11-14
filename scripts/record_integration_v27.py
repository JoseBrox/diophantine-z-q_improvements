#!/usr/bin/env python3
"""Record successful release executions without manufacturing mathematical approval."""
from __future__ import annotations
import argparse,hashlib,json,platform,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--legacy-receipt',required=True,type=Path)
 ap.add_argument('--new-receipt',required=True,type=Path)
 ap.add_argument('--execution-label',required=True)
 ap.add_argument('--source-commit',required=True)
 a=ap.parse_args()
 old=json.loads(a.legacy_receipt.read_text());new=json.loads(a.new_receipt.read_text())
 if old.get('status')!='PASS' or len(old.get('stages',[]))!=126 or any(s['status']!='PASS' for s in old['stages']):
  raise SystemExit('The complete 126-stage legacy receipt is required.')
 if new.get('status')!='PASS' or new.get('top_level_commands')!=10 or not new.get('native_general_sources_authenticated'):
  raise SystemExit('The authenticated cumulative v27 receipt is required.')
 builds=json.loads((ROOT/'data/audits/pdf_builds_20261114_v27.json').read_text())
 for b in builds['papers']:
  if sha(ROOT/b['source'])!=b['source_sha256'] or sha(ROOT/b['pdf'])!=b['pdf_sha256']:
   raise SystemExit('Changed proof source or PDF: '+b['source'])
 oldout=ROOT/'data/audits/legacy_verification_20261114_v27.json'
 newout=ROOT/'data/audits/verification_20261114_v27.json'
 shutil.copyfile(a.legacy_receipt,oldout)
 if a.new_receipt.resolve()!=newout.resolve():shutil.copyfile(a.new_receipt,newout)
 paths=['README.md','data/results_20261114_v27.json','data/audits/source_applications_20261114_v27.json',
 'data/audits/pdf_builds_20261114_v27.json','data/audits/reference_chart_correction_20261114_v27.json']
 # The correction is prose, not a fabricated machine approval.
 paths[-1]='docs/audits/reference_chart_correction_20261114_v27.md'
 for folder in ['reciprocal204_v27','compressed_reference_v27','abc79_v27','pole81_v27']:
  paths.extend(p.relative_to(ROOT).as_posix() for p in (ROOT/'computation/quartic'/folder).rglob('*') if p.is_file() and p.suffix in ('.py','.json','.md'))
 report=dict(schema='publication-integration/v27',date='2026-11-14',
  execution_label=a.execution_label,checked_source_commit=a.source_commit,
  python_version=platform.python_version(),native_python312=(sys.version_info[:2]==(3,12)),
  legacy_verification=dict(stages=126,status='PASS',receipt=oldout.relative_to(ROOT).as_posix(),sha256=sha(oldout),pari_rank_checks_run=old.get('pari_rank_checks_run',False)),
  cumulative_verification=dict(top_level_commands=10,status='PASS',receipt=newout.relative_to(ROOT).as_posix(),sha256=sha(newout)),
  pdfs_built=len(builds['papers']),source_and_pdf_bindings='data/audits/pdf_builds_20261114_v27.json',
  new_results=dict(inherited_quartic_variables=204,explicit_quartic_variables=260,abc_quartic_variables=79,general_variables=25,abc_general_variables=13),
  corrected_prior_error='The omitted f*S coefficient in the printed v26 reference chart is restored and all affected current uses are rebuilt.',
  files=[dict(path=p,sha256=sha(ROOT/p)) for p in sorted(set(paths))],
  independent_non_author_review=False,complete_external_arithmetic_audit=False,
  scope='These are execution and byte-binding records, not formal proof or independent mathematical acceptance. The original arithmetic premises remain explicit; the new authored proofs cover their changed applications. Exact public publication is established by the Git ref and independent readback, not by this status record.')
 (ROOT/'data/audits/integration_20261114_v27.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ['native_python312','pdfs_built','new_results']},indent=2))
if __name__=='__main__':main()
