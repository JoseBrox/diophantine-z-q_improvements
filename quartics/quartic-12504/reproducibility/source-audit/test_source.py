"""Bounded mutations of an actual generated reciprocal source package."""
import argparse
from copy import deepcopy
import gzip
import hashlib
import json
from math import isfinite
from pathlib import Path
import shutil
import tempfile
import time
import check_source as c


def remove_rows(module, selected):
    selected = set(selected)
    mapping = {}; rows = []
    for i, row in enumerate(module['residuals']):
        if i not in selected:
            mapping[i] = len(rows); rows.append(row)
    logs = []
    for op in module['construction_log']:
        if op[0] == 'equation':
            if op[1] in selected:
                continue
            op[1] = mapping[op[1]]
        logs.append(op)
    module['residuals'] = rows; module['construction_log'] = logs


def tagged(module, label):
    return [op[1] for op in module['construction_log'] if op[0] == 'equation' and op[2] == label]


def change_first(module, label):
    i = tagged(module, label)[0]
    module['residuals'][i][0][0] *= -1


def must_reject(name, fn):
    c.tick()
    try:
        fn()
    except c.CheckerResourceError:
        raise
    except (AssertionError, KeyError, ValueError, IndexError, TypeError):
        return name
    raise AssertionError('Malformed source accepted: '+name)


def resource_regressions():
    """Resource aborts are tested separately; none counts as source rejection."""
    checked = []
    def must_abort(name, fn):
        try:
            must_reject(name, fn)
        except c.CheckerResourceError:
            checked.append(name)
        else:
            raise AssertionError('Resource failure was counted as a semantic rejection: '+name)
    saved = c.DEADLINE
    try:
        c.DEADLINE = time.monotonic()-1
        must_abort('expired deadline propagates', c.tick)
    finally:
        c.DEADLINE = saved
    c.tick()
    must_abort('excessive free allocation propagates', lambda: c.Module({
        'free': c.MAX_COORDINATES+1, 'locals': 0, 'residuals': [], 'construction_log': [], 'calls': []}))
    must_abort('excessive multiplication degree propagates',
               lambda: c.mul({(0,)*c.MAX_DEGREE: c.Q(1)}, {(0,): c.Q(1)}))
    must_abort('excessive coefficient propagates',
               lambda: c.add((1, {(): c.Q(1 << c.MAX_COEFFICIENT_BITS)})))
    must_abort('normalization denominator growth propagates', lambda: c.normal({
        (0,): c.Q(1, 1 << (c.MAX_COEFFICIENT_BITS-1)), (1,): c.Q(1, 3)}))
    return checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--original', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--seconds', type=float, default=120)
    args = parser.parse_args()
    assert isfinite(args.seconds) and 0 < args.seconds <= 600
    c.DEADLINE = time.monotonic()+args.seconds
    abort_checks = resource_regressions()
    base_report, visits = c.check(args.source, args.original)
    contract = c.load(args.source/'PROPOSED_SOURCE.json')
    high, label, compressed = (contract[k] for k in ('high_precision','label_precision','compressed_primary_charts'))
    comparison = c.load(args.source/'modules/q_compare4.json')
    batch = c.load(args.source/'modules/q_batch41.json')
    rejected = []
    def comparison_mutation(name, mutate):
        bad = deepcopy(comparison); mutate(bad)
        rejected.append(must_reject(name, lambda: c.check_compare(bad, high, label, compressed)))
    comparison_mutation('changed reciprocal coefficient or D', lambda m: change_first(m, 'arithmetic'))
    comparison_mutation('missing difference parameter equation',
                        lambda m: remove_rows(m, tagged(m, 'difference formal parameter.0')[:1]))
    comparison_mutation('missing subtraction guard',
                        lambda m: remove_rows(m, tagged(m, 'distinct abscissae guard')[:1]))
    comparison_mutation('wrong subtraction sign',
                        lambda m: change_first(m, 'difference line at first point.0'))
    comparison_mutation('wrong declared shared precision', lambda m: m.update(precision=16))
    comparison_mutation('wrong field-order position',
                        lambda m: m['field_inequality_orders'].__setitem__(15, 1))
    def swap_primary(m):
        aa = m['calls'][0]['args']
        aa[24:26], aa[26:28] = aa[26:28], aa[24:26]
    comparison_mutation('swapped beta and other primary tests', swap_primary)
    def swap_alternate(m):
        aa = m['calls'][0]['args']
        aa[32:34], aa[34:36] = aa[34:36], aa[32:34]
    comparison_mutation('swapped H and beta alternate tests', swap_alternate)
    comparison_mutation('missing scalar root-error test', lambda m: m['calls'][0]['args'].pop(1))
    comparison_mutation('wrong scalar contact argument', lambda m: m['calls'][0]['args'].__setitem__(0, 29))
    def extra_core_row(m):
        row = len(m['residuals'])
        m['residuals'].append([[1, [0]]])
        m['construction_log'].append(['equation', row, 'unrequested core constraint'])
    comparison_mutation('extra coherent core constraint', extra_core_row)
    comparison_mutation('extra unlogged residual', lambda m: m['residuals'].append([[1, [0]]]))
    comparison_mutation('extra module call', lambda m: m['calls'].append(deepcopy(m['calls'][0])))
    def dependency(m, kind):
        row = tagged(m, 'arithmetic')[0]
        if kind == 'outside':
            variable = m['free']+m['locals']
        elif kind == 'forward':
            variable = m['free']+m['locals']-1
        else:
            # The arithmetic allocation immediately precedes its equation.
            position = m['construction_log'].index(['equation', row, 'arithmetic'])
            variable = m['construction_log'][position-1][1]
        mon = [variable, variable] if kind == 'self' else [variable]
        m['residuals'][row].append([1, mon])
    comparison_mutation('undeclared arithmetic dependency', lambda m: dependency(m, 'outside'))
    comparison_mutation('forward arithmetic dependency', lambda m: dependency(m, 'forward'))
    comparison_mutation('nonlinear arithmetic self-dependency', lambda m: dependency(m, 'self'))
    if compressed:
        comparison_mutation('missing Lambda pH interface',
                            lambda m: remove_rows(m, tagged(m, 'H pH=GH.0')+tagged(m, 'H pH=GH.1')))
        comparison_mutation('missing Ai=Ci*pi interface',
                            lambda m: remove_rows(m, tagged(m, 'A=C p.0')[:1]+tagged(m, 'A=C p.1')[:1]))
        comparison_mutation('wrong Lambda sign', lambda m: change_first(m, 'H pH=GH.0'))
        comparison_mutation('wrong numerator interface', lambda m: change_first(m, 'A H=G.0'))
        comparison_mutation('missing compressed chart inverse xf=1',
                            lambda m: remove_rows(m, tagged(m, 'X0.xf=1.0')+tagged(m, 'X0.xf=1.1')))
    else:
        comparison_mutation('missing logarithm inverse real equation',
                            lambda m: remove_rows(m, tagged(m, 'field inverse real')))
        comparison_mutation('wrong logarithm inverse sign', lambda m: change_first(m, 'field inverse real'))
    orders = [1]*23+[label]*2+[high]*8+[label]*2+[high]*6
    def batch_mutation(name, mutate):
        bad = deepcopy(batch); mutate(bad)
        rejected.append(must_reject(name, lambda: c.check_batch(bad, orders)))
    batch_mutation('wrong rational order', lambda m: m['orders'].__setitem__(23, 1))
    batch_mutation('omitted bottom norm constraint',
                   lambda m: remove_rows(m, tagged(m, 'fused normalized pair')[:1]))
    batch_mutation('wrong first constant leaf', lambda m: change_first(m, 'fused constant leaf norm'))
    batch_mutation('wrong power definition', lambda m: change_first(m, 'shared contact power'))
    batch_mutation('wrong upper norm sign', lambda m: change_first(m, 'cubic norm node'))
    batch_mutation('wrong parity input', lambda m: m['calls'][0]['args'].__setitem__(0, 0))
    modules = {name: c.load(args.source/'modules'/f'{name}.json') for name in c.ORIGINAL_MODULES}
    originals = {name: c.load(args.original/'modules'/f'{name}.json') for name in c.ORIGINAL_MODULES}
    for name, mutate in [
        ('changed height order', lambda mm: mm['q_height_batch']['orders'].__setitem__(4, 16)),
        ('changed root fixed constant', lambda mm: mm['Z_definition']['residuals'][0][0].__setitem__(0, 123)),
        ('changed anchor squarings', lambda mm: mm['q_anchor'].update(anchor_squarings=1)),
        ('changed root contact call', lambda mm: mm['Z_definition']['calls'][-1]['args'].__setitem__(-1, 0)),
        ('omitted parity equation', lambda mm: mm['q_primeparity']['residuals'].pop()),
    ]:
        bad = deepcopy(modules); mutate(bad)
        rejected.append(must_reject(name, lambda bad=bad: c.unchanged_modules(bad, originals, high)))

    # These tests use actual files and the independent flattening pass.
    # Only the tiny required metadata and the bounded residual stream are
    # copied into a temporary test directory, not the compiler or repository.
    selected = args.source/base_report['source_residual_file']
    if selected.suffix == '.gz':
        with gzip.open(selected, 'rt') as stream:
            flat_text = stream.read(50_000_001)
    else:
        with selected.open('rt') as stream:
            flat_text = stream.read(50_000_001)
    c.resource(len(flat_text) <= 50_000_000, 'Mutation fixture stream bound reached')
    flat_lines = flat_text.splitlines(keepends=True)
    with tempfile.TemporaryDirectory(prefix='reciprocal-audit-mutations-') as temp:
        directory = Path(temp)
        for name in ('shared.json', 'counts.json', 'polynomial.json'):
            shutil.copyfile(args.source/name, directory/name)
        def flat_mutation(name, change, changed_modules=None):
            lines = list(flat_lines); change(lines)
            (directory/'residuals.jsonl').write_text(''.join(lines))
            rejected.append(must_reject(name, lambda: c.flatten_and_check(
                directory, modules if changed_modules is None else changed_modules, high)))
        flat_mutation('missing flattened residual', lambda lines: lines.pop(1))
        flat_mutation('extra flattened residual', lambda lines: lines.append(lines[1]))
        def wrong_coefficient(lines):
            row = json.loads(lines[1]); row[0][0] += 1
            lines[1] = json.dumps(row)+'\n'
        flat_mutation('corrupted flattened coefficient', wrong_coefficient)
        def wrong_coordinate(lines):
            row = json.loads(lines[2])
            next(term[1] for term in row if term[1])[0] = 0
            lines[2] = json.dumps(row)+'\n'
        flat_mutation('corrupted shared-to-global coordinate map', wrong_coordinate)
        bad_modules = deepcopy(modules)
        bad_modules['Z_definition']['calls'][-1]['args'][-1] = 0
        flat_mutation('corrupted call-to-local coordinate map', lambda lines: None, bad_modules)
        (directory/'residuals.jsonl').write_text(flat_text)
        with gzip.open(directory/'residuals.jsonl.gz', 'wb') as stream:
            stream.write(b'{}\n')
        rejected.append(must_reject('mismatching raw and compressed residual streams',
                                    lambda: c.flatten_and_check(directory, modules, high)))
    canonical_map = c.construction_map_bytes(visits)
    assert hashlib.sha256(canonical_map).hexdigest() == base_report['construction_map_sha256']
    bad_visits = deepcopy(visits); bad_visits[0]['first_local'] += 1
    assert hashlib.sha256(c.construction_map_bytes(bad_visits)).hexdigest() != base_report['construction_map_sha256']
    c.tick()
    report = dict(status='PASS', valid_complete_source=base_report['status'],
                  malformed_sources_rejected=len(rejected), cases=rejected,
                  resource_abort_regressions=abort_checks, construction_map_digest_regression='PASS',
                  scope='source equations/order/privacy and frozen-module mutations; not analytic theorem review')
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
