#!/usr/bin/env python3
"""Exact checks for the two displayed anisotropic forms over Q(i).

Only Python's standard library is required. The cubic coefficient formula
is checked by independent symbolic expansion of a multiplication matrix.
Complete residue-field checks certify the finite norm assertions used
in the valuation proof; they are not a search for number-field zeros.
"""
from collections import defaultdict
from hashlib import sha256
from itertools import permutations, product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent


def poly_add(*terms):
    result = defaultdict(int)
    for term in terms:
        for monomial, coefficient in term.items():
            result[monomial] += coefficient
    return {m: c for m, c in result.items() if c}


def poly_scale(poly, scalar):
    return {m: scalar*c for m, c in poly.items() if scalar*c}


def poly_mul(a, b):
    result = defaultdict(int)
    for am, ac in a.items():
        for bm, bc in b.items():
            result[tuple(sorted(am+bm))] += ac*bc
    return {m: c for m, c in result.items() if c}


def determinant(matrix):
    n = len(matrix)
    terms = []
    for permutation in permutations(range(n)):
        inversions = sum(permutation[i] > permutation[j]
                         for i in range(n) for j in range(i+1, n))
        term = {(): (-1)**inversions}
        for i, j in enumerate(permutation):
            term = poly_mul(term, matrix[i][j])
        terms.append(term)
    return poly_add(*terms)


def gauss_add(x, y, modulus=None):
    a, b = x[0]+y[0], x[1]+y[1]
    return (a % modulus, b % modulus) if modulus else (a, b)


def gauss_mul(x, y, modulus=None):
    a, b = x[0]*y[0]-x[1]*y[1], x[0]*y[1]+x[1]*y[0]
    return (a % modulus, b % modulus) if modulus else (a, b)


def gauss_pow(x, n, modulus=None):
    result = (1, 0)
    for _ in range(n):
        result = gauss_mul(result, x, modulus)
    return result


def main():
    path = ROOT/'anisotropic_forms.json'
    data = json.loads(path.read_text())
    a, b, c = ({(i,): 1} for i in range(3))
    minus_b_c = poly_scale(poly_add(b, c), -1)
    matrix = [[a, poly_scale(c, -1), poly_scale(b, -1)],
              [b, poly_add(a, poly_scale(c, -1)), minus_b_c],
              [c, b, poly_add(a, poly_scale(c, -1))]]
    computed_norm = determinant(matrix)
    recorded_norm = {tuple(t['variables']): t['coefficient']
                     for t in data['cubic']['norm_terms']}
    assert computed_norm == recorded_norm
    assert len(computed_norm) == 8

    expected_cubic = {}
    for block, weight in enumerate([(1, 0), (1, 1), (0, 2)]):
        for monomial, coefficient in computed_norm.items():
            expected_cubic[tuple(i+3*block for i in monomial)] = (
                coefficient*weight[0], coefficient*weight[1])
    recorded_cubic = {tuple(t['variables']): tuple(t['coefficient'])
                      for t in data['cubic']['terms']}
    assert recorded_cubic == expected_cubic
    assert len(recorded_cubic) == 24
    assert all(len(m) == 3 for m in recorded_cubic)

    # Irreducibility of U^3+U+1 over F_2 and the complete norm table.
    assert all((u**3+u+1) % 2 for u in range(2))
    cubic_units = 0
    for values in product(range(2), repeat=3):
        value = 0
        for monomial, coefficient in computed_norm.items():
            term = coefficient
            for variable in monomial:
                term *= values[variable]
            value += term
        assert bool(value % 2) == bool(any(values))
        cubic_units += bool(any(values))
    assert cubic_units == 7

    # F_9 = F_3[i]/(i^2+1); 1+i is a nonsquare.
    assert all((u*u+1) % 3 for u in range(3))
    alpha = (1, 1)
    assert gauss_pow(alpha, 4, 3) == (2, 0)
    field9 = list(product(range(3), repeat=2))
    assert alpha not in {gauss_pow(x, 2, 3) for x in field9}
    quadratic_units = 0
    for x, y in product(field9, repeat=2):
        norm = gauss_add(gauss_pow(x, 2, 3),
                         gauss_mul((-1, -1), gauss_pow(y, 2, 3), 3), 3)
        assert bool(norm != (0, 0)) == bool(x != (0, 0) or y != (0, 0))
        quadratic_units += norm != (0, 0)
    assert quadratic_units == 80
    expected_quadratic = {(0, 0): (1, 0), (1, 1): (-1, -1),
                          (2, 2): (3, 0), (3, 3): (-3, -3)}
    recorded_quadratic = {tuple(t['variables']): tuple(t['coefficient'])
                          for t in data['quadratic']['terms']}
    assert expected_quadratic == recorded_quadratic
    assert gauss_pow((1, 1), 2) == (0, 2)

    result = {
        'status': 'PASS',
        'cubic_norm_identity': 'exact symbolic determinant expansion',
        'cubic_norm_monomials': 8, 'cubic_form_monomials': 24,
        'cubic_nonzero_residue_vectors_checked': cubic_units,
        'quadratic_nonzero_residue_vectors_checked': quadratic_units,
        'complete_residue_checks': True,
        'number_field_anisotropy_basis': 'proved least-valuation argument in Lemma sys:anisotropic-form',
        'unproved_arithmetic_inputs': [],
        'data_sha256': sha256(path.read_bytes()).hexdigest(),
        'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (ROOT/'anisotropic-forms-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
