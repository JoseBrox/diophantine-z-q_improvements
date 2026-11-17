#!/usr/bin/env python3
"""Exact certificate for the reference point on the small trace cubic.

Only the Python standard library is used.  Polynomial lists are in ascending
powers of w.  Run with --write-data once to create the coefficient checkpoint;
the default run independently recomputes and checks the saved arrays.
"""
from fractions import Fraction
from functools import lru_cache
from math import gcd
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
DATA = HERE / "rank_coefficients.json"
CERT = HERE / "rank_certificate.json"


def trim(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def add(a, b):
    c = [0] * max(len(a), len(b))
    for i, ai in enumerate(a):
        c[i] += ai
    for i, bi in enumerate(b):
        c[i] += bi
    return trim(c)


def scale(a, c):
    return trim([c * ai for ai in a])


def sub(a, b):
    return add(a, scale(b, -1))


def mul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            c[i + j] += ai * bj
    return trim(c)


def power(a, n):
    assert n >= 0
    p = [1]
    while n:
        if n & 1:
            p = mul(p, a)
        a = mul(a, a)
        n //= 2
    return p


def exact_div_scalar(a, d):
    assert d and all(ai % d == 0 for ai in a)
    return trim([ai // d for ai in a])


def evaluate(a, x):
    v = 0
    for ai in reversed(a):
        v = v * x + ai
    return v


A2 = [-4, -1]
A4 = [4, 4]
X, Y = 4, 4
assert add(add([X**3], scale(A2, X**2)), scale(A4, X)) == [Y**2]

# Standard initial division polynomials specialized at (x,y)=(4,4).
PSI3 = sub(add(add([3 * X**4], scale(A2, 4 * X**3)),
               scale(A4, 6 * X**2)), power(A4, 2))
PSI4 = scale(sub(sub(sub(add(add([X**6], scale(A2, 2 * X**5)),
                                 scale(A4, 5 * X**4)),
                             scale(power(A4, 2), 5 * X**2)),
                         scale(mul(A2, power(A4, 2)), 2 * X)),
                     power(A4, 3)), 4 * Y)
assert PSI3 == [112, 96, -16]
assert PSI4 == [3072, 23552, -11264, 1024]


@lru_cache(None)
def psi(n):
    initial = {0: (0,), 1: (1,), 2: (8,),
               3: tuple(PSI3), 4: tuple(PSI4)}
    if n in initial:
        return initial[n]
    if n % 2:
        m = (n - 1) // 2
        value = sub(mul(psi(m + 2), power(psi(m), 3)),
                    mul(psi(m - 1), power(psi(m + 1), 3)))
    else:
        m = n // 2
        bracket = sub(mul(psi(m + 2), power(psi(m - 1), 2)),
                      mul(psi(m - 2), power(psi(m + 1), 2)))
        value = exact_div_scalar(mul(psi(m), bracket), 8)
    return tuple(value)


def primitive_row(n):
    coefficients = psi(n)
    content = 0
    for ai in coefficients:
        content = gcd(content, abs(ai))
    q = exact_div_scalar(coefficients, content)
    assert q[-1] > 0
    q_content = 0
    for ai in q:
        q_content = gcd(q_content, abs(ai))
    assert q_content == 1
    assert scale(q, content) == list(coefficients)
    return {"n": n, "content": content, "degree": len(q) - 1,
            "leading_coefficient": q[-1],
            "primitive_coefficients_ascending": q}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-data", action="store_true")
    parser.add_argument("--output", type=Path, default=CERT)
    args = parser.parse_args()
    for n in range(13):
        psi(n)
    rows = [primitive_row(n) for n in (8, 10, 12)]
    expected = [(8, 2**35, 15, 1), (10, 2**51, 24, 5),
                (12, 2**74, 35, 3)]
    for row, values in zip(rows, expected):
        assert tuple(row[k] for k in ("n", "content", "degree",
                                     "leading_coefficient")) == values
    data = {
        "curve": "y^2=x*(x^2-(w+4)*x+4*(w+1))",
        "point": [4, 4],
        "coefficient_order": "ascending powers of w",
        "division_normalization": "psi_1=1; psi_2=2*y=8",
        "rows": rows,
    }
    if args.write_data:
        DATA.write_text(json.dumps(data, indent=2) + "\n")
    assert json.loads(DATA.read_text()) == data

    # Discriminant = 16*a4^2*(a2^2-4*a4).
    other_2_torsion_discriminant = sub(power(A2, 2), scale(A4, 4))
    assert other_2_torsion_discriminant == [0, -8, 1]
    discriminant = scale(mul(power(A4, 2),
                             other_2_torsion_discriminant), 16)
    assert discriminant == [0, -2048, -3840, -1536, 256]

    # Exact tangent arithmetic verifies 4*x(2P)=(w-3)^2 and
    # 8*y(2P)=(w-3)*(w^2-8*w-1).
    slope_num = add(add([3 * X**2], scale(A2, 2 * X)), A4)
    assert slope_num == [20, -4]  # slope = slope_num / (2Y).
    x2_num_64 = sub(sub(power(slope_num, 2), scale(A2, 64)),
                      [128 * X])
    assert x2_num_64 == scale(power([-3, 1], 2), 16)
    y2_num_512 = sub(mul(slope_num, sub([64 * X], x2_num_64)),
                      [512 * Y])
    assert y2_num_512 == scale(mul([-3, 1], [-1, -8, 1]), 64)

    q10 = rows[1]["primitive_coefficients_ascending"]
    value = evaluate(q10, Fraction(1, 5))
    mod3 = evaluate(q10, 2) % 3
    psi_mod3 = {str(n): evaluate(psi(n), 2) % 3
                for n in (2, 3, 4, 5, 7, 10)}
    assert psi_mod3 == {"2": 2, "3": 0, "4": 1,
                        "5": 2, "7": 1, "10": 1}
    assert mod3 == 2 and value != 0
    assert value == Fraction(-55421818556438910529961984,
                            11920928955078125)
    certificate = {
        "status": "PASS",
        "arithmetic": "exact integer polynomials and rational numbers; stdlib only",
        "division_recurrence_verified_through": 12,
        "saved_primitive_coefficient_arrays_verified": True,
        "curve_point_discriminant_and_doubling_identities_verified": True,
        "primitive_data": [{k: v for k, v in row.items()
                            if k != "primitive_coefficients_ascending"}
                           for row in rows],
        "Q10_at_1_over_5": {"numerator": value.numerator,
                            "denominator": value.denominator,
                            "modulo_3": mod3},
        "psi_n_at_w_2_modulo_3": psi_mod3,
        "rational_root_denominator_exclusions": {
            "Q8": "denominator divides 1; no positive root <=1/4",
            "Q10": "denominator divides 5; sole candidate 1/5 is nonzero modulo 3",
            "Q12": "denominator divides 3; no positive root <=1/4",
        },
        "external_theorem": "Mazur, Modular curves and the Eisenstein ideal (1977), Theorem (8), p.35",
        "scope": {
            "rational_weight_range": "0 < w <= 1/4",
            "reference_point_infinite_order_proved": True,
            "positive_rank_proved": True,
            "actual_prescribed_trace_realization_proved": False,
            "new_diophantine_variable_bound_proved": False,
            "torsion_classification_for_all_rational_weights_claimed": False,
        },
    }
    args.output.write_text(json.dumps(certificate, indent=2) + "\n")
    print(json.dumps(certificate, indent=2))


if __name__ == "__main__":
    main()
