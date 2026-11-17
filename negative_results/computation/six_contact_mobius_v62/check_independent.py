#!/usr/bin/env python3
"""Standard-library cross-check using explicit interpolation, not nullspaces.

All rational-function identities are checked by exact polynomial coefficient
multiplication. This check is independent of SymPy and the main script.
"""
from fractions import Fraction as Q
from functools import reduce
from hashlib import sha256
from itertools import permutations
from math import gcd, lcm
from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[3]
PAPER = ROOT / 'negative_results/papers/pole_parameters/six_contact_mobius_obstruction_20261117_v62.tex'
R = (Q(0), Q(-1), Q(-1, 2), Q(-1, 3), Q(-1, 4), Q(-2, 5))


def polynomial_product(factors):
    result = [Q(1)]
    for factor in factors:
        product = [Q(0)] * (len(result)+len(factor)-1)
        for i, a in enumerate(result):
            for j, b in enumerate(factor):
                product[i+j] += a*b
        result = product
    return result


def normalize(matrix):
    denom = lcm(*(x.denominator for x in matrix))
    entries = [int(x*denom) for x in matrix]
    content = reduce(gcd, entries)
    entries = [x//content for x in entries]
    if next(x for x in entries if x) < 0:
        entries = [-x for x in entries]
    return tuple(entries)


def group_and_identities():
    group = set()
    for u, v, w in permutations(R, 3):
        # Solve explicitly for the images of 0, -1, -1/2.
        D = v-w
        C = u+v-2*w
        A = v*C+(u-v)*D
        B = u*D
        matrix = normalize((A, B, C, D))
        A, B, C, D = matrix
        if A*D-B*C == 0 or any(C*r+D == 0 for r in R):
            continue
        if {(A*r+B)/(C*r+D) for r in R} == set(R):
            group.add(matrix)
    assert len(group) == 12
    base = polynomial_product([[-r, Q(1)] for r in R])
    rows = []
    for A, B, C, D in sorted(group):
        image = polynomial_product([[B-r*D, A-r*C] for r in R])
        kappa = image[-1]
        assert image == [kappa*x for x in base]
        rows.append({'matrix': [A, B, C, D], 'multiplier': str(kappa)})
    return group, rows


def uniform_gaps(group):
    cases = 0
    margins = {}
    for e in (4, 6):
        q = 4**e
        p = q*4**e+57**e
        current = []
        for A, B, C, D in sorted(group):
            if B == 0:
                continue
            K = 4*B*C*(A*D-B*C)
            n1 = D*D
            n0 = -D*A+2*C*B
            # Coefficients of p^2,pq,q^2 in D^2 G = N^2 + K q^2.
            assert [D**4, D*D*(-2*D*A+4*C*B), D*D*A*A] == [n1*n1, 2*n1*n0, n0*n0+K]
            N = n1*p+n0*q
            margin = 2*N-1-abs(K)*q*q
            assert N > 0 and K != 0 and margin > 0
            current.append(margin)
            cases += 1
        margins[e] = min(current)
    assert cases == 20
    return cases, margins


def integer_valuation(n, p):
    assert n
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def fixture_values():
    p = 76253
    assert all(p % d != 0 for d in range(2, 277))
    assert pow(2, (p-1)//2, p) == p-1
    rows = []
    for e, B in [(4, 88285), (6, 99329)]:
        q = 4**e
        numerator = q*(B+1)**e+57**e
        factors = [numerator-q, numerator+q, 4*numerator-q,
                   3*numerator-2*q, 2*numerator-3*q, numerator-4*q]
        orders = [integer_valuation(x, p) for x in factors]
        assert sum(orders) == 1
        # These are exactly the denominator and scale units at t=lambda, a lambda.
        for unit in [numerator, numerator+q, 6*numerator+q, numerator+6*q, q]:
            assert unit % p != 0
        rows.append({'exponent': e, 'shift': B, 'factor_valuations': orders,
                     'progression_modulus': 2*p*p})
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    group, rows = group_and_identities()
    cases, margins = uniform_gaps(group)
    record = {'status': 'PASS', 'source_sha256': sha256(PAPER.read_bytes()).hexdigest(),
              'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'method': 'Explicit fractional interpolation and polynomial coefficient multiplication; no SymPy.',
              'ordered_image_triples': 120, 'automorphisms': rows,
              'uniform_square_gap_cases': cases, 'minimum_gap_margins': margins,
              'integer_numerator_fixtures': fixture_values()}
    if args.output:
        args.output.write_text(json.dumps(record, indent=2)+'\n')
    print('PASS: independent exact interpolation, 12 polynomial identities, 20 square gaps, 2 integer-numerator fixtures.')


if __name__ == '__main__':
    main()
