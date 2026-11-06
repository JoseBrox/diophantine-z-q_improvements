#!/usr/bin/env python3
"""Restore the one historical JSON file stored losslessly as gzip on GitHub.

Checks its exact byte size and SHA-256 against the frozen archive manifest.
No external modules or network access required.
"""
import gzip
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
SOURCE='research/optimization/polynomial-855/polynomial-circuit.json'

def main():
    manifest=json.loads((ROOT/'MANIFEST.json').read_text(encoding='utf-8'))
    try: record=next(x for x in manifest['files'] if x['path']==SOURCE)
    except StopIteration: raise SystemExit('Source is not covered by the frozen archive manifest')
    target=ROOT/SOURCE
    compressed=ROOT/(SOURCE+'.gz')
    if target.is_file():
        content=target.read_bytes()
    elif compressed.is_file():
        content=gzip.decompress(compressed.read_bytes())
    else:
        raise SystemExit(f'Missing {SOURCE} and its .gz alternative')
    actual=hashlib.sha256(content).hexdigest()
    if actual!=record['sha256'] or len(content)!=record['bytes']:
        raise SystemExit(f'Integrity failure for {SOURCE}: {actual}')
    if not target.is_file():
        target.write_bytes(content)
        print(f'Restored {SOURCE}: {len(content):,} bytes (SHA-256 verified)')
    else:
        print(f'Already present and verified: {SOURCE}')
    return 0

if __name__=='__main__':sys.exit(main())
