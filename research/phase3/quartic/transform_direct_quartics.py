#!/usr/bin/env python3
"""Two exact transformations of frozen phase3 quadratic residual systems.

This program neither modifies the original producers nor overwrites their
artifacts. The translated table uses the fixed coefficient S=3^(2^27),
so the original fixed integer kappa is S^2. S is never a coordinate.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
import gzip
import hashlib
import json
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def add_term(out, key, value):
    value = Q(value)
    out[key] = out.get(key, Q(0)) + value
    if not out[key]:
        del out[key]


def multiply(a, b):
    out = {}
    for (ma, ka), ca in a.items():
        for (mb, kb), cb in b.items():
            add_term(out, (tuple(sorted(ma + mb)), ka + kb), ca * cb)
    return out


def parse(terms):
    out = {}
    for monomial, k, c in terms:
        key = tuple(monomial), k
        assert key not in out and c != 0
        out[key] = Q(c)
    return out


def substitute(poly, replacements, coefficient_power_scale=1):
    out = {}
    for (monomial, k), c in poly.items():
        term = {((), k * coefficient_power_scale): c}
        for v in monomial:
            term = multiply(term, replacements.get(v, {((v,), 0): Q(1)}))
        for key, coefficient in term.items():
            add_term(out, key, coefficient)
    return out


def dump(poly):
    assert all(c.denominator == 1 for c in poly.values())
    return [[list(m), k, c.numerator] for (m, k), c in sorted(poly.items())]


def square_sum(residuals):
    out = {}
    for row in residuals:
        square = multiply(parse(row['terms']), parse(row['terms']))
        for key, c in square.items():
            add_term(out, key, c)
    return out


def load_parent(relative):
    path = HERE / relative / 'polynomial.json.gz'
    raw = gzip.decompress(path.read_bytes())
    obj = json.loads(raw)
    parent = {'path': str(path.relative_to(ROOT)),
              'uncompressed_sha256': hashlib.sha256(raw).hexdigest(),
              'variables': len(obj['variables']),
              'residuals': len(obj['residuals'])}
    return obj, parent


def stats(variables, residuals, polynomial):
    assert all(len(m) <= 2 for row in residuals for m, k, c in row['terms'])
    assert max(len(m) for m, k in polynomial) == 4
    assert polynomial[((0, 0, 0, 0), 0)] == 1
    assert all(m == tuple(sorted(m)) for m, k in polynomial)
    coefficient_gcd = 0
    for c in polynomial.values():
        assert c.denominator == 1
        coefficient_gcd = gcd(coefficient_gcd, abs(c.numerator))
    assert coefficient_gcd == 1
    return {'total_variables': len(variables),
            'existential_witnesses': len(variables) - 1,
            'quadratic_residuals': len(residuals),
            'total_degree': 4,
            'encoded_coefficient_entries': len(polynomial),
            'distinct_variable_monomials': len({m for m, k in polynomial}),
            'coefficient_symbol_content': 1,
            'primitive_integer_content_after_specialization': 1,
            'unit_input_fourth_power_coefficient': 1,
            'max_encoded_integer_coefficient_bits': max(abs(c.numerator).bit_length()
                                                       for c in polynomial.values()),
            'categories': dict(Counter(v['category'] for v in variables))}


def emit(directory, variables, residuals, polynomial, constants,
         symbol, parent, certificate, report):
    obj = {'format': 'diophantine-z-q-quartic-transformation/v1',
           'variables': variables,
           'residuals': residuals,
           'expanded_polynomial': dump(polynomial),
           'fixed_constants': constants,
           'coefficient_symbol': symbol,
           'coefficient_encoding': '[monomial,k,c] means c*symbol^k times the '
                                   'listed coordinate monomial; the symbol is a '
                                   'specified fixed integer, never a coordinate.',
           'parent': parent,
           'transformation': certificate,
           'report': report}
    path = HERE / directory
    path.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(obj, separators=(',', ':')) + '\n').encode('ascii')
    (path / 'polynomial.json.gz').write_bytes(gzip.compress(raw, compresslevel=1, mtime=0))
    digest = hashlib.sha256(raw).hexdigest()
    full_report = report | {'uncompressed_json_bytes': len(raw),
                            'uncompressed_sha256': digest,
                            'parent': parent,
                            'verification_status': 'Producer exact identities passed; '
                                                   'independent audit is separate.'}
    (path / 'construction-report.json').write_text(json.dumps(full_report, indent=2) + '\n')
    (path / 'transformation-certificate.json').write_text(json.dumps(
        {'parent': parent, 'result_uncompressed_sha256': digest,
         'transformation': certificate}, indent=2) + '\n')
    return {'directory': str(path.relative_to(ROOT)), **full_report}


def translate():
    parent_obj, parent = load_parent('quartic-direct')
    assert parent['uncompressed_sha256'] == 'dbd50fdd3484df9aa27b0133406f644689f9bff776c34bf2fdad64494270a5ff'
    assert parent_obj['fixed_constants'] == {'K': '3^(2^28)'}
    original = parent_obj['residuals']
    private = (55, 56, 57)
    assert [parent_obj['variables'][i]['name'] for i in private] == ['anchor.u', 'anchor.v', 'anchor.w']
    for v in private:
        assert [i for i, row in enumerate(original)
                if any(v in m for m, k, c in row['terms'])] == [46]
    expected_parent = {
        ((52, 52), 0): -3, ((52, 53), 0): -6, ((52, 54), 0): 6,
        ((53, 53), 0): -3, ((53, 54), 0): 6, ((54, 54), 0): -3,
        ((55, 55), 0): 16, ((56, 56), 0): 96, ((57, 57), 0): -32,
        ((), 1): 32}
    assert parse(original[46]['terms']) == expected_parent
    replacement = {
        55: {((55,), 0): Q(1, 4), ((56,), 0): Q(-3, 4),
             ((57,), 0): Q(3, 4), ((), 1): Q(1)},
        56: {((56,), 0): Q(1, 4), ((), 1): Q(1, 2)},
        57: {((57,), 0): Q(1, 4), ((), 1): Q(3, 2)}}
    rows = deepcopy(original)
    for row in rows:
        row['terms'] = dump(substitute(parse(row['terms']), replacement, 2))
    expected_new = {
        ((52, 52), 0): -3, ((52, 53), 0): -6, ((52, 54), 0): 6,
        ((53, 53), 0): -3, ((53, 54), 0): 6, ((54, 54), 0): -3,
        ((55, 55), 0): 1, ((55, 56), 0): -6, ((55, 57), 0): 6,
        ((56, 56), 0): 15, ((56, 57), 0): -18, ((57, 57), 0): 7,
        ((55,), 1): 8}
    assert parse(rows[46]['terms']) == expected_new
    assert all(rows[i] == original[i] for i in range(len(rows)) if i != 46)
    polynomial = square_sum(rows)
    assert polynomial == substitute(parse(parent_obj['expanded_polynomial']), replacement, 2)
    assert polynomial[((55, 55), 2)] == 64
    assert [(m, k) for m, k in polynomial if k == 2] == [((55, 55), 2)]
    assert all(k <= 2 for m, k in polynomial)
    assert max(abs(c) for (m, k), c in polynomial.items() if k == 1) == 288
    assert max(abs(c.numerator).bit_length() for (m, k), c in polynomial.items() if k == 0) <= 1020
    # No two powers of S share the same ordinary variable monomial.
    assert len({m for m, k in polynomial}) == len(polynomial)
    variables = deepcopy(parent_obj['variables'])
    for i, name in zip(private, ('anchor.U', 'anchor.V', 'anchor.W')):
        variables[i]['parent_name'] = variables[i]['name']
        variables[i]['name'] = name
    certificate = {
        'kind': 'invertible rational affine change of three private witnesses',
        'parent_coefficient_symbol': 'K',
        'parent_symbol_substitution': 'K=S^2',
        'fixed_S': '3^(2^27)',
        'input_coordinate_fixed': 0,
        'changed_parent_residual_indices': [46],
        'changed_coordinates': [55, 56, 57],
        'parent_from_new': {
            'X55': 'S+(X55-3*X56+3*X57)/4',
            'X56': 'S/2+X56/4',
            'X57': '3*S/2+X57/4'},
        'new_from_parent': {
            'X55': '4*X55+12*X56-12*X57+8*S',
            'X56': '4*X56-2*S',
            'X57': '4*X57-6*S'},
        'linear_determinant': '1/64',
        'other_coordinates': 'identity',
        'parent_anchor_terms': original[46]['terms'],
        'new_anchor_terms': rows[46]['terms'],
        'identity_checked': 'P_new=P_parent after K=S^2 and the displayed affine '
                            'substitution; every transformed residual and every '
                            'expanded coefficient agrees exactly.',
        'field_scope': 'The affine change is a bijection over every characteristic-zero '
                       'field. It preserves both the common residual zero set and the '
                       'literal single-polynomial input projection.'}
    report = stats(variables, rows, polynomial)
    assert report['total_variables'] == 1315 and report['quadratic_residuals'] == 1272
    report |= {
        'exact_primitive_coefficient_height': '64*S^2 = 64*3^(2^28)',
        'coefficient_height_upper_bound': '2^429496736',
        'height_proof': 'The unique S^2 coefficient is64 at X55^2. The S-linear '
                        'coefficients are at most288; all remaining coefficients '
                        'are smaller than2^1020. S=3^(2^27) makes64*S^2 dominate '
                        'both bounds. There is no overlap between different S-powers '
                        'at an ordinary monomial. The X0^4 coefficient is1.',
        'representation': 'Complete sparse residuals and quartic table with one fixed '
                          'integer coefficient symbol S; no new witness.'}
    return emit('quartic-direct-translated', variables, rows, polynomial,
                {'S': '3^(2^27)'}, 'S', parent, certificate, report)


def eliminate():
    parent_obj, parent = load_parent('quartic-direct-small-coefficients')
    assert parent['uncompressed_sha256'] == '9486590b47c79aa4e37bf185dc278e2010567c3d98023785b6eb7bd6eeaa72e0'
    assert parent_obj['fixed_constants'] == {}
    original = parent_obj['residuals']
    assert [i for i, row in enumerate(original)
            if any(81 in m for m, k, c in row['terms'])] == [69, 70]
    assert parse(original[69]['terms']) == {((80, 80), 0): 1, ((81,), 0): -1}
    replacement = {v: {((v if v < 81 else v - 1,), 0): Q(1)}
                   for v in range(len(parent_obj['variables'])) if v != 81}
    replacement[81] = {((80, 80), 0): Q(1)}
    rows = []
    for i, row in enumerate(original):
        transformed = substitute(parse(row['terms']), replacement)
        if i == 69:
            assert not transformed
            continue
        new_row = deepcopy(row)
        new_row['terms'] = dump(transformed)
        rows.append(new_row)
    polynomial = square_sum(rows)
    assert polynomial == substitute(parse(parent_obj['expanded_polynomial']), replacement)
    assert all(k == 0 for m, k in polynomial)
    variables = []
    for old in parent_obj['variables']:
        if old['index'] == 81:
            continue
        new = deepcopy(old)
        new['parent_index'] = old['index']
        new['index'] = len(variables)
        variables.append(new)
    certificate = {
        'kind': 'eliminate a uniquely defined square coordinate',
        'input_coordinate_fixed': 0,
        'deleted_parent_coordinate': 81,
        'deleted_parent_residual_index': 69,
        'pivot_equation': 'X80^2-X81=0',
        'affected_other_parent_residual_indices': [70],
        'substitution': 'parent_X81=new_X80^2',
        'old_to_new_coordinate_indices': [i if i < 81 else None if i == 81 else i - 1
                                          for i in range(len(parent_obj['variables']))],
        'parent_from_new': 'Insert X81=X80^2; old indices above81 are one greater '
                           'than their new indices; all earlier indices agree.',
        'new_from_parent_on_residual_solutions': 'Delete coordinate81.',
        'parent_pivot_terms': original[69]['terms'],
        'parent_anchor_terms': original[70]['terms'],
        'new_anchor_terms': rows[69]['terms'],
        'identity_checked': 'P_new=P_parent after the displayed polynomial '
                            'substitution. The pivot residual becomes identicallyzero.',
        'field_scope': 'This is a bijection of common residual zero sets over every '
                       'characteristic-zero field. Equivalence of the literal SOS '
                       'input projections follows over formally real fields, in '
                       'particular Q; it is not asserted here for nonreal fields.'}
    report = stats(variables, rows, polynomial)
    assert report['total_variables'] == 1338 and report['quadratic_residuals'] == 1295
    height = max(abs(c.numerator) for c in polynomial.values())
    assert height.bit_length() <= 1020
    report |= {'exact_primitive_coefficient_height': str(height),
               'coefficient_height_upper_bound': '2^1020',
               'coefficient_height_bound_is_strict': True,
               'representation': 'Complete ordinary integer residuals and quartic '
                                 'coefficient table; no coefficient symbol remains.'}
    return emit('quartic-direct-small-coefficients-1338', variables, rows, polynomial,
                {}, None, parent, certificate, report)


def inline_initial_chain():
    parent_obj, parent = load_parent('quartic-direct-small-coefficients-1338')
    assert parent['uncompressed_sha256'] == '69a280afdd6a98f6b13ac3b9455baf36b92cc3bd203d7664860269004baab0a8'
    assert parent_obj['fixed_constants'] == {}
    original = parent_obj['residuals']
    constants = {58: 3**32, 59: 3**64, 60: 3**128}
    assert parse(original[46]['terms']) == {((), 0): 3**32, ((58,), 0): -1}
    assert parse(original[47]['terms']) == {((58, 58), 0): 1, ((59,), 0): -1}
    assert parse(original[48]['terms']) == {((59, 59), 0): 1, ((60,), 0): -1}
    assert parse(original[49]['terms']) == {((60, 60), 0): 1, ((61,), 0): -1}
    for v, indices in [(58, [46, 47]), (59, [47, 48]), (60, [48, 49])]:
        assert [i for i, row in enumerate(original)
                if any(v in m for m, k, c in row['terms'])] == indices
    index_map = [None if 58 <= i <= 60 else i if i < 58 else i - 3
                 for i in range(len(parent_obj['variables']))]
    replacement = {i: {((), 0): Q(constants[i])} if i in constants
                   else {((index_map[i],), 0): Q(1)}
                   for i in range(len(parent_obj['variables']))}
    rows = []
    for i, row in enumerate(original):
        transformed = substitute(parse(row['terms']), replacement)
        if i in (46, 47, 48):
            assert not transformed
            continue
        new_row = deepcopy(row)
        new_row['terms'] = dump(transformed)
        rows.append(new_row)
    assert parse(rows[46]['terms']) == {((), 0): 3**256, ((58,), 0): -1}
    polynomial = square_sum(rows)
    assert polynomial == substitute(parse(parent_obj['expanded_polynomial']), replacement)
    assert all(k == 0 for m, k in polynomial)
    variables = []
    for old in parent_obj['variables']:
        if old['index'] in constants:
            continue
        new = deepcopy(old)
        new['parent_index'] = old['index']
        new['index'] = len(variables)
        variables.append(new)
    certificate = {
        'kind': 'inline three uniquely defined initial constants',
        'input_coordinate_fixed': 0,
        'deleted_parent_coordinates': [58, 59, 60],
        'deleted_parent_residual_indices': [46, 47, 48],
        'affected_other_parent_residual_indices': [49],
        'constant_substitutions': {'X58': '3^32', 'X59': '3^64', 'X60': '3^128'},
        'old_to_new_coordinate_indices': index_map,
        'parent_from_new': 'Insert the three specified constants; old indices above60 '
                           'are three greater than their new indices.',
        'new_from_parent_on_residual_solutions': 'Delete coordinates58,59,60.',
        'parent_deleted_residuals': [original[i]['terms'] for i in (46, 47, 48)],
        'parent_first_remaining_chain_residual': original[49]['terms'],
        'new_first_remaining_chain_residual': rows[46]['terms'],
        'identity_checked': 'P_new=P_parent after the displayed constant substitution. '
                            'The three deleted residuals become identicallyzero.',
        'field_scope': 'A bijection of common residual zero sets over every '
                       'characteristic-zero field; equality of literal SOS input '
                       'projections follows over formally real fields, including Q.'}
    report = stats(variables, rows, polynomial)
    assert report['total_variables'] == 1335 and report['quadratic_residuals'] == 1292
    height = max(abs(c.numerator) for c in polynomial.values())
    parent_height = max(abs(c) for m, k, c in parent_obj['expanded_polynomial'])
    assert height == parent_height and height.bit_length() <= 1020
    assert (3**512).bit_length() == 812
    report |= {'exact_primitive_coefficient_height': str(height),
               'coefficient_height_upper_bound': '2^1020',
               'coefficient_height_bound_is_strict': True,
               'height_unchanged_from_parent': True,
               'first_retained_chain_constant': '3^256',
               'new_squared_constant_bits': 812,
               'representation': 'Complete ordinary integer residuals and quartic '
                                 'coefficient table; no coefficient symbol remains.'}
    return emit('quartic-direct-small-coefficients-1335', variables, rows, polynomial,
                {}, None, parent, certificate, report)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--initial-chain-only', action='store_true',
                        help='Read the frozen1338 package and emit only its1335 refinement.')
    args = parser.parse_args()
    outputs = [inline_initial_chain()] if args.initial_chain_only else [
        translate(), eliminate(), inline_initial_chain()]
    print(json.dumps({'status': 'PASS', 'outputs': outputs}, indent=2))


if __name__ == '__main__':
    main()
