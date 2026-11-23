#!/usr/bin/env python3
"""Independent symbolic audit of the affine contact progression tables.

This checker does not import the compiler.  In particular it reconstructs
the substitutions and every omitted-row identity independently.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def expression(row, names):
    return sp.expand(sum(sp.sympify(term['coefficient']) *
                         sp.prod(sp.Symbol(names[j-1]) for j in term['monomial'])
                         for term in row['terms']))


def verify(m):
    predecessor = ROOT / f'undecidability/source_repair_v93/coefficients/corrected_ceiling_m{m}_quadrics.json'
    path = HERE / f'affine_contact_m{m}_quadrics.json'
    old = json.loads(predecessor.read_bytes())
    new = json.loads(path.read_bytes())
    certificate = json.loads(path.with_name(f'affine_contact_m{m}_certificate.json').read_bytes())
    assert new['affine_contact_predecessor_sha256'] == hashlib.sha256(predecessor.read_bytes()).hexdigest()
    assert certificate['predecessor_sha256'] == hashlib.sha256(predecessor.read_bytes()).hexdigest()
    assert certificate['table_sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
    labels = ['b', 'g', 't', 'm', 'w', 's', 'h', 'c', 'gamma', 'o', 'j', 'i']
    assert old['ordinary_integer_inputs'] + ['i'] == labels
    def z(label, index):
        return sp.Symbol(f'int_{"i_reciprocal" if label == "i" else label}_{index}')
    t, u, f = (z('b', index) for index in (2, 60, 61))
    c, ci, ci2 = (z('b', index) for index in ((159, 160, 161) if m == 163 else (162, 163, 164)))
    names = ['contact_common_spacing', 'contact_common_mixed_square',
             'contact_common_spacing_square', 'contact_common_fourth_coefficient_1',
             'contact_common_fourth_coefficient_2', 'contact_common_fourth_coefficient_3',
             'contact_common_fourth_coefficient_4']
    d, v, w, a1, a2, a3, a4 = map(sp.Symbol, names)
    replacement = {}
    for i, label in enumerate(labels[1:], 1):
        replacement[z(label, 2)] = t + i*d
        replacement[z(label, 60)] = u + 2*i*v + i*i*w
        replacement[z(label, 61)] = f + i*a1 + i*i*a2 + i**3*a3 + i**4*a4
    deleted = set(map(str, replacement))
    assert new['variable_names'] == [name for name in old['variable_names'] if name not in deleted] + names
    assert new['variables'] == old['variables'] - 26 == (1048 if m == 163 else 1228)
    assert len(new['residuals']) == len(old['residuals']) - 16 == (908 if m == 163 else 1064)
    newrows = {row['name']: expression(row, new['variable_names']) for row in new['residuals']}
    assert len(newrows) == len(new['residuals'])
    oldrows = {row['name']: expression(row, old['variable_names']) for row in old['residuals']}
    omitted = {f'integer.{label}.additive.detector0.{suffix}' for label in labels[1:]
               for suffix in ('contactSquare', 'contactFourthPower')}
    suffixes = ['mixed_square', 'spacing_square', 'fourth_coefficient_1', 'fourth_coefficient_2',
                'fourth_coefficient_3', 'fourth_coefficient_4']
    assert [row['name'] for row in new['residuals']] == [row['name'] for row in old['residuals']
                                                        if row['name'] not in omitted] + [
                                                            'contact.progression.' + suffix for suffix in suffixes]
    if m == 163:
        expected = [ci2*v - d*(t-ci), ci2*w-d*d,
                    a1-4*u*v, a2-2*u*w-4*v*v, a3-4*v*w, a4-w*w]
        square0 = (t-ci)**2 - ci2*u + ci2-ci**2
        fourth0 = u*u-f
    else:
        expected = [ci*v-22*d*(22*t-3), ci*w-484*d*d,
                    c*a1-4*u*v, c*a2-2*u*w-4*v*v, c*a3-4*v*w, c*a4-w*w]
        square0 = (22*t-3)**2-ci*u
        fourth0 = u*u-c*f
    for suffix, target in zip(suffixes, expected, strict=True):
        assert sp.expand(newrows['contact.progression.'+suffix]-target) == 0
    assert sp.expand(oldrows['integer.b.additive.detector0.contactSquare']-square0) == 0
    assert sp.expand(oldrows['integer.b.additive.detector0.contactFourthPower']-fourth0) == 0
    # These are polynomial identities, not evaluations on sample solutions.
    # They prove all 22 omitted rows from the root rows and six new rows.
    for i, label in enumerate(labels[1:], 1):
        square = oldrows[f'integer.{label}.additive.detector0.contactSquare'].subs(replacement, simultaneous=True)
        fourth = oldrows[f'integer.{label}.additive.detector0.contactFourthPower'].subs(replacement, simultaneous=True)
        assert sp.expand(square-square0+2*i*expected[0]+i*i*expected[1]) == 0
        assert sp.expand(fourth-fourth0+sum(i**(j+1)*expected[j+2] for j in range(4))) == 0
    changed = []
    for name, before in oldrows.items():
        if name in omitted:
            continue
        after = newrows[name]
        if before.free_symbols & set(replacement):
            changed.append(name)
            target = sp.expand(before.subs(replacement, simultaneous=True))
            variables = sorted(target.free_symbols, key=str)
            primitive = sp.Poly(target, *variables, domain=sp.QQ).clear_denoms(convert=True)[1].primitive()[1]
            assert sp.expand(after-primitive.as_expr()) == 0, name
        else:
            assert before == after, name
    # Explicitly pin the two nonvanishing/scale equations used in reconstruction.
    assert sp.expand(newrows['integer.b.unit.c_inverse']-(c*ci-1)) == 0
    assert sp.expand(newrows['integer.b.unit.c_inverse_square']-(ci2-ci*ci)) == 0
    allowed_parameters = set(map(sp.Symbol, new['parameters']))
    support = set()
    for row in new['residuals']:
        for term in row['terms']:
            assert len(term['monomial']) <= 2
            support.update(term['monomial'])
            coefficient = sp.sympify(term['coefficient'])
            assert coefficient.free_symbols <= allowed_parameters
            assert sp.Poly(coefficient, *sorted(allowed_parameters, key=str), domain=sp.ZZ)
    assert support == set(range(1, new['variables']+1))
    assert new['source_universality_verified'] is True
    assert new['source_universality_hypothesis'] is None
    assert new['unconditional_undecidability_claim'] is False
    assert new['source_coding_theorem'] == old['source_coding_theorem']
    assert new['source_coding_theorem_independently_reproved'] is False
    assert new['affine_contact_occurrences'] == {
        name: [row['name'] for row in old['residuals'] if any(
            old['variable_names'][j-1] == name for term in row['terms'] for j in term['monomial'])]
        for name in deleted}
    return {'status': 'PASS', 'm': m, 'variables': new['variables'], 'quadratic_rows': len(new['residuals']),
            'coordinate_saving': 26, 'row_saving': 16, 'changed_retained_rows': len(changed),
            'omitted_row_polynomial_identities': 22, 'table_sha256': certificate['table_sha256'],
            'scope': 'Complete exact coefficient transformation and reconstruction identities; arithmetic completeness is a separate theorem.'}


if __name__ == '__main__':
    print(json.dumps([verify(m) for m in (163, 179)], indent=2))
