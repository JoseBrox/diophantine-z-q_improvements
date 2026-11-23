#!/usr/bin/env python3
"""Remove private field numerators from a common quadratic norm quotient.

The coefficient transformation is exact under the nonzero R and reference
field already enforced by the source.  No universality assertion is added.
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


def build(m, root=ROOT):
    path = root / f'undecidability/coefficients/jones1980_scalar_rechart/scalar_rechart_m{m}_quadrics.json'
    source_bytes = path.read_bytes()
    old = json.loads(source_bytes)
    maps = json.loads((root / f'computation/variable_reductions_v82/general/quartic{m}/maps.json').read_text())
    labels = {int(k): v for k, v in maps['source_labels'].items()}
    names = old['variable_names']
    blocks = old['ordinary_integer_inputs'] + ['i_reciprocal']
    assert len(blocks) == 12

    def slot(b, j):
        n = f'int_{b}_{labels[j]}'
        assert n in names
        return n

    def z(b, j):
        return sp.Symbol(slot(b, j))

    def expr(row):
        return sp.expand(sum(sp.sympify(t['coefficient']) *
                             sp.prod(sp.Symbol(names[j-1]) for j in t['monomial'])
                             for t in row['terms']))

    K0, K1 = (sp.Symbol('common_scalar_Z_square_' + part) for part in ('real', 'imag'))
    Q0, Q1 = z('b', 64), 2*z('b', 65)
    A, B, C = (sp.Symbol('common_scalar_norm_' + s) for s in ('constant', 'linear', 'quadratic'))
    removed = {slot(b, j) for b in blocks for j in (109, 110)}
    affected = {'v82.scalar.field.0', 'v82.scalar.field.1', 'v82.scalar.partial_trace'}
    removed_rows = []
    rows = []
    for row in old['residuals']:
        n = row['name']
        if n.startswith('integer.') and n.split('.', 2)[2] in affected:
            removed_rows.append(n)
            continue
        e = expr(row)
        assert not set(map(str, e.free_symbols)) & removed, (n, e)
        rows.append((n, e))
    assert len(removed_rows) == 36
    rows.extend([
        ('scalar_norm.common.constant', 2*K0*A - K0*K0 + 2*K1*K1),
        ('scalar_norm.common.linear', 2*K0*B - 2*K0*Q0 + 4*K1*Q1),
        ('scalar_norm.common.quadratic', 2*K0*C - Q0*Q0 + 2*Q1*Q1),
    ])
    for b in blocks:
        R, R2, tau = (z(b, j) for j in (113, 112, 111))
        rows.append((f'scalar_norm.{b}.quotient', R*tau - A - B*R - C*R2))
    final_names = [n for n in names if n not in removed] + list(map(str, (A, B, C)))
    residuals = sparse_rows(rows, list(map(sp.Symbol, final_names)),
                            list(map(sp.Symbol, old['parameters'])))
    assert len(final_names) == (1122 if m == 163 else 1302)
    assert len(residuals) == (966 if m == 163 else 1122)
    result = dict(old)
    result.update({
        'variables': len(final_names), 'variable_names': final_names, 'residuals': residuals,
        'scalar_norm_predecessor_sha256': hashlib.sha256(source_bytes).hexdigest(),
        'scalar_norm_removed_coordinates': sorted(removed),
        'scalar_norm_added_coordinates': list(map(str, (A, B, C))),
        'scalar_norm_removed_rows': removed_rows,
        'scalar_norm_recovery': 'Jhat_i = Q + K/R_i; Q=f^2; K=Z^2; A=N(K)/Tr(K), B=Tr(K*conj(Q))/Tr(K), C=N(Q)/Tr(K)',
        'scalar_norm_status': 'exact quadratic equivalence with automatic common trace guard; U_em remains unverified',
        'scalar_norm_coordinate_saving': 21,
        'scalar_norm_row_saving': 21,
        'scalar_norm_pell_core_applied': False,
    })
    return result


def main():
    out = ROOT / 'undecidability/coefficients/jones1980_scalar_norm'
    out.mkdir(exist_ok=True)
    for m in (163, 179):
        data = build(m)
        path = out / f'scalar_norm_m{m}_quadrics.json'
        path.write_text(json.dumps(data, sort_keys=True, separators=(',', ':')) + '\n')
        cert = {
            'interface_coordinates': m,
            'variables': data['variables'],
            'quadratic_rows': len(data['residuals']),
            'degree': 4,
            'table_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'predecessor_sha256': data['scalar_norm_predecessor_sha256'],
            'integer_input_blocks': 12,
            'private_coordinates_removed': 24,
            'common_coordinates_added': 3,
            'coordinate_saving': 21,
            'quadratic_row_saving': 21,
            'source_universality_hypothesis': 'U_em',
            'source_universality_verified': False,
            'unconditional_undecidability_claim': False,
            'retained_arithmetic_interfaces': True,
            'new_abc_assumption': False,
            'pell_core_reduction_already_included': False,
            'proof': 'undecidability/papers/scalar_norm_compression.tex',
            'independent_verifier': 'undecidability/verify_scalar_norm_compression.py',
        }
        (out / f'scalar_norm_m{m}_certificate.json').write_text(json.dumps(cert, sort_keys=True, indent=2) + '\n')
        print({'m': m, 'N': data['variables'], 'rows': len(data['residuals']), 'sha256': cert['table_sha256']})


if __name__ == '__main__':
    main()
