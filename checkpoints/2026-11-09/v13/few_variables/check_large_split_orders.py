#!/usr/bin/env python3
"""Independent exact certificates for odd conjugate reduction orders.

PARI/GP located the examples.  This verifier uses only integer modular
arithmetic and the Python standard library; no PARI result is trusted.
"""
from math import gcd, isqrt, lcm
from pathlib import Path
import json


def factor(n):
    answer = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            answer[d] = answer.get(d, 0) + 1
            n //= d
        d = 3 if d == 2 else d + 2
    if n > 1:
        answer[n] = answer.get(n, 0) + 1
    return answer


def prime(n):
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def add(a, b, D, p):
    if a is None:
        return b
    if b is None:
        return a
    x, y = a
    u, v = b
    if x == u and (y + v) % p == 0:
        return None
    if a == b:
        slope = (3 * x * x - D) * pow(2 * y, -1, p) % p
    else:
        slope = (v - y) * pow(u - x, -1, p) % p
    new_x = (slope * slope - x - u) % p
    new_y = (slope * (x - new_x) - y) % p
    assert (new_y * new_y - new_x**3 + D * new_x) % p == 0
    return new_x, new_y


def multiply(n, point, D, p):
    result, current = None, point
    while n:
        if n & 1:
            result = add(result, current, D, p)
        current = add(current, current, D, p)
        n >>= 1
    return result


def count_curve(D, p):
    # First count: independently tabulate the number of square roots of
    # every residue, then sum the counts for all abscissas.
    frequencies = [0] * p
    for y in range(p):
        frequencies[y * y % p] += 1
    by_square_roots = 1 + sum(frequencies[(x**3 - D * x) % p] for x in range(p))
    # Second count: Euler's criterion, with no square-root table.
    by_euler = 1
    for x in range(p):
        rhs = (x**3 - D * x) % p
        if rhs == 0:
            by_euler += 1
        elif pow(rhs, (p - 1) // 2, p) == 1:
            by_euler += 2
    assert by_square_roots == by_euler
    return by_euler


def verify(p, root, proposed_orders):
    assert prime(p) and p > 76176 and p % 8 == 1
    assert root * root % p == 2
    rows = []
    for r, order in zip((root, p - root), proposed_orders):
        D = (11 - 6 * r) % p
        assert D == (3 - r) ** 2 % p and D != 0
        point = (
            (57 - 28 * r) * pow(8, -1, p) % p,
            (-660 + 417 * r) * pow(32, -1, p) % p,
        )
        x, y = point
        assert (y * y - x**3 + D * x) % p == 0
        fs = factor(order)
        assert all(prime(q) for q in fs)
        assert order % 2 == 1 and multiply(order, point, D, p) is None
        witnesses = {}
        for q in fs:
            witness = multiply(order // q, point, D, p)
            assert witness is not None
            witnesses[str(q)] = {
                "multiplier": order // q,
                "nonidentity_point": list(witness),
            }
        cardinality = count_curve(D, p)
        assert cardinality % order == 0
        rows.append({
            "sqrt2_residue": r,
            "D_residue": D,
            "P_reduction": list(point),
            "curve_cardinality": cardinality,
            "cardinality_verified_by": ["square-root-frequency table", "Euler criterion"],
            "point_order": order,
            "order_factorization": {str(q): e for q, e in fs.items()},
            "order_multiple_is_identity": True,
            "proper_prime_quotient_witnesses": witnesses,
        })
    index = lcm(*proposed_orders)
    assert index % 2 == 1
    assert all(multiply(index, tuple(row["P_reduction"]), row["D_residue"], p) is None for row in rows)
    return {
        "p": p,
        "prime_checked_by": "trial division through floor(sqrt(p))",
        "p_mod_8": p % 8,
        "p_mod_7": p % 7,
        "both_curves_have_good_reduction": True,
        "conjugate_reductions": rows,
        "odd_index_making_both_reductions_identity": index,
    }


records = [verify(77017, 18810, (2141, 2405)), verify(76249, 6193, (2377, 19109))]
assert records[0]["p_mod_7"] == 3
certificate = {
    "status": "PASS",
    "scope": "Exact counterexamples to a universal parity-of-index branch shortcut, including a split good prime above the exceptional cutoff with p=1 mod8 and p=3 mod7. Full Gaussian ray and reduction-order avoidance conditions of a prime-pattern theorem are not asserted.",
    "source_curve": "E:y^2=x^3-(11-6sqrt(2))*x",
    "source_point": "P=((57-28sqrt(2))/8,(-660+417sqrt(2))/32)",
    "examples": records,
}
output = Path(__file__).with_name("large-split-order-certificate.json")
output.write_text(json.dumps(certificate, indent=2) + "\n")
print(json.dumps(certificate, indent=2))
