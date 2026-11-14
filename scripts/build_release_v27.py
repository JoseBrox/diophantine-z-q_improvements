#!/usr/bin/env python3
"""Build the current proof PDFs and bind their exact source and output bytes.

This performs document builds, not mathematical review or publication. Run the
cumulative and legacy verification programs separately as documented.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    'papers/elliptic_heights/product_height_20261113_v23.tex',
    'papers/local_tests/height_precision_20261113_v23.tex',
    'papers/finite_algebra/triangular_separation_20261113_v24.tex',
    'papers/quartic/coefficient_balancing_20261113_v24.tex',
    'papers/trace_heights/trace_on_all_points_20261113_v25.tex',
    'papers/quartic_existence/quartic212_20261113_v25.tex',
    'papers/quartic_existence/quartic_abc81_20261113_v25.tex',
    'papers/trace_heights/weighted_trace_20261114_v27.tex',
    'papers/quartic_existence/quartic204_20261114_v27.tex',
    'papers/elliptic_charts/compressed_reference_20261114_v27.tex',
    'papers/pole_parameters/congruent_twist_poles_20261114_v27.tex',
    'papers/quartic_existence/quartic_abc79_20261114_v27.tex',
    'papers/quartic/explicit260_20261114_v27.tex',
]

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-pdfs', action='store_true',
                        help='Run pdflatex twice; otherwise authenticate existing PDFs.')
    args = parser.parse_args()
    if args.build_pdfs and not shutil.which('pdflatex'):
        raise SystemExit('pdflatex is required; install the documented TeX packages.')
    env = dict(os.environ, SOURCE_DATE_EPOCH='1794614400', FORCE_SOURCE_DATE='1')
    records = []
    for rel in SOURCES:
        source = ROOT / rel
        target = source.with_suffix('.pdf')
        if args.build_pdfs:
            with tempfile.TemporaryDirectory(prefix='zinq-v27-tex-') as folder:
                for _ in range(2):
                    run = subprocess.run(
                        ['pdflatex', '-interaction=nonstopmode', '-halt-on-error',
                         '-file-line-error', '-output-directory', folder, str(source)],
                        cwd=source.parent, env=env, text=True, capture_output=True)
                    if run.returncode:
                        raise SystemExit(f'{rel}: TeX build failed\n{run.stdout}\n{run.stderr}')
                log = (Path(folder) / (source.stem + '.log')).read_text(errors='replace')
                if 'There were undefined references' in log or 'undefined citations' in log:
                    raise SystemExit(f'{rel}: unresolved references or citations')
                shutil.copyfile(Path(folder) / target.name, target)
        if not target.is_file() or not target.read_bytes().startswith(b'%PDF-'):
            raise SystemExit(f'Missing or invalid PDF: {target}')
        row = {'source': rel, 'source_sha256': digest(source),
               'pdf': target.relative_to(ROOT).as_posix(), 'pdf_sha256': digest(target),
               'pdf_bytes': target.stat().st_size}
        records.append(row)
        print('Built' if args.build_pdfs else 'Authenticated', rel, flush=True)
    output = ROOT / 'data/audits/pdf_builds_20261114_v27.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({
        'schema': 'source-pdf-bindings/v27', 'date': '2026-11-14',
        'build_command': 'python -B scripts/build_release_v27.py --build-pdfs',
        'source_date_epoch': 1794614400, 'papers': records,
        'scope': 'Exact source and PDF bindings after two serial pdflatex runs. '
                 'Document compilation is not mathematical proof verification. '
                 'Historical dated receipts retain their original scope.'
    }, indent=2) + '\n')

if __name__ == '__main__':
    main()
