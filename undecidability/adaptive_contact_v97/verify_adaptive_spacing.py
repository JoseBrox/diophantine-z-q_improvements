#!/usr/bin/env python3
"""Independent exact coefficient audit for the adaptive-spacing candidate.

No builder is imported. Arithmetic completeness is blocked by reference
dependence of the contact positions. Passing this verifier does not establish
a lower undecidability bound.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def expression(row, names):
    return sp.expand(sum(sp.sympify(term['coefficient'])*
                         sp.prod(sp.Symbol(names[j-1]) for j in term['monomial'])
                         for term in row['terms']))


def named(row, names):
    return sorted((term['coefficient'], tuple(sorted(names[j-1] for j in term['monomial'])))
                  for term in row['terms'])


def verify(m):
    predecessor = ROOT / f'undecidability/pell_halftrace_v96/halftrace_m{m}_quadrics.json'
    path = HERE / f'adaptive_spacing_m{m}_quadrics.json'
    certificate_path = HERE / f'adaptive_spacing_m{m}_certificate.json'
    old, new, certificate = [json.loads(p.read_bytes()) for p in (predecessor, path, certificate_path)]
    assert certificate['table_sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert certificate['predecessor_sha256'] == hashlib.sha256(predecessor.read_bytes()).hexdigest()
    assert new['variable_names'] == [name for name in old['variable_names'] if name != 'contact_common_spacing']
    assert new['variables'] == old['variables']-1
    assert len(new['residuals']) == len(old['residuals'])
    assert (new['variables'], len(new['residuals'])) == {163: (981, 854), 179: (1146, 997)}[m]
    oldrows = {row['name']: row for row in old['residuals']}
    newrows = {row['name']: row for row in new['residuals']}
    assert list(oldrows) == list(newrows)
    t, u, d = map(sp.Symbol, ('int_b_2', 'int_b_60', 'contact_common_spacing'))
    rho, epsilon, epsilon2 = map(sp.Symbol, [f'int_b_{j}' for j in ((159,160,161) if m == 163 else (162,163,164))])
    D = sp.Symbol('common_scalar_r_imag' if m == 163 else 'int_b_113') / sp.Integer(2)**24
    v, w = map(sp.Symbol, ('contact_common_mixed_square', 'contact_common_spacing_square'))
    used_rows = {name for name, row in oldrows.items()
                 if d in expression(row, old['variable_names']).free_symbols
                 or (m == 163 and t in expression(row, old['variable_names']).free_symbols)}
    assert used_rows == set(new['adaptive_spacing_changed_rows'])
    changed, unchanged = 0, 0
    for name, row in oldrows.items():
        if name not in used_rows:
            assert named(row, old['variable_names']) == named(newrows[name], new['variable_names']), name
            unchanged += 1
            continue
        before = expression(row, old['variable_names'])
        after = expression(newrows[name], new['variable_names'])
        if m == 163:
            # Interpret the old scaled chart in the new physical coordinates,
            # then impose only the two existing gauge-unit identities.
            pulled_back = before.subs({t: epsilon*t, d: epsilon*D}, simultaneous=True)
            pulled_back = sp.cancel(pulled_back.subs({rho: 1/epsilon, epsilon2: epsilon**2}, simultaneous=True))
            compared_after = sp.cancel(after.subs({rho: 1/epsilon, epsilon2: epsilon**2}, simultaneous=True))
            if name == 'integer.b.additive.detector0.contactSquare':
                expected = t*t-2*t+1-u
                assert sp.expand(after-expected) == 0
                pulled_back /= epsilon**2
            elif name == 'contact.progression.mixed_square':
                expected = v-D*(t-1)
                pulled_back /= epsilon**2
            elif name == 'contact.progression.spacing_square':
                expected = w-D*D
                pulled_back /= epsilon**2
            else:
                assert name.startswith('integer.') and name.endswith('.new.aggregate')
                expected = None
        else:
            pulled_back = before.subs(d, D)
            compared_after = after
            expected = None
        ratio = sp.cancel(compared_after/pulled_back)
        assert ratio.is_Rational and ratio != 0, (name, ratio)
        if expected is not None:
            active = sorted(expected.free_symbols, key=str)
            primitive = sp.Poly(expected, *active, domain=sp.QQ).clear_denoms(convert=True)[1].primitive()[1].as_expr()
            assert sp.expand(after-primitive) == 0
        # Primitive normalization is by a constant only, so it changes no zero set.
        active = sorted(after.free_symbols, key=str)
        assert sp.Poly(after, *active, domain=sp.ZZ).content() == 1
        changed += 1
    for guard in ('integer.b.unit.c_inverse','integer.b.unit.c_inverse_square'):
        assert named(oldrows[guard], old['variable_names']) == named(newrows[guard], new['variable_names'])
    parameters = tuple(map(sp.Symbol, new['parameters']))
    support = set()
    for row in new['residuals']:
        for term in row['terms']:
            assert len(term['monomial']) <= 2
            support.update(term['monomial'])
            coefficient = sp.sympify(term['coefficient'])
            assert coefficient.free_symbols <= set(parameters)
            assert sp.Poly(coefficient, *parameters, domain=sp.ZZ)
    assert support == set(range(1,new['variables']+1))
    assert new['ordinary_integer_inputs'] == old['ordinary_integer_inputs']
    assert new['integer_blocks'] == old['integer_blocks']
    assert new['source_universality_hypothesis'] is None
    assert new['unconditional_undecidability_claim'] is False
    assert certificate['smaller_undecidability_count_claimed'] is False
    return {'status': 'ALGEBRA PASS; COMPLETENESS BLOCKED BY REFERENCE DEPENDENCE', 'm': m,
            'variables_in_candidate': new['variables'], 'quadratic_rows': len(new['residuals']),
            'changed_rows_checked': changed, 'unchanged_rows_checked': unchanged,
            'table_sha256': certificate['table_sha256'],
            'smaller_undecidability_count_claimed': False}


if __name__ == '__main__':
    print(json.dumps([verify(m) for m in (163,179)], sort_keys=True, indent=2))
