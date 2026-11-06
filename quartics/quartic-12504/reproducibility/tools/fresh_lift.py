"""Untrusted fresh quadratic lift of one named, independently audited source."""
import argparse
from collections import defaultdict
from fractions import Fraction
import gzip
import hashlib
import itertools
import json
import math
from pathlib import Path

import polynomial_ops as op
from export_artifact import export


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--adapter', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    entry_bytes = (a.adapter/'source-entry.json').read_bytes()
    entry = json.loads(entry_bytes)
    source_path = a.adapter/'source-residuals.jsonl.gz'
    assert hashlib.sha256(source_path.read_bytes()).hexdigest() == entry['source_sha256']
    source = [{tuple(m): c for c, m in json.loads(line)} for line in gzip.decompress(source_path.read_bytes()).splitlines()[1:]]
    count = entry['source_variables']; source_rows = entry['source_rows']
    assert len(source) == source_rows
    assert set().union(*(op.vars_in(r) for r in source)) == set(range(count))
    assert all(len(m) <= 4 for r in source for m in r)

    # Reuse only explicit source equations xy=s*v with s nonzero. The separate
    # checker validates every anchor and compares each lifted source equation.
    rules = {}; reuse = []; anchors = set()
    for index, row in enumerate(source):
        if len(row) != 2:
            continue
        products = [m for m in row if len(m) == 2]
        targets = [m[0] for m in row if len(m) == 1 and m[0] != 0]
        if len(products) != 1 or len(targets) != 1:
            continue
        pair, variable = products[0], targets[0]
        if variable in pair or pair in rules:
            continue
        scale = Fraction(-row[(variable,)], row[pair])
        rules[pair] = (variable, scale); anchors.add(index)
        reuse.append(dict(product=list(pair), variable=variable,
                          scale=[scale.numerator, scale.denominator], anchor=index))

    # Make guard-dependent product coordinates private whenever possible.
    # This affects efficiency only, never the lift verification contract.
    visits = json.loads((a.adapter/'construction-map.json').read_bytes())['instantiations']
    module = json.loads((a.adapter/'source/modules/q_compare4.json').read_bytes())
    local_variables = [x for kind, x, label in module['construction_log'] if kind=='variable' and label=='distinct abscissae guard']
    local_rows = [x for kind, x, label in module['construction_log'] if kind=='equation' and label=='distinct abscissae guard']
    assert len(local_variables) == len(local_rows) == 5
    preferred = {}
    for visit in visits:
        if visit['module'] != 'q_compare4':
            continue
        for local_row, local_variable in zip(local_rows, local_variables):
            preferred[visit['first_residual']+local_row] = visit['first_local']+local_variable-module['free']

    gates = []; gate_rows = []; products = {}; allocated = count
    def bind(pair):
        nonlocal allocated
        pair = tuple(sorted(pair))
        if pair not in products:
            products[pair] = allocated
            gates.append(dict(variable=allocated, product=list(pair)))
            gate_rows.append({pair:-1, (allocated,):1})
            allocated += 1
        return products[pair]

    rows = []
    for index, row in enumerate(source):
        if index in anchors or all(len(m)<=2 for m in row):
            rows.append(row.copy()); continue
        lifted = defaultdict(Fraction)
        for mon, coefficient in row.items():
            mon = list(mon); coefficient = Fraction(coefficient)
            if len(mon)>2:
                while True:
                    choices = sorted(set(itertools.combinations(mon,2)) & rules.keys())
                    if not choices:
                        break
                    pair = choices[0]; variable, scale = rules[pair]
                    for x in pair:
                        mon.remove(x)
                    mon.append(variable); mon.sort(); coefficient *= scale
            while len(mon)>2:
                guard = preferred.get(index)
                if guard in mon:
                    other = next(x for x in mon if x != guard)
                    pair = tuple(sorted((guard,other)))
                else:
                    pair = tuple(mon[:2])
                variable = bind(pair)
                for x in pair:
                    mon.remove(x)
                mon.append(variable); mon.sort()
            lifted[tuple(mon)] += coefficient
        lifted = {m:c for m,c in lifted.items() if c}
        denominator = math.lcm(*(c.denominator for c in lifted.values()))
        integers = {m:int(c*denominator) for m,c in lifted.items()}
        rows.append(dict(op.primitive(integers)) if integers else {})
    rows.extend(gate_rows)
    initial = dict(kind='initial', source_id=entry['source_id'],
                   source_entry_sha256=hashlib.sha256(entry_bytes).hexdigest(),
                   source_sha256=entry['source_sha256'], source_variables=count,
                   source_rows=source_rows, reuse=reuse, gates=gates,
                   rows=[[[c,list(m)] for m,c in row.items()] for row in rows])
    report = export(a.output, source_path, rows, [initial], allocated,
                    dict(fresh_source_id=entry['source_id'], initial_lift_gates=len(gates), reused_source_products=len(reuse)))
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
