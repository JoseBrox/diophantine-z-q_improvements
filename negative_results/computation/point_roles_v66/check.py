#!/usr/bin/env python3
"""Exact algebra certificates for point_role_restrictions_20261117_v66.tex.

Requires SymPy. Run: python check.py --output certificate.json
The checks do not establish the source's external arithmetic premises or
the unresolved joint prime/real realization for the shifted coupling.
"""
import argparse
import hashlib
import json
from math import isqrt
from pathlib import Path

import sympy as sp


def polynomial_degrees(expr, a, n, t, coefficient_symbols):
    poly = sp.Poly(sp.expand(expr), a, n, t, *coefficient_symbols)
    monomials = poly.monoms()
    return {
        "degree_in_a_n_together": max(m[0] + m[1] for m in monomials),
        "degree_in_t": max(m[2] for m in monomials),
        "degree_in_relation_coefficients": max(sum(m[3:]) for m in monomials),
        "integer_coefficient_monomials": len(monomials),
    }


def check_conic_and_resultants():
    a, n, t, b = sp.symbols("a n t b")
    form = sp.Matrix([
        [1, -a * (a - 2) / 2, 0],
        [-a * (a - 2) / 2, (a - 2) ** 2, 0],
        [0, 0, -1],
    ])
    determinant = sp.factor(form.det())
    target = -(a - 2) ** 2 * (1 - a ** 2 / 4)
    assert sp.expand(determinant - target) == 0
    assert set(sp.solve(determinant, a)) == {-2, 2}

    f0, f1, f2, g0, g1, g2 = sp.symbols("f0 f1 f2 g0 g1 g2")
    f = f2 * b ** 2 + f1 * b + f0
    g = g2 * b ** 2 + g1 * b + g0
    formula = (f2 * g0 - f0 * g2) ** 2 - (f2 * g1 - f1 * g2) * (f1 * g0 - f0 * g1)
    assert sp.expand(sp.resultant(f, g, b) - formula) == 0
    linear_formula = f2 * g0 ** 2 - f1 * g0 * g1 + f0 * g1 ** 2
    assert sp.expand(sp.resultant(f, g1 * b + g0, b) - linear_formula) == 0
    assert sp.resultant(f, g0, b) == g0 ** 2
    # The degree-two Sylvester expression has the expected extra factor when
    # the second input's actual degree drops; the paper uses the actual degree.
    assert sp.expand(formula.subs(g2, 0) - f2 * linear_formula) == 0
    assert sp.expand(formula.subs({g2: 0, g1: 0}) - f2 ** 2 * g0 ** 2) == 0

    coeffs = sp.symbols("c_tt c_tb c_bb c_ta c_tn c_t0 c_ba c_bn c_b0 c_aa c_an c_nn c_a c_n c_0")
    (c_tt, c_tb, c_bb, c_ta, c_tn, c_t0, c_ba, c_bn, c_b0,
     c_aa, c_an, c_nn, c_a, c_n, c_0) = coeffs
    relation_b0 = (
        c_tt * t ** 2 + (c_ta * a + c_tn * n + c_t0) * t
        + c_aa * a ** 2 + c_an * a * n + c_nn * n ** 2
        + c_a * a + c_n * n + c_0
    )
    relation_b1 = c_tb * t + c_ba * a + c_bn * n + c_b0
    relation = c_bb * b ** 2 + relation_b1 * b + relation_b0
    assert sp.Poly(relation, a, n, t, b).total_degree() == 2
    substitution = {
        f2: (a - 2) ** 2,
        f1: -a * (a - 2) * t,
        f0: t ** 2 - 1,
        g2: c_bb,
        g1: relation_b1,
        g0: relation_b0,
    }
    strata = {
        "quadratic_in_b": formula.subs(substitution, simultaneous=True),
        "linear_in_b": linear_formula.subs(substitution, simultaneous=True),
        "constant_in_b": relation_b0 ** 2,
    }
    degrees = {name: polynomial_degrees(expr, a, n, t, coeffs)
               for name, expr in strata.items()}
    assert degrees["quadratic_in_b"]["degree_in_a_n_together"] == 8
    assert degrees["linear_in_b"]["degree_in_a_n_together"] == 6
    assert degrees["constant_in_b"]["degree_in_a_n_together"] == 4
    assert all(data["degree_in_t"] == 4 for data in degrees.values())
    assert all(data["degree_in_relation_coefficients"] == 2 for data in degrees.values())
    return {
        "conic_determinant": str(determinant),
        "singular_parameters": [-2, 2],
        "universal_quadratic_resultant_identity": True,
        "actual_degree_drop_identities": True,
        "fully_generic_total_degree_two_relation": True,
        "resultant_degree_certificates": degrees,
    }


def check_scalar_contacts_and_forced_prime():
    x = sp.symbols("X")
    beta = 216 * x ** 4 + 450459
    factors = [beta, beta - 1, beta - 2401, 32 * beta + 343, 2 * beta - 1]
    product = sp.Poly(sp.prod(factors), x)
    assert product.degree() == 20
    assert sp.gcd(product, product.diff()).degree() == 0
    contacts = [sp.Rational(0), sp.Rational(1), sp.Rational(2401), -sp.Rational(343, 32), sp.Rational(1, 2)]
    assert len(set(contacts)) == 5
    assert all(sp.Poly(factor, x).degree() == 4 and factor.subs(x, 0) != 0 for factor in factors)

    ell = 76249
    assert all(ell % divisor for divisor in range(2, isqrt(ell) + 1))
    roots = [6193, 70056]
    assert roots[0] != roots[1]
    reductions = []
    for rho in roots:
        assert rho * rho % ell == 2
        d = (11 - 6 * rho) % ell
        xp = (57 - 28 * rho) * pow(8, -1, ell) % ell
        yp = (-660 + 417 * rho) * pow(32, -1, ell) % ell
        discriminant = 64 * pow(d, 3, ell) % ell
        assert discriminant != 0
        assert (yp * yp - xp ** 3 + d * xp) % ell == 0
        reductions.append({"sqrt2": rho, "D": d, "x(P)": xp, "y(P)": yp,
                           "discriminant": discriminant, "affine_nonidentity": True})
    return {
        "scalar_product_degree": product.degree(),
        "scalar_product_squarefree_over_Q": True,
        "distinct_contacts": [str(c) for c in contacts],
        "forced_prime": ell,
        "primality_method": "exact trial division through floor(sqrt(76249))",
        "split_good_reductions": reductions,
        "no_reduction_order_or_rank_computation_claimed": True,
    }


def integer_matrix_mul(a, b):
    return (
        a[0] * b[0] + a[1] * b[2], a[0] * b[1] + a[1] * b[3],
        a[2] * b[0] + a[3] * b[2], a[2] * b[1] + a[3] * b[3],
    )


def integer_matrix_power(matrix, exponent):
    result = (1, 0, 0, 1)
    while exponent:
        if exponent & 1:
            result = integer_matrix_mul(result, matrix)
        matrix = integer_matrix_mul(matrix, matrix)
        exponent //= 2
    return result


def check_shifted_lucas():
    a, y = sp.symbols("a y")
    matrix = sp.Matrix([[a, -1], [1, 0]])
    j_matrix = sp.Matrix([[1, -2], [2, -1]])
    remainder = matrix.subs(a, 1 + y) ** 3 + sp.eye(2) - y * j_matrix
    assert all(sp.rem(sp.Poly(entry, y), sp.Poly(y ** 2, y)).is_zero for entry in remainder)
    assert matrix.subs(a, 1) ** 3 == -sp.eye(2)
    assert matrix.subs(a, -1) ** 3 == sp.eye(2)

    symbolic_derivative_checks = 0
    u, v = sp.Integer(0), sp.Integer(1)
    for index in range(1, 37):
        u, v = v, sp.expand(a * v - u)
        if index % 3 == 0:
            k = index // 3
            assert u.subs(a, 1) == 0
            assert sp.diff(u, a).subs(a, 1) == 2 * k * (-1) ** (k + 1)
            symbolic_derivative_checks += 1

    cases = parity_cases = max_bits = 0
    for av in range(3, 50):
        for r in range(1, 7):
            index = 6 * (av - 2) * r
            power = integer_matrix_power((av, -1, 1, 0), index)
            uj, t = power[2], power[0]
            # Compare binary matrix powering with an independent scalar recurrence.
            u, v = 0, 1
            for _ in range(index):
                u, v = v, av * v - u
            assert (uj, t) == (u, v)
            divisor = (av - 1) * (av - 2)
            assert uj % divisor == 0
            h, b = uj // divisor, uj // (av - 2)
            assert h > 0 and b > 0 and t > 0
            assert b == (av - 1) * h
            assert (h + 4 * r) % (av - 1) == 0
            assert t * t - av * (av - 2) * t * b + (av - 2) ** 2 * b * b == 1
            if av % 2:
                assert b % 2 == 0 and t % 2 == 1
                parity_cases += 1
            cases += 1
            max_bits = max(max_bits, t.bit_length())
    return {
        "universal_matrix_identity_mod_a_minus_1_squared": True,
        "parameter_plus_minus_one_matrix_periods": True,
        "symbolic_Lucas_derivative_checks": symbolic_derivative_checks,
        "exact_integer_cases": cases,
        "a_range": [3, 49],
        "r_range": [1, 6],
        "odd_parameter_parity_cases": parity_cases,
        "matrix_power_independently_matches_recurrence": True,
        "integrality_Pell_and_shifted_congruence": True,
        "largest_t_bit_length": max_bits,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="Destination JSON certificate")
    args = parser.parse_args()
    certificate = {
        "status": "PASS",
        "scope": "Exact algebra and finite specializations; no proof of external arithmetic premises or joint realization",
        "sympy_version": sp.__version__,
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "conic_and_resultants": check_conic_and_resultants(),
        "scalar_contacts_and_forced_prime": check_scalar_contacts_and_forced_prime(),
        "shifted_Lucas": check_shifted_lucas(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(json.dumps(certificate, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
