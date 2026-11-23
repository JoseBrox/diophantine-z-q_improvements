#!/usr/bin/env python3
"""Factor the private scalar normalizers out of the common point chart.

This is an exact quadratic-table transformation.  Its rational-solution
interpretation uses the nonvanishing already proved for the predecessor;
it does not prove the unresolved source universality hypothesis U_em.
"""
from __future__ import annotations
from pathlib import Path
import hashlib
import json
import sys
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'undecidability/code'))
from quadratic_utils import sparse_rows


def add(a, b):
    return tuple(sp.expand(x + y) for x, y in zip(a, b))


def sub(a, b):
    return tuple(sp.expand(x - y) for x, y in zip(a, b))


def scale(a, b):
    return tuple(sp.expand(x * b) for x in a)


def mul(a, b):
    return (sp.expand(a[0]*b[0] + 2*a[1]*b[1]),
            sp.expand(a[0]*b[1] + a[1]*b[0]))


def build(m, root=ROOT):
    source = root / f'undecidability/coefficients/jones1980_global_gauge/global_gauge_m{m}_quadrics.json'
    source_bytes = source.read_bytes()
    old = json.loads(source_bytes)
    maps = json.loads((root / f'computation/variable_reductions_v82/general/quartic{m}/maps.json').read_text())
    labels = {int(k): v for k, v in maps['source_labels'].items()}
    oldnames = old['variable_names']
    blocks = old['ordinary_integer_inputs'] + ['i_reciprocal']
    assert len(blocks) == 12

    def slot(b, j):
        candidate = f'int_{b}_{labels[j]}'
        return candidate if candidate in oldnames else f'int_b_{labels[j]}'

    def z(b, j):
        return sp.Symbol(slot(b, j))

    def field(b, j):
        return (z(b, j), z(b, j+1))

    def expression(row):
        return sp.expand(sum(sp.sympify(t['coefficient']) *
                             sp.prod(sp.Symbol(oldnames[j-1]) for j in t['monomial'])
                             for t in row['terms']))

    p = tuple(sp.Symbol('common_scalar_x_' + suffix) for suffix in ('real', 'imag'))
    K = tuple(sp.Symbol('common_scalar_Z_square_' + suffix) for suffix in ('real', 'imag'))
    r = (tuple(sp.Symbol('common_scalar_r_' + suffix) for suffix in ('real', 'imag'))
         if m == 163 else field('b', 190))
    U, V, W, Z = (field('b', j) for j in (182, 184, 186, 102))
    S = field('b', 17)  # Source X17/c, with weight c, is this stored field.
    D = (sp.Integer(11), sp.Integer(-6))
    M = scale(add(scale(S, 2), W), -1)
    f2 = (z('b', 64), 2*z('b', 65))
    r2 = field('b', 194)
    if m == 179:
        r2 = scale(r2, z('b', 400))

    removed_sources = [192, 193] + ([190, 191] if m == 163 else [])
    deleted = {slot(b, j) for b in blocks for j in removed_sources}
    if m == 179:
        deleted.update(slot(b, 114) for b in blocks)
    native_sources = [11, 12, 13, 14, 104, 105, 106, 107, 108]
    native_row_names = {'v82.scalar.' + n for n in
                        ('inverse', 'input', 'p2', 'q2', 'first', 'middle', 'second')}
    removed_row_prefixes = tuple('v82.point.' + x for x in ('product.', 'r.', 'sum.', 'pair.', 'r2.'))
    removed_rows = []
    modified_rows = []
    rows = []
    for row in old['residuals']:
        n = row['name']
        e = expression(row)
        if n.startswith('integer.'):
            _, label, local = n.split('.', 2)
            b = 'i_reciprocal' if label == 'i' else label
            if m == 179 and local == 'unit.R_inverse':
                removed_rows.append(n)
                continue
            if local.startswith(removed_row_prefixes):
                removed_rows.append(n)
                continue
            if local.startswith('v82.scalar.field.'):
                component = int(local.rsplit('.', 1)[1])
                e = sub(scale(sub(field(b, 109), f2), z(b, 113)), K)[component]
                modified_rows.append(n)
            elif local in ('new.aggregate', 'new.aggregate_shift'):
                component = 0 if local == 'new.aggregate' else 1
                old_part = z(b, 192+component)
                if m == 179:
                    old_part *= z(b, 114)
                new_part = z(b, 113)*p[component] if m == 163 else p[component]
                e = sp.expand(e - old_part + new_part)
                modified_rows.append(n)
            elif m == 179 and local in native_row_names:
                # All nine homogeneous pole coordinates now denote their
                # physical values, instead of those values divided by R_i.
                if local == 'v82.scalar.inverse':
                    e = z(b, 111)*z(b, 104) - z(b, 112)**2
                elif local == 'v82.scalar.input':
                    e = z(b, 104)*z(b, 105) - z(b, 112) - 9792*z(b, 113)
                modified_rows.append(n)
        assert not (set(map(str, e.free_symbols)) & deleted), (n, e)
        rows.append((n, e))

    common = [
        ('Z_square', sub(K, mul(Z, Z))),
        ('product', sub(mul(U, V), mul(K, p))),
        ('r', sub(mul(p, W), r)),
        ('sum', add(mul(r, sub(sub(add(U, V), W), scale(S, 4))), mul(D, K))),
        ('pair', sub(add(mul(U, V), mul(W, add(U, V))), mul(M, M))),
        ('r_square', sub(r2, mul(r, r))),
    ]
    for n, pair in common:
        for j, e in enumerate(pair):
            rows.append((f'scalar_common.{n}.{j}', e))

    added = list(map(str, (*p, *K, *r))) if m == 163 else list(map(str, (*p, *K)))
    names = [n for n in oldnames if n not in deleted] + added
    assert len(names) == len(set(names))
    residuals = sparse_rows(rows, list(map(sp.Symbol, names)), list(map(sp.Symbol, old['parameters'])))
    assert len(names) == (1143 if m == 163 else 1323), (m, len(names))
    assert len(residuals) == (987 if m == 163 else 1143), (m, len(residuals))
    if m == 179:
        native_names = {slot(b, j) for b in blocks for j in native_sources}
        for row in old['residuals']:
            touched = {oldnames[j-1] for t in row['terms'] for j in t['monomial']}
            if touched & native_names:
                assert row['name'].split('.', 2)[2] in native_row_names
    result = dict(old)
    result.update({
        'variables': len(names), 'variable_names': names, 'residuals': residuals,
        'scalar_rechart_predecessor_sha256': hashlib.sha256(source_bytes).hexdigest(),
        'scalar_rechart_removed_coordinates': sorted(deleted),
        'scalar_rechart_added_coordinates': added,
        'scalar_rechart_removed_rows': removed_rows,
        'scalar_rechart_modified_rows': modified_rows,
        'scalar_rechart_status': 'exact equivalence under the retained nonvanishing; U_em remains unverified',
        'scalar_rechart_private_point_recovery': 'Pstar_i=R_i*p; source190_i=R_i*r for m163 and r for m179',
        'scalar_rechart_native_pole_sources_reweighted': native_sources if m == 179 else [],
        'scalar_rechart_native_pole_recovery': 'old stored native coordinate = new coordinate/R_i' if m == 179 else 'unchanged',
        'scalar_rechart_pell_core_applied': False,
    })
    return result


def main():
    out = ROOT / 'undecidability/coefficients/jones1980_scalar_rechart'
    out.mkdir(exist_ok=True)
    for m in (163, 179):
        d = build(m)
        p = out / f'scalar_rechart_m{m}_quadrics.json'
        p.write_text(json.dumps(d, sort_keys=True, separators=(',', ':')) + '\n')
        cert = {
            'interface_coordinates': m, 'variables': d['variables'],
            'quadratic_rows': len(d['residuals']), 'degree': 4,
            'table_sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
            'predecessor_sha256': d['scalar_rechart_predecessor_sha256'],
            'coordinates_removed': len(d['scalar_rechart_removed_coordinates']),
            'coordinates_added': len(d['scalar_rechart_added_coordinates']),
            'coordinate_saving': 42 if m == 163 else 32,
            'source_universality_hypothesis': 'U_em',
            'source_universality_verified': False,
            'unconditional_undecidability_claim': False,
            'retained_arithmetic_interfaces': True, 'new_abc_assumption': False,
            'pell_core_reduction_already_included': False,
            'proof': 'undecidability/papers/scalar_rechart_quartic_checkpoint.tex',
            'independent_verifier': 'undecidability/verify_scalar_rechart.py',
        }
        (out / f'scalar_rechart_m{m}_certificate.json').write_text(json.dumps(cert, indent=2, sort_keys=True) + '\n')
        print({'m': m, 'N': d['variables'], 'rows': len(d['residuals']), 'sha256': cert['table_sha256']})


if __name__ == '__main__':
    main()
