#!/usr/bin/env python3
"""Authenticate and install the source-only v27 publication overlay."""
import base64,hashlib,io,json,lzma,tarfile,urllib.request
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parents[2]
parts=[ROOT/f'publication/v27/overlay-{i:02d}.b64' for i in range(1,11)]
raw=base64.b64decode(''.join(p.read_text().strip() for p in parts),validate=True)
expected='1ce0ddb35995af15662e62c625dff19a9e2768a51dca02358215cfd16e44ad22'
if hashlib.sha256(raw).hexdigest()!=expected:raise SystemExit('Overlay SHA-256 mismatch')
with tarfile.open(fileobj=io.BytesIO(lzma.decompress(raw)),mode='r:') as tf:
    entries=tf.getmembers()
    if len(entries)!=69:raise SystemExit('Unexpected source file count')
    for item in entries:
        p=PurePosixPath(item.name)
        if not item.isfile() or p.is_absolute() or '..' in p.parts or p.parts[0]=='.git':
            raise SystemExit('Unsafe source member: '+item.name)
        target=ROOT/item.name
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(tf.extractfile(item).read())
url='https://raw.githubusercontent.com/elliotglazer/diophantine-z-q/1f7e1f1fb0438feda3c9f3da9cc16982126aeeed/research/quartic214/construction/artifacts/candidate214-brox/candidate214-polynomial.json'
with urllib.request.urlopen(url,timeout=60) as response: source=response.read()
if hashlib.sha256(source).hexdigest()!='9f461531df52ac73e02cf7a4ce270422715642c0d3112952cad4968d9a7e24ea':
    raise SystemExit('Pinned predecessor polynomial SHA-256 mismatch')
(ROOT/'computation/quartic/balanced214_v24/source/polynomial214.json').write_bytes(source)
p=ROOT/'data/results.json';data=json.loads(p.read_text())
data.update(current_results_reference='data/results_20261114_v27.json',current_results_guide='docs/results_20261114_v27.md',retained_source_records_notice='The pre-v27 entries in this file are retained pinned source constructions, not the current best table. Current bounds and successors are in current_results_reference.')
p.write_text(json.dumps(data,indent=2)+'\n')
for rel in ['docs/reproducibility.md','docs/arithmetic_inputs.md','docs/research_directions.md','computation/quartic/README.md','computation/few_variables/README.md']:
    p=ROOT/rel;text=p.read_text();link='../../README.md' if rel.startswith('computation/') else '../README.md'
    banner=f'> **Retained source guide.** This page describes the dated constructions on the previous main branch. For the current counts, corrected proofs, exact specifications, and verification commands, see the repository [README]({link}) and `data/results_20261114_v27.json`. Historical source equations and assumptions below are retained, not replaced silently.\n\n'
    if not text.startswith('> **Retained source guide.**'):p.write_text(banner+text)
print('Authenticated 69-file source overlay and exact upstream polynomial; metadata updated.')
