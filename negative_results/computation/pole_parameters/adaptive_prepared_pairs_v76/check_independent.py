#!/usr/bin/env python3
"""Independent quadratic-field reconstruction; imports no producer or CAS."""
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path
import argparse
import hashlib
import json


def plus(a, b):
    return a[0]+b[0], a[1]+b[1]


def times(a, b):
    return a[0]*b[0]+2*a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def inverse(a):
    norm = a[0]*a[0]-2*a[1]*a[1]
    assert norm != 0
    return a[0]/norm, -a[1]/norm


def vp(x, p):
    x = Q(x)
    assert x != 0
    a, b, value = abs(x.numerator), x.denominator, 0
    while a % p == 0:
        a //= p
        value += 1
    while b % p == 0:
        b //= p
        value -= 1
    return value


def residue(x, modulus):
    x = Q(x)
    return x.numerator*pow(x.denominator, -1, modulus) % modulus


def is_local_square(x, p):
    x = Q(x)
    if x == 0:
        return True
    v = vp(x, p)
    if v % 2:
        return False
    unit = x/Q(p)**v
    if p == 2:
        return residue(unit, 8) == 1
    return pow(residue(unit, p), (p-1)//2, p) == 1


def pair(u, h):
    u = Q(u)
    h = tuple(Q(v) for v in h)
    w = u/(1+u)**2
    W = plus((Q(1), Q(0)), times((w, Q(0)), times(h, h)))
    V = 2*inverse(W)[0]
    C = V*V+w*(2-V)
    b = 4*w/(V*V)
    return dict(u=u, w=w, h0=h[0], h1=h[1],
                W_real_component=W[0], W_sqrt2_component=W[1],
                W_norm=times(W, (W[0], -W[1]))[0], V=V, C=C, b=b)


def verify_preparation(d):
    w, V, C, b = (d[k] for k in ("w", "V", "C", "b"))
    assert 0 < w < Q(1, 4)
    assert Q(200, 101) < V < 2 and 0 < b < Q(1, 7)
    assert isqrt(b.denominator)**2 == b.denominator
    assert vp(b, 2) >= 4 and is_local_square(b, 2)
    assert vp(b, 7) >= 0
    assert all(is_local_square(b, p) for p in (3, 17))
    assert vp(b, 3) > 0 and vp(b, 17) >= 2
    assert all(is_local_square(C, p) for p in (2, 3, 7, 17))
    return {str(p): vp(b, p) for p in (2, 3, 7, 17)}


# A small sparse polynomial implementation supplies exact coefficient checks.
NAMES = ("q", "V", "b", "z", "B", "X", "Y", "y", "n")
DIM = len(NAMES)


def const(c):
    return {} if c == 0 else {(0,)*DIM: Q(c)}


def var(name):
    powers = [0]*DIM
    powers[NAMES.index(name)] = 1
    return {tuple(powers): Q(1)}


def add(a, b, scale=1):
    out = dict(a)
    for powers, coefficient in b.items():
        out[powers] = out.get(powers, 0)+scale*coefficient
        if out[powers] == 0:
            del out[powers]
    return out


def mul(a, b):
    out = {}
    for x, c in a.items():
        for y, d in b.items():
            key = tuple(i+j for i, j in zip(x, y))
            out[key] = out.get(key, 0)+c*d
    return {key: value for key, value in out.items() if value}


def power(a, n):
    out = const(1)
    for _ in range(n):
        out = mul(out, a)
    return out


def scale(a, c):
    return mul(a, const(c))


def polynomial_checks():
    q, V, b, z, B, X, Y, y, n = (var(name) for name in NAMES)
    one = const(1)
    left = add(power(add(add(power(q, 2), scale(q, -2)), const(-1)), 2),
               scale(mul(mul(q, add(power(q, 2), const(-1))), V), 4))
    right = add(power(add(power(q, 2), one), 2),
                scale(mul(mul(add(V, const(-1)), q), add(power(q, 2), const(-1))), 4))
    assert left == right
    # Divide the quartic by q^2 and set t=q-1/q. The quadratic has
    # root sum -4(V-1), product4, and squared difference16V(V-2).
    root_sum = scale(add(V, const(-1)), -4)
    sum_t_squared = add(power(root_sum, 2), const(-8))
    product_t_squared_plus_4 = add(scale(sum_t_squared, 4), const(32))
    assert product_t_squared_plus_4 == scale(power(add(V, const(-1)), 2), 64)
    squared_difference = scale(mul(V, add(V, const(-2))), 16)
    discriminant = mul(product_t_squared_plus_4, power(squared_difference, 2))
    expected = scale(mul(mul(power(V, 2), power(add(V, const(-2)), 2)),
                         power(add(V, const(-1)), 2)), 16384)
    assert discriminant == expected
    # Quartic-to-cubic map, checked after taking the curve relation out.
    Xmap = mul(mul(B, power(b, 2)), power(z, 2))
    Ymap = mul(mul(mul(B, power(b, 2)), z), y)
    nmap = mul(B, b)
    lhs = add(add(power(Ymap, 2), power(Xmap, 3), -1), mul(power(nmap, 2), Xmap), -1)
    quartic = add(power(y, 2), mul(B, add(one, mul(power(b, 2), power(z, 4)))), -1)
    multiplier = mul(mul(power(B, 2), power(b, 4)), power(z, 2))
    assert lhs == mul(multiplier, quartic)
    # The two-isogeny relation with denominator X^4 cleared.
    Xm = add(power(X, 2), power(n, 2))
    difference = add(power(X, 2), power(n, 2), -1)
    lhs = add(mul(power(Y, 2), power(difference, 2)), mul(X, power(Xm, 3)), -1)
    lhs = add(lhs, scale(mul(mul(power(n, 2), power(X, 3)), Xm), 4))
    cubic = add(add(power(Y, 2), power(X, 3), -1), mul(power(n, 2), X), -1)
    assert lhs == mul(power(difference, 2), cubic)
    return {"delta_identity": True, "quartic_discriminant_via_q_minus_inverse_q": True,
            "quartic_to_plus_cubic_map": True, "two_isogeny_after_clearing_denominators": True}


def main(output):
    here = Path(__file__).parent
    raw = (here/"certificate.json").read_bytes()
    certificate = json.loads(raw)
    p = 100003
    assert all(p % d for d in range(2, isqrt(p)+1))
    assert p % 24 == 19 and pow(2, (p-1)//2, p) == p-1
    m, z = Q(509796, 28707122557), Q(509796, 32337379873)
    first = pair(m*m, (z*(1+m*m)/m, 0))
    assert first["W_real_component"] == 1+z*z
    assert first["b"] == (m*(1+z*z)/(1+m*m))**2
    assert residue(m, p) == 7121 and residue(z, p) == 1
    assert [residue(first[k], p) for k in ("w", "V", "C")] == [1, 1, 2]
    assert not is_local_square(first["C"], p)
    assert all(is_local_square(first["C"]*(1+24*first["V"]), ell) for ell in (2, 3, 7, 17))
    r, M = 44974, 714**2
    u = 52581464203154325228257242401217852539664811276478096
    assert vp(r*r+2, p) == 1
    conditions = ((p**3, p*p-1), (128, 16), (27, 9), (4913, 289), (7, 1))
    assert all(u % modulus == value for modulus, value in conditions)
    H = M*p**3*(r+2)
    assert u >= 100*H*H+100
    second = pair(u, (M*p**3*r, M*p**3))
    assert second["w"]*H*H < Q(1, 100)
    fresh = {name: vp(second[name], p) for name in ("u", "w", "V", "C", "b")}
    fresh["2-V"] = vp(2-second["V"], p)
    assert fresh == {"u": 0, "w": -4, "V": 0, "C": -1, "b": -4, "2-V": 3}
    reports = []
    for fixture, rebuilt in zip(certificate["fixtures"], (first, second)):
        assert {key: Q(value) for key, value in fixture["native_pair"].items()} == rebuilt
        reports.append({"name": fixture["name"], "all_exact_rational_values_match": True,
                        "b_valuations": verify_preparation(rebuilt)})
    result = {"status": "PASS", "producer_imported": False, "cas_used": False,
              "certificate_sha256": hashlib.sha256(raw).hexdigest(),
              "method": "quadratic-field arithmetic, exact rational valuations, sparse polynomial coefficient checks",
              "fixtures": reports, "fresh_prime_valuations_second_fixture": fresh,
              "polynomial_checks": polynomial_checks(),
              "scope": "Prepared abstract native products; no actual elliptic or physical lifting asserted"}
    output.write_text(json.dumps(result, indent=2)+"\n")
    print("PASS: independent native-pair reconstruction, local preparation, and polynomial maps")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("independent_certificate.json"))
    main(parser.parse_args().output)
