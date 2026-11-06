#!/usr/bin/env python3
"""Check original archived files against immutable archive SHA-256 manifest.

Only standard library required. Does not purport to verify arithmetic theorems.
"""
import hashlib
import gzip
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def main():
    m=json.loads((ROOT/'MANIFEST.json').read_text('utf-8'))
    errors=[]
    checked_gzip=0
    for e in m['files']:
        path=ROOT/e['path']
        if path.is_file():
            if path.stat().st_size!=e['bytes']:errors.append(f'wrong size: {e["path"]}')
            if sha(path)!=e['sha256']:errors.append(f'wrong SHA256: {e["path"]}')
            continue
        # One oversized historical JSON is distributed losslessly in gzip form;
        # verify decompressed bytes against the original immutable manifest.
        if e['path']=='research/optimization/polynomial-855/polynomial-circuit.json':
            archive=ROOT/(e['path']+'.gz')
            if archive.is_file():
                try:
                    data=gzip.decompress(archive.read_bytes())
                    checked_gzip+=1
                    if len(data)!=e['bytes'] or hashlib.sha256(data).hexdigest()!=e['sha256']:
                        errors.append(f'incorrect compressed payload: {e["path"]}')
                    continue
                except (OSError,EOFError) as exc:
                    errors.append(f'invalid gzip for {e["path"]}: {exc}')
                    continue
        errors.append(f'missing: {e["path"]}')
    paper=ROOT/'paper/diophantine_optimization_20261106_v3.tex'
    original=ROOT/'research/phase3/diophantine_optimization_20261106_v3.tex'
    # The publication manuscript is editorially revised. Only the frozen
    # original is covered by MANIFEST.json; equality is not expected.
    if not paper.is_file(): errors.append('missing publication manuscript')
    if not original.is_file(): errors.append('missing frozen source manuscript')
    specs=[('indexed-41','research/phase3/finite_fibre/polynomial-41/construction-report.json',41),('indexed-43-semilocal','research/phase3/finite_fibre/polynomial-43-semilocal/construction-report.json',43),('source-preserving-558','research/phase2/finite_fibre/polynomial-558/construction-report.json',558),('quartic-1315-translated','research/phase3/quartic/quartic-direct-translated/construction-report.json',1315),('quartic-1335-integer','research/phase3/quartic/quartic-direct-small-coefficients-1335/construction-report.json',1335),('original-12504','quartics/quartic-12504/verification.json',12504)]
    rows=json.loads((ROOT/'data/polynomial_benchmarks.json').read_text())['rows']
    if len(rows)!=len(specs):errors.append('benchmark table row count mismatch')
    else:
        for row,(tag,report,vars_expected) in zip(rows,specs):
            d=json.loads((ROOT/report).read_text())
            n=d.get('total_variables',d.get('variables'))
            if row['id']!=tag or row['variables']!=n or n!=vars_expected:errors.append(f'benchmark mismatch: {tag}')
            target=ROOT/row['artifact']
            if not target.is_file() or target.stat().st_size!=row['file_bytes']:errors.append(f'benchmark file mismatch: {tag}')
            if isinstance(row['monomials'],int) and row['monomials']!=d.get('distinct_variable_monomials',d.get('monomials')):errors.append(f'monomial mismatch: {tag}')
    result={'checked_historic_manifest_files':len(m['files']),'checked_via_gzip':checked_gzip,'benchmark_rows':len(rows),'publication_paper_sha256':sha(paper) if paper.is_file() else None,'original_paper_sha256':sha(original) if original.is_file() else None,'status':'PASS' if not errors else 'FAIL','errors':errors}
    print(json.dumps(result,indent=2))
    return 0 if not errors else 1
if __name__=='__main__':sys.exit(main())
