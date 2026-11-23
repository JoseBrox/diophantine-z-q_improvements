#!/usr/bin/env python3
"""Compile the adaptive-spacing candidate; arithmetic acceptance is separate.

This folder records a blocked research checkpoint. The complete coefficient
operation is checked, but the spacing depends on the reference subsequently
retuned at the selected primes. No lower undecidability count is asserted.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SCALE = sp.Rational(1, 2**24)


def expression(row, names):
    return sp.expand(sum(sp.sympify(term['coefficient'])*
                         sp.prod(sp.Symbol(names[j-1]) for j in term['monomial'])
                         for term in row['terms']))


def build(m):
    predecessor = ROOT / f'undecidability/pell_halftrace_v96/halftrace_m{m}_quadrics.json'
    raw = predecessor.read_bytes()
    old = json.loads(raw)
    names = old['variable_names']
    spacing_name = 'contact_common_spacing'
    assert spacing_name in names
    d = sp.Symbol(spacing_name)
    t, u = map(sp.Symbol, ('int_b_2', 'int_b_60'))
    rname = 'common_scalar_r_imag' if m == 163 else 'int_b_113'
    assert rname in names
    D = SCALE*sp.Symbol(rname)
    rho = sp.Symbol('int_b_159' if m == 163 else 'int_b_162')
    v, w = map(sp.Symbol, ('contact_common_mixed_square', 'contact_common_spacing_square'))
    new_names = [name for name in names if name != spacing_name]
    ids = {name: j+1 for j, name in enumerate(new_names)}
    rows, changed, multipliers = [], [], {}
    old_occurrences = {name: [] for name in (spacing_name, 'int_b_2')}
    for row in old['residuals']:
        used = {names[j-1] for term in row['terms'] for j in term['monomial']}
        for name in old_occurrences:
            if name in used:
                old_occurrences[name].append(row['name'])
        is_changed = spacing_name in used or (m == 163 and 'int_b_2' in used)
        if not is_changed:
            rows.append({'name': row['name'], 'terms': [
                {'coefficient': term['coefficient'],
                 'monomial': sorted(ids[names[j-1]] for j in term['monomial'])}
                for term in row['terms']]})
            continue
        e = expression(row, names)
        if m == 179:
            target = sp.expand(e.subs(d, D))
        elif row['name'] == 'integer.b.additive.detector0.contactSquare':
            target = t*t-2*t+1-u
        elif row['name'] == 'contact.progression.mixed_square':
            target = v-D*(t-1)
        elif row['name'] == 'contact.progression.spacing_square':
            target = w-D*D
        else:
            assert row['name'].startswith('integer.') and row['name'].endswith('.new.aggregate')
            target = 0
            for term in row['terms']:
                factors = [sp.Symbol(names[j-1]) for j in term['monomial']]
                coefficient = sp.sympify(term['coefficient'])
                if t in factors:
                    assert sorted(factors, key=str) == sorted([t, rho], key=str)
                    target += coefficient*t
                elif d in factors:
                    assert sorted(factors, key=str) == sorted([d, rho], key=str)
                    target += coefficient*D
                else:
                    target += coefficient*sp.prod(factors)
        active = sorted(target.free_symbols, key=str)
        polynomial = sp.Poly(target, *active, domain=sp.QQ)
        denominator, integral = polynomial.clear_denoms(convert=True)
        content, primitive = integral.primitive()
        multiplier = sp.Rational(denominator, content)
        multipliers[row['name']] = str(multiplier)
        changed.append(row['name'])
        terms = []
        for monomial, coefficient in primitive.terms():
            factors = [str(symbol) for symbol, power in zip(active, monomial)
                       for _ in range(power)]
            assert len(factors) <= 2
            terms.append({'coefficient': str(coefficient),
                          'monomial': sorted(ids[name] for name in factors)})
        rows.append({'name': row['name'], 'terms': terms})
    assert len(new_names) == old['variables']-1
    assert len(rows) == len(old['residuals'])
    assert {i for row in rows for term in row['terms'] for i in term['monomial']} == set(ids.values())
    new = dict(old)
    new.update(variable_names=new_names, variables=len(new_names), residuals=rows)
    new.update(
        adaptive_spacing_predecessor=str(predecessor.relative_to(ROOT)),
        adaptive_spacing_predecessor_sha256=hashlib.sha256(raw).hexdigest(),
        adaptive_spacing_formula=f'D={rname}/16777216',
        adaptive_spacing_removed_coordinate=spacing_name,
        adaptive_spacing_relative_depth=8,
        adaptive_spacing_minimum_reference_depth=6,
        adaptive_spacing_changed_rows=changed,
        adaptive_spacing_row_multipliers=multipliers,
        adaptive_spacing_old_occurrences=old_occurrences,
        adaptive_spacing_general_root_reinterpretation='int_b_2 now stores physical lambda; predecessor int_b_2=epsilon*lambda and spacing=epsilon*D' if m == 163 else None,
        adaptive_spacing_research_checkpoint='undecidability/joint_research_v94/continuation.md',
        adaptive_spacing_arithmetic_audit_status='Blocked: r_imag depends on the reference h subsequently retuned at selected contact primes, so translated contact positions are not established fixed data for the retained supplier',
        adaptive_spacing_coordinate_saving=1,
        adaptive_spacing_row_saving=0)
    certificate = {
        'interface_coordinates': m, 'variables': new['variables'],
        'quadratic_rows': len(rows), 'quartic_degree': 4,
        'predecessor': str(predecessor.relative_to(ROOT)),
        'predecessor_sha256': hashlib.sha256(raw).hexdigest(),
        'changed_rows': changed, 'old_occurrences': old_occurrences,
        'coordinate_saving': 1, 'quadratic_row_saving': 0,
        'arithmetic_audit_status': new['adaptive_spacing_arithmetic_audit_status'],
        'unconditional_undecidability_claim': False,
        'smaller_undecidability_count_claimed': False,
        'scope': 'Complete exact coefficient transformation and rational soundness reconstruction. Arithmetic completeness is blocked by reference-dependent contact coefficients.'}
    return new, certificate


if __name__ == '__main__':
    for m in (163, 179):
        table, certificate = build(m)
        path = HERE / f'adaptive_spacing_m{m}_quadrics.json'
        path.write_text(json.dumps(table, sort_keys=True, separators=(',', ':'))+'\n')
        certificate['table_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        path.with_name(f'adaptive_spacing_m{m}_certificate.json').write_text(
            json.dumps(certificate, sort_keys=True, indent=2)+'\n')
        print(json.dumps({'m': m, 'variables': table['variables'],
                          'rows': len(table['residuals']),
                          'arithmetic_status': 'blocked by reference dependence', 'sha256': certificate['table_sha256']}))
