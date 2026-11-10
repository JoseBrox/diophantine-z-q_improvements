#!/usr/bin/env python3
"""Exact checks for quadratic covers of the six-contact function.

This independent, standard-library checker verifies the universal section
by polynomial identities, reconstructs T(3) in two ways, and certifies an
inert-prime obstruction to that section. The genus and finiteness statements
are proved in the companion paper; they are not inferred from samples.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import argparse
import json


def trim(p):
    p = list(p)
    while len(p) > 1 and not p[-1]:
        p.pop()
    return tuple(p)


def padd(*ps):
    out = [F(0)] * max(map(len, ps))
    for p in ps:
        for j, c in enumerate(p):
            out[j] += c
    return trim(out)


def pscale(c, p):
    return trim([F(c)*x for x in p])


def pmul(a, b):
    out = [F(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return trim(out)


def ppow(a, n):
    out = (F(1),)
    for _ in range(n):
        out = pmul(out, a)
    return out


def pprod(ps):
    out = (F(1),)
    for p in ps:
        out = pmul(out, p)
    return out


def homogeneous_F(u, v):
    return pscale(F(1, 120), pprod([
        u, padd(u, v), padd(pscale(2, u), v),
        padd(pscale(3, u), v), padd(pscale(4, u), v),
        padd(pscale(5, u), pscale(2, v))]))


def rational_R(t):
    return (t*(t+1)*(2*t+1)*(3*t+1)*(4*t+1)*(5*t+2)
            / (120*(t-1)**8))


def valuation(q, p):
    q = F(q)
    assert q
    a, b = abs(q.numerator), q.denominator
    v = 0
    while a % p == 0:
        a //= p
        v += 1
    while b % p == 0:
        b //= p
        v -= 1
    return v


def residue(q, modulus):
    q = F(q)
    return q.numerator*pow(q.denominator, -1, modulus) % modulus


def q(a=0, b=0):
    return F(a), F(b)


def qa(*xs):
    return tuple(sum((x[j] for x in xs), F(0)) for j in (0, 1))


def qn(x):
    return -x[0], -x[1]


def qm(x, y):
    a, b = x
    c, d = y
    return a*c+2*b*d, a*d+b*c


def qi(x):
    a, b = x
    norm = a*a-2*b*b
    assert norm
    return a/norm, -b/norm


def qd(x, y):
    return qm(x, qi(y))


def qp(x, n):
    out = q(1)
    for _ in range(n):
        out = qm(out, x)
    return out


def on_curve(P, D):
    return P is None or qp(P[1], 2) == qa(qp(P[0], 3), qn(qm(D, P[0])))


def add_point(P, Q, D):
    if P is None:
        return Q
    if Q is None:
        return P
    x, y = P
    xx, yy = Q
    if x == xx and y == qn(yy):
        return None
    if P == Q:
        slope = qd(qa(qm(q(3), qp(x, 2)), qn(D)), qm(q(2), y))
    else:
        slope = qd(qa(yy, qn(y)), qa(xx, qn(x)))
    X = qa(qp(slope, 2), qn(x), qn(xx))
    Y = qa(qm(slope, qa(x, qn(X))), qn(y))
    result = X, Y
    assert on_curve(result, D)
    return result


def finite_add(P, Q, p, D):
    def add(x, y):
        return (x[0]+y[0]) % p, (x[1]+y[1]) % p

    def neg(x):
        return -x[0] % p, -x[1] % p

    def mul(x, y):
        return ((x[0]*y[0]+2*x[1]*y[1]) % p,
                (x[0]*y[1]+x[1]*y[0]) % p)

    def div(x, y):
        z = pow((y[0]*y[0]-2*y[1]*y[1]) % p, -1, p)
        return mul(x, (y[0]*z % p, -y[1]*z % p))

    if P is None:
        return Q
    if Q is None:
        return P
    x, y = P
    xx, yy = Q
    if x == xx and y == neg(yy):
        return None
    if P == Q:
        slope = div(add(mul((3, 0), mul(x, x)), neg(D)), mul((2, 0), y))
    else:
        slope = div(add(yy, neg(y)), add(xx, neg(x)))
    X = add(add(mul(slope, slope), neg(x)), neg(xx))
    Y = add(mul(slope, add(x, neg(X))), neg(y))
    assert mul(Y, Y) == add(mul(mul(X, X), X), neg(mul(D, X)))
    return X, Y


def finite_multiple(n, P, p, D):
    out = None
    while n:
        if n & 1:
            out = finite_add(out, P, p, D)
        P = finite_add(P, P, p, D)
        n //= 2
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path,
                    default=Path(__file__).with_name('quadratic-contact-covers-certificate.json'))
    args = ap.parse_args()
    one, aa = (F(1),), (F(0), F(1))
    u = pscale(-1, padd(aa, one))
    v0, v1 = pscale(5, aa), (F(5),)
    r0n = pmul(homogeneous_F(u, v0), ppow(v0, 2))
    r0d = ppow(padd(u, pscale(-1, v0)), 8)
    r1n = pmul(homogeneous_F(u, v1), ppow(v1, 2))
    r1d = ppow(padd(u, pscale(-1, v1)), 8)
    linear_factors = [(1, 1), (-4, 1), (-3, 2),
                      (-2, 3), (-1, 4), (-1, 1)]
    six = pprod([tuple(map(F, t)) for t in linear_factors])
    section_n = pscale(25, pmul(aa, six))
    section_d = pscale(24, pmul(ppow((F(6), F(1)), 4),
                               ppow((F(1), F(6)), 4)))
    assert padd(pmul(pmul(r0n, r1n), ppow(section_d, 2)),
                pmul(ppow(section_n, 2), pmul(r0d, r1d))) == (0,)
    assert padd(pscale(24, pmul(r1n, ppow((F(6), F(1)), 8))),
                pscale(-25, pmul(six, r1d))) == (0,)

    nonzero_contacts = list(map(F, [-1]))+[F(-1, 2), F(-1, 3), F(-1, 4), F(-2, 5)]
    collision_scales = sorted({x/y for x in nonzero_contacts for y in nonzero_contacts})
    assert min(collision_scales) == F(1, 4) and max(collision_scales) == 4
    assert len(set(nonzero_contacts)) == 5
    # Therefore a>4 leaves ten distinct branch points, all simple.
    assert (10-2)//2 == 4 and (6-2)//2 == 2

    D = q(11, -6)
    P = q(F(57, 8), F(-7, 2)), q(F(-165, 8), F(417, 32))
    R0 = q(1, 1), q(0, 2)
    assert on_curve(P, D) and on_curve(R0, D)
    assert add_point(R0, R0, D) == P
    P3 = add_point(add_point(P, P, D), P, D)
    x, y = P
    psi2 = qm(q(2), y)
    psi3 = qa(qm(q(3), qp(x, 4)), qn(qm(q(6), qm(D, qp(x, 2)))), qn(qp(D, 2)))
    psi4 = qm(qm(q(4), y), qa(qp(x, 6), qn(qm(q(5), qm(D, qp(x, 4)))),
              qn(qm(q(5), qm(qp(D, 2), qp(x, 2)))), qp(D, 3)))
    x3_division = qa(x, qn(qd(qm(psi2, psi4), qp(psi3, 2))))
    assert x3_division == P3[0]
    T3 = 2*P3[0][0]
    assert T3 == F(59609817879309699127684977, 508847420105479203017476)
    a3 = F(3)**8+T3**8
    lam = -(a3+1)/(5*a3)
    t1 = a3*lam
    r0, r1 = rational_R(lam), rational_R(t1)
    section_q = (25*a3*(a3-4)*(a3-1)*(a3+1)*(2*a3-3)*(3*a3-2)*(4*a3-1)
                 /(24*(a3+6)**4*(6*a3+1)**4))
    assert r0 < 0 < r1 and r0*r1 == -section_q**2
    assert F(-1, 4) < lam < F(-1, 5) and t1 < -1

    p = 315467
    assert p > 76176 and all(p % d for d in range(2, isqrt(p)+1))
    assert p % 8 == 3 and pow(2, (p-1)//2, p) == p-1
    assert all(t.denominator % p for point in (P, P3) for xy in point for t in xy)
    assert valuation(a3-4, p) == 1
    assert valuation(r0, p) == valuation(r1, p) == 1
    assert valuation(lam+F(1, 4), p) == valuation(t1+1, p) == 1
    fp = tuple(tuple(residue(t, p) for t in xy) for xy in P)
    fd = tuple(residue(t, p) for t in D)
    m = p+1
    assert finite_multiple(m, fp, p, fd) is None
    # Independent addition order: sum binary powers from the highest bit.
    acc = None
    for bit in bin(m)[2:]:
        acc = finite_add(acc, acc, p, fd)
        if bit == '1':
            acc = finite_add(acc, fp, p, fd)
    assert acc is None
    actual_order = m
    for ell in (2, 3, 23, 127):
        while actual_order % ell == 0 and finite_multiple(actual_order//ell, fp, p, fd) is None:
            actual_order //= ell
    assert m % actual_order == 0
    modulus = 2*p*p*m
    report = {
        'status': 'PASS',
        'symbolic_identities': [
            'R(-(a+1)/(5a))*R(-(a+1)/5)=-section_q(a)^2',
            'R(-(a+1)/5)=25*(a+1)*(a-4)*(2a-3)*(3a-2)*(4a-1)*(a-1)/(24*(a+6)^8)'],
        'nonzero_contact_collision_scales': list(map(str, collision_scales)),
        'genus_proof_data': {'single_contact_branch_count': 6, 'single_genus': 2,
                            'product_branch_count_for_a_gt4': 10, 'product_genus': 4},
        'trace_reconstruction': {'T3': str(T3), 'methods': ['chord-and-tangent addition', 'third division polynomial']},
        'inert_prime': p,
        'primality_method': 'Trial division through isqrt(p)',
        'legendre_2': -1,
        'a3_mod_p2': residue(a3, p*p),
        'a3_minus4_over_p_mod_p': residue((a3-4)/p, p),
        'contact_valuations': {'lambda_plus_quarter': 1, 'a_lambda_plus_one': 1,
                               'R_lambda': 1, 'R_a_lambda': 1},
        'P_mod_p': fp,
        'P3_affine_integral_at_p': True,
        'certified_annihilator_mod_p': m,
        'computed_point_order_mod_p': actual_order,
        'shift_progression': {'residue': 3, 'modulus': modulus,
                             'explanation': 'For every nonnegative k, B=3+k*modulus, X=0,n=B preserves a(B)=4 modulo p with depth exactly1; the formal group and congruence argument is proved in the paper.'},
        'scope': 'Certifies identities and one explicit inert-prime obstruction to the displayed section. It does not exclude every rational point on the genus-four cover or prove a new defining-variable count.'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ('status', 'inert_prime', 'a3_mod_p2',
                      'a3_minus4_over_p_mod_p', 'computed_point_order_mod_p', 'shift_progression')}))


if __name__ == '__main__':
    main()
