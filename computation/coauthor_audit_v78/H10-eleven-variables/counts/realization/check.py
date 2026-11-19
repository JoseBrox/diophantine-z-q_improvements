"""Verify the finite-field cases and the global examples in diagonal-intrinsic.md."""
from fractions import Fraction as Q
from math import isqrt


def radicand(d, v):
    return d * ((d + v*v)**2 * v**4 - (d - v*v)**2 * (1 - d)**2)


def check_finite_fields():
    checked = 0
    for p in (5, 13, 17, 29):
        squares = {x*x % p for x in range(p)}
        for D in range(1, p):
            if D in squares:
                continue
            for h in ((1 - D) % p, -D % p):
                assert h != 0
                for x in range(p):
                    r = x*x
                    f = D * ((D+r)**2 * r*r - (D-r)**2 * h*h) % p
                    df = 4*D*x * (r*r*(D+r) + r*(D+r)**2 + (D-r)*h*h) % p
                    if f in squares and (f != 0 or df != 0):
                        break
                else:
                    raise AssertionError((p, D, h))
                checked += 1
    return checked


def add_base(P, Qpoint):
    if P is None:
        return Qpoint
    if Qpoint is None:
        return P
    x, y = P
    u, v = Qpoint
    if x == u and y == -v:
        return None
    m = (3*x*x + 8) / (2*y) if P == Qpoint else (v-y) / (u-x)
    z = m*m - x - u
    return z, m*(x-z) - y


def multiply_base(n, P):
    value = None
    while n:
        if n % 2:
            value = add_base(value, P)
        P, n = add_base(P, P), n // 2
    return value


def v_two(n):
    return (abs(n) & -abs(n)).bit_length() - 1


def is_prepared(d):
    if not 0 < d < 1 or isqrt(d.denominator)**2 != d.denominator:
        return False
    e = v_two(d.numerator) - v_two(d.denominator)
    if e < 4 or e % 2:
        return False
    unit = d / 2**e
    return unit.numerator * pow(unit.denominator, -1, 8) % 8 == 7


def check_nonzero_family():
    L, M, N = 35945, 98, -7
    d, r, v = Q(448,4489), Q(8,67), Q(24,67)
    y = Q(5999616,1350125107)
    z = y/(2*r**3)
    assert is_prepared(d) and radicand(d, v) == y*y
    assert 1-d == Q(9*449, 67**2)
    assert z == Q(5859,4489) and z*z == L*r**4 + M*r*r + N
    x, u = L*r*r, L*r*z
    assert u*u == x**3 + M*x*x + L*N*x
    assert L % 67 and x.denominator == 67**2
    assert M*M - 4*L*N != 0



def check_zero_family():
    x, y = multiply_base(71, (Q(8), Q(24)))
    x8 = x/8
    v = Q(isqrt(x8.numerator), isqrt(x8.denominator))
    assert x8 == v*v
    zs = (y/(8*v), -y/(8*v))
    prepared = [(1+2*v*v-z)/2 for z in zs if is_prepared((1+2*v*v-z)/2)]
    assert len(prepared) == 1 and radicand(prepared[0], v) == 0
    return prepared[0], v


if __name__ == '__main__':
    print('Finite-field cases with a smooth affine point:', check_finite_fields())
    check_nonzero_family()
    print('Infinite-order elliptic seed and exact nonzero ordinate: verified')
    d, v = check_zero_family()
    print('Zero-ordinate [71]P example verified, numerator/denominator bit sizes:')
    for name, value in [('d', d), ('v', v)]:
        print(name, value.numerator.bit_length(), value.denominator.bit_length())
