#!/usr/bin/env python3
"""Compile a common arithmetic progression of first contact arguments.

The arithmetic completeness theorem chooses its spacing after all point
differences have been fixed.  The seven common registers below are polynomial
coefficients of the centered square and fourth power along that progression.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import hashlib
import json
from math import gcd, lcm
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
BLOCKS = ['b', 'g', 't', 'm', 'w', 's', 'h', 'c', 'gamma', 'o', 'j', 'i']
NEW = ['contact_common_spacing', 'contact_common_mixed_square',
       'contact_common_spacing_square', 'contact_common_fourth_coefficient_1',
       'contact_common_fourth_coefficient_2', 'contact_common_fourth_coefficient_3',
       'contact_common_fourth_coefficient_4']


def slot(label, index):
    return f'int_{"i_reciprocal" if label == "i" else label}_{index}'


def build(m):
    baseline = ROOT / f'undecidability/source_repair_v93/coefficients/corrected_ceiling_m{m}_quadrics.json'
    raw = baseline.read_bytes()
    old = json.loads(raw)
    assert old['ordinary_integer_inputs'] + ['i'] == BLOCKS
    assert old['source_universality_verified'] is True
    assert old['source_universality_hypothesis'] is None
    assert old['unconditional_undecidability_claim'] is False
    names = old['variable_names']
    assert not set(NEW) & set(names)
    d, v, w, a1, a2, a3, a4 = NEW
    t, u, f = (slot('b', j) for j in (2, 60, 61))
    c, ci, ci2 = (slot('b', j) for j in ((159, 160, 161) if m == 163 else (162, 163, 164)))
    substitution = {}
    for i, label in enumerate(BLOCKS[1:], 1):
        substitution[slot(label, 2)] = {t: 1, d: i}
        substitution[slot(label, 60)] = {u: 1, v: 2*i, w: i*i}
        substitution[slot(label, 61)] = {f: 1, a1: i, a2: i*i, a3: i**3, a4: i**4}
    deleted = set(substitution)
    assert deleted <= set(names)
    newnames = [name for name in names if name not in deleted] + NEW
    ids = {name: j + 1 for j, name in enumerate(newnames)}
    removed = {f'integer.{label}.additive.detector0.{suffix}'
               for label in BLOCKS[1:] for suffix in ('contactSquare', 'contactFourthPower')}
    occurrences = {name: [] for name in deleted}
    rows, multipliers = [], {}
    for row in old['residuals']:
        used = {names[j-1] for term in row['terms'] for j in term['monomial']}
        for name in used & deleted:
            occurrences[name].append(row['name'])
        if row['name'] in removed:
            continue
        if not used & deleted:
            rows.append({'name': row['name'], 'terms': [
                {'coefficient': term['coefficient'],
                 'monomial': sorted(ids[names[j-1]] for j in term['monomial'])}
                for term in row['terms']]})
            continue
        accum = defaultdict(Fraction)
        for term in row['terms']:
            partial = {(): Fraction(term['coefficient'])}
            for j in term['monomial']:
                nxt = defaultdict(Fraction)
                name = names[j-1]
                for monomial, coefficient in partial.items():
                    for target, factor in substitution.get(name, {name: 1}).items():
                        nxt[tuple(sorted((*monomial, ids[target])))] += coefficient * factor
                partial = {monomial: coefficient for monomial, coefficient in nxt.items() if coefficient}
            for monomial, coefficient in partial.items():
                accum[monomial] += coefficient
        accum = {monomial: coefficient for monomial, coefficient in accum.items() if coefficient}
        denominator = lcm(*(coefficient.denominator for coefficient in accum.values()))
        integer = {monomial: int(coefficient * denominator) for monomial, coefficient in accum.items()}
        content = gcd(*integer.values())
        multipliers[row['name']] = str(Fraction(denominator, content))
        rows.append({'name': row['name'], 'terms': [
            {'coefficient': str(coefficient // content), 'monomial': list(monomial)}
            for monomial, coefficient in sorted(integer.items())]})

    def append(name, terms):
        rows.append({'name': 'contact.progression.' + name, 'terms': [
            {'coefficient': str(coefficient), 'monomial': sorted(ids[name] for name in factors)}
            for coefficient, factors in terms]})

    if m == 163:
        append('mixed_square', [(1, [ci2, v]), (-1, [d, t]), (1, [d, ci])])
        append('spacing_square', [(1, [ci2, w]), (-1, [d, d])])
        scale = []
    else:
        append('mixed_square', [(1, [ci, v]), (-484, [d, t]), (66, [d])])
        append('spacing_square', [(1, [ci, w]), (-484, [d, d])])
        scale = [c]
    append('fourth_coefficient_1', [(1, [*scale, a1]), (-4, [u, v])])
    append('fourth_coefficient_2', [(1, [*scale, a2]), (-2, [u, w]), (-4, [v, v])])
    append('fourth_coefficient_3', [(1, [*scale, a3]), (-4, [v, w])])
    append('fourth_coefficient_4', [(1, [*scale, a4]), (-1, [w, w])])
    assert len(newnames) == old['variables'] - 26
    assert len(rows) == len(old['residuals']) - 16
    assert max(len(term['monomial']) for row in rows for term in row['terms']) == 2
    assert {j for row in rows for term in row['terms'] for j in term['monomial']} == set(ids.values())
    result = dict(old)
    result.update(
        variables=len(newnames), variable_names=newnames, residuals=rows,
        affine_contact_predecessor=str(baseline.relative_to(ROOT)),
        affine_contact_predecessor_sha256=hashlib.sha256(raw).hexdigest(),
        affine_contact_blocks=BLOCKS,
        affine_contact_new_coordinates=NEW,
        affine_contact_substitution=substitution,
        affine_contact_removed_rows=sorted(removed),
        affine_contact_occurrences=occurrences,
        affine_contact_row_multipliers=multipliers,
        affine_contact_savings={'coordinates': 26, 'quadratic_rows': 16},
        affine_contact_proof='undecidability/general_contact_v94/affine_contact_progressions.tex',
        affine_contact_equivalence_scope='Same outer-input projection under the retained arithmetic interfaces: rational reconstruction into the predecessor and simultaneous completeness with a spacing chosen after all point differences.')
    certificate = {
        'interface_coordinates': m,
        'variables': len(newnames),
        'quadratic_rows': len(rows),
        'quartic_degree': 4,
        'coefficient_parameters': old['parameters'],
        'predecessor': str(baseline.relative_to(ROOT)),
        'predecessor_sha256': result['affine_contact_predecessor_sha256'],
        'new_coordinates': NEW,
        'removed_coordinates': sorted(deleted),
        'removed_rows': sorted(removed),
        'coordinate_saving': 26,
        'quadratic_row_saving': 16,
        'source_coding_theorem': old['source_coding_theorem'],
        'source_universality_hypothesis': None,
        'source_universality_verified': True,
        'source_coding_theorem_independently_reproved': False,
        'unconditional_undecidability_claim': False,
        'arithmetic_hypotheses_unchanged': True,
        'arithmetic_proof': result['affine_contact_proof'],
        'verified': ['Every affine coordinate substitution in the complete table',
                     'Exact polynomial identities recovering every omitted row',
                     'All old guards retained', 'Integer coefficient domain, quadratic degree, complete support and exact counts'],
        'not_verified': ['Retained arithmetic interfaces', 'A new proof of the classical coding theorem',
                         'Global minimality']}
    return result, certificate


def main():
    for m in (163, 179):
        table, certificate = build(m)
        output = HERE / f'affine_contact_m{m}_quadrics.json'
        output.write_text(json.dumps(table, sort_keys=True, separators=(',', ':')) + '\n')
        certificate['table_sha256'] = hashlib.sha256(output.read_bytes()).hexdigest()
        output.with_name(f'affine_contact_m{m}_certificate.json').write_text(
            json.dumps(certificate, sort_keys=True, indent=2) + '\n')
        print(json.dumps({'m': m, 'variables': table['variables'], 'rows': len(table['residuals']),
                          'sha256': certificate['table_sha256']}))


if __name__ == '__main__':
    main()
