#!/usr/bin/env python3
"""Reproduce all distributed polynomial data and exact certificates offline."""
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

ROOT=Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(label, script, *args):
    start=time.monotonic()
    result=subprocess.run([sys.executable,str(script),*map(str,args)],
        cwd=script.parent,capture_output=True,text=True)
    if result.returncode:
        sys.stderr.write((result.stdout+'\n'+result.stderr)[-12000:])
        raise SystemExit(label+' failed')
    print(label+': PASS',flush=True)
    return {'stage':label,'status':'PASS','seconds':round(time.monotonic()-start,3)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full',action='store_true',help='run all supplied checks (also the default)')
    parser.add_argument('--receipt',type=Path)
    args=parser.parse_args()
    assert sys.version_info>=(3,10)
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    for entry in manifest['files']:
        path=ROOT/entry['path']
        assert path.is_file() and path.stat().st_size==entry['bytes'],entry['path']
        assert digest(path)==entry['sha256'],entry['path']
    print('Publication manifest: PASS ('+str(len(manifest['files']))+' files)',flush=True)
    quartic_root=ROOT/'computation/quartic'
    provenance=json.loads((quartic_root/'PROVENANCE.json').read_text())
    for name, entry in provenance['files'].items():
        path=quartic_root/name
        assert path.stat().st_size==entry['bytes'] and digest(path)==entry['sha256'],name
    for proof in provenance['proofs'].values():
        for extension in ('tex','pdf'):
            assert digest(quartic_root/proof[extension])==proof[extension+'_sha256'],proof[extension]
    documentation=provenance['documentation']
    assert digest(quartic_root/documentation['dataFormat'])==documentation['dataFormatSHA256']
    print('Quartic source and proof provenance: PASS',flush=True)
    stages=[]
    with tempfile.TemporaryDirectory(prefix='diophantine-verification-') as directory:
        work=Path(directory)
        shutil.copytree(ROOT/'computation',work/'computation',
            ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        shutil.copytree(ROOT/'data',work/'data')
        restored=restore(work)
        quartic=work/'computation/quartic'
        originals={name:(quartic/'final392'/name).read_bytes() for name in
            ('quadratic-system392.json','polynomial392.json','construction-report392.json')}
        stages.append(run('392-variable quartic reconstruction',quartic/'build_quartic392.py'))
        for name,raw in originals.items():
            assert (quartic/'final392'/name).read_bytes()==raw,name
        stages.append(run('Independent full 394/392 coefficient and source checks',quartic/'verify_quartic392.py'))
        stages.append(run('Quadratic-extension specialization, two exact evaluations',quartic/'check_field_specialization392.py'))
        for count, folder, prefix in [(389,'final389',''),(329,'family329','family'),(317,'family317','family')]:
            names = ([f'quadratic-system{count}.json',f'polynomial{count}.json',f'construction-report{count}.json']
                     if not prefix else
                     [f'quadratic-family{count}.json',f'polynomial-family{count}.json',f'construction-report{count}.json'])
            fixed_tables = {name:(quartic/folder/name).read_bytes() for name in names}
            stages.append(run(f'{count}-coordinate exact quadratic construction',quartic/f'build_quartic{count}.py'))
            for name, raw in fixed_tables.items():
                assert (quartic/folder/name).read_bytes()==raw,name
            stages.append(run(f'{count}-coordinate independent full coefficient checks',quartic/f'check_quartic{count}.py'))
            if count==389:
                stages.append(run('All three detector affine normalizations',quartic/'verify_detector_normalizations.py'))
        few=work/'computation/few_variables'
        module=few/'forced_prime29'
        module_manifest=json.loads((module/'manifest.json').read_text())
        for entry in module_manifest['files']:
            assert digest(module/entry['path'])==entry['sha256'],entry['path']
        old_source=(module/'source.json.gz').read_bytes()
        old_spec=(module/'polynomial-specification.json').read_bytes()
        stages.append(run('29-variable source, finite algebra, and weighted coefficient bounds',module/'reproduce.py'))
        assert (module/'source.json.gz').read_bytes()==old_source
        assert (module/'polynomial-specification.json').read_bytes()==old_spec
        stages.append(run('27-variable cubic-chart family and uniform degree bound',
            few/'trace27_cubic_family/reproduce.py','--anchor-exponent','137731'))
        stages.append(run('Quadratic extension square chart: exact cubic identities',
            work/'computation/quadratic_squares/check_quadratic_square_chart.py'))
        stages.append(run('Scalar normalization: Bezout certificate and exhaustive residue check',
            work/'computation/scalar_normalization/check_scalar_normalization.py'))
        stages.append(run('Independent fixed-prime numerical certificates',
            work/'computation/arithmetic/check_forced_prime_20261108_v8.py'))
        stages.append(run('Elliptic chart arithmetic',few/'verify_elliptic_chart.py'))
        stages.append(run('Quadratic elliptic-height identities and constants',few/'verify_quadratic_height.py'))
        constants=work/'computation/constants'
        fixed={name:(constants/'data'/name).read_bytes() for name in ('height19.bin','height19-primes.json')}
        stages.append(run('Two independent prime enumerations and exact height constant',constants/'check_height_constant.py'))
        for name,raw in fixed.items():
            assert (constants/'data'/name).read_bytes()==raw
        stages.append(run('Anisotropic forms and residue fields',
            work/'computation/field_extensions/verify_anisotropic_examples.py'))
    report={'status':'PASS','manifest_files_checked':len(manifest['files']),
        'compressed_tables_restored':restored,'stages':stages,
        'scope':'Exact source identities, full quartic coefficients, finite-algebra specification, local constants and quantitative bounds. The global arithmetic projection premises are stated separately in the papers.'}
    if args.receipt:
        args.receipt.parent.mkdir(parents=True,exist_ok=True)
        args.receipt.write_text(json.dumps(report,indent=2)+'\n')
    print('All supplied checks passed; published inputs were unchanged.')


if __name__=='__main__':
    main()
