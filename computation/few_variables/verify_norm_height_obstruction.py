#!/usr/bin/env python3
"""Exact finite-field certificate for the split-prime height obstruction."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def reduce_rational(value, p):
    value = Fraction(value)
    return value.numerator*pow(value.denominator, -1, p) % p


def add(P, Q, D, p):
    if P is None:
        return Q
    if Q is None:
        return P
    x, y = P
    u, v = Q
    if x == u and (y+v) % p == 0:
        return None
    if P == Q:
        slope = (3*x*x-D)*pow(2*y, -1, p) % p
    else:
        slope = (v-y)*pow(u-x, -1, p) % p
    xx = (slope*slope-x-u) % p
    yy = (slope*(x-xx)-y) % p
    assert (yy*yy-xx*xx*xx+D*xx) % p == 0
    return xx, yy


def multiply(n, P, D, p):
    out = None
    while n:
        if n & 1:
            out = add(out, P, D, p)
        P = add(P, P, D, p)
        n //= 2
    return out


def main():
    p = 41
    rows = []
    for root, expected_D, expected_P, expected_order in [
            (17, 32, (4, 10), 13), (24, 31, (0, 0), 2)]:
        assert root*root % p == 2
        D = (11-6*root) % p
        P = ((reduce_rational(Fraction(57, 8), p)-reduce_rational(Fraction(7, 2), p)*root) % p,
             (reduce_rational(Fraction(-165, 8), p)+reduce_rational(Fraction(417, 32), p)*root) % p)
        assert D == expected_D and P == expected_P
        assert (P[1]**2-P[0]**3+D*P[0]) % p == 0
        assert (64*D**3) % p != 0
        multiples = [multiply(j, P, D, p) for j in range(1, expected_order+1)]
        assert all(Q is not None for Q in multiples[:-1]) and multiples[-1] is None
        rows.append({'sqrt2': root, 'D': D, 'point': list(P), 'exact_reduction_order': expected_order,
                     'thirteenth_multiple': multiply(13, P, D, p),
                     'all_multiples_until_order': multiples})
    report = {
        'status': 'passed', 'prime': p, 'reductions': rows,
        'proved_local_pattern': 'x(13P) has a negative valuation at sqrt(2)=17 and a positive valuation at sqrt(2)=24.',
        'consequence': 'For C=x(13P)^4, h(Norm(C))<2h(C). No assertion excluding all other height comparisons is made.',
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (HERE/'norm-height-obstruction-verification.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
