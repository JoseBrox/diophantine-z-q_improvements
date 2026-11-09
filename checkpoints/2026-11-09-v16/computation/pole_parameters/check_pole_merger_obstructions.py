#!/usr/bin/env python3
"""Exact checks for the specified common-parameter and product obstructions."""
from fractions import Fraction
from hashlib import sha256
from math import isqrt
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def add(p, q):
    n = max(len(p), len(q))
    return trim([(p[i] if i < len(p) else 0) +
                 (q[i] if i < len(q) else 0) for i in range(n)])


def scale(p, c):
    return trim([c * v for v in p])


def mul(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for i, u in enumerate(p):
        for j, v in enumerate(q):
            r[i + j] += u * v
    return trim(r)


def power(p, n):
    r = [1]
    for _ in range(n):
        r = mul(r, p)
    return r


def compose(p, q):
    r = [0]
    for c in reversed(p):
        r = add(mul(r, q), [c])
    return r


def valuation(q, p):
    q = Fraction(q)
    n, d, ans = abs(q.numerator), q.denominator, 0
    assert n
    while n % p == 0:
        n //= p
        ans += 1
    while d % p == 0:
        d //= p
        ans -= 1
    return ans


def local_square(q, p):
    v = valuation(q, p)
    if v % 2:
        return False
    unit = Fraction(q) / Fraction(p) ** v
    modulus = 8 if p == 2 else p
    r = unit.numerator * pow(unit.denominator, -1, modulus) % modulus
    return r == 1 if p == 2 else pow(r, (p - 1) // 2, p) == 1


def prepared(q):
    q = Fraction(q)
    assert 0 < q < 17
    assert isqrt(q.denominator) ** 2 == q.denominator
    values = {p: valuation(q, p) for p in (2, 3, 17)}
    assert values[2] >= 3 and values[3] >= 1 and values[17] >= 2
    assert all(local_square(q, p) for p in values)
    return {str(p): v for p, v in values.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    b0 = Fraction(204, 55) ** 2
    b1 = 409 * Fraction(204, 1001) ** 2
    assert b1 / b0 == 409 * Fraction(55, 1001) ** 2
    assert all(409 % d for d in range(2, isqrt(409) + 1))
    assert valuation(b1 / b0, 409) == 1
    preparation = [prepared(b0), prepared(b1)]

    F = [1]
    for j in range(1, 5):
        F = mul(F, add(power([-1, 1], 2), [-j * j]))
    assert compose(F, [2, -1]) == F
    assert power([-1, 1], 10) == power([1, -1], 10)
    # lambda=2/(a+1), a*lambda=2a/(a+1).  Their sum is two.
    assert add([2], [0, 2]) == scale([1, 1], 2)
    # Clear the common denominator (a+1)^8 from F at both arguments.
    numerators = []
    for delta in ([1, -1], [-1, 1]):
        numerator = [1]
        for j in range(1, 5):
            numerator = mul(numerator, add(power(delta, 2),
                             scale(power([1, 1], 2), -j * j)))
        numerators.append(mul(numerator, power([1, 1], 2)))
    assert numerators[0] == numerators[1]
    assert mul(numerators[0], numerators[1]) == power(numerators[0], 2)

    # This additional exact identity is used by the weak-abc contact map.
    # All terms are homogeneous of degree four, so checking y=1 checks
    # every coefficient of the homogeneous identity as well.
    A = mul([0, 1], power([2, 1], 3))
    C = power([1, 2], 3)
    assert add(A, scale(C, -1)) == mul(power([-1, 1], 3), [1, 1])
    assert add(scale([2, 1], 2), scale([1, 2], -1)) == [3]

    dependency = HERE / "fixed-e-obstruction-certificate.json"
    cert = json.loads(dependency.read_text())
    assert cert["status"] == "PASS"
    assert [row["b"] for row in cert["prepared_inputs"]] == [str(b0), str(b1)]
    receipt = {
        "status": "PASS",
        "prepared_inputs": [str(b0), str(b1)],
        "prepared_input_valuations": preparation,
        "nonsquare_ratio_prime": 409,
        "contact_polynomial_coefficients_descending": [
            int(c) for c in reversed(F)
        ],
        "reflection_identity": "R(2-t)=R(t)",
        "scale_substitution": "lambda=2/(a+1)",
        "scaled_product_identity": "R(lambda)*R(a*lambda)=R(lambda)^2",
        "weak_abc_contact_identity": "x*(x+2*y)^3-y*(2*x+y)^3=(x-y)^3*(x+y)",
        "fixed_e_rank_dependency_sha256": sha256(dependency.read_bytes()).hexdigest(),
        "scope": (
            "Exact rational preparation, the nonsquare ratio, reflection and "
            "scaled-product identities, and the degree-four weak-abc identity. "
            "The fixed-e rank obstruction is a separately reproducible dependency. "
            "No global variable minimum or solvability of a complete merged source "
            "is asserted."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "exact_identities": 5, "prepared_inputs": 2}))


if __name__ == "__main__":
    main()
