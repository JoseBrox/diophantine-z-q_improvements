#!/usr/bin/env python3
"""Exact finite checks accompanying the norm-image reduction theorem.

The theorem for every positive degree is proved in the TeX paper.
These standard-library calculations check the displayed coefficient
identity in degrees 1..64 and the quadratic specialization independently.
They do not prove any Diophantine definition of a number field's integers.
"""
from fractions import Fraction
from math import comb, factorial
from pathlib import Path
import json


def shifted_power_coefficients(shift, degree):
    return [comb(degree, k) * shift ** (degree-k)
            for k in range(degree+1)]


def check_degree(n):
    coefficients = [0] * (n+1)
    for j in range(n):
        factor = (-1) ** (n-1-j) * comb(n-1, j)
        for k, coefficient in enumerate(shifted_power_coefficients(j, n)):
            coefficients[k] += factor * coefficient
    expected = [factorial(n)*(n-1)//2, factorial(n)] + [0] * (n-1)
    assert coefficients == expected, (n, coefficients, expected)
    # Completeness of the resulting linear image for a nonintegral sample.
    q = Fraction(13, 17)
    t = q / factorial(n) - Fraction(n-1, 2)
    value = sum((-1)**(n-1-j) * comb(n-1, j) * (t+j)**n
                for j in range(n))
    assert value == q
    return {"degree": n, "identity": "PASS", "rational_specialization": "PASS"}


def quadratic_checks():
    cases = []
    # Norm of rational a in a quadratic extension is a^2, independent of d.
    for q in [Fraction(0), Fraction(-7, 3), Fraction(1, 2), Fraction(13, 17)]:
        a = (q+1)/2
        b = (q-1)/2
        assert a*a-b*b == q
        cases.append(str(q))
    # x=a+b*sqrt(d): N(x)-x^2 = -2*d*b^2-2*a*b*sqrt(d).
    # A nonsquare d is nonzero; simultaneous zero forces b=0.
    for d in [Fraction(2), Fraction(-1), Fraction(-3), Fraction(5)]:
        for a in [Fraction(0), Fraction(1), Fraction(-3, 7)]:
            for b in [Fraction(0), Fraction(1), Fraction(2, 9)]:
                norm_minus_square = (-2*d*b*b, -2*a*b)
                assert (norm_minus_square == (0,0)) == (b == 0)
    return {"rational_difference_samples": cases,
            "quadratic_norm_fixed_field_samples": "PASS"}


def elliptic_reduction_checks():
    """Enumerate all residue-field points in two independent ways."""
    curve_reports = []
    for p, expected in [(5, 6), (7, 7)]:
        direct = [(x,y) for x in range(p) for y in range(p)
                  if (y*y-x*x*x+2) % p == 0]
        counts = [sum((y*y-x*x*x+2) % p == 0 for y in range(p))
                  for x in range(p)]
        legendre_count = 1
        for x in range(p):
            rhs = (x*x*x-2) % p
            legendre_count += 1 if rhs == 0 else (2 if pow(rhs,(p-1)//2,p)==1 else 0)
        assert len(direct)+1 == sum(counts)+1 == legendre_count == expected
        assert (-1728) % p != 0
        curve_reports.append({"prime":p,"affine_ordinate_counts":counts,
                              "group_order":expected,"good_reduction":True,
                              "independent_legendre_count":legendre_count})
    assert pow((-2)%5,2,5)==4  # Euler criterion for a nonsquare.
    x,y = Fraction(3),Fraction(5)
    slope = 3*x*x/(2*y)
    x2 = slope*slope-2*x
    y2 = slope*(x-x2)-y
    assert (x2,y2)==(Fraction(129,100),Fraction(-383,1000))
    assert y2*y2==x2*x2*x2-2
    return {"curve":"y^2=x^3-2","point":[3,5],
            "double":[str(x2),str(y2)],"reductions":curve_reports,
            "constant_coefficient_nonsquare_mod_5":True,
            "scope":"Exact group counts and doubling; torsion and valuation deductions are proved in the paper."}


def main():
    report = {
        "status": "PASS",
        "scope": "Finite exact checks of coefficient identities and illustrative quadratic substitutions; general algebraic reductions are proved in the accompanying paper.",
        "degrees_checked": [check_degree(n) for n in range(1,65)],
        "quadratic_checks": quadratic_checks(),
        "elliptic_abscissa_obstruction": elliptic_reduction_checks(),
        "general_statement": "For every characteristic-zero finite extension L/K of degree n, K is Diophantine in L iff the relative norm image is Diophantine as a subset of L.",
        "does_not_claim": "No ring-of-integers definition or counterexample for a new number field is asserted by these finite checks."
    }
    destination = Path(__file__).with_name('norm-image-reduction-verification.json')
    destination.write_text(json.dumps(report, indent=2)+'\n')
    print(f'PASS: finite differences in degrees 1..64; quadratic examples; elliptic reductions at 5 and 7. Wrote {destination.name}.')


if __name__ == '__main__':
    main()
