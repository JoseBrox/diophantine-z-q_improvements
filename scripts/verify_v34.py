#!/usr/bin/env python3
"""Verify the complete 78-variable abc quartic without changing source data."""
from pathlib import Path
import argparse,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path);a=ap.parse_args()
 subprocess.run([sys.executable,'-B',str(ROOT/'computation/quartic/abc78_v34/check.py')],cwd=ROOT,check=True)
 report=json.loads((ROOT/'computation/quartic/abc78_v34/independent-verification.json').read_text())
 if report.get('status')!='PASS':raise SystemExit('No passing independent receipt')
 if a.report:a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,indent=2)+'\n')
 print('PASS: 78 coordinates, 70 quadrics, complete coefficient reconstruction and mixed-height checks.')
