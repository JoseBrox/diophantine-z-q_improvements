#!/usr/bin/env python3
"""Exact identities and an infinite-family certificate for six contacts.

All polynomial arithmetic uses integer coefficient lists in ascending order.
Finite evaluations supplement, but do not replace, the symbolic identities.
This is an obstruction to an unrestricted contact-height inequality, not a
counterexample to the restricted thirteen-variable defining source.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import hashlib
import json


def add(a, b):
    out = [0] * max(len(a), len(b))
    for i, c in enumerate(a):
        out[i] += c
    for i, c in enumerate(b):
        out[i] += c
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def scale(a, n):
    return [n*c for c in a]


def mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, c in enumerate(a):
        for j, d in enumerate(b):
            out[i+j] += c*d
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def product(polynomials):
    out = [1]
    for p in polynomials:
        out = mul(out, p)
    return out


def evaluate(p, x):
    out = Q(0)
    for c in reversed(p):
        out = out*x+c
    return out


def check():
    x = [0, 1]
    factors = [[0, 1], [1, 1], [1, 2], [1, 3], [1, 4], [2, 5]]
    f = product(factors)  # 120 F(t)
    numerator, denominator = [-1, -2], [2, 3]
    transformed = product([add(scale(numerator, a), scale(denominator, b))
                           for b, a in factors])
    assert transformed == scale(f, -1)
    assert add(numerator, scale(denominator, -1)) == [-3, -5]
    matrix = [[-2, -1], [3, 2]]
    squared_matrix = [[sum(matrix[i][k]*matrix[k][j] for k in range(2))
                       for j in range(2)] for i in range(2)]
    assert squared_matrix == [[1, 0], [0, 1]]
    theta = [Q(0), Q(-1, 2), Q(-1, 4), Q(-2, 5), Q(-1), Q(-1, 3)]
    phi = lambda t: -(2*t+1)/(3*t+2)
    images = [phi(t) for t in theta]
    assert images == [theta[i] for i in (1, 0, 3, 2, 4, 5)]
    # For a(m)=m(m-2)/(2m-3): a-1=(m-1)(m-3)/(2m-3).
    a_numerator, a_denominator = [0, -2, 1], [-3, 2]
    assert add(a_numerator, scale(a_denominator, -1)) == mul([-1, 1], [-3, 1])
    # 2*m*(m-2)-(m-2)*(2m-3)=3*(m-2)>0 for m>=5.
    assert add(scale(a_numerator, 2), scale(mul([-2, 1], a_denominator), -1)) == [-6, 3]
    samples = 0
    F = lambda t: evaluate(f, t)/120
    R = lambda t: F(t)/(t-1)**8
    for m in range(5, 201):
        t = Q(-1, m)
        a = Q(m*(m-2), 2*m-3)
        u = a*t
        assert u == phi(t) and a > 1
        assert Q(-1, 4) < t < 0 and Q(-1, 2) < u < Q(-2, 5)
        assert t not in theta and u not in theta and t != 1 and u != 1
        square_root = F(t)*(3*t+2)/((t-1)**4*(5*t+3)**4)
        assert square_root and R(t)*R(u) == -square_root**2
        samples += 1
    return {
        'status': 'PASS',
        'polynomial_coefficient_order': 'ascending',
        '120F_coefficients': f,
        'homogeneous_transform_coefficients': transformed,
        'homogeneous_transform_multiplier': -1,
        'involution_matrix': matrix,
        'involution_matrix_square': squared_matrix,
        'contacts': [str(t) for t in theta],
        'contact_permutation_indices': [1, 0, 3, 2, 4, 5],
        'product_identity': 'R(t)R(phi(t))=-(F(t)(3t+2)/((t-1)^4(5t+3)^4))^2',
        'infinite_family': {'m': 'any integer at least 5', 'lambda': '-1/m',
                            'a': 'm(m-2)/(2m-3)', 'a_minus_one': '(m-1)(m-3)/(2m-3)',
                            'growth': 'a>(m-2)/2', 'odd_product_radical': 1},
        'exact_fraction_samples': samples,
        'sample_range': [5, 200],
        'restricted_abc_scale_verified': False,
        'remaining_source_witnesses_constructed': False,
        'scope': 'Universal polynomial identities and an unbounded positive-scale family obstructing an unrestricted one-product contact-height inequality. No counterexample to the restricted abc defining source is asserted.'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    result = check()
    result['checker_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    text = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
