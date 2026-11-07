#!/usr/bin/env python3
"""Record byte lengths and SHA-256 hashes of the distributed publication files."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_SUFFIXES = {'.pyc','.aux','.log','.out','.toc','.fls','.fdb_latexmk'}


def main():
    restored = {x['path'] for x in json.loads((ROOT/'data/compressed_sources.json').read_text())}
    entries = []
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT)
        if any(x in ('.git','__pycache__','.verification','.tex-build') for x in rel.parts):
            continue
        if str(rel) == 'MANIFEST.json' or str(rel) in restored or p.suffix in EXCLUDED_SUFFIXES:
            continue
        if p.name == 'build-output.txt':
            continue
        raw = p.read_bytes()
        entries.append({'path':str(rel),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    report = {'schema':'diophantine-publication-manifest/v1',
              'date':'2026-11-07','files':entries,
              'scope':'Distributed proofs, polynomial specifications, exact computational dependencies, and reproduction tools. The manifest itself and generated files are excluded.'}
    (ROOT/'MANIFEST.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Recorded',len(entries),'publication files.')


if __name__ == '__main__':
    main()
