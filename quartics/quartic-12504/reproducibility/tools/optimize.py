"""Minimize witnesses by checked quadratic-preserving substitutions.

This is an untrusted producer. The existing independent certificate checker
verifies every substitution and the complete resulting quartic expansion.
"""
from collections import Counter, defaultdict
from pathlib import Path
import argparse, gzip, hashlib, json, math, random, shutil, sys, time

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / 'quartic-search-20261105'
import polynomial_ops as s

def enc(r): return [[c, list(m)] for m, c in r.items()]
def dec(r): return {tuple(m): c for c, m in r}
def raw(obj): return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode('ascii')

def substitute_rational(row, variable, numerator, denominator):
    """Clear one common denominator before collecting integer terms."""
    max_power = max((m.count(variable) for m in row), default=0)
    result = {}
    for m, c in row.items():
        power = m.count(variable)
        term = {tuple(v for v in m if v != variable): c * denominator**(max_power-power)}
        for _ in range(power): term = s.product(term, numerator)
        s.poly_add(result, term)
    return dict(s.primitive(result)) if result else {}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--parent', type=Path, default=OLD / 'quartic-108585')
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--max-terms', type=int, default=32)
    p.add_argument('--rounds', type=int, default=20)
    p.add_argument('--rational', action='store_true')
    p.add_argument('--initial-lift', action='store_true', help='Start before the earlier monomial-reduction transformations')
    p.add_argument('--row-combine', action='store_true', help='Cancel proportional quadratic parts to expose linear equations')
    p.add_argument('--gaussian', action='store_true', help='Sparse elimination of quadratic monomials to expose linear consequences')
    p.add_argument('--seed', type=int, default=0)
    p.add_argument('--row-order', choices=['short','reverse','random'], default='short')
    p.add_argument('--pivot-score', choices=['terms','incidence'], default='terms')
    p.add_argument('--gaussian-order', choices=['rare','common','lex'], default='rare')
    a = p.parse_args()
    start = time.monotonic()
    a.output.mkdir(exist_ok=False)
    rows = [dec(r) for r in json.loads(gzip.decompress((a.parent / 'candidate-rows.json.gz').read_bytes()))]
    records = [json.loads(line) for line in gzip.decompress((a.parent / 'certificate.jsonl.gz').read_bytes()).splitlines()]
    allocated = records[-1]['allocated_variables']
    records = [r for r in records if r['kind'] not in ('weights', 'final')]
    if a.initial_lift:
        records = records[:1]
        rows = [dec(r) for r in records[0]['rows']]
        allocated = records[0]['source_variables'] + len(records[0]['gates'])
    parent_steps = len(records) - 1
    incidence = defaultdict(set)
    poly = {}
    squares = []
    for i, r in enumerate(rows):
        for v in s.vars_in(r): incidence[v].add(i)
        squares.append(s.square(r))
        s.poly_add(poly, squares[-1])
    limit = 2**80
    assert max(map(abs, poly.values())) < limit
    initial_variables = sum(bool(ids) for ids in incidence.values())
    reasons = Counter()
    rng = random.Random(a.seed)
    for sweep in range(a.rounds):
        accepted = 0
        combined = 0
        if a.row_combine:
            groups = defaultdict(list)
            for i, r in enumerate(rows):
                high = {m: c for m, c in r.items() if len(m) == 2}
                if high: groups[s.primitive(high)].append(i)
            for signature, ids in groups.items():
                if len(ids) < 2: continue
                j = min(ids, key=lambda k: (len(rows[k]), max(map(abs, rows[k].values())), k))
                anchor = signature[0][0]
                for i in ids:
                    if i == j: continue
                    ac, bc = rows[j][anchor], -rows[i][anchor]
                    g = math.gcd(ac, bc)
                    ac //= g; bc //= g
                    new = {}
                    s.poly_add(new, rows[i], ac); s.poly_add(new, rows[j], bc)
                    new = dict(s.primitive(new)) if new else {}
                    assert all(len(m) < 2 for m in new)
                    new_square = s.square(new)
                    delta = {m: -c for m, c in squares[i].items()}
                    s.poly_add(delta, new_square)
                    if len(new) > a.max_terms or any(abs(poly.get(m, 0)+c) >= limit for m,c in delta.items()):
                        reasons['row_combine_bound'] += 1
                        continue
                    records.append({'kind':'linear','data':{'target':i,'other':j,'a':ac,'b':bc},
                                    'patches':[[i,enc(new)]]})
                    s.poly_add(poly, delta)
                    for v in s.vars_in(rows[i]): incidence[v].remove(i)
                    rows[i] = new; squares[i] = new_square
                    for v in s.vars_in(new): incidence[v].add(i)
                    combined += 1
        if a.gaussian:
            frequency_q = Counter(m for row in rows for m in row if len(m)==2)
            qkey = {'rare':lambda m:(frequency_q[m],m),
                    'common':lambda m:(-frequency_q[m],m), 'lex':lambda m:m}[a.gaussian_order]
            rank = {m: k for k,m in enumerate(sorted(frequency_q, key=qkey))}
            pivots = {}
            order = sorted(range(len(rows)), key=lambda i:(sum(len(m)==2 for m in rows[i]),len(rows[i]),i))
            for i in order:
                while True:
                    high = [m for m in rows[i] if len(m)==2]
                    if not high: break
                    leading = min(high, key=rank.__getitem__)
                    if leading not in pivots:
                        pivots[leading] = i
                        break
                    j = pivots[leading]
                    ac, bc = rows[j][leading], -rows[i][leading]
                    g = math.gcd(ac, bc); ac //= g; bc //= g
                    new = {}
                    s.poly_add(new, rows[i], ac); s.poly_add(new, rows[j], bc)
                    new = dict(s.primitive(new)) if new else {}
                    assert leading not in new
                    if len(new)>a.max_terms:
                        reasons['gaussian_term_cap'] += 1
                        break
                    new_square = s.square(new)
                    delta = {m:-c for m,c in squares[i].items()}
                    s.poly_add(delta,new_square)
                    if any(abs(poly.get(m,0)+c)>=limit for m,c in delta.items()):
                        reasons['gaussian_coefficient_bound'] += 1
                        break
                    records.append({'kind':'linear','data':{'target':i,'other':j,'a':ac,'b':bc},
                                    'patches':[[i,enc(new)]]})
                    s.poly_add(poly,delta)
                    for v in s.vars_in(rows[i]): incidence[v].remove(i)
                    rows[i] = new; squares[i] = new_square
                    for v in s.vars_in(new): incidence[v].add(i)
                    combined += 1
        elimination_order = list(range(len(rows)))
        if a.row_order == 'random': rng.shuffle(elimination_order)
        elif a.row_order == 'reverse': elimination_order.reverse()
        elimination_order.sort(key=lambda i:len(rows[i]))
        for i in elimination_order:
            row = rows[i]
            if not row: continue
            best = None
            for m, c in row.items():
                if len(m) != 1 or m[0] == 0: continue
                v = m[0]
                if any(v in n for n in row if n != m): continue
                if not a.rational and any(d % c for n, d in row.items() if n != m):
                    reasons['noninteger_replacement'] += 1
                    continue
                replacement = {n: -d * (1 if c > 0 else -1) for n, d in row.items() if n != m}
                denominator = abs(c)
                common = math.gcd(denominator, *replacement.values())
                replacement = {n: d // common for n, d in replacement.items()}
                denominator //= common
                affected = sorted(incidence[v] - {i})
                degree = max(map(len, replacement), default=0)
                if degree > 1 and any(any(v in n and len(n) > 1 for n in rows[j]) for j in affected):
                    reasons['degree_obstruction'] += 1
                    continue
                changes = []
                delta = {n: -d for n, d in squares[i].items()}
                for j in affected:
                    new = substitute_rational(rows[j], v, replacement, denominator)
                    if len(new) > a.max_terms:
                        reasons['row_term_cap'] += 1
                        break
                    if any(len(n) > 2 for n in new):
                        reasons['degree_obstruction'] += 1
                        break
                    new_square = s.square(new)
                    s.poly_add(delta, squares[j], -1)
                    s.poly_add(delta, new_square)
                    changes.append((j, new, new_square))
                else:
                    if any(abs(poly.get(n, 0) + d) >= limit for n, d in delta.items()):
                        reasons['coefficient_bound'] += 1
                        continue
                    term_delta = sum(bool(poly.get(n, 0) + d) - (n in poly) for n, d in delta.items())
                    score = (term_delta, len(affected), degree, len(replacement), v)
                    if a.pivot_score == 'incidence': score = (len(affected),degree,len(replacement),term_delta,v)
                    if best is None or score < best[0]:
                        best = (score, v, replacement, denominator, affected, changes, delta)
            if best is None: continue
            score, v, replacement, denominator, affected, changes, delta = best
            patches = [[j, enc(new)] for j, new, sq in changes] + [[i, []]]
            records.append({'kind': 'eliminate', 'data': {
                'row': i, 'variable': v, 'replacement': enc(replacement),
                'affected': affected, 'denominator': denominator, 'variable_search': True,
            }, 'patches': patches})
            s.poly_add(poly, delta)
            for j, new, square in changes + [(i, {}, {})]:
                for w in s.vars_in(rows[j]): incidence[w].remove(j)
                rows[j] = new
                squares[j] = square
                for w in s.vars_in(new): incidence[w].add(j)
            assert not incidence[v]
            accepted += 1
        print(json.dumps({'sweep': sweep, 'eliminated': accepted, 'linear_combinations': combined,
                          'variables': sum(bool(ids) for ids in incidence.values()),
                          'monomials': len(poly), 'seconds': round(time.monotonic() - start, 2)}), flush=True)
        if not accepted and not combined: break

    frequency = Counter(v for m in poly for v in m)
    active = [0] + sorted(set(frequency) - {0}, key=lambda v: (-frequency[v], v))
    assert set(active) == {v for v, ids in incidence.items() if ids}
    mapping = {v: i for i, v in enumerate(active)}
    compact = [{tuple(sorted(mapping[v] for v in m)): c for m, c in r.items()} for r in rows if r]
    final_poly = {}
    for r in compact: s.poly_add(final_poly, s.square(r))
    report = {'witnesses': len(active)-1, 'variables': len(active),
              'rows': len(compact), 'monomials': len(final_poly),
              'degree': max(map(len, final_poly)),
              'max_abs_coefficient': max(map(abs, final_poly.values())),
              'allocated_variables': allocated, 'initial_variables': initial_variables,
              'new_operations': len(records)-1-parent_steps,
              'new_eliminations': sum(r['kind']=='eliminate' for r in records[1+parent_steps:]),
              'parent': str(a.parent), 'max_row_terms': a.max_terms,
              'rational_eliminations_enabled': a.rational,
              'started_from_initial_lift': a.initial_lift,
              'combined_proportional_quadratic_parts': a.row_combine,
              'sparse_quadratic_elimination': a.gaussian,
              'seed':a.seed, 'row_order':a.row_order, 'pivot_score':a.pivot_score,
              'gaussian_order':a.gaussian_order, 'sweeps_run':sweep+1,
              'stopped_at_fixed_point':not (accepted or combined),
              'rejection_counts': dict(reasons), 'seconds': round(time.monotonic()-start, 3),
              'status': 'CANDIDATE: independent certificate verification pending'}
    assert report['degree'] == 4 and report['max_abs_coefficient'] < limit
    records += [{'kind': 'weights', 'values': [1]*len(rows)},
                {'kind': 'final', 'allocated_variables': allocated, 'report': report,
                 'rows_sha256': hashlib.sha256(raw([enc(r) for r in rows])).hexdigest()}]
    shutil.copyfile(a.parent/'source-residuals.jsonl.gz', a.output/'source-residuals.jsonl.gz')
    for name, content in [('candidate-rows.json.gz', raw([enc(r) for r in rows])),
                          ('residuals.json.gz', raw([enc(r) for r in compact])),
                          ('certificate.jsonl.gz', b''.join(raw(r)+b'\n' for r in records))]:
        (a.output/name).write_bytes(gzip.compress(content, compresslevel=1, mtime=0))
    (a.output/'variable-map.json').write_bytes(raw(active)+b'\n')
    (a.output/'weights.json').write_bytes(raw([1]*len(compact))+b'\n')
    expanded = b'# coefficient followed by repeated variable indices; input is variable 0\n' + b''.join(
        (' '.join(map(str, (c, *m)))+'\n').encode('ascii') for m, c in sorted(final_poly.items()))
    (a.output/'polynomial.expanded.txt').write_bytes(expanded)
    (a.output/'polynomial.expanded.txt.gz').write_bytes(gzip.compress(expanded, compresslevel=1, mtime=0))
    (a.output/'producer-report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2), flush=True)

if __name__ == '__main__': main()
