#!/usr/bin/env python3
"""Exact algebra and explicitly bounded search for four-coordinate filters.

Standard library only.  The bounded elliptic search proves no global
nonexistence assertion.  The ordinate obstruction is proved in the note.
"""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import json


def add(*terms):
    result = defaultdict(int)
    for coefficient, polynomial in terms:
        for monomial, value in polynomial.items():
            result[monomial] += coefficient * value
    return {m: c for m, c in result.items() if c}


def mul(a, b):
    result = defaultdict(int)
    for m, c in a.items():
        for n, d in b.items():
            result[tuple(x + y for x, y in zip(m, n))] += c * d
    return {m: c for m, c in result.items() if c}


one = {(0, 0, 0, 0): 1}
t = {(1, 0, 0, 0): 1}
slope_a = add((1, {(2, 2, 1, 0): 1}), (-9, {(0, 0, 3, 0): 1}), (-1, one))
slope_b = add((1, {(0, 2, 0, 1): 1}), (-9, {(0, 0, 0, 3): 1}), (-1, one))
ordinate_a = add((1, {(2, 2, 0, 0): 1}), (-1, {(0, 0, 3, 0): 1}), (-9, one))
ordinate_b = add((1, {(0, 2, 0, 0): 1}), (-1, {(0, 0, 0, 3): 1}), (-9, one))
polynomials = {
    "slope": mul(t, add((1, mul(slope_a, slope_a)), (-2, mul(slope_b, slope_b)))),
    "ordinate": mul(t, add((1, mul(ordinate_a, ordinate_a)), (-2, mul(ordinate_b, ordinate_b)))),
}
records = {}
for name, p in polynomials.items():
    records[name] = {
        "total_coordinates": 4,
        "degree": max(map(sum, p)),
        "height": max(map(abs, p.values())),
        "monomials": len(p),
        "terms": [{"exponents": list(m), "coefficient": c} for m, c in sorted(p.items())],
    }
assert (records["slope"]["degree"], records["slope"]["height"], records["slope"]["monomials"]) == (11, 162, 11)
assert (records["ordinate"]["degree"], records["ordinate"]["height"], records["ordinate"]["monomials"]) == (9, 81, 11)


def neg(p):
    return None if p is None else (p[0], -p[1])


def point_add(p, q):
    if p is None:
        return q
    if q is None:
        return p
    x, y = p
    u, v = q
    if x == u and y == -v:
        return None
    slope = (3 * x * x) / (2 * y) if p == q else (v - y) / (u - x)
    new_x = slope * slope - x - u
    new_y = slope * (x - new_x) - y
    assert new_y * new_y == new_x**3 + 9
    return new_x, new_y


generator = (F(-2), F(1))
torsion = (F(0), F(3))
assert point_add(torsion, torsion) == neg(torsion)
assert point_add(point_add(torsion, torsion), torsion) is None
assert point_add((F(3), F(6)), (F(3), F(6))) == (F(-15, 16), F(183, 64))
multiples = {0: None}
for n in range(1, 31):
    multiples[n] = point_add(multiples[n - 1], generator)
    multiples[-n] = neg(multiples[n])
slopes = set()
ordinates = set()
abscissas = set()
points = set()
for n in range(-30, 31):
    p = multiples[n]
    for k in range(3):
        if p is not None:
            points.add(p)
            ordinates.add(p[1])
            if p[0]:
                slopes.add(p[1] / p[0])
                abscissas.add(p[0])
        p = point_add(p, torsion)
assert F(0) not in ordinates and F(0) not in slopes
bounded_hits = {
    str(a): any(a * value in slopes for value in slopes)
    for a in map(F, [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
}
assert not bounded_hits["2"] and not bounded_hits["3"]


def vp(value, prime):
    assert value
    numerator, denominator = abs(value.numerator), value.denominator
    result = 0
    while numerator % prime == 0:
        numerator //= prime
        result += 1
    while denominator % prime == 0:
        denominator //= prime
        result -= 1
    return result


assert {pow(a, 3, 7) for a in range(7)} == {0, 1, 6}
assert (-9) % 7 == 5
assert all(vp(y, 7) % 3 == 0 for y in ordinates)

certificate = {
    "status": "PASS",
    "scope": "Exact expansions, finite residue obstruction, and explicitly bounded elliptic search. No global completeness or slope nonexistence assertion is proved by the search.",
    "polynomials": records,
    "ordinate_obstruction": {
        "prime": 7,
        "cubes_mod_prime": [0, 1, 6],
        "minus_nine_mod_prime": 5,
        "excluded_input": 7,
        "proof": "For v7(x)<0 the curve equation gives 2v7(y)=3v7(x); for integral x the residue obstruction forces y a unit. Thus all ordinate ratios have v7 divisible by3.",
    },
    "bounded_search": {
        "curve": "y^2=x^3+9",
        "generator_used": [-2, 1],
        "torsion_point": [0, 3],
        "points": "n*(-2,1)+k*(0,3), |n|<=30, k=0,1,2",
        "distinct_affine_points": len(points),
        "distinct_nonzero_slopes": len(slopes),
        "slope_ratio_hits": bounded_hits,
        "all_sampled_ordinate_valuations_divisible_by_three": True,
        "warning": "Failure to find a ratio in this finite set does not prove its absence from the full rational projection.",
    },
}
output = Path(__file__).with_name("rationality-filter-certificate.json")
output.write_text(json.dumps(certificate, indent=2) + "\n")
print(json.dumps({"status": "PASS", "polynomials": {
    name: {k: rec[k] for k in ["degree", "height", "monomials"]}
    for name, rec in records.items()
}, "distinct_nonzero_slopes": len(slopes), "bounded_slope_ratio_hits": bounded_hits}))
