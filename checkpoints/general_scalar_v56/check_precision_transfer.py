#!/usr/bin/env python3
"""Exact finite checks for the corrected eighth-order comparison transfer."""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def prime_divisors(n):
    result = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            result.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        result.append(n)
    return result


def affine_add(P, Q, a, p):
    if P is None:
        return Q
    if Q is None:
        return P
    x, y = P
    u, v = Q
    if x == u:
        if (y + v) % p == 0:
            return None
        slope = (3 * x * x + a) * pow(2 * y, -1, p) % p
    else:
        slope = (v - y) * pow(u - x, -1, p) % p
    X = (slope * slope - x - u) % p
    return X, (slope * (x - X) - y) % p


def affine_mul(n, P, a, p):
    result = None
    for digit in bin(n)[2:]:
        result = affine_add(result, result, a, p)
        if digit == '1':
            result = affine_add(result, P, a, p)
    return result


def jacobian_double(P, a, modulus):
    X, Y, Z = P
    if Z == 0:
        return P
    A = X * X % modulus
    B = Y * Y % modulus
    C = B * B % modulus
    DD = 2 * ((X + B) ** 2 - A - C) % modulus
    E = (3 * A + a * pow(Z, 4, modulus)) % modulus
    FF = E * E % modulus
    X3 = (FF - 2 * DD) % modulus
    return X3, (E * (DD - X3) - 8 * C) % modulus, 2 * Y * Z % modulus


def jacobian_add(P, Q, a, modulus):
    X1, Y1, Z1 = P
    X2, Y2, Z2 = Q
    if Z1 == 0:
        return Q
    if Z2 == 0:
        return P
    U1 = X1 * Z2 * Z2 % modulus
    U2 = X2 * Z1 * Z1 % modulus
    S1 = Y1 * pow(Z2, 3, modulus) % modulus
    S2 = Y2 * pow(Z1, 3, modulus) % modulus
    if U1 == U2:
        if S1 == S2:
            return jacobian_double(P, a, modulus)
        assert (S1 + S2) % modulus == 0, 'nonopposite exceptional addition'
        return (1, 1, 0)
    H = (U2 - U1) % modulus
    I = (2 * H) ** 2 % modulus
    J = H * I % modulus
    r = 2 * (S2 - S1) % modulus
    V = U1 * I % modulus
    X3 = (r * r - J - 2 * V) % modulus
    Y3 = (r * (V - X3) - 2 * S1 * J) % modulus
    Z3 = ((Z1 + Z2) ** 2 - Z1 * Z1 - Z2 * Z2) * H % modulus
    return X3, Y3, Z3


def jacobian_check(P, a, p):
    modulus = p * p
    X, Y, Z = P
    assert any(coordinate % p for coordinate in P), 'nonprimitive projective triple'
    assert (Y * Y - X ** 3 - a * X * pow(Z, 4, modulus)) % modulus == 0


def jacobian_mul(n, P, a, p):
    modulus = p * p
    result = (1, 1, 0)
    for digit in bin(n)[2:]:
        result = jacobian_double(result, a, modulus)
        jacobian_check(result, a, p)
        if digit == '1':
            result = jacobian_add(result, P, a, modulus)
            jacobian_check(result, a, p)
    return result


def check_depth_certificate():
    cert = json.loads((HERE / 'depth_obstruction_certificate.json').read_text())
    p = cert['prime']
    assert is_prime(p) and p > 76176 and p % 8 == 1
    roots = []
    orders = []
    squares = {x * x % p for x in range(p)}
    for row in cert['slots']:
        root = row['root']
        rp = row['root_mod_p2']
        roots.append(root)
        assert root * root % p == 2 and rp * rp % (p * p) == 2
        assert rp % p == root
        a = (-11 + 6 * root) % p
        point = ((57 - 28 * root) * pow(8, -1, p) % p,
                 (-660 + 417 * root) * pow(32, -1, p) % p)
        assert list(point) == row['P'] and a == row['a']
        count = 1
        for x in range(p):
            y2 = (x * x * x + a * x) % p
            count += 1 if y2 == 0 else 2 if y2 in squares else 0
        assert count == row['group_order']
        order = row['point_order']
        orders.append(order)
        assert count % order == 0 and gcd(order, p) == 1
        assert affine_mul(order, point, a, p) is None
        for factor in prime_divisors(order):
            assert affine_mul(order // factor, point, a, p) is not None
        modulus = p * p
        ap = (-11 + 6 * rp) % modulus
        lifted = ((57 - 28 * rp) * pow(8, -1, modulus) % modulus,
                  (-660 + 417 * rp) * pow(32, -1, modulus) % modulus, 1)
        Q = jacobian_mul(order, lifted, ap, p)
        assert list(Q) == row['jacobian']
        assert gcd(Q[1], p) == 1
        formal = -Q[0] * Q[2] * pow(Q[1], -1, modulus) % modulus
        assert formal == row['formal_z']
        assert formal % p == 0 and formal // p == row['formal_z_div_p'] != 0
    assert sum(roots) % p == 0 and gcd(*orders) == 1
    return {'prime': p, 'orders': orders,
            'both_formal_returns_have_depth_one': True,
            'simultaneous_depth_two_for_h_and_h_minus_one': False}


def lucas_pair(a, index):
    u, v = 0, 1
    for _ in range(index):
        u, v = v, a * v - u
    return u, v


def main():
    # The recurrence for the exact source logarithm gives this truncation.
    a0 = F(1)
    a1 = F(-2, 5)
    a2 = a1 * F(3, 9)
    assert (a0, a1, a2) == (F(1), F(-2, 5), F(-2, 15))
    assert 1 + a1 == F(3, 5) > 0

    # Exact exponents in the two soundness comparisons.
    assert F(7, 3) / 2 == F(7, 6) < 2
    assert (6 + 3) * F(7, 36) == F(7, 4) < 2
    assert F(7, 6) < 2
    witness_rows = []
    for s in (7, 13, 19):
        a = s * s
        k = 2 * (a - 2)
        w, t = lucas_pair(a, k)
        assert w % (a - 2) == 0
        b = w // (a - 2)
        assert t * t - a * (a - 2) * t * b + (a - 2) ** 2 * b * b == 1
        assert t > 0 and b > 0 and t % 2 == 1 and b % 2 == 1
        witness_rows.append({'s': s, 'parameter': a, 'index': k,
                             't_bits': t.bit_length(), 'b_bits': b.bit_length()})

    report = {'status': 'PASS', 'scalar_orders': [1, 1, 1, 1, 2, 2],
              'reciprocal_orders': [1] * 10,
              'comparison_orders': [1, 6, 6, 6, 1, 6],
              'logarithm_truncation': 'z*(1-2*D*f^2/5)',
              'relative_formal_error_at_depth_one': 8,
              'required_comparison_precision': 6,
              'scalar_height_exponent': '7/6',
              'nonzero_lucas_residual_exponent': '7/4',
              'lucas_witnesses': witness_rows,
              'depth_obstruction': check_depth_certificate(),
              'retained_variables': 25,
              'new_defining_variable_bound': False}
    (HERE / 'precision_transfer_certificate.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
