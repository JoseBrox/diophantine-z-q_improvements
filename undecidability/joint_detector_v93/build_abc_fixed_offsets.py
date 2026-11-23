#!/usr/bin/env python3
"""Share the abc contact parameter by fixed dyadic translations.

Completeness is the fixed-place separation theorem in the accompanying paper.
The algebraic map alone would only certify a restriction of the source system.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
import hashlib
import json
from math import gcd, lcm
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BASELINE = ROOT / 'undecidability/coefficients/jones1980_ceiling_power/ceiling_power_m56_quadrics.json'
DEFAULT_OUTPUT = Path(__file__).resolve().parent / 'abc_fixed_offsets_quadrics.json'


def build(baseline: Path):
    raw = baseline.read_bytes()
    old = json.loads(raw)
    assert old['integer_definition_total_variables'] == 56
    assert old['source_universality_verified'] is False
    assert old['unconditional_undecidability_claim'] is False
    assert old['shared_reference_ids'] == [2, 3, 4, 5, 6, 7]
    labels = old['ordinary_integer_inputs']
    assert labels == ['b', 'g', 't', 'm', 'w', 's', 'h', 'c', 'gamma', 'o', 'j', 'i']
    names = old['variable_names']
    physical = lambda label: 'i_reciprocal' if label == 'i' else label
    old_contact = {label: f'int_{physical(label)}_48' for label in labels}
    assert set(old_contact.values()) <= set(names)
    common = old_contact[labels[0]]
    grid_denominator = 2**((len(labels) - 1).bit_length())
    offsets = {label: Fraction(j, grid_denominator) for j, label in enumerate(labels)}
    sum_coordinate = {label: f'int_{physical(label)}_50' for label in labels}
    difference_coordinate = {label: f'int_{physical(label)}_49' for label in labels}
    square = 'abc_common_contact_square'
    assert square not in names
    deleted = (set(old_contact.values()) - {common}) | set(sum_coordinate.values())
    newnames = [name for name in names if name not in deleted] + [square]
    ids = {name: j + 1 for j, name in enumerate(newnames)}
    substitution = {old_contact[label]: {common: Fraction(1), None: offsets[label]}
                    for label in labels}
    substitution.update({sum_coordinate[label]: {
        difference_coordinate[label]: Fraction(1), square: Fraction(2),
        common: 4 * offsets[label], None: 2 * offsets[label]**2}
        for label in labels})
    occurrences = {name: [] for name in set(old_contact.values()) | set(sum_coordinate.values())}
    removed_rows = {f'integer.{label}.contact.difference' for label in labels}
    multipliers = {}
    rows = []
    for row in old['residuals']:
        used = {names[j - 1] for term in row['terms'] for j in term['monomial']}
        for name in used & set(occurrences):
            occurrences[name].append(row['name'])
        if row['name'] in removed_rows:
            continue
        if not used & deleted:
            rows.append({'name': row['name'], 'terms': [
                {'coefficient': term['coefficient'],
                 'monomial': sorted(ids[names[j - 1]] for j in term['monomial'])}
                for term in row['terms']]})
            continue
        accum = defaultdict(Fraction)
        for term in row['terms']:
            partial = {(): Fraction(term['coefficient'])}
            for j in term['monomial']:
                name = names[j - 1]
                nxt = defaultdict(Fraction)
                for monomial, coefficient in partial.items():
                    for target, factor in substitution.get(name, {name: Fraction(1)}).items():
                        if target is None:
                            nxt[monomial] += coefficient * factor
                        else:
                            nxt[tuple(sorted((*monomial, ids[target])))] += coefficient * factor
                partial = {m: c for m, c in nxt.items() if c}
            for monomial, coefficient in partial.items():
                accum[monomial] += coefficient
        accum = {m: c for m, c in accum.items() if c}
        denominator = lcm(*(coefficient.denominator for coefficient in accum.values()))
        integers = {m: int(c * denominator) for m, c in accum.items()}
        content = gcd(*integers.values())
        multipliers[row['name']] = str(Fraction(denominator, content))
        rows.append({'name': row['name'], 'terms': [
            {'coefficient': str(coefficient // content), 'monomial': list(monomial)}
            for monomial, coefficient in sorted(integers.items())]})
    for label in labels:
        assert occurrences[old_contact[label]] == [f'integer.{label}.contact.difference']
        assert set(occurrences[sum_coordinate[label]]) == {
            f'integer.{label}.contact.{suffix}' for suffix in
            ('sum', 'difference', 'A1', 'A2', 'partialCombined', 'derivativeQuotient')}
    rows.append({'name': 'abc.common_contact_square', 'terms': [
        {'coefficient': '-1', 'monomial': [ids[common], ids[common]]},
        {'coefficient': '1', 'monomial': [ids[square]]}]})
    assert len(newnames) == old['variables'] - 2 * (len(labels) - 1)
    assert len(rows) == len(old['residuals']) - (len(labels) - 1)
    assert max(len(term['monomial']) for row in rows for term in row['terms']) == 2
    assert {j for row in rows for term in row['terms'] for j in term['monomial']} == set(ids.values())
    result = dict(old)
    result.update(variables=len(newnames), variable_names=newnames, residuals=rows,
                  fixed_offset_predecessor_sha256=hashlib.sha256(raw).hexdigest(),
                  fixed_offset_common_coordinate=common,
                  fixed_offset_common_square=square,
                  fixed_offset_grid_denominator=grid_denominator,
                  fixed_offset_translations={label: str(offsets[label]) for label in labels},
                  fixed_offset_occurrences=occurrences,
                  fixed_offset_row_multipliers=multipliers,
                  fixed_offset_savings={'coordinates': 2 * (len(labels) - 1),
                                        'quadratic_rows': len(labels) - 1},
                  fixed_offset_removed_rows=sorted(removed_rows),
                  fixed_offset_proof='undecidability/papers/abc_fixed_contact_offsets_v93.tex',
                  fixed_offset_equivalence_scope='Same outer-input projection under the retained abc interface, for positive-source completeness; affine restriction followed by the fixed-place simultaneous-witness theorem.')
    cert = {key: value for key, value in result.items()
            if key not in ('variable_names', 'residuals', 'power_chain')}
    cert['quadratic_residuals'] = len(rows)
    cert['verified'] = ['Exact occurrence list for every contact parameter',
                        'Literal affine substitution with nonzero rational row scalings',
                        'Every unchanged row preserved up to coordinate numbering',
                        'Shared contact square with all private sum coordinates eliminated',
                        'Twenty-two-coordinate and eleven-row saving, quadratic degree, integral coefficient domain, full support']
    cert['not_verified'] = ['U_em source universality', 'Retained arithmetic hypotheses',
                            'Sufficient numeric abc parameter', 'Global minimality']
    return result, cert


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, default=DEFAULT_BASELINE)
    parser.add_argument('--out', type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result, cert = build(args.baseline)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, separators=(',', ':'), sort_keys=True) + '\n')
    cert['table_sha256'] = hashlib.sha256(args.out.read_bytes()).hexdigest()
    args.out.with_name(args.out.stem.replace('_quadrics', '') + '_certificate.json').write_text(
        json.dumps(cert, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'variables': result['variables'], 'rows': len(result['residuals']),
                      'sha256': cert['table_sha256']}))


if __name__ == '__main__':
    main()
