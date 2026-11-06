# Generated locator adapter; --repo names the isolated adapter directory.
"""Untrusted producer for removing chart y when y=x*p stays quadratic."""
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
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import polynomial_ops as ops
    from export_artifact import enc, export
    rows = [{tuple(m): c for c, m in r} for r in json.loads(gzip.decompress((args.parent / 'candidate-rows.json.gz').read_bytes()))]
    records = [json.loads(line) for line in gzip.decompress((args.parent / 'certificate.jsonl.gz').read_bytes()).splitlines()]
    allocated = records[-1]['allocated_variables']
    records = [r for r in records if r['kind'] not in ('weights', 'final')]
    chart_data = [r['data'] for r in records if r['kind'] == 'gpoint_chart']
    expected = json.loads((args.repo/'source-entry.json').read_bytes())['uncompressed_chart_count']
    assert len(chart_data) == expected
    incidence = defaultdict(set)
    for i, row in enumerate(rows):
        for v in ops.vars_in(row):
            incidence[v].add(i)
    def plus(*pairs):
        result = {}
        for poly, scalar in pairs:
            ops.poly_add(result, poly, scalar)
        return result
    def fm(a, b):
        return [plus((ops.product(a[0], b[0]), 1), (ops.product(a[1], b[1]), 2)),
                plus((ops.product(a[0], b[1]), 1), (ops.product(a[1], b[0]), 1))]
    applied, skipped = 0, []
    for chart in chart_data:
        coords = {name: chart['coordinates'][name] for name in ('x', 'y', 'z', 'f')}
        coords['p'] = chart['new_variables']
        proofs = {'xf=1': chart['rows']['xf=1'], 'p=yf': chart['rows']['w2+v2=2'],
                  'yz+x=0': chart['rows']['yz+x=0']}
        pairs = {name: [{(v,): 1} for v in ids] for name, ids in coords.items()}
        xp = dict(zip(coords['y'], fm(pairs['x'], pairs['p'])))
        pz = fm(pairs['p'], pairs['z'])
        ops.poly_add(pz[0], {(): 1})
        affected = incidence[coords['y'][0]] | incidence[coords['y'][1]]
        patches = {}
        bad = []
        for i in affected:
            if i in proofs['p=yf']:
                patches[i] = {}
                continue
            if i in proofs['yz+x=0']:
                patches[i] = pz[proofs['yz+x=0'].index(i)]
                continue
            out = {}
            for monomial, coefficient in rows[i].items():
                term = {(): coefficient}
                for v in monomial:
                    term = ops.product(term, xp.get(v, {(v,): 1}))
                ops.poly_add(out, term)
            if any(len(m) > 2 for m in out):
                bad.append(i)
            patches[i] = out
        if bad:
            skipped.append({'y': coords['y'], 'higher_degree_rows': bad})
            continue
        patches = {i: dict(ops.primitive(row)) if row else {} for i, row in patches.items()}
        records.append({'kind': 'field_ordinate', 'data': {'coordinates': coords, 'rows': proofs},
                        'patches': [[i, enc(row)] for i, row in sorted(patches.items())]})
        for i, row in patches.items():
            for v in ops.vars_in(rows[i]):
                incidence[v].remove(i)
            rows[i] = row
            for v in ops.vars_in(row):
                incidence[v].add(i)
        applied += 1
    report = export(args.output, args.parent / 'source-residuals.jsonl.gz', rows, records, allocated,
                    {'removed_field_ordinates': applied, 'raw_rational_variables_saved': applied * 2,
                     'skipped': skipped})
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
