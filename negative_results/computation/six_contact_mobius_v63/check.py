#!/usr/bin/env python3
"""Exact finite certificates for the integer-power six-contact obstruction.

Uses only the Python standard library. Infinite assertions are proved in the
manuscript by the displayed recurrence, root-field lemma and Chebotarev/CRT;
they are not inferred from the finite menu of numerical fixtures below.
"""
from fractions import Fraction as Q
from functools import reduce
from hashlib import sha256
from itertools import permutations
from math import gcd, isqrt, lcm
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
PAPER_NAME = "six_contact_mobius_obstruction_20261117_v63.tex"
PAPER_CANDIDATES = (
    HERE / PAPER_NAME,
    HERE.parents[2] / "negative_results/papers/pole_parameters" / PAPER_NAME,
)
R = (Q(0), Q(-1), Q(-1, 2), Q(-1, 3), Q(-1, 4), Q(-2, 5))
MATRICES = (
    (1, 0, 0, 1, 1),
    (1, 0, -5, -1, -1),
    (1, 1, 2, -1, 27),
    (4, 1, -7, -1, -27),
    (2, 1, -3, -2, -1),
    (3, 1, -7, -2, 1),
    (2, 1, -7, -3, 1),
    (3, 1, -8, -3, -1),
    (1, 1, -7, -4, -27),
    (4, 1, -13, -4, 27),
    (5, 2, -11, -5, 27),
    (5, 2, -14, -5, -27),
)
EXPECTED_GAPS = (
    19672769, 15732929, 84184839, 83133191, 189348561,
    189086929, 334379039, 329660447, 513765617, 509040881,
)
FIXTURES = (
    (4, 76213, 11332, 2832),
    (5, 76333, 44199, 30132),
    (6, 76259, 34651, 65856),
    (7, 76261, 16102, 42155),
    (8, 76243, 36746, 47307),
    (10, 76253, 28091, 26085),
    (12, 76379, 10315, 59862),
    (16, 76283, 9710, 40568),
    (32, 76421, 24909, 63542),
)


def polynomial_product(factors):
    result = [Q(1)]
    for factor in factors:
        product = [Q(0)] * (len(result) + len(factor) - 1)
        for i, a in enumerate(result):
            for j, b in enumerate(factor):
                product[i + j] += a * b
        result = product
    return result


def normalize(matrix):
    denominator = lcm(*(x.denominator for x in matrix))
    entries = [int(x * denominator) for x in matrix]
    content = reduce(gcd, entries)
    entries = [x // content for x in entries]
    if next(x for x in entries if x) < 0:
        entries = [-x for x in entries]
    return tuple(entries)


def check_group():
    group = set()
    triples = 0
    for u, v, w in permutations(R, 3):
        triples += 1
        delta = v - w
        gamma = u + v - 2 * w
        alpha = v * gamma + (u - v) * delta
        beta = u * delta
        matrix = normalize((alpha, beta, gamma, delta))
        a, b, c, d = matrix
        if a * d - b * c == 0 or any(c * r + d == 0 for r in R):
            continue
        if {(a * r + b) / (c * r + d) for r in R} == set(R):
            group.add(matrix)
    assert triples == 120
    assert group == {row[:4] for row in MATRICES}
    base = polynomial_product([[-r, Q(1)] for r in R])
    records = []
    for a, b, c, d, kappa in MATRICES:
        image = polynomial_product([[b - r * d, a - r * c] for r in R])
        assert image == [kappa * x for x in base]
        records.append({"matrix": [a, b, c, d], "multiplier": kappa})
    return {"ordered_image_triples": triples, "automorphisms": records}


def check_gaps():
    records = []
    for row_number, ((a, b, c, d, _), expected) in enumerate(
        zip(MATRICES[2:], EXPECTED_GAPS), start=3
    ):
        constant = -d * a + 2 * c * b
        k = 4 * b * c * (a * d - b * c)
        # Compare coefficients of p^2, p*q, q^2 in d^2*G=N^2+K*q^2.
        left = [d**4, d * d * (-2 * d * a + 4 * c * b), d * d * a * a]
        right = [d**4, 2 * d * d * constant, constant**2 + k]
        assert left == right
        q = 4**4
        p = 16**4 + 57**4
        n = d * d * p + constant * q
        g4 = 2 * n - 1 - abs(k) * q * q
        assert n > 0 and k != 0 and g4 == expected and g4 > 0
        # g_e is a linear combination of 57^e,16^e,4^e,1.
        coefficients = {57: 2 * d * d, 16: 2 * d * d - abs(k),
                        4: 2 * constant, 1: -1}
        recurrence = {base: coefficient * (base - 16)
                      for base, coefficient in coefficients.items()}
        assert recurrence == {57: 82 * d * d, 16: 0,
                              4: -24 * constant, 1: 15}
        assert d * d >= 1 and constant <= 5
        assert 57 > 2 * 4
        positive_lower_coefficient = 164 * d * d - 24 * max(constant, 0)
        assert positive_lower_coefficient > 0
        records.append({"row": row_number, "c": constant, "K": k,
                        "gap_e4_B3": g4,
                        "recurrence_lower_coefficient": positive_lower_coefficient})
    assert len(records) == 10
    # Elementary base inequality used for every k>=2:
    # 4*(16/57)^k <= 4*(16/57)^2 < 1.
    assert 16 < 57 and 4 * 16**2 < 57**2
    return records


def check_involution():
    f_factors = [(1, 0), (1, 1), (2, 1), (3, 1), (4, 1), (5, 2)]
    h = polynomial_product([[-1, 1], [1, 1], [-1, 4],
                            [-2, 3], [-3, 2], [-4, 1]])
    # lambda=-(a+1)/(5a); each linear factor becomes k*(-a-1)+l*5a.
    f0_numerator = polynomial_product([[-k, -k + 5 * ell] for k, ell in f_factors])
    # a*lambda=-(a+1)/5; each factor becomes k*(-a-1)+l*5.
    f1_numerator = polynomial_product([[-k + 5 * ell, -k] for k, ell in f_factors])
    assert 120 * 5**6 == 5 * 375000
    assert f0_numerator == [-5 * x for x in h]
    assert f1_numerator == [5 * x for x in h]
    derivative_at_four = sum(i * h[i] * 4**(i - 1) for i in range(1, len(h)))
    assert derivative_at_four == 11250
    assert sum(h[i] * 4**i for i in range(len(h))) == 0
    return {"H_coefficients_low_to_high": [int(x) for x in h],
            "H_derivative_at_four": int(derivative_at_four)}


def f_mod(t, modulus):
    numerator = 1
    for factor in (t, t + 1, 2 * t + 1, 3 * t + 1, 4 * t + 1, 5 * t + 2):
        numerator = numerator * factor % modulus
    return numerator * pow(120, -1, modulus) % modulus


def contact_fixture(e, p, y, shift):
    assert p > 76176
    assert all(p % d for d in range(2, isqrt(p) + 1))
    assert p % 8 in (3, 5)
    assert pow(2, (p - 1) // 2, p) == p - 1
    m_mod_p = (pow(57, e, p) - pow(4, e + 1, p)) % p
    assert e * m_mod_p % p != 0
    assert (pow(y, e, p) + m_mod_p) % p == 0
    assert e * pow(y, e - 1, p) % p != 0
    assert (4 * (shift + 1) - y) % p == 0
    modulus = p * p
    a = (pow(shift + 1, e, modulus)
         + pow(57, e, modulus) * pow(pow(4, e, modulus), -1, modulus)) % modulus
    assert a % p == 4 and a != 4
    factors = [a - 1, a + 1, 4 * a - 1, 3 * a - 2, 2 * a - 3, a - 4]
    h = 1
    for factor in factors:
        h = h * factor % modulus
    assert h % p == 0 and h != 0
    lam = -(a + 1) * pow(5 * a, -1, modulus) % modulus
    t1 = a * lam % modulus
    units = [a, lam, lam - 1, t1 - 1, 5 * lam + 1]
    assert all(unit % p for unit in units)
    assert lam % p == -pow(4, -1, p) % p and t1 % p == p - 1
    for t in (lam, t1):
        d = f_mod(t, modulus)
        w = d * pow(4 * pow(t - 1, 8, modulus), -1, modulus) % modulus
        assert d % p == 0 and d != 0
        assert w % p == 0 and w != 0
    return {"exponent": e, "prime": p, "binomial_root": y,
            "shift_residue_mod_p_squared": shift % modulus,
            "contact_valuation": 1, "prime_trial_division_bound": isqrt(p)}


def check_finite_menu():
    assert len({p for _, p, _, _ in FIXTURES}) == len(FIXTURES)
    records = [contact_fixture(*fixture) for fixture in FIXTURES]
    shift, modulus = 1, 2
    for _, p, _, residue in FIXTURES:
        next_modulus = p * p
        assert gcd(modulus, next_modulus) == 1
        multiple = (residue - shift) * pow(modulus, -1, next_modulus) % next_modulus
        shift += modulus * multiple
        modulus *= next_modulus
        assert 0 <= shift < modulus
    assert shift % 2 == 1 and shift >= 3
    for e, p, y, residue in FIXTURES:
        assert shift % (p * p) == residue
        contact_fixture(e, p, y, shift)
    return {"fixtures": records, "common_odd_shift": shift,
            "progression_modulus": modulus,
            "exceptional_set_for_fixture": [2, 3, 5, 7]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    paper = next((p for p in PAPER_CANDIDATES if p.is_file()), None)
    assert paper is not None, "Cannot locate the v63 manuscript"
    group = check_group()
    gaps = check_gaps()
    involution = check_involution()
    menu = check_finite_menu()
    record = {
        "status": "PASS",
        "source_sha256": sha256(paper.read_bytes()).hexdigest(),
        "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "method": "Exact rational interpolation, coefficient arithmetic, modular arithmetic and trial division; Python standard library.",
        "group": group,
        "uniform_gap_recurrence_certificates": gaps,
        "involution": involution,
        "simultaneous_finite_menu": menu,
        "infinite_claims": "Proved in the manuscript by the positive recurrence and the root-field, Chebotarev and CRT arguments; not inferred from fixtures.",
    }
    if args.output:
        args.output.write_text(json.dumps(record, indent=2) + "\n")
    print("PASS: 120 triples; 12 symmetries; 10 square-gap recurrence certificates; "
          "involution identities; 9-prime simultaneous CRT certificate.")


if __name__ == "__main__":
    main()
