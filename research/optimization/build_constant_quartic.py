#!/usr/bin/env python3
"""Remove the remaining constant chain, with exact coefficients in Z[M].

M denotes the fixed integer 3**(2**26), not another variable.  The output
does not expand this integer into decimal digits.  The only mathematical
change is substitution of uniquely determined constants into quadratics.
"""
from collections import defaultdict
import argparse
import gzip
import hashlib
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--parent', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    rows = [{tuple(m): c for c, m in row} for row in json.loads(
        gzip.decompress((args.parent / 'residuals.json.gz').read_bytes()))]
    old_map = json.loads((args.parent / 'variable-map.json').read_text())
    loc = {old: new for new, old in enumerate(old_map)}
    chain = [loc[k] for k in range(11, 26)]
    assert rows[0] == {(): 3**1024, (chain[0],): -1}
    for k in range(1, 15):
        assert rows[k] == {(chain[k-1], chain[k-1]): -1, (chain[k],): 1}
    anchor_r, anchor_D, au, av, aw = [loc[k] for k in range(16794, 16799)]
    D_row = {(anchor_D,): 1, (chain[-1], chain[-1]): -1}
    D_ids = [i for i, r in enumerate(rows) if r == D_row]
    assert len(D_ids) == 1
    D_id = D_ids[0]
    anchor_row = {(au, au): 1, (av, av): 6, (aw, aw): -2,
                  (anchor_r, anchor_r): -3, (anchor_D, anchor_D): 2}
    anchor_ids = [i for i, r in enumerate(rows) if r == anchor_row]
    assert len(anchor_ids) == 1
    anchor_id = anchor_ids[0]
    deleted_rows = set(range(15)) | {D_id}
    deleted_vars = set(chain) | {anchor_D}
    for i, row in enumerate(rows):
        for mon in row:
            if deleted_vars.intersection(mon):
                assert i in deleted_rows or (i == anchor_id and mon == (anchor_D, anchor_D))
    active = [v for v in range(len(old_map)) if v not in deleted_vars]
    remap = {v: i for i, v in enumerate(active)}
    formal_rows = []
    for i, row in enumerate(rows):
        if i in deleted_rows:
            continue
        terms = []
        for mon, coefficient in row.items():
            if i == anchor_id and mon == (anchor_D, anchor_D):
                terms.append([coefficient, 1, []])
            else:
                terms.append([coefficient, 0, sorted(remap[v] for v in mon)])
        formal_rows.append(terms)
    # Coefficients are polynomials in the fixed constant M.  This is an
    # exact coefficient table, although the enormous integer M is symbolic.
    table = defaultdict(int)
    for row in formal_rows:
        for ca, ea, ma in row:
            for cb, eb, mb in row:
                table[(tuple(sorted(ma + mb)), ea + eb)] += ca * cb
    table = {key: c for key, c in table.items() if c}
    assert len(active) == 12449
    assert {v for (m, _), c in table.items() for v in m} == set(range(len(active)))
    assert max(len(m) for m, _ in table) == 4
    assert table[((), 2)] == 4 and table.get(((), 1), 0) == 0
    constant_part = table.get(((), 0), 0)
    assert 0 <= constant_part < 2**3247
    # Every other coefficient has absolute value at most
    # 2**3247 + 24*M, strictly smaller than 4*M**2 + constant_part.
    assert all(abs(c) < 2**3247 for (m, e), c in table.items() if e == 0)
    assert all(abs(c) <= 24 for (m, e), c in table.items() if e == 1)
    assert all(m == () for (m, e), c in table.items() if e == 2)
    # A private anchor fourth power has coefficient exactly one.
    assert table[((remap[au],)*4, 0)] == 1
    obj = {
        'format': 'integer-quartic-with-one-fixed-power-constant-v1',
        'constant_M': {'base': 3, 'exponent': 2**26, 'is_a_variable': False},
        'parent': 'quartic-anchor-packed-large',
        'parent_residuals_sha256': hashlib.sha256((args.parent/'residuals.json.gz').read_bytes()).hexdigest(),
        'variables': len(active), 'variable_map_to_parent': active,
        'deleted_parent_variables': sorted(deleted_vars),
        'deleted_parent_rows': sorted(deleted_rows),
        'parent_anchor_row': anchor_id,
        'residuals': formal_rows,
        'coefficient_table': [[c, e, list(m)] for (m, e), c in sorted(table.items())],
    }
    report = {
        'status': 'CANDIDATE: independent checker required',
        'total_variables': len(active), 'existential_witnesses': len(active)-1,
        'degree': 4, 'residuals': len(formal_rows),
        'monomials': len({m for m, e in table}),
        'variables_removed': len(deleted_vars),
        'max_abs_coefficient': {'power_term': {'coefficient': 4, 'base': 3, 'exponent': 2**27}, 'addend': constant_part},
        'coefficient_bit_bound': 2**28+3,
        'constant_integer_not_expanded_to_decimal': True,
        'scope': 'Exact constant substitution and quartic expansion over Z[M]. No new arithmetic assertion.'
    }
    args.output.mkdir(exist_ok=True, parents=True)
    raw = (json.dumps(obj, separators=(',', ':'))+'\n').encode()
    (args.output/'polynomial-symbolic.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    report['uncompressed_sha256'] = hashlib.sha256(raw).hexdigest()
    (args.output/'construction-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
