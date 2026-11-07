#!/usr/bin/env python3
"""Verify the published files and reproduce the exact constructions in isolation."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time

from restore_data import restore

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(label, script, *args):
    start = time.monotonic()
    result = subprocess.run([sys.executable, str(script), *map(str,args)],
                            capture_output=True, text=True, cwd=script.parent)
    if result.returncode:
        sys.stderr.write((result.stdout+'\n'+result.stderr)[-12000:])
        raise SystemExit(label+' failed')
    print(label+': PASS', flush=True)
    return {'stage': label, 'status': 'PASS',
            'seconds': round(time.monotonic()-start,3)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full', action='store_true',
                        help='also replay the complete baseline arithmetic circuit (requires Node18+)')
    parser.add_argument('--receipt', type=Path,
                        help='optional path for a fresh verification receipt')
    args = parser.parse_args()
    assert sys.version_info >= (3,10), 'Python3.10 or newer is required'
    manifest = json.loads((ROOT/'MANIFEST.json').read_text())
    for entry in manifest['files']:
        p = ROOT/entry['path']
        assert p.is_file() and p.stat().st_size == entry['bytes'], entry['path']
        assert digest(p) == entry['sha256'], entry['path']
    print('Published manifest: PASS ('+str(len(manifest['files']))+' files)', flush=True)
    stages = []
    with tempfile.TemporaryDirectory(prefix='diophantine-verification-') as directory:
        work = Path(directory)
        shutil.copytree(ROOT/'computation', work/'computation',
                        ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        shutil.copytree(ROOT/'data', work/'data')
        restored = restore(work)
        quartic = work/'computation/quartic'
        if args.full:
            stages.append(run('Baseline source semantics', quartic/'baseline/verify.py'))
            assert digest(quartic/'baseline/data/system474/residuals.json') == digest(quartic/'source/parent474-residuals.json')
        rebuilt = quartic/'reconstructed-456'
        stages.append(run('Quartic producer', quartic/'build_quartic456.py', '--output', rebuilt))
        for filename in ('polynomial.json','residuals.json','transformation-certificate.json'):
            assert (rebuilt/filename).read_bytes() == (quartic/'polynomial-456'/filename).read_bytes(), filename
        stages.append(run('Independent complete quartic checker', quartic/'verify_quartic456.py', '--directory', rebuilt))
        few = work/'computation/few_variables'
        stages.append(run('29/31 source and specification reproduction', few/'construction29/reproduce_preferred.py'))
        stages.append(run('Elliptic chart arithmetic', few/'verify_elliptic_chart.py'))
        for filename, label in (
            ('check_scalar_normalization.py','Scalar normalization residue tables'),
            ('check_three_adic_anchor_depth.py','Local index depth and anchor constants'),
            ('check_odd_norm_cancellation.py','Odd norm identity'),
        ):
            stages.append(run(label,work/'computation/local'/filename))
        constants = work/'computation/constants'
        original_constant = (constants/'data/height19.bin').read_bytes()
        original_primes = (constants/'data/height19-primes.json').read_bytes()
        stages.append(run('Independent height-constant enumerations', constants/'check_height_constant.py'))
        assert original_constant == (constants/'data/height19.bin').read_bytes()
        assert original_primes == (constants/'data/height19-primes.json').read_bytes()
        fields = work/'computation/field_extensions'
        stages.append(run('Anisotropic form coefficients and residue fields', fields/'verify_anisotropic_examples.py'))
        stages.append(run('Quadratic-extension counterexample, two exact evaluations',
                          fields/'check_field_extension.py', rebuilt))
    report = {'status':'PASS', 'full_baseline_replay':args.full,
              'manifest_files_checked':len(manifest['files']),
              'compressed_tables_restored':restored,
              'stages':stages,
              'scope':'Exact source, algebraic, coefficient, finite-field, and numerical checks. The global arithmetic projection premises are stated separately in the papers.'}
    if args.receipt:
        args.receipt.parent.mkdir(parents=True,exist_ok=True)
        args.receipt.write_text(json.dumps(report,indent=2)+'\n')
    print('All requested checks passed; published inputs were unchanged.')


if __name__ == '__main__':
    main()
