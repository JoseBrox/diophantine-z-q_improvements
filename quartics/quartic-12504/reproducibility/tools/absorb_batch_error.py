# Generated locator adapter; --repo names the isolated adapter directory.
"""Source-matched producer; apply before generic elimination/unit scaling.

Example from repository root:
 python research/quartic-variables/astra-wave9/batching/absorb_batch_error.py \
   --repo . --parent build/quartic-variables-wave6/norm-base --output build/batch-absorb

This producer does not import the independent rule checker.
"""
import argparse
from collections import defaultdict
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import sys


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--parent', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--diagnostic-only', action='store_true')
    a = ap.parse_args()
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import polynomial_ops as op
    from export_artifact import enc, export
    def decode(rr):
        return {tuple(m): c for c, m in rr}
    def normalized(rr):
        return op.primitive(rr) if rr else ()
    def add(*parts):
        rr = {}
        for c, pp in parts:
            op.poly_add(rr, pp, c)
        return rr
    def var(i):
        return {(i,): 1}
    def prod(*pp):
        out = {(): 1}
        for p in pp:
            out = op.product(out, p)
        return out
    def assert_same(i, pp):
        assert normalized(rows[i]) == normalized(pp), ('changed required row', i)
    source_bytes = (a.parent/'source-residuals.jsonl.gz').read_bytes()
    # The exact source hash is checked below without depending on source count.
    entry = json.loads((a.repo/'source-entry.json').read_bytes())
    assert hashlib.sha256(source_bytes).hexdigest() == entry['source_sha256']
    source = [decode(json.loads(line)) for line in gzip.decompress(source_bytes).splitlines()[1:]]
    rows = [decode(rr) for rr in json.loads(gzip.decompress((a.parent/'candidate-rows.json.gz').read_bytes()))]
    records = [json.loads(line) for line in gzip.decompress((a.parent/'certificate.jsonl.gz').read_bytes()).splitlines()]
    allocated = records[-1]['allocated_variables']
    records = [x for x in records if x['kind'] not in ('weights', 'final')]
    initial = records[0]
    gate_defs = {g['variable']: (len(source)+j, tuple(g['product']))
                 for j, g in enumerate(initial['gates'])}
    modules = {name: json.loads((a.repo/'source/modules'/f'{name}.json').read_bytes())
               for name in ('Z_definition', 'q_compare4', 'q_batch41')}
    instances = json.loads((a.repo/'construction-map.json').read_bytes())['instantiations']
    roots = [i for i in instances if i['module'] == 'Z_definition']
    assert len(roots) == 1
    root = roots[0]; rm = modules['Z_definition']; bm = modules['q_batch41']
    def global_var(inst, mod, t):
        if t < 0:
            raise AssertionError('unexpected global constant')
        return inst['arguments'][t] if t < mod['free'] else inst['first_local']+t-mod['free']
    def global_row(inst, mod, rr):
        return {tuple(sorted(global_var(inst, mod, t) for t in m)): c for m, c in decode(rr).items()}
    erows = [x[1] for x in rm['construction_log'] if x[0] == 'equation' and x[2] == 'root error']
    assert len(erows) == 1
    root_i = root['first_residual']+erows[0]
    root_pp = global_row(root, rm, rm['residuals'][erows[0]])
    theta, = [m[0] for m in root_pp if len(m) == 2 and m[0] == m[1]]
    E, = [m[0] for m in root_pp if len(m) == 1]
    assert_same(root_i, add((1, var(E)), (-1, prod(var(theta), var(theta))), (2, {(): 1})))

    # Locate exact E*B aliases by the frozen comparison call's own argument
    # map, including signs from conjugation. Shared aliases are deduplicated.
    aliases = {}
    for inst in instances:
        if inst['module'] != 'q_compare4':
            continue
        mod = modules['q_compare4']
        call, = [c for c in mod['calls'] if c['module'] == 'q_batch41']
        assert global_var(inst, mod, call['args'][1]) == E
        for position in range(2, len(call['args']), 2):
            local_x = call['args'][position]
            candidates = []
            for j, raw in enumerate(mod['residuals']):
                pp = decode(raw); c = pp.get((local_x,), 0)
                if not c or any(local_x in mon for mon in pp if mon != (local_x,)):
                    continue
                rhs = add((-Fraction(1, c), pp), (1, var(local_x)))
                local_e = call['args'][1]
                if not rhs or not all(local_e in mon for mon in rhs):
                    continue
                base = {}
                for mon, coeff in rhs.items():
                    mm = list(mon); mm.remove(local_e)
                    base[tuple(mm)] = coeff
                if all(len(mon) <= 1 for mon in base):
                    candidates.append((j, base))
            assert len(candidates) == 1, (inst, local_x, candidates)
            j, base = candidates[0]
            assert all(c.denominator == 1 for c in base.values())
            gb = {tuple(sorted(global_var(inst, mod, t) for t in mon)): int(c) for mon, c in base.items()}
            x = global_var(inst, mod, local_x); i = inst['first_residual']+j
            # The initial lift can already reuse an earlier E*B alias here.
            # Check the frozen source identity now; check the current complete
            # acyclic alias expansion after all source aliases are collected.
            assert normalized(source[i]) == normalized(add((1, var(x)), (-1, prod(var(E), gb))))
            if x in aliases:
                assert aliases[x] == (i, gb)
            aliases[x] = (i, gb)

    alias_values = {}; alias_order = []; alias_visiting = set()
    def expand_alias(x):
        if x in alias_values:
            return alias_values[x]
        assert x not in alias_visiting, ('cyclic current alias', x)
        alias_visiting.add(x)
        i, base = aliases[x]
        c = rows[i].get((x,), 0)
        assert c, ('current alias lost its constant leading coefficient', i, x)
        rhs = add((-Fraction(1, c), rows[i]), (1, var(x)))
        assert x not in op.vars_in(rhs), ('current alias has nonlinear self-use', i, x)
        value = {}
        for mon, coeff in rhs.items():
            term = {(): coeff}
            for z in mon:
                term = prod(term, expand_alias(z) if z in aliases else var(z))
            op.poly_add(value, term)
        assert value == prod(var(E), base), ('current alias does not expand to E*B', i, x)
        alias_visiting.remove(x)
        alias_values[x] = value; alias_order.append(x)
        return value
    for x in sorted(aliases, key=lambda z: aliases[z][0]):
        expand_alias(x)

    incidence = defaultdict(set)
    for i, rr in enumerate(rows):
        for t in op.vars_in(rr):
            incidence[t].add(i)
    defs = {x: i for x, (i, _) in aliases.items()}
    ordered_gates = []
    seen = set()
    def visit(t):
        if t not in gate_defs or t in seen:
            return
        i, pair = gate_defs[t]
        assert_same(i, add((1, var(t)), (-1, prod(*(var(j) for j in pair)))))
        for z in pair:
            visit(z)
        defs[t] = i; seen.add(t); ordered_gates.append(t)
    specs = []; pair_records = []; first = []; lows = {}; odds = {}; squares = {}
    nextvar = allocated
    def fresh(spec):
        nonlocal nextvar
        spec['variable'] = nextvar; nextvar += 1; specs.append(spec)
        return spec['variable']
    norm_vars = [x[1] for x in bm['construction_log'] if x[0] == 'variable' and x[2] == 'normalized bottom norm']
    norm_rows = [x[1] for x in bm['construction_log'] if x[0] == 'equation' and x[2] == 'fused normalized pair']
    plan = [p for p in bm['norm_tree'] if p['type'] == 'pair']
    assert len(norm_vars) == len(norm_rows) == len(plan)
    assert len(plan)*2+2 == bm['free']
    first_local, = [x[1] for x in bm['construction_log'] if x[0] == 'variable' and x[2] == 'constant leaf norm']
    first_row, = [x[1] for x in bm['construction_log'] if x[0] == 'equation' and x[2] == 'fused constant leaf norm']
    for inst in instances:
        if inst['module'] != 'q_batch41':
            continue
        gv = lambda t: global_var(inst, bm, t)
        r, f = gv(0), gv(first_local)
        assert gv(1) == E
        fi = inst['first_residual']+first_row
        assert_same(fi, add((1, prod(var(r), var(f))), (-1, var(r)), (-1, prod(var(E), var(E)))))
        first.append([r, f, fi])
        for local_n, local_i, entry in zip(norm_vars, norm_rows, plan):
            i, n = inst['first_residual']+local_i, gv(local_n)
            pp = global_row(inst, bm, bm['residuals'][local_i])
            assert normalized(pp) == normalized(source[i])
            x, t = (gv(z) for z in entry['tests'])
            assert x in aliases
            B = aliases[x][1]
            p, = [j for mon in pp if n in mon for j in mon if j != n]
            expected_source = add((1, prod(var(p), var(n))), (-1, prod(var(x), var(x))),
                                  (-1, prod(var(r), var(t), var(t))))
            assert normalized(pp) == normalized(expected_source)
            for z in op.vars_in(rows[i]):
                visit(z)
            if entry['order'] == 1:
                want = add((1, var(p)), (-1, prod(var(r), var(r))))
                found = [j for j in range(inst['first_residual'], inst['first_residual']+len(bm['residuals']))
                         if normalized(rows[j]) == normalized(want)]
                assert len(found) == 1
                lows[r, p] = [r, p, found[0]]; o = r
            else:
                if (r, p) not in odds:
                    odds[r, p] = fresh({'kind': 'odd_power', 'factor': r, 'even': p})
                o = odds[r, p]
            key = tuple(sorted(op.square(B).items()))
            if key not in squares:
                squares[key] = fresh({'kind': 'square', 'base': enc(B)})
            q = squares[key]
            pair_records.append(dict(row=i, factor=r, first=f, even=p, odd=o, norm=n,
                                     test=t, base=enc(B), square=q))

    # Delete only the largest closed private subset. Any definition with an
    # outside consumer stays, and its dependency definitions stay as needed.
    pair_ids = {p['row'] for p in pair_records}
    removed = set(defs)
    while True:
        selected = pair_ids | {defs[t] for t in removed}
        bad = {t for t in removed if not incidence[t] <= selected}
        if not bad:
            break
        removed -= bad
    old_defs = [[aliases[x][0], x] for x in alias_order]
    old_defs += [[defs[t], t] for t in ordered_gates]
    data = dict(root=theta, error=E, root_row=root_i, first_leaves=first,
                definitions=old_defs, removed=sorted(removed), low_powers=list(lows.values()),
                new_variables=specs, pairs=pair_records)
    patches = {i: {} for i in pair_ids | {defs[t] for t in removed}}
    for pair in pair_records:
        F, N, U, Q, O = (var(pair[k]) for k in ('first', 'norm', 'test', 'square', 'odd'))
        patches[pair['row']] = add((1, prod(O, N)), (-1, prod(F, Q)), (1, Q), (-1, prod(U, U)))
    for k, spec in enumerate(specs):
        V = var(spec['variable'])
        if spec['kind'] == 'odd_power':
            rr = add((1, prod(var(spec['factor']), V)), (-1, var(spec['even'])))
        else:
            rr = add((1, V), (-1, op.square(decode(spec['base']))))
        patches[len(rows)+k] = rr
    for i, rr in list(patches.items()):
        patches[i] = dict(normalized(rr)) if rr else {}
    event = {'kind': 'batch_absorb', 'data': data, 'patches': [[i, enc(rr)] for i, rr in sorted(patches.items())]}
    report = dict(pairs=len(pair_records), batches=len(first), old_definitions=len(defs),
                  aliases=len(aliases), aliases_removed=len(removed & aliases.keys()),
                  lift_gates_removed=len(removed - aliases.keys()), new_odd_powers=len(odds),
                  new_squares=len(squares), net_raw_variables_removed=len(removed)-len(specs),
                  retained_aliases=[dict(variable=x, outside=sorted(incidence[x]-pair_ids-{defs[z] for z in removed}))
                                    for x in aliases if x not in removed])
    if a.diagnostic_only:
        a.output.mkdir(parents=True, exist_ok=True)
        (a.output/'event.json').write_text(json.dumps(event, separators=(',', ':'))+'\n')
    else:
        for i, rr in sorted(patches.items()):
            if i == len(rows):
                rows.append(rr)
            else:
                rows[i] = rr
        report.update(export(a.output, a.parent/'source-residuals.jsonl.gz', rows,
                             records+[event], nextvar, {'batch_absorb': report.copy()}))
    (a.output/'batch-absorb-report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
