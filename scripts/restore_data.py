#!/usr/bin/env python3
"""Restore losslessly compressed coefficient tables, checking their exact bytes."""
from pathlib import Path
import argparse
import gzip
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def restore(root=ROOT):
    entries = json.loads((root/'data/compressed_sources.json').read_text())
    for entry in entries:
        raw = gzip.decompress((root/entry['compressed_path']).read_bytes())
        assert len(raw) == entry['bytes'], entry['path']
        assert hashlib.sha256(raw).hexdigest() == entry['sha256'], entry['path']
        destination = root/entry['path']
        if destination.exists():
            assert destination.read_bytes() == raw, 'Conflicting file: '+entry['path']
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(raw)
    return len(entries)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    print('Restored and checked', restore(args.root), 'exact tables.')
