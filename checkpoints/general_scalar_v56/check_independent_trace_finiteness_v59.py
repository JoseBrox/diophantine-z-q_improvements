#!/usr/bin/env python3
"""Exact algebraic inputs to the independent-point finiteness proof.

The CM scaling and all nonzero direction parities are checked exactly.
Mordell--Lang, the endomorphism descent, and real nonconstancy are
proved geometrically; they are not inferred from these finite checks.
"""
from fractions import Fraction as Q
from pathlib import Path
import json


def add(a, b):
    return (a[0]+b[0], a[1]+b[1])


def neg(a):
    return (-a[0], -a[1])


def mul(a, b):
    return (a[0]*b[0]+2*a[1]*b[1], a[0]*b[1]+a[1]*b[0])


def inv(a):
    norm = a[0]*a[0]-2*a[1]*a[1]
    assert norm
    return (a[0]/norm, -a[1]/norm)


def power(a, n):
    result = (Q(1), Q(0))
    for _ in range(n):
        result = mul(result, a)
    return result


def scalar(c):
    return (Q(c), Q(0))


def rank_mod_two(rows):
    a = [[v % 2 for v in row] for row in rows]
    rank = 0
    for column in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][column]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        for i in range(len(a)):
            if i != rank and a[i][column]:
                a[i] = [(x+y) % 2 for x, y in zip(a[i], a[rank])]
        rank += 1
    return rank


def certify_directions(rows):
    r = len(rows[0])
    assert rank_mod_two(rows) == r
    witnesses = []
    for mask in range(1, 2**r):
        vector = [(mask >> i) & 1 for i in range(r)]
        odd = [j for j, row in enumerate(rows)
               if sum(x*y for x, y in zip(vector, row)) % 2]
        assert odd
        witnesses.append(odd[0])
    return {'number_of_roles': r, 'matrix_rank_modulo_two': r,
            'tested_point_matrix': rows,
            'nonzero_parity_vectors_checked': len(witnesses),
            'first_odd_test_by_nonzero_binary_mask': witnesses}


d, dp = (Q(3), Q(-1)), (Q(3), Q(1))
assert mul(d, dp) == scalar(7)
q = mul(dp, inv(d))
assert q == (Q(11, 7), Q(6, 7))
assert q == mul(scalar(7), inv(power(d, 2)))
# x' = q*x, y' = (7*sqrt(7)/d^3)*y.
# Its y-scaling square is 343/d^6 = q^3, and q^2*d^2=dp^2.
assert power(q, 3) == mul(scalar(343), inv(power(d, 6)))
assert mul(power(q, 2), power(d, 2)) == power(dp, 2)

# Conditional role order: A,H,U. Constants such as P have zero direction.
conditional = [[0, 1, 0], [0, 0, 1],
               [0, 1, 0], [-1, 0, 1]]

# General role order: Q1,Q2,Q3,Q4,H,U1,U2,U3,U4.
general = []
for index in (4, 5, 6, 7, 8):
    row = [0]*9
    row[index] = 1
    general.append(row)
general.append(general[0][:])  # H-P
for i in range(4):
    row = [0]*9
    row[5+i] = 1
    row[i] = -1
    general.append(row)

report = {
    'status': 'PASS',
    'exact_field': 'Q(sqrt(2)) using pairs of rational fractions',
    'CM_isomorphism': 'x -> 7*x/d^2; y -> 7*sqrt(7)*y/d^3',
    'CM_isomorphism_identities_checked': True,
    'conditional': certify_directions(conditional),
    'general': certify_directions(general),
    'mathematical_inputs_not_replaced_by_computation': [
        '7 is not a square in K(i)',
        'Galois descent of geometric CM endomorphisms',
        'Poincare complete reducibility over Q',
        'surjectivity of odd multiplication on real elliptic curves',
        'nonconstancy on each guarded rational abelian translate',
        'Mordell--Lang for the rational subgroup'],
    'scope': 'Fixed input and fixed positive block-0 coefficients',
    'variable_slope_or_point_dependent_curve_coefficients_excluded': False,
    'new_defining_variable_bound_proved': False,
}
out = Path(__file__).with_name('independent_trace_finiteness_v59_certificate.json')
out.write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({'status': 'PASS', 'CM_identities': True,
                  'parity_vectors_checked': 7+511}))
