#!/usr/bin/env python3
"""Read-only independent finite checks for amplified rationality descent.

No construction module or computer-algebra package is imported.  The default
command recomputes the finite assertions and compares the committed certificate
if it exists.  --report PATH explicitly writes a fresh report instead.

The arithmetic existence inputs, the all-place approximation lemma, and the
height proof are mathematical assertions reviewed separately in proof_review.md.
Finite valuation checks below supplement, rather than replace, their proofs.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path


class Poly:
    """Small exact sparse Laurent-polynomial ring used only for identities."""

    def __init__(self, n, terms=None):
        self.n = n
        self.terms = {e: Fraction(c) for e, c in (terms or {}).items() if c}

    @classmethod
    def constant(cls, n, c):
        return cls(n, {(0,) * n: c})

    @classmethod
    def variable(cls, n, i):
        e = [0] * n
        e[i] = 1
        return cls(n, {tuple(e): 1})

    def coerce(self, other):
        return other if isinstance(other, Poly) else Poly.constant(self.n, other)

    def __add__(self, other):
        other = self.coerce(other)
        result = Counter(self.terms)
        for e, c in other.terms.items():
            result[e] += c
        return Poly(self.n, result)

    __radd__ = __add__

    def __neg__(self):
        return Poly(self.n, {e: -c for e, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        result = Counter()
        for e, c in self.terms.items():
            for f, d in other.terms.items():
                result[tuple(a + b for a, b in zip(e, f))] += c * d
        return Poly(self.n, result)

    __rmul__ = __mul__

    def __pow__(self, power):
        assert isinstance(power, int)
        if power < 0:
            assert len(self.terms) == 1
            e, c = next(iter(self.terms.items()))
            return Poly(self.n, {tuple(power * a for a in e): c**power})
        result = Poly.constant(self.n, 1)
        base = self
        while power:
            if power & 1:
                result *= base
            base *= base
            power //= 2
        return result

    def __eq__(self, other):
        other = self.coerce(other)
        return self.n == other.n and self.terms == other.terms


def variables(n):
    return [Poly.variable(n, i) for i in range(n)]


def trim(p):
    p = list(p)
    while len(p) > 1 and not p[-1]:
        p.pop()
    return p


def multiply(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i + j] += a * b
    return trim(r)


def derivative(p):
    return trim([i * p[i] for i in range(1, len(p))])


def determinant(matrix):
    """Fraction-free elimination with exact-division assertions."""
    a = [row[:] for row in matrix]
    n = len(a)
    sign, previous = 1, 1
    for k in range(n - 1):
        if not a[k][k]:
            swap = next((j for j in range(k + 1, n) if a[j][k]), None)
            if swap is None:
                return 0
            a[k], a[swap] = a[swap], a[k]
            sign *= -1
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                assert numerator % previous == 0
                a[i][j] = numerator // previous
            a[i][k] = 0
        previous = pivot
    return sign * a[-1][-1]


def resultant(p, q):
    m, n = len(p) - 1, len(q) - 1
    pd, qd = list(reversed(p)), list(reversed(q))
    rows = []
    for i in range(n):
        rows.append([0] * i + pd + [0] * (n - 1 - i))
    for i in range(m):
        rows.append([0] * i + qd + [0] * (m - 1 - i))
    return determinant(rows)


def discriminant(p):
    n = len(p) - 1
    numerator = (-1) ** (n * (n - 1) // 2) * resultant(p, derivative(p))
    assert numerator % p[-1] == 0
    return numerator // p[-1]


def factor(n):
    n = abs(n)
    assert n
    answer = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            answer[p] = answer.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        answer[n] = answer.get(n, 0) + 1
    return answer


def vp(n, p):
    n = Fraction(n)
    assert n
    out = 0
    a, b = abs(n.numerator), n.denominator
    while a % p == 0:
        a //= p
        out += 1
    while b % p == 0:
        b //= p
        out -= 1
    return out


def unit_residue(n, p):
    n = Fraction(n) / Fraction(p) ** vp(n, p)
    return n.numerator * pow(n.denominator, -1, p) % p


def square_class_odd(n, p):
    unit = unit_residue(n, p)
    sign = pow(unit, (p - 1) // 2, p)
    return vp(n, p) % 2, 1 if sign == 1 else -1


def square_class_two(n):
    n = Fraction(n)
    e = vp(n, 2)
    unit = n / Fraction(2) ** e
    return e % 2, unit.numerator * pow(unit.denominator, -1, 8) % 8


def check_menus():
    menu = {
        1: [7], 2: [7],
        3: [7, 23, 39, 15], 6: [7, 23, 39, 15],
        5: [31, 7, 55, 15], 10: [31, 7, 55, 15],
        7: [15, 31, 7, 119], 14: [15, 31, 7, 119],
    }
    mus = sorted([sign * m for m in menu for sign in [-1, 1]])
    assert len(mus) == 16
    assert all(g > 0 and g % 8 == 7 for values in menu.values() for g in values)
    classes = {}
    for p in [3, 5, 7]:
        classes[str(p)] = [list(square_class_odd(g, p)) for g in menu[p]]
        assert {tuple(c) for c in classes[str(p)]} == {(i, j) for i in [0, 1] for j in [-1, 1]}
    choices = []
    for sign in [-1, 1]:
        for parity in [0, 1]:
            for unit in [1, 3, 5, 7]:
                b = sign * 2**parity * unit
                candidates = [mu for mu in mus if mu * b > 0 and square_class_two(-mu * b) == (0, 1)]
                assert len(candidates) == 1
                mu = candidates[0]
                assert square_class_two(Fraction(b, mu)) == (0, 7)
                choices.append({"input_sign": sign, "valuation_parity": parity,
                                "positive_unit_mod8": unit, "mu": mu})
    branches = [(mu, mu * g) for mu in mus for g in menu[abs(mu)]]
    assert len(branches) == len(set(branches)) == 52
    support = sorted({p for mu, delta in branches for p in factor(mu * delta)})
    assert support == [2, 3, 5, 7, 11, 13, 17, 23, 31]
    # For every odd prime dividing mu, every local class of b can be made
    # a square by one of that mu's four choices delta=mu*gamma.
    coverage = 0
    for mu in mus:
        odd = [p for p in factor(mu) if p != 2]
        assert len(odd) <= 1
        if not odd:
            continue
        p = odd[0]
        ns = next(a for a in range(1, p) if pow(a, (p - 1) // 2, p) == p - 1)
        for parity in [0, 1]:
            for unit in [1, ns]:
                b = p**parity * unit
                suitable = [g for g in menu[abs(mu)] if square_class_odd(mu * g * b, p) == (0, 1)]
                assert len(suitable) == 1
                coverage += 1
    assert coverage == 48
    assert all(vp(mu, 2) <= 1 and all(vp(mu, p) <= 1 for p in [3, 5, 7]) for mu in mus)
    return {"mu_values": mus, "mu_choices": choices, "gamma_menu": menu,
            "gamma_local_classes": classes, "original_phi_branch_count": len(branches),
            "original_phi_bad_primes": support, "local_menu_coverage_cases": coverage,
            "prepared_intrinsic_bad_primes": [2, 3, 5, 7],
            "prepared_intrinsic_pair_branch_count": len(mus)**2}


def check_normalizations():
    a, e, v, w, y, z, h = variables(7)
    old1 = y**2 - a**3 * v**4 + a * e**2
    old2 = z**2 - a**3 * w**4 + a * e**2 * h**2
    new1 = (y * v**-2)**2 - a**3 + a * (e * v**-2)**2
    new2 = (z * v**-2)**2 - a**3 * (w * v**-1)**4 + a * (e * v**-2)**2 * h**2
    assert old1 == v**4 * new1
    assert old2 == v**4 * new2

    a, r, w, z, h = variables(5)
    den = a + r**2
    en = a * (a - r**2)
    yn = 2 * a**2 * r
    assert yn**2 - a**3 * den**2 + a * en**2 == 0
    radicand = a * den**2 * w**4 - a * (a - r**2)**2 * h**2
    assert a**2 * (z**2 - radicand) == a**2 * z**2 - a**3 * den**2 * w**4 + a * en**2 * h**2
    # The inverse r=Y/(a+E) follows after using Y^2=a(a^2-E^2).
    a, e, y = variables(3)
    conic = y**2 - a**3 + a * e**2
    assert a * (a + e)**2 + y**2 - 2 * a**2 * (a + e) == conic
    assert a * (a * (a + e)**2 - y**2) - e * (a * (a + e)**2 + y**2) == -(a + e) * conic

    a, b, z, fa, fb = variables(5)
    assert b * (a + z * fa) - a * (b + z * fb) == z * (b * fa - a * fb)
    return {"first_abscissa_scaling": "two exact Laurent identities",
            "conic_chart": "two exact polynomial identities and two inverse identities",
            "formal_ratio_error": "exact numerator identity",
            "formal_ratio_bound": "v_p(error) >= v_p(z)-2*v_p(b), when v_p(z)>v_p(b)"}


def check_intrinsic():
    d, v, s = variables(3)
    p = d * (d + v**2)**2 * s**4 - d * (d - v**2)**2 * (1 - d)**2
    assert len(p.terms) == 12
    assert max(sum(e) for e in p.terms) == 9
    assert max(abs(c) for c in p.terms.values()) == 4
    b, v, s, y, mu = variables(5)
    omega = mu**5 * y**2 - mu**2 * b * (b + mu * v**2)**2 * s**4 + b * (b - mu * v**2)**2 * (mu - b)**2
    scaled = mu**5 * (y**2 - (b * mu**-1) * (b * mu**-1 + v**2)**2 * s**4
                        + (b * mu**-1) * (b * mu**-1 - v**2)**2 * (1 - b * mu**-1)**2)
    assert omega == scaled
    a, bden, v, s, y, mu = variables(6)
    rational_input = a * bden**-1
    substituted = mu**5 * y**2 - mu**2 * rational_input * (rational_input + mu * v**2)**2 * s**4 + rational_input * (rational_input - mu * v**2)**2 * (mu - rational_input)**2
    cleared = mu**5 * y**2 * bden**5 - mu**2 * a * (a + mu * v**2 * bden)**2 * s**4 * bden**2 + a * (a - mu * v**2 * bden)**2 * (mu * bden - a)**2
    assert cleared == bden**5 * substituted
    # Weight numerator/denominator by their degree bound d; intrinsic
    # coordinates each have degree 1, and mu is a fixed coefficient.
    for d_bound in range(0, 25):
        degree_bound = max(d_bound * (e[0] + e[1]) + e[2] + e[3] + e[4]
                           for e in cleared.terms)
        assert degree_bound == 5 * d_bound + 8
    branch_heights = {}
    for multiplier in [-14, -10, -7, -6, -5, -3, -2, -1, 1, 2, 3, 5, 6, 7, 10, 14]:
        b, v, s, y = variables(4)
        om = multiplier**5 * y**2 - multiplier**2 * b * (b + multiplier * v**2)**2 * s**4 + b * (b - multiplier * v**2)**2 * (multiplier - b)**2
        assert len(om.terms) == 13
        assert max(sum(e) for e in om.terms) == 9
        assert om.terms[(5, 0, 0, 0)] == 1  # primitive integer content
        branch_heights[str(multiplier)] = int(max(abs(c) for c in om.terms.values()))
    assert max(branch_heights.values()) == 537824
    # A complete symbolic valuation partition: n=-(2j+1), with r any
    # integer, and s-valuation l.  The two term valuations differ by
    # 4l-2n=2(2l+2j+1), which cannot vanish; both are odd.
    cases = 0
    for j in range(25):
        n = -2 * j - 1
        for vv in range(-25, 26):
            r = min(n, 2 * vv)
            for sv in range(-25, 26):
                term1, term2 = n + 2 * r + 4 * sv, 3 * n + 2 * r
                assert term1 % 2 == term2 % 2 == 1 and term1 != term2
                cases += 1
        # The v=0 case has r=n; the s=0 case leaves only term2.
        assert (3 * n + 2 * n) % 2 == 1
    return {"degree": 9, "monomials": 12, "coefficient_height": 4,
            "omega_scaling_identity": "Omega_mu = mu^5 * (Y^2-P_(b/mu)(v,s))",
            "omega_branch_degree": 9, "omega_branch_monomials": 13,
            "omega_branch_coefficient_heights": branch_heights,
            "omega_maximum_coefficient_height": 537824,
            "omega_primitive_coefficient": "coefficient of b^5 is 1",
            "rational_input_clearing": "B^5*Omega_mu(A/B), exact Laurent identity",
            "cleared_pole_degree_bound": "5*d+8, d=max(deg A,deg B)",
            "aggregated_degree_bound": "7*max(3,16*(5*d+8),deg G+1)",
            "supplementary_valuation_cases": cases,
            "symbolic_noncollision": "term1-term2 = 2*(2*l+2*j+1), j>=0",
            "zero_coordinates": "v=0 gives r=n; s=0 leaves a nonzero odd-valuation second term"}


def check_contact_function():
    p, q = [-2, 0, 0, 1], [-3, 0, 0, 1]
    div = multiply(p, q)
    assert div == [6, 0, 0, -5, 0, 0, 1]
    assert resultant(p, q) == -1
    assert discriminant(p) == -108
    assert discriminant(q) == -243
    assert discriminant(div) == 26244
    assert factor(discriminant(div)) == {2: 2, 3: 8}
    nonsquare_fibers = []
    for name, value, prime in [("zero", Fraction(2), 2), ("pole", Fraction(3), 3),
                               ("minus_one", Fraction(5, 2), 2)]:
        exponent = vp(value, prime)
        assert exponent % 3 != 0
        nonsquare_fibers.append({"fiber": name, "cube_value": str(value),
                                "obstructing_prime": prime, "valuation": exponent})
    return {"numerator_ascending": p, "denominator_ascending": q,
            "divisor_polynomial_ascending": div, "resultant": -1,
            "discriminants": [-108, -243, 26244], "branch_degree": 6,
            "geometric_bad_primes": [2, 3], "no_rational_special_fibers": nonsquare_fibers}


def check_valuation_propagation():
    # These parameterizations exhaust the signs of every nonzero odd e.
    j, k = variables(2)
    ep, en = 2 * j + 1, -2 * j - 1
    dp, dn = 3 * j + 2, -j
    assert 2 * dp - 3 * ep == 1
    assert 2 * dn - en == 1
    assert dp - ep == j + 1
    assert dn - en == j + 1
    depth = (2 * k - 1) * j + k
    assert 2 * depth - (2 * k - 1) * (2 * j + 1) == 1
    assert depth - k == (2 * k - 1) * j
    cases = 0
    for e in range(-101, 102, 2):
        assert e != 0
        for difference in range(-160, 161):
            first = 2 * difference + 2 * min(0, e) - 3 * e
            assert first % 2 == 1
            if first >= 0:
                assert difference > e
            cases += 1
        # lambda=-1 forces the same contradiction at either sign of e.
        special = 4 * min(0, e) - 3 * e
        assert special < 0 and special % 2 == 1
        for amplification in range(1, 13):
            least_depth = ((2 * amplification - 1) * abs(e) + 1) // 2
            assert least_depth >= amplification
    return {"first_positive_e": "e=2*j+1 -> v(lambda-g)>=3*j+2 -> v(lambda)=e",
            "first_negative_e": "e=-2*j-1 -> v(lambda-g)>=-j -> v(lambda)=e",
            "second_depth": "v(beta-t)>=(2*k-1)*j+k, |e|=2*j+1",
            "lambda_minus_one": "4*min(0,e)-3*e is negative and odd",
            "supplementary_integer_cases": cases,
            "zero_difference_cases": "lambda=g is already exact; beta=t implies t rational"}


def check_heights_and_counts():
    examples = []
    for r, k, epsilon in [(6, 2, Fraction(1, 4)), (5, 3, Fraction(1, 12))]:
        theta = r - 2 - epsilon
        odd_lower = 2 * theta - r
        upper = Fraction(2, k)
        margin = odd_lower - upper
        assert margin > 0
        examples.append({"divisor_degree": r, "amplification": k,
                         "vojta_epsilon": str(epsilon), "truncated_lower": str(theta),
                         "odd_support_lower": str(odd_lower), "conjugacy_upper": str(upper),
                         "margin": str(margin)})
    # The local truncated/full/odd counting inequality holds for all positive
    # intersection multiplicities by these exhaustive parity parameterizations.
    j = variables(1)[0]
    assert 2 * j + 2 - 2 == 2 * j  # even multiplicity 2j+2
    assert 2 * j + 1 + 1 - 2 == 2 * j  # odd multiplicity 2j+1
    counts = {"normalized_conics": 1 + 8 + 2 * 5 + 1,
              "rational_conic_chart": 1 + 8 + 2 * 4 + 1,
              "prepared_intrinsic_chart": 1 + 8 + 2 * 3 + 1}
    assert counts == {"normalized_conics": 20, "rational_conic_chart": 18,
                      "prepared_intrinsic_chart": 16}
    return {"examples": examples, "coordinate_censuses": counts,
            "census_scope": "Q as a subfield of K; all four affine elliptic point pairs retained",
            "not_a_rational_integer_record": True,
            "counting_identity": "2*N_D_truncated <= N_D_full + N_D_odd"}


def report():
    result = {
        "schema": "pasten-vidaux-v81-independent-v1",
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "menus": check_menus(),
        "normalizations": check_normalizations(),
        "intrinsic_pole": check_intrinsic(),
        "contact_function": check_contact_function(),
        "valuation_propagation": check_valuation_propagation(),
        "height_margins_and_censuses": check_heights_and_counts(),
        "not_computationally_certified": [
            "abc or the stated truncated-counting lower bound over K",
            "positive stable rank for an elliptic curve defined over Q",
            "Burungale's simultaneous-twist theorem and rational completeness",
            "formal-group and real-place approximation proofs",
            "the global conjugacy/height argument and the ineffective exceptional polynomial",
            "any count below 25 or 11 for defining Z in Q",
        ],
    }
    return json.loads(json.dumps(result, sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, help="explicitly write the computed certificate")
    args = parser.parse_args()
    result = report()
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.write_text(serialized)
    else:
        committed = Path(__file__).with_name("independent_certificate.json")
        if committed.exists():
            assert json.loads(committed.read_text()) == result, "committed certificate differs"
    print("PASS: menus, source maps, intrinsic pole, contact divisor, valuation identities, and counts")
    print("Arithmetic inputs and the global proof remain the separate manual review's scope.")


if __name__ == "__main__":
    main()
