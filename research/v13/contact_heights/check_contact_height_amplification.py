#!/usr/bin/env python3
"""Exact finite certificate for disjoint rational contact sets.

This does not verify or assume a numerical instance of the underlying
arithmetic height hypothesis. Only the explicitly specified finite
linear algebra, exceptional sets and exponent inequalities are checked.
"""
from argparse import ArgumentParser
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import gcd, isqrt, prod
from pathlib import Path
import json


@lru_cache(maxsize=None)
def factor(n):
    n = abs(n)
    assert n != 0
    original = n
    result = {}
    d = 2
    while d*d <= n:
        while n % d == 0:
            result[d] = result.get(d, 0) + 1
            n //= d
        d = 3 if d == 2 else d+2
    if n > 1:
        result[n] = result.get(n, 0) + 1
    assert prod(p**e for p, e in result.items()) == original
    # Independent primality verification of every returned factor.
    for p in result:
        assert all(p % k for k in range(2, isqrt(p)+1))
    return result


def forms(r):
    return [(j, k, a, b) for j in range(r)
            for k, (a, b) in enumerate([
                (1, -3*j), (2, 1-6*j), (1, 1-3*j),
                (2399, -(7197*j+1)), (407, 32-1221*j)])]


def check(r):
    ls = forms(r)
    theta = [Fraction(0), Fraction(-1, 2), Fraction(-1),
             Fraction(1, 2399), Fraction(-32, 407)]
    roots = [Fraction(-b, a) for j, k, a, b in ls]
    assert roots == [3*j+c for j in range(r) for c in theta]
    assert len(set(roots)) == 5*r and Fraction(1) not in roots
    assert all(gcd(a, b) == 1 for j, k, a, b in ls)
    exceptional = set()
    integer_count = 0
    largest = 1
    for j, k, a, b in ls:
        for z in (a, a+b):
            assert z != 0
            exceptional.update(factor(z))
            largest = max(largest, abs(z))
            integer_count += 1
    for (_, _, a, b), (_, _, c, d) in combinations(ls, 2):
        det = a*d-c*b
        assert det != 0
        exceptional.update(factor(det))
        largest = max(largest, abs(det))
        integer_count += 1
    extra = sorted(p for p in exceptional if p > 76176)
    E = prod(extra)
    norms = []
    for j in range(r):
        A = ((2, 1-6*j), (1, -3*j))
        B = ((3*j, 1-6*j), (1, -2))
        assert A[0][0]*A[1][1]-A[0][1]*A[1][0] == -1
        assert [[sum(A[i][k]*B[k][h] for k in range(2))
                 for h in range(2)] for i in range(2)] == [[1, 0], [0, 1]]
        norm = max(sum(map(abs, row)) for row in B)
        assert norm == max(3, 9*j-1)
        norms.append(norm)
        # Each source contact form pulls back to the listed integral form.
        u, v = A
        pulled = [v, u, tuple(u[k]-v[k] for k in range(2)),
                  tuple(2401*v[k]-u[k] for k in range(2)),
                  tuple(32*u[k]+343*v[k] for k in range(2))]
        assert pulled == [(a, b) for jj, kk, a, b in ls if jj == j]
    assert max(norms) == max(3, 9*r-10)
    k = 38//r+1
    mu = 19//(2*r)+1
    assert r*k > 38 and (k == 1 or r*(k-1) <= 38)
    assert 2*r*mu > 19 and (mu == 1 or 2*r*(mu-1) <= 19)
    d = 5*r
    epsilon = 1 if r % 2 else 2
    assert (d+epsilon) % 2 == 0 and 4-epsilon > 0
    # Exponents of (F,a,delta) in all rational normalization identities.
    R = (1, -d, -d-epsilon)
    e = (-1, d, d)
    q = (-1, d, d+epsilon-4)
    assert tuple(R[i]+e[i]+(epsilon if i == 2 else 0)
                 for i in range(3)) == (0, 0, 0)
    assert tuple(q[i]+(4-epsilon if i == 2 else 0)
                 for i in range(3)) == e
    return {
        'r': r, 'number_of_contacts': 5*r,
        'forms': [{'translate': j, 'contact': k, 'a': a, 'b': b}
                  for j, k, a, b in ls],
        'all_roots_distinct_and_not_one': True,
        'primitive_forms': True, 'unimodular_transforms': True,
        'factored_integer_count': integer_count,
        'largest_factored_integer': largest,
        'extra_exceptional_primes': extra,
        'extra_exceptional_prime_product': str(E),
        'height_norm': max(norms), 'height_exponent': str(Fraction(19, r)),
        'least_residual_order_k': k, 'least_input_order_mu': mu,
        'normalizing_delta_exponent': d+epsilon,
        'q_clearing_delta_exponent': 4-epsilon,
        'normalization_identities': 'PASS'
    }


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    values = [1, 2, 3, 4, 5, 6, 7, 10, 13, 20, 39]
    records = [check(r) for r in values]
    result = {
        'status': 'PASS',
        'scope': 'Exact finite algebra only; all height conclusions retain the stated five-contact arithmetic premise.',
        'base_prime_cutoff': 76176,
        'records': records
    }
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'records': [
        {key: rec[key] for key in ['r', 'number_of_contacts',
                                  'extra_exceptional_primes',
                                  'least_residual_order_k', 'least_input_order_mu']}
        for rec in records]}, indent=2))


if __name__ == '__main__':
    main()
