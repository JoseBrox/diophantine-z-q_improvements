# Generated locator adapter; --repo names the isolated adapter directory.
"""Untrusted producer and incidence diagnostic for gpoint chart replacement.

Run against the structured norm-base artifact, before elimination/unit scaling.
Only standard library plus the existing untrusted polynomial/export tools.
"""
import argparse
from collections import defaultdict
import gzip
import json
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--parent', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--diagnostic', type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import polynomial_ops as ops
    from export_artifact import enc, export
    rows = [{tuple(m): c for c, m in r} for r in json.loads(gzip.decompress((args.parent / 'candidate-rows.json.gz').read_bytes()))]
    records = [json.loads(line) for line in gzip.decompress((args.parent / 'certificate.jsonl.gz').read_bytes()).splitlines()]
    allocated = records[-1]['allocated_variables']
    records = [r for r in records if r['kind'] not in ('weights', 'final')]
    incidence = defaultdict(set)
    for i, row in enumerate(rows):
        for v in ops.vars_in(row):
            incidence[v].add(i)
    def plus(*polys):
        result = {}
        for poly, coefficient in polys:
            ops.poly_add(result, poly, coefficient)
        return result
    def field_product(a, b):
        return [plus((ops.product(a[0], b[0]), 1), (ops.product(a[1], b[1]), 2)),
                plus((ops.product(a[0], b[1]), 1), (ops.product(a[1], b[0]), 1))]
    def variable_pair(pair):
        return [{(i,): 1} for i in pair]
    modules = {}
    for name in ('Z_definition', 'q_compare4'):
        module = json.loads((args.repo / 'source/modules' / (name + '.json')).read_bytes())
        modules[name] = module
    instances = json.loads((args.repo / 'construction-map.json').read_bytes())['instantiations']
    diagnostics = []
    blocks = ('f=u^2', 'v2+df=1', 'w2+v2=2', 'h=vw', 'zh+u=0', 'xf=1', 'yz+x=0')
    for instance in instances:
        if instance['module'] not in modules:
            continue
        module = modules[instance['module']]
        labels = {op[2]: op[1] for op in module['construction_log'] if op[0] == 'variable'}
        equations = {op[2]: op[1] for op in module['construction_log'] if op[0] == 'equation'}
        def global_variable(v):
            return instance['arguments'][v] if v < module['free'] else instance['first_local'] + v - module['free']
        for label in labels:
            if not label.endswith('.u.0'):
                continue
            prefix = label[:-4]
            if prefix + '.w.0' not in labels:
                continue  # The audited compressed primary chart is already reduced.
            coords = {part: [global_variable(labels[prefix + '.' + part + '.' + str(k)]) for k in range(2)]
                      for part in ('u', 'v', 'w', 'z', 'f', 'h', 'x', 'y')}
            row_ids = {block: [instance['first_residual'] + equations[prefix + '.' + block + '.' + str(k)] for k in range(2)] for block in blocks}
            exact = all(ops.primitive(rows[i]) == ops.primitive({tuple(sorted(global_variable(v) for v in mon)): c for c, mon in module['residuals'][i - instance['first_residual']]})
                        for pair in row_ids.values() for i in pair)
            changed = set(row_ids['w2+v2=2'] + row_ids['h=vw'] + row_ids['zh+u=0'])
            removed = coords['w'] + coords['h']
            outside = {str(v): sorted(incidence[v] - changed) for v in removed if incidence[v] - changed}
            item = {'instance': instance['path'], 'chart': prefix, 'exact_old_rows': exact,
                    'outside_uses': outside, 'removed': removed, 'old_rows': row_ids}
            diagnostics.append(item)
            if not args.output:
                continue
            assert exact and not outside, item
            fresh = [allocated, allocated + 1]
            allocated += 2
            p, f, x, y = map(variable_pair, (fresh, coords['f'], coords['x'], coords['y']))
            yf = field_product(y, f)
            pp = field_product(p, p)
            df = field_product([{(): 11}, {(): -6}], f)
            new_rows = [[plus((p[k], 1), (yf[k], -1)) for k in range(2)],
                        [plus((pp[k], 1), (x[k], -1), (df[k], 1)) for k in range(2)]]
            patches = {i: {} for i in changed}
            for block, pair in zip(('w2+v2=2', 'h=vw'), new_rows):
                for i, row in zip(row_ids[block], pair):
                    assert max(map(len, row), default=0) <= 2
                    patches[i] = dict(ops.primitive(row))
            records.append({'kind': 'gpoint_chart', 'data': {'coordinates': coords, 'rows': row_ids,
                            'new_variables': fresh, 'droot': [3, -1]},
                            'patches': [[i, enc(row)] for i, row in sorted(patches.items())]})
            for i, row in patches.items():
                rows[i] = row
    report = {'chart_count': len(diagnostics), 'all_exact': all(d['exact_old_rows'] for d in diagnostics),
              'all_private': all(not d['outside_uses'] for d in diagnostics),
              'raw_rational_variables_saved': 2 * len(diagnostics), 'charts': diagnostics}
    args.diagnostic.write_text(json.dumps(report, indent=2) + '\n')
    if args.output:
        expected_charts = sum(sum(op[0] == 'variable' and op[2].endswith('.w.0')
                                  for op in modules[inst['module']]['construction_log'])
                              for inst in instances if inst['module'] in modules)
        assert len(diagnostics) == expected_charts and expected_charts > 0
        report = export(args.output, args.parent / 'source-residuals.jsonl.gz', rows, records, allocated,
                        {'gpoint_chart_replacements': len(diagnostics), 'raw_rational_variables_saved': 2 * len(diagnostics)})
    print(json.dumps({k: v for k, v in report.items() if k != 'charts'}, indent=2), flush=True)


if __name__ == '__main__':
    main()
