#!/usr/bin/env python3
"""Independently replay scalar norm compression, without importing its builder."""
from pathlib import Path
import hashlib
import json
import sympy as s

ROOT = Path(__file__).resolve().parents[1]


def expr(row, names):
    return s.expand(sum(s.sympify(t['coefficient']) *
                        s.prod(s.Symbol(names[j-1]) for j in t['monomial'])
                        for t in row['terms']))


def main():
    x, y, u, v, R = s.symbols('x y u v R', nonzero=True)
    # Norm(K+RQ), with K=x+y sqrt(2), Q=u+v sqrt(2).
    assert s.expand((x+R*u)**2-2*(y+R*v)**2 -
                    (x*x-2*y*y + 2*R*(x*u-2*y*v) + R*R*(u*u-2*v*v))) == 0
    reports = []
    for m in (163, 179):
        old_path = ROOT / f'undecidability/coefficients/jones1980_scalar_rechart/scalar_rechart_m{m}_quadrics.json'
        new_path = ROOT / f'undecidability/coefficients/jones1980_scalar_norm/scalar_norm_m{m}_quadrics.json'
        cert_path = ROOT / f'undecidability/coefficients/jones1980_scalar_norm/scalar_norm_m{m}_certificate.json'
        old_bytes, new_bytes = old_path.read_bytes(), new_path.read_bytes()
        old, new = json.loads(old_bytes), json.loads(new_bytes)
        cert = json.loads(cert_path.read_text())
        assert cert['table_sha256'] == hashlib.sha256(new_bytes).hexdigest()
        assert cert['predecessor_sha256'] == hashlib.sha256(old_bytes).hexdigest()
        assert new['scalar_norm_predecessor_sha256'] == cert['predecessor_sha256']
        maps = json.loads((ROOT / f'computation/variable_reductions_v82/general/quartic{m}/maps.json').read_text())
        labels = {int(k): v for k, v in maps['source_labels'].items()}
        blocks = old['ordinary_integer_inputs'] + ['i_reciprocal']
        assert len(blocks) == 12
        def z(b, j):
            return s.Symbol(f'int_{b}_{labels[j]}')
        old_by = {r['name']: expr(r, old['variable_names']) for r in old['residuals']}
        new_by = {r['name']: expr(r, new['variable_names']) for r in new['residuals']}
        removed_vars = {str(z(b, j)) for b in blocks for j in (109, 110)}
        affected = {'v82.scalar.field.0', 'v82.scalar.field.1', 'v82.scalar.partial_trace'}
        removed_rows = {n for n in old_by if n.startswith('integer.') and n.split('.', 2)[2] in affected}
        assert len(removed_rows) == 36
        assert removed_vars == set(new['scalar_norm_removed_coordinates'])
        assert removed_rows == set(new['scalar_norm_removed_rows'])
        assert all(not set(map(str, e.free_symbols)) & removed_vars
                   for n, e in old_by.items() if n not in removed_rows)
        for n, e in old_by.items():
            if n not in removed_rows:
                assert n in new_by and s.expand(new_by[n]-e) == 0, n
        K0, K1 = (s.Symbol('common_scalar_Z_square_' + p) for p in ('real', 'imag'))
        Q0, Q1 = z('b', 64), 2*z('b', 65)
        A, B, C = (s.Symbol('common_scalar_norm_' + p) for p in ('constant', 'linear', 'quadratic'))
        expected = {
            'scalar_norm.common.constant': 2*K0*A-K0*K0+2*K1*K1,
            'scalar_norm.common.linear': 2*K0*B-2*K0*Q0+4*K1*Q1,
            'scalar_norm.common.quadratic': 2*K0*C-Q0*Q0+2*Q1*Q1,
        }
        for b in blocks:
            label = 'i' if b == 'i_reciprocal' else b
            J0, J1, tau, R2, Ri = (z(b, j) for j in (109, 110, 111, 112, 113))
            assert s.expand(old_by[f'integer.{label}.v82.scalar.field.0'] -
                            (Ri*(J0-Q0)-K0)) == 0
            assert s.expand(old_by[f'integer.{label}.v82.scalar.field.1'] -
                            (Ri*(J1-Q1)-K1)) == 0
            assert s.expand(old_by[f'integer.{label}.v82.scalar.partial_trace'] -
                            (2*tau*(J0-Q0)-J0*J0+2*J1*J1)) == 0
            assert s.expand(new_by[f'integer.{label}.unit.R_square'] - (R2-Ri*Ri)) == 0
            expected[f'scalar_norm.{b}.quotient'] = Ri*tau-A-B*Ri-C*R2
        for name, e in expected.items():
            assert name in new_by and s.expand(new_by[name]-e) == 0, name
        assert set(new_by) == (set(old_by)-removed_rows) | set(expected)
        # The literal common square identities are preserved.
        assert s.expand(new_by['scalar_common.Z_square.0']-
                        (K0-z('b',102)**2-2*z('b',103)**2)) == 0
        assert s.expand(new_by['scalar_common.Z_square.1']-
                        (K1-2*z('b',102)*z('b',103))) == 0
        assert s.expand(new_by['integer.b.testSquare.40.0.0.definition']-
                        (z('b',15)*z('b',16)-z('b',65))) == 0
        assert s.expand(new_by['integer.b.testSquare.40.0.1.definition']-
                        (z('b',15)**2+2*z('b',16)**2-z('b',64))) == 0
        for j in (102,103,109,110,111):
            assert maps['c_weights'][str(j)] == maps['R_weights'][str(j)] == maps['parameter_weights'][str(j)] == 0
        for j in (64,65):
            assert maps['c_weights'][str(j)] == 1
            assert maps['R_weights'][str(j)] == maps['parameter_weights'][str(j)] == 0
        assert len(set(new['variable_names'])) == new['variables'] == old['variables']-21
        assert len(new['residuals']) == len(old['residuals'])-21
        assert set(new['variable_names']) == (set(old['variable_names'])-removed_vars) | set(map(str,(A,B,C)))
        used = set()
        parameter_symbols = set(map(s.Symbol, new['parameters']))
        for row in new['residuals']:
            for t in row['terms']:
                assert len(t['monomial']) <= 2
                used.update(t['monomial'])
                coefficient = s.sympify(t['coefficient'])
                assert coefficient.free_symbols <= parameter_symbols
                assert s.Poly(coefficient, *parameter_symbols).domain.is_ZZ
        assert used == set(range(1,new['variables']+1))
        assert not cert['source_universality_verified']
        assert not cert['unconditional_undecidability_claim']
        assert not cert['new_abc_assumption']
        assert not cert['pell_core_reduction_already_included']
        reports.append({'m':m,'variables':new['variables'],'rows':len(new['residuals']),
                        'coordinate_saving':21,'row_saving':21,'untouched_rows_verified':len(old_by)-36,
                        'all_removed_coordinate_occurrences_audited':True,
                        'literal_square_and_normalizer_rows_verified':True,
                        'table_sha256':cert['table_sha256']})
    print(json.dumps({'status':'PASS','norm_identity_exact':True,'tables':reports},indent=2))


if __name__ == '__main__':
    main()
