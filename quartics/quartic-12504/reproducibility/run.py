"""Reproduce and independently check the frozen 12,504-variable quartic.

The package is read-only. All generated files go into a new --output directory.
Only the Python standard library is used. Child checks always enable assertions.
"""
if not __debug__:
    raise RuntimeError('Assertions are required; run Python without -O.')

import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import signal
import subprocess
import sys
import time
import zlib

SOURCE_ID = 'reciprocal64-beta16-compressed-s1-b5e836d77643'
SOURCE_SHA = 'ce9eeac7c4730aced8cfb70a1ab3b1b6a7fb2110c597afad1f56ddc92aeea73f'
CHECKER_SHA = 'd2079177a4960740c5b7d42fbd0756dfc4ce8953cc947cee91c8786ba26fa8ba'
AUDITOR_SHA = '495ca32737687fca335704c6bdbabacf8f20a7698839aa680639e8e1b60a948f'
EXPECTED = dict(variables=12504, witnesses=12503, rows=11939, monomials=135721,
                degree=4, max_abs_coefficient=685783949153203534233601,
                expanded_bytes=3239486,
                expanded_sha256='7f5aa3117af82a0b323f0a4e74a18599204f5540408106d3ce99612b5ed830ca')
CANDIDATE_FILES = ('source-residuals.jsonl.gz', 'certificate.jsonl.gz',
                   'candidate-rows.json.gz', 'residuals.json.gz',
                   'variable-map.json', 'weights.json',
                   'polynomial.expanded.txt', 'polynomial.expanded.txt.gz')


def sha(path):
    digest=hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''):
            digest.update(chunk)
    return digest.hexdigest()


def load(path):
    return json.loads(path.read_bytes())


def save(path,obj):
    path.write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8',newline='\n')


def contained(root,name):
    assert not Path(name).is_absolute()
    result=(root/name).resolve()
    assert result.is_relative_to(root.resolve()) and result!=root.resolve(), name
    return result


def compare_report(actual,expected):
    actual=dict(actual); expected=dict(expected)
    actual.pop('seconds',None); expected.pop('seconds',None)
    assert actual==expected, 'Fresh source audit differs from frozen audit'


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--package',type=Path,default=Path(__file__).resolve().parents[1])
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--stage-seconds',type=int,default=300)
    a=p.parse_args()
    assert 1<=a.stage_seconds<=1200
    package=a.package.resolve(); output=a.output.resolve()
    assert not output.is_relative_to(package), 'Use an output directory outside the immutable package'
    manifest=load(package/'reproducibility/manifest.json')
    assert manifest['format']=='quartic-12504-reproducibility/v1'
    assert manifest['expected']==EXPECTED
    for name,record in manifest['files'].items():
        path=contained(package,name)
        assert path.is_file() and path.stat().st_size==record['bytes'] and sha(path)==record['sha256'], name
    assert sha(package/'verify_certificate.py')==CHECKER_SHA
    assert sha(package/'reproducibility/source-audit/check_source.py')==AUDITOR_SHA
    assert sha(package/'source-residuals.jsonl.gz')==SOURCE_SHA
    entry=load(package/'source-entry.json')
    assert entry['source_id']==SOURCE_ID and entry['source_sha256']==SOURCE_SHA
    assert entry['source_variables']==12064 and entry['source_rows']==11499
    assert entry['high']==64 and entry['label']==16 and entry['compressed'] is True
    assert sha(package/'source-audit.json')==entry['source_audit_sha256']
    assert sha(package/'construction-map.json')==entry['construction_map_sha256']
    frozen_source=(package/'source-residuals.jsonl.gz').read_bytes()
    raw_source=(package/'source/residuals.jsonl').read_bytes()
    assert gzip.decompress(frozen_source)==raw_source
    assert gzip.compress(raw_source,compresslevel=1,mtime=0)==frozen_source, (
        'Exact-byte reproduction needs the frozen gzip behavior. Use Linux CPython 3.12 with compatible zlib; '
        'the unchanged verify_certificate.py can separately replay the frozen artifact on other platforms.')
    output.mkdir(parents=True,exist_ok=False)
    steps=[]; started=time.monotonic()
    env=dict(os.environ)
    env.pop('PYTHONOPTIMIZE',None)
    env['PYTHONDONTWRITEBYTECODE']='1'
    def run(label,script,*arguments):
        command=[sys.executable,'-E','-B',str(script),*map(str,arguments)]
        log=output/(label+'.log'); before=time.monotonic()
        print(json.dumps({'step':label,'command':command}),flush=True)
        with log.open('wb') as stream:
            child=subprocess.Popen(command,cwd=output,env=env,stdout=stream,stderr=subprocess.STDOUT,
                                   start_new_session=(os.name=='posix'))
            try:
                code=child.wait(timeout=a.stage_seconds)
            except subprocess.TimeoutExpired:
                if os.name=='posix':
                    os.killpg(child.pid,signal.SIGKILL)
                else:
                    child.kill()
                child.wait()
                steps.append(dict(step=label,status='TIMEOUT: NOT VERIFIED',log=log.name))
                save(output/'steps.json',steps)
                raise
        steps.append(dict(step=label,exit_code=code,seconds=round(time.monotonic()-before,3),log=log.name))
        save(output/'steps.json',steps)
        assert code==0, ('Failed check; see log',label,log)
    def verify(label,candidate,*,endpoint=False):
        run(label,package/'verify_certificate.py',candidate)
        report=load(candidate/'verification.json')
        assert report['status']=='PASS' and report['source_id']==SOURCE_ID
        assert report['source_sha256']==SOURCE_SHA and report['checker_sha256']==CHECKER_SHA
        assert report['degree']==4 and report['max_abs_coefficient']<2**80
        if endpoint:
            for key,value in EXPECTED.items():
                assert report[key]==value, (key,report[key],value)
        return report

    original=package/'reproducibility/original'
    for family,filename in [('parity','check_parity.py'),('anchor','check_anchor.py'),
                            ('sieve','check_constants.py'),('geometry','check_published_quotients.py')]:
        run('original-'+family,original/'arithmetic'/family/filename,'--output',output/('original-'+family+'.json'))
    run('reciprocal-arithmetic',package/'reproducibility/reciprocal-checks/check_arithmetic_contract.py')
    audit=package/'reproducibility/source-audit'
    run('source-audit',audit/'check_source.py','--source',package/'source','--original',original,
        '--report',output/'source-audit.json','--write-map',output/'construction-map.json','--seconds',min(a.stage_seconds,600))
    compare_report(load(output/'source-audit.json'),load(package/'source-audit.json'))
    assert sha(output/'construction-map.json')==entry['construction_map_sha256']
    run('source-mutations',audit/'test_source.py','--source',package/'source','--original',original,
        '--report',output/'source-mutations.json','--seconds',min(a.stage_seconds,600))
    mutations=load(output/'source-mutations.json')
    assert mutations['status']=='PASS' and mutations['malformed_sources_rejected']==38
    assert len(mutations['resource_abort_regressions'])==5

    reference=output/'reference-replay'; reference.mkdir()
    for name in CANDIDATE_FILES:
        shutil.copyfile(package/name,reference/name)
    checked=verify('frozen-certificate',reference,endpoint=True)
    assert checked['certificate_sha256']=='9f7979c1e786bebad624b9ea4631b7eccd879f4bebb5b9ab69250b945973b268'
    run('certificate-mutations',package/'reproducibility/test_certificate.py',
        '--checker',package/'verify_certificate.py','--artifact',reference,
        '--report',output/'certificate-mutations.json',
        '--seconds-per-case',min(45,a.stage_seconds),'--seconds-total',min(600,a.stage_seconds))
    negative=load(output/'certificate-mutations.json')
    assert negative['status']=='PASS' and negative['malformed_cases']==30

    compiler=package/'source/compiler'
    rebuilt=output/'rebuilt-source'
    run('source-regeneration',compiler/'build_reciprocal_source.py','--builder',compiler/'archive_build.py',
        '--out',rebuilt,'--high',64,'--label',16,'--hscale',1,'--compressed-primary-charts')
    for name,digest in entry['inspected_files_sha256'].items():
        assert sha(rebuilt/name)==digest, ('Regenerated source differs',name)
    run('rebuilt-source-audit',audit/'check_source.py','--source',rebuilt,'--original',original,
        '--report',output/'rebuilt-source-audit.json','--write-map',output/'rebuilt-map.json',
        '--seconds',min(a.stage_seconds,600))
    compare_report(load(output/'rebuilt-source-audit.json'),load(package/'source-audit.json'))

    # Fresh construction starts from the just regenerated source. The frozen
    # entry/map are copied only after their bytes were independently rechecked.
    adapter=output/'rebuilt-adapter'; adapter.mkdir()
    shutil.copytree(rebuilt,adapter/'source')
    for name in ('source-entry.json','source-audit.json','construction-map.json'):
        shutil.copyfile(package/name,adapter/name)
    regenerated_raw=(rebuilt/'residuals.jsonl').read_bytes()
    source_bytes=gzip.compress(regenerated_raw,compresslevel=1,mtime=0)
    assert hashlib.sha256(source_bytes).hexdigest()==SOURCE_SHA
    (adapter/'source-residuals.jsonl.gz').write_bytes(source_bytes)
    tools=package/'reproducibility/tools'
    current=output/'fresh-lift'
    run('fresh-lift',tools/'fresh_lift.py','--adapter',adapter,'--output',current)
    verify('verify-fresh-lift',current)
    for name,script in [('norms','reduce_norms.py'),('charts','replace_charts.py'),
                        ('ordinates','remove_chart_ordinates.py'),('parity','produce_parity.py'),
                        ('batch','absorb_batch_error.py')]:
        target=output/name
        options=['--adapter' if name=='norms' else '--repo',adapter,'--parent',current,'--output',target]
        if name=='charts':
            options+=['--diagnostic',output/'chart-diagnostic.json']
        run(name,tools/script,*options); verify('verify-'+name,target); current=target
    target=output/'optimized'
    run('optimize',tools/'optimize.py','--parent',current,'--output',target,'--max-terms',96,'--rounds',8,
        '--rational','--gaussian','--row-combine','--row-order','reverse')
    verify('verify-optimized',target); current=target
    target=output/'coordinates'
    run('merge-coordinates',tools/'merge_coordinates.py','--parent',current,'--output',target)
    regenerated=verify('verify-regenerated-endpoint',target,endpoint=True)
    for name in CANDIDATE_FILES:
        if name=='certificate.jsonl.gz':
            continue  # Its final diagnostic report contains elapsed time.
        assert (package/name).read_bytes()==(target/name).read_bytes(), ('Endpoint bytes differ',name)
    def certificate_data(path):
        records=[json.loads(line) for line in gzip.decompress(path.read_bytes()).splitlines()]
        for record in records:
            if record['kind']=='final':
                record['report'].pop('seconds',None)
        return records
    assert certificate_data(package/'certificate.jsonl.gz')==certificate_data(target/'certificate.jsonl.gz')
    report=dict(status='PASS: FROZEN REPLAY AND CLEAN REPRODUCTION',expected=EXPECTED,
                source_id=SOURCE_ID,source_sha256=SOURCE_SHA,checker_sha256=CHECKER_SHA,
                regenerated_certificate_sha256=regenerated['certificate_sha256'],
                certificate_comparison='All records identical after removing only final.report.seconds',
                source_mutations=38,source_resource_abort_regressions=5,
                certificate_mutations=negative,python=sys.version,platform=platform.platform(),
                zlib_compile_version=zlib.ZLIB_VERSION,zlib_runtime_version=zlib.ZLIB_RUNTIME_VERSION,
                seconds=round(time.monotonic()-started,3),steps=steps,
                scope='Exact finite construction, projection-preserving certificate replay, full integer expansion, and reproducibility. Arithmetic theorem review remains separate.')
    save(output/'SUMMARY.json',report)
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
