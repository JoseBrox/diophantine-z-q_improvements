#!/usr/bin/env python3
"""Independent exact checker for the fixed dyadic contact translations.

The checker uses symbolic substitution, independently of the producer's
fraction-dictionary expansion. It does not certify arithmetic hypotheses.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BASELINE = ROOT / 'undecidability/coefficients/jones1980_ceiling_power/ceiling_power_m56_quadrics.json'
DEFAULT_TABLE = Path(__file__).resolve().parent / 'abc_fixed_offsets_quadrics.json'


def expression(row, names):
    return sp.expand(sum(sp.sympify(term['coefficient']) *
                         sp.prod(sp.Symbol(names[j - 1]) for j in term['monomial'])
                         for term in row['terms']))


def valuation_two(value: Fraction):
    assert value
    numerator, denominator = abs(value.numerator), value.denominator
    result = 0
    while numerator % 2 == 0:
        numerator //= 2
        result += 1
    while denominator % 2 == 0:
        denominator //= 2
        result -= 1
    return result


def verify(baseline: Path, table: Path):
    old = json.loads(baseline.read_bytes())
    new = json.loads(table.read_bytes())
    cert = json.loads(table.with_name(table.stem.replace('_quadrics', '') + '_certificate.json').read_bytes())
    assert new['fixed_offset_predecessor_sha256'] == hashlib.sha256(baseline.read_bytes()).hexdigest()
    assert cert['table_sha256'] == hashlib.sha256(table.read_bytes()).hexdigest()
    labels = ['b', 'g', 't', 'm', 'w', 's', 'h', 'c', 'gamma', 'o', 'j', 'i']
    assert old['ordinary_integer_inputs'] == labels
    physical = lambda label: 'i_reciprocal' if label == 'i' else label
    offsets = {label: sp.Rational(j, 16) for j, label in enumerate(labels)}
    z = sp.Symbol('int_b_48')
    substitution = {sp.Symbol(f'int_{physical(label)}_48'): z + offsets[label]
                    for label in labels[1:]}
    square = sp.Symbol('abc_common_contact_square')
    substitution.update({sp.Symbol(f'int_{physical(label)}_50'):
                         sp.Symbol(f'int_{physical(label)}_49') + 2*square +
                         4*offsets[label]*z + 2*offsets[label]**2
                         for label in labels})
    removed = {str(symbol) for symbol in substitution}
    assert new['variable_names'] == [name for name in old['variable_names'] if name not in removed] + [str(square)]
    assert new['variables'] == old['variables'] - 22
    assert len(new['residuals']) == len(old['residuals']) - 11
    removed_rows = {f'integer.{label}.contact.difference' for label in labels}
    oldrows = [row for row in old['residuals'] if row['name'] not in removed_rows]
    assert [row['name'] for row in new['residuals']] == [row['name'] for row in oldrows] + ['abc.common_contact_square']
    assert sp.expand(expression(new['residuals'][-1], new['variable_names']) - square + z*z) == 0
    for row in old['residuals']:
        if row['name'] in removed_rows:
            assert sp.expand(expression(row, old['variable_names']).subs(substitution, simultaneous=True) - 2*(square-z*z)) == 0
    changed = []
    for before, after in zip(oldrows, new['residuals'][:-1], strict=True):
        original = expression(before, old['variable_names'])
        actual = expression(after, new['variable_names'])
        if original.free_symbols & set(substitution):
            changed.append(before['name'])
            target = sp.Poly(original.subs(substitution, simultaneous=True), *sorted(actual.free_symbols, key=str), domain=sp.QQ)
            _, cleared = target.clear_denoms(convert=True)
            _, primitive = cleared.primitive()
            assert sp.expand(actual - primitive.as_expr()) == 0, before['name']
        else:
            assert sp.expand(original - actual) == 0, before['name']
    assert set(changed) == {f'integer.{label}.contact.{suffix}' for label in labels
                           for suffix in ('sum', 'A1', 'A2', 'partialCombined', 'derivativeQuotient')}
    assert new['fixed_offset_translations'] == {label: str(offsets[label]) for label in labels}
    assert new['source_universality_verified'] is False and new['unconditional_undecidability_claim'] is False
    allowed_parameters = set(map(sp.Symbol, new['parameters']))
    support = set()
    for row in new['residuals']:
        for term in row['terms']:
            assert len(term['monomial']) <= 2
            support.update(term['monomial'])
            coefficient = sp.sympify(term['coefficient'])
            assert coefficient.free_symbols <= allowed_parameters
            assert sp.Poly(coefficient, *sorted(allowed_parameters, key=str), domain=sp.ZZ)
    assert support == set(range(1, new['variables'] + 1))
    # Exact valuation witnesses illustrate the separation theorem; the general
    # proof, rather than this finite computation, covers all integral centers.
    centers = [Fraction(17 + 8*j, 2*j + 1) for j in range(12)]
    radii = [-8, -7, -4, -1, 1, 4, 7, 8]
    contacts = []
    for j, center in enumerate(centers):
        delta = Fraction(j, 16)
        group = [sign * (center + radius) - delta for sign in (-1, 1) for radius in radii]
        contacts.append(group)
    assert all(set(contacts[i]).isdisjoint(contacts[j]) for i in range(12) for j in range(i))
    assert all(valuation_two(a-b) < 0 for i in range(12) for j in range(i)
               for a in contacts[i] for b in contacts[j])
    return {'status': 'PASS', 'variables': new['variables'], 'quadratic_rows': len(new['residuals']),
            'removed_coordinates': 22, 'removed_rows': 11, 'changed_rows': changed,
            'predecessor_sha256': new['fixed_offset_predecessor_sha256'],
            'table_sha256': cert['table_sha256'],
            'scope': 'Every affine substitution, coefficient, occurrence, guard-retention and complete count checked; arithmetic completeness is proved separately.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, default=DEFAULT_BASELINE)
    parser.add_argument('--table', type=Path, default=DEFAULT_TABLE)
    args = parser.parse_args()
    print(json.dumps(verify(args.baseline, args.table), indent=2))


if __name__ == '__main__':
    main()
