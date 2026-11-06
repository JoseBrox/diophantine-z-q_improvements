"""Targeted negative tests for the exact 12,504-variable release certificate.

The pinned checker is imported only in a bounded child process. A malformed
case passes only on AssertionError at its expected semantic check. Timeouts,
resource failures, import errors and other exceptions fail this test run.
The source artifact and checker are never edited.
"""
import argparse
import gzip
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import traceback

if not __debug__:
    raise RuntimeError('Run without -O: assertions must remain enabled')

CHECKER_SHA = 'd2079177a4960740c5b7d42fbd0756dfc4ce8953cc947cee91c8786ba26fa8ba'
SOURCE_ID = 'reciprocal64-beta16-compressed-s1-b5e836d77643'
SOURCE_SHA = 'ce9eeac7c4730aced8cfb70a1ab3b1b6a7fb2110c597afad1f56ddc92aeea73f'
CERTIFICATE_SHA = '9f7979c1e786bebad624b9ea4631b7eccd879f4bebb5b9ab69250b945973b268'
EXPANDED_SHA = '7f5aa3117af82a0b323f0a4e74a18599204f5540408106d3ce99612b5ed830ca'
EXPECTED = dict(variables=12504, witnesses=12503, rows=11939,
                monomials=135721, degree=4,
                max_abs_coefficient=685783949153203534233601,
                source_id=SOURCE_ID, source_sha256=SOURCE_SHA,
                expanded_sha256=EXPANDED_SHA, certificate_sha256=CERTIFICATE_SHA,
                checker_sha256=CHECKER_SHA, total_operations=1467,
                weights_greater_than_one=0)
FILES = ('source-residuals.jsonl.gz', 'certificate.jsonl.gz',
         'candidate-rows.json.gz', 'variable-map.json', 'residuals.json.gz',
         'polynomial.expanded.txt', 'polynomial.expanded.txt.gz')
MAX_FILE = 50_000_000
MAX_EXPANDED = 150_000_000

# These are source statements in the frozen independent checker. Checking the
# rejection location prevents an unrelated, earlier failure from earning PASS.
CASES = {
    'unknown_source_id': 'assert source_id in SOURCE_ENTRIES',
    'wrong_source_entry_digest': "first['source_entry_sha256']",
    'changed_source_header': "==entry['source_header']",
    'changed_source_body': "==entry['uncompressed_sha256']",
    'changed_source_gzip_bytes': '==SOURCE_SHA',
    'wrong_initial_row_count': "initial['source_rows']==SOURCE_ROWS",
    'wrong_reuse_scale': 'normal(source[index])==normal',
    'missing_product_gate': 'len(rows)==SOURCE_ROWS+len(gates)',
    'forward_product_dependency': 'all(w in expanded_vars for w in pair)',
    'wrong_product_definition': 'rows[SOURCE_ROWS+position]==',
    'changed_retained_anchor': "('anchor',i)",
    'changed_lifted_source_row': "('source',i)",
    'free_input_elimination': 'assert v!=0',
    'missed_elimination_consumer': 'set(affected)==incidence[v]-{i}',
    'zero_elimination_denominator': 'denominator>0',
    'singular_linear_operation': 'a!=0',
    'wrong_operation_patch': "('incorrect row',i)",
    'wrong_final_allocation_count': "final['allocated_variables']==nextvar",
    'wrong_final_rows_digest': "==final['rows_sha256']",
    'data_after_final_record': 'Data after final record',
    'changed_saved_candidate': 'assert saved==rows',
    'moved_free_input': 'assert active[0]==0',
    'omitted_active_coordinate': 'assert set(active)==',
    'changed_compact_residual': 'assert compact==',
    'changed_expanded_coefficient': 'assert polynomial==supplied',
    'omitted_expanded_term': 'assert polynomial==supplied',
    'duplicate_expanded_term': 'm not in supplied',
    'changed_gzip_twin': 'gzip.decompress',
    'wrong_reported_variable_count': "stats[key]==final['report'][key]",
    'oversized_exact_quartic': "maximum<2**80",
}


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode('ascii')


def bounded_bytes(path):
    if path.stat().st_size > MAX_FILE:
        raise RuntimeError('Input file exceeds test resource limit: '+str(path))
    return path.read_bytes()


def uncompressed(path):
    with gzip.open(path, 'rb') as stream:
        data = stream.read(MAX_EXPANDED+1)
    if len(data) > MAX_EXPANDED:
        raise RuntimeError('Expanded input exceeds test resource limit')
    return data


def write_gzip(path, data):
    path.write_bytes(gzip.compress(data, mtime=0))


def read_json(path):
    return json.loads(uncompressed(path) if path.suffix == '.gz' else bounded_bytes(path))


def write_json(path, value):
    data = canonical(value)
    if path.suffix == '.gz':
        write_gzip(path, data)
    else:
        path.write_bytes(data+b'\n')


def shift_constant(row):
    for term in row:
        if term[1] == []:
            term[0] += 1
            if not term[0]:
                row.remove(term)
            return
    row.append([1, []])


def expanded_lines(root):
    lines = bounded_bytes(root/'polynomial.expanded.txt').splitlines()
    indexes = [i for i, line in enumerate(lines) if line and not line.startswith(b'#')]
    if not indexes:
        raise RuntimeError('No expanded terms')
    return lines, indexes


def write_expanded(root, lines):
    data = b'\n'.join(lines)+b'\n'
    (root/'polynomial.expanded.txt').write_bytes(data)
    write_gzip(root/'polynomial.expanded.txt.gz', data)


def mutate(root, case):
    cert_path = root/'certificate.jsonl.gz'
    records = [json.loads(line) for line in uncompressed(cert_path).splitlines()]
    initial, final = records[0], records[-1]
    if initial['kind'] != 'initial' or final['kind'] != 'final':
        raise RuntimeError('Unexpected certificate structure')
    def operation(kind):
        return next(r for r in records if r['kind'] == kind)
    if case == 'unknown_source_id':
        initial['source_id'] = SOURCE_ID+'-unapproved'
    elif case == 'wrong_source_entry_digest':
        initial['source_entry_sha256'] = '0'*64
    elif case in ('changed_source_header', 'changed_source_body'):
        source = root/'source-residuals.jsonl.gz'
        lines = uncompressed(source).splitlines()
        if case == 'changed_source_header':
            header = json.loads(lines[0]); header['witnesses'] += 1
            lines[0] = canonical(header)
        else:
            row = json.loads(lines[1]); shift_constant(row)
            lines[1] = canonical(row)
        write_gzip(source, b'\n'.join(lines)+b'\n')
    elif case == 'changed_source_gzip_bytes':
        source = root/'source-residuals.jsonl.gz'
        data = bytearray(bounded_bytes(source))
        data[4] ^= 1  # Only MTIME changes; the plain source stays identical.
        source.write_bytes(data)
    elif case == 'wrong_initial_row_count':
        initial['source_rows'] += 1
    elif case == 'wrong_reuse_scale':
        initial['reuse'][0]['scale'][0] *= -1
    elif case == 'missing_product_gate':
        initial['gates'].pop()
    elif case == 'forward_product_dependency':
        g = initial['gates'][0]; g['product'][0] = g['variable']
    elif case == 'wrong_product_definition':
        shift_constant(initial['rows'][initial['source_rows']])
    elif case == 'changed_retained_anchor':
        shift_constant(initial['rows'][initial['reuse'][0]['anchor']])
    elif case == 'changed_lifted_source_row':
        anchors = {r['anchor'] for r in initial['reuse']}
        index = next(i for i, row in enumerate(initial['rows'][:initial['source_rows']])
                     if i not in anchors and any(term[1] for term in row))
        shift_constant(initial['rows'][index])
    elif case == 'free_input_elimination':
        operation('eliminate')['data']['variable'] = 0
    elif case == 'missed_elimination_consumer':
        event = next(r for r in records if r['kind']=='eliminate' and r['data']['affected'])
        event['data']['affected'].pop()
    elif case == 'zero_elimination_denominator':
        operation('eliminate')['data']['denominator'] = 0
    elif case == 'singular_linear_operation':
        operation('linear')['data']['a'] = 0
    elif case == 'wrong_operation_patch':
        event = operation('norm_inverse')
        row = next(row for _, row in event['patches'] if row)
        shift_constant(row)
    elif case == 'wrong_final_allocation_count':
        final['allocated_variables'] += 1
    elif case == 'wrong_final_rows_digest':
        final['rows_sha256'] = '0'*64
    elif case == 'data_after_final_record':
        records.append({'kind': 'unaccepted_trailing_data'})
    elif case == 'changed_saved_candidate':
        path = root/'candidate-rows.json.gz'; rows = read_json(path)
        shift_constant(next(row for row in rows if row)); write_json(path, rows)
    elif case in ('moved_free_input', 'omitted_active_coordinate'):
        path = root/'variable-map.json'; active = read_json(path)
        if case == 'moved_free_input':
            active[0], active[1] = active[1], active[0]
        else:
            active.pop()
        write_json(path, active)
    elif case == 'changed_compact_residual':
        path = root/'residuals.json.gz'; rows = read_json(path)
        shift_constant(rows[0]); write_json(path, rows)
    elif case in ('changed_expanded_coefficient', 'omitted_expanded_term',
                  'duplicate_expanded_term', 'changed_gzip_twin', 'oversized_exact_quartic'):
        lines, indexes = expanded_lines(root)
        if case == 'changed_expanded_coefficient':
            parts = lines[indexes[0]].split(); c = int(parts[0])
            parts[0] = str(c+(1 if c>0 else -1)).encode('ascii')
            lines[indexes[0]] = b' '.join(parts)
        elif case == 'omitted_expanded_term':
            lines.pop(indexes[0])
        elif case == 'duplicate_expanded_term':
            lines.append(lines[indexes[0]])
        elif case == 'changed_gzip_twin':
            write_gzip(root/'polynomial.expanded.txt.gz', b'\n'.join(lines)+b'\n#changed\n')
        else:
            multiplier = 1 << 80
            rows = read_json(root/'candidate-rows.json.gz')
            weight_events = [r for r in records if r['kind']=='weights']
            if len(weight_events) > 1:
                raise RuntimeError('Fixture has multiple weights events')
            if weight_events:
                weights = weight_events[0]['values']
                if len(weights) != len(rows) or any(type(w) is not int or w <= 0 for w in weights):
                    raise RuntimeError('Malformed fixture weights')
                weight_events[0]['values'] = [w*multiplier for w in weights]
            else:
                weights = [1]*len(rows)
                records.insert(-1, {'kind':'weights', 'values':[multiplier]*len(rows)})
            write_json(root/'weights.json', [w*multiplier for row,w in zip(rows,weights) if row])
            for i in indexes:
                parts = lines[i].split()
                parts[0] = str(int(parts[0])*multiplier).encode('ascii')
                lines[i] = b' '.join(parts)
        if case != 'changed_gzip_twin':
            write_expanded(root, lines)
    elif case == 'wrong_reported_variable_count':
        final['report']['variables'] += 1
    else:
        raise RuntimeError('Unknown mutation: '+case)
    write_gzip(cert_path, b''.join(canonical(r)+b'\n' for r in records))


def load_checker(path):
    if hashlib.sha256(bounded_bytes(path)).hexdigest() != CHECKER_SHA:
        raise RuntimeError('Independent checker is not the frozen release checker')
    spec = importlib.util.spec_from_file_location('release_independent_checker', path)
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    return checker


def worker(args):
    checker = load_checker(args.checker)
    if args.worker == 'valid':
        report = checker.verify(args.artifact, False)
        if any(report.get(key) != value for key, value in EXPECTED.items()):
            raise RuntimeError('Valid artifact does not match the exact release claim')
        print(json.dumps({'status':'VALID', 'verified':EXPECTED}))
        return 0
    with tempfile.TemporaryDirectory(prefix='quartic12504-negative-') as directory:
        scratch = Path(directory)
        for name in FILES+('weights.json',):
            path = args.artifact/name
            if path.exists():
                bounded_bytes(path)
                shutil.copyfile(path, scratch/name)
            elif name in FILES:
                raise RuntimeError('Missing artifact file: '+name)
        mutate(scratch, args.worker)
        try:
            checker.verify(scratch, False)
        except AssertionError as error:
            frames = traceback.extract_tb(error.__traceback__)
            lines = [frame.line or '' for frame in frames
                     if Path(frame.filename).resolve() == args.checker.resolve()]
            expected = CASES[args.worker]
            if not any(expected in line for line in lines):
                raise RuntimeError('Rejected at an unexpected checkpoint: '+repr(lines)) from error
            print(json.dumps({'status':'REJECTED', 'case':args.worker,
                              'checkpoint':expected, 'exception':'AssertionError'}))
            return 17
        raise RuntimeError('Independent checker accepted mutation: '+args.worker)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artifact', type=Path, required=True)
    parser.add_argument('--checker', type=Path, required=True)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--seconds-per-case', type=float, default=45)
    parser.add_argument('--seconds-total', type=float, default=600)
    parser.add_argument('--worker', choices=['valid']+list(CASES), help=argparse.SUPPRESS)
    args = parser.parse_args()
    for value in (args.seconds_per_case, args.seconds_total):
        if not math.isfinite(value) or not 0 < value <= 1800:
            parser.error('Time limits must be finite, positive and at most 1800 seconds')
    args.artifact = args.artifact.resolve(); args.checker = args.checker.resolve()
    if args.worker:
        return worker(args)
    if args.report is None:
        parser.error('--report is required')
    if args.report.resolve().is_relative_to(args.artifact):
        parser.error('Place the report outside the frozen artifact')
    for name in FILES:
        bounded_bytes(args.artifact/name)
    if hashlib.sha256(bounded_bytes(args.checker)).hexdigest() != CHECKER_SHA:
        raise RuntimeError('Checker byte pin differs')
    for name, expected in [('source-residuals.jsonl.gz',SOURCE_SHA),
                           ('certificate.jsonl.gz',CERTIFICATE_SHA),
                           ('polynomial.expanded.txt',EXPANDED_SHA)]:
        if hashlib.sha256(bounded_bytes(args.artifact/name)).hexdigest() != expected:
            raise RuntimeError('Exact release fixture byte pin differs: '+name)
    start = time.monotonic(); results = []
    for case in ['valid']+list(CASES):
        left = args.seconds_total-(time.monotonic()-start)
        if left <= 0:
            raise RuntimeError('Overall resource deadline expired; no PASS is issued')
        command = [sys.executable, '-E', '-B', str(Path(__file__).resolve()), '--artifact',
                   str(args.artifact), '--checker', str(args.checker), '--worker', case]
        # TimeoutExpired propagates. Any code/import/resource failure is fatal.
        run = subprocess.run(command, capture_output=True, text=True,
                             timeout=min(args.seconds_per_case,left))
        required_code = 0 if case == 'valid' else 17
        if run.returncode != required_code:
            raise RuntimeError('Case '+case+' failed: '+run.stdout[-4000:]+run.stderr[-4000:])
        result = json.loads(run.stdout)
        if result.get('status') != ('VALID' if case=='valid' else 'REJECTED'):
            raise RuntimeError('Unexpected worker report')
        results.append(result)
    if time.monotonic()-start > args.seconds_total:
        raise RuntimeError('Overall resource deadline expired; no PASS is issued')
    report = dict(status='PASS', valid_exact_artifact='PASS', malformed_cases=len(CASES),
                  cases=results[1:], release_claim=EXPECTED,
                  test_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  seconds=round(time.monotonic()-start,3),
                  scope='Named-source lift, certificate, compaction and exact quartic bounds; not arithmetic theorem proof')
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
