#!/usr/bin/env python3
"""Verify every retained package file against the manifest (standard library)."""
from pathlib import Path
from hashlib import sha256
import json

HERE = Path(__file__).resolve().parent
manifest = json.loads((HERE / "MANIFEST.json").read_text())
for name, expected in manifest["files"].items():
    raw = (HERE / name).read_bytes()
    if len(raw) != expected["bytes"] or sha256(raw).hexdigest() != expected["sha256"]:
        raise SystemExit("Manifest mismatch: " + name)
print(json.dumps({"status": "PASS", "files_verified": len(manifest["files"])}))
