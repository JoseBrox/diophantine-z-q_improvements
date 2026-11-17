#!/usr/bin/env python3
"""Exact algebra checks for the v69 actual-trace curve/family obstruction.

The geometric finiteness and abelian-family theorems are proved in the TeX
paper; finite valuation cases are regression checks, not their proof.
Requires SymPy. Example: python check.py --output certificate.json
"""
import argparse
import hashlib
import json
from pathlib import Path

import sympy as s


def point_count_prime(d, p):
    brute = 1 + sum((y*y-x*x*x+d*x) % p == 0
                    for x in range(p) for y in range(p))
    squares = {y*y % p for y in range(1, p)}
    table = [0, 0, 0]
    for x in range(p):
        value = (x*x*x-d*x) % p
        table[0 if value == 0 else 1 if value in squares else 2] += 1
    second = 1 + table[0] + 2*table[1]
    assert brute == second
    return {'point_count': brute, 'zero_square_nonsquare_abscissas': table}


def twist_and_reductions():
    rho, root7 = s.sqrt(2), s.sqrt(7)
    d, conjugate_d = 3-rho, 3+rho
    lam = conjugate_d/root7
    delta = conjugate_d/d
    assert s.simplify(d*conjugate_d-7) == 0
    assert s.simplify(lam**2-delta) == 0
    assert s.simplify(d**2*lam**4-conjugate_d**2) == 0
    x, y = s.symbols('x y')
    transformed = (lam**3*y)**2-(lam**2*x)**3+conjugate_d**2*lam**2*x
    assert s.simplify(transformed-lam**6*(y*y-x**3+d*d*x)) == 0
    assert 6*6 % 17 == 2 and 4*4 % 17 == 16
    assert (11-6*6) % 17 == 9 and (11+6*6) % 17 == 13
    reductions = {str(dv): point_count_prime(dv, 17) for dv in (9, 13)}
    assert reductions['9']['point_count'] == 20
    assert reductions['13']['point_count'] == 16
    assert all(64*dv**3 % 17 for dv in (9, 13))
    return {'twist_isomorphism_symbolically_verified': True,
            'lambda': '(3+sqrt(2))/sqrt(7)', 'reduction_prime': 17,
            'reductions': reductions}


def contacts_and_infinity():
    a, z, u, c, t, r, j, v4 = s.symbols('a z u c t r j v4')
    shifts = (-10, -8, -5, 1, 2, 3, 4, 6, 7)
    assert sum(shifts) == 0
    f = s.Poly(s.prod((a+k)**2-z*z for k in shifts), z, a).as_expr()
    fa, fz = s.diff(f, a), s.diff(f, z)
    verified = []
    for k in shifts:
        pc = s.prod((other-k)*(2*a+k+other) for other in shifts if other != k)
        for epsilon in (-1, 1):
            contact = epsilon*(a+k)
            assert s.Poly(f.subs(z, contact), a).is_zero
            assert s.Poly(fa.subs(z, contact)-2*(a+k)*pc, a).is_zero
            assert s.Poly(fz.subs(z, contact)+2*epsilon*(a+k)*pc, a).is_zero
            assert s.cancel(-18*(-2*epsilon*(a+k)*pc)/(2*(a+k)*pc)) == 18*epsilon
            verified.append({'shift': k, 'sign': epsilon,
                             'u_derivative': 18*epsilon, 'C_derivative': 36*epsilon})
    assert s.Poly(f, z).coeff_monomial(z**18) == -1
    assert s.Poly(fa, z).coeff_monomial(z**16) == 18*a
    # Generic reciprocal balanced factor at u=0 and u=infinity.
    inverse_factor = u*(1+u*c*c)**2/(u*(1+u*c*c)**2+c**4)
    assert s.simplify(s.limit(inverse_factor/u, u, 0)-c**-4) == 0
    infinity_factor = s.cancel(inverse_factor.subs(u, 1/t))
    expansion = s.series(infinity_factor, t, 0, 4).removeO()
    assert s.simplify(expansion-(1-t**3)) == 0
    v = 2-r*t**3+j*t**4
    w = t/(1+t)**2
    radicand = s.series(v*v+w*(2-v), t, 0, 4).removeO()
    assert s.expand(radicand-(4-4*r*t**3)) == 0
    v = u**4*v4
    contact_expansion = s.series(v*v+u/(1+u)**2*(2-v), u, 0, 2).removeO()
    assert contact_expansion == 2*u
    v, w = s.symbols('V w')
    classes = [s.Integer(1), v+2, v*v-v+2, 1+w*(2-v)]
    assert [x.subs({v: 0, w: 0}) for x in classes] == [1, 2, 2, 1]
    assert [x.subs({v: 2, w: 0}) for x in classes] == [1, 4, 4, 1]
    return {'shifts': list(shifts), 'contacts': verified,
            'F_leading_term': '-z^18', 'F_a_leading_term': '18*a*z^16',
            'u_infinity_leading_term': 'z^2/a',
            'inverse_factor_infinity': '1-u^(-3)+O(u^(-4))',
            'C_infinity': '4+O(z^(-6))',
            'rational_infinity_ordinates': [-2, 2],
            'small_class_contact_units': [1, 2, 2, 1],
            'small_class_infinity_values': [1, 4, 4, 1]}


def order_at_zero(expr, t):
    numerator, denominator = s.fraction(s.cancel(expr))
    def order(poly):
        polynomial = s.Poly(poly, t)
        assert not polynomial.is_zero
        return min(power[0] for power in polynomial.monoms())
    return order(numerator)-order(denominator)


def balanced_boundary_checks():
    t = s.symbols('t')
    cases = nonpositive = 0
    for nu in range(1, 16, 2):
        for exponent in range(-12, 13):
            u, c = t**nu, t**exponent
            d = c*c/(1+u*c*c)
            factor = 1+d*d/u
            vd, vf = order_at_zero(d, t), order_at_zero(factor, t)
            assert vd == max(2*exponent, -nu)
            assert vf == min(0, 2*vd-nu)
            if exponent <= 0:
                assert vf <= -nu
                nonpositive += 1
            cases += 1
    return {'exact_Laurent_cases': cases,
            'nonpositive_test_cases_enforcing_inverse_order_at_least_nu': nonpositive,
            'nu_range_odd': [1, 15], 'test_valuation_range': [-12, 12],
            'zero_test_case': 'D=0 and factor=1 exactly',
            'scope': 'Finite exact regression cases; the manuscript gives the general parity proof.'}


def general_contacts():
    t, rho, r, scalar = s.symbols('t rho r scalar')
    theta = [s.Rational(0), -s.Rational(1, 2), s.Rational(-1),
             s.Rational(1, 2399), -s.Rational(32, 407)]
    contacts = [shift+value for shift in (2, 4) for value in theta]
    assert len(set(contacts)) == 10 and -1 not in contacts
    numerator = s.prod(t-value for value in contacts)
    derivatives = []
    for contact in contacts:
        derivative = s.prod(contact-other for other in contacts if other != contact)/(contact+1)**10
        assert derivative != 0
        assert s.diff(numerator, t).subs(t, contact)/(contact+1)**10 == derivative
        derivatives.append({'contact': str(contact), 'R_derivative': str(derivative)})
    w = rho*r/(1+rho*r)**2
    for kappa in (1, 3):
        g = r**(kappa+1)*(r*scalar/(1+r*scalar))
        expected = r**5*scalar**2*(1+rho*r)**(4*kappa-2)/(rho**(2*kappa-1)*(1+r*scalar)**2)
        assert s.cancel(g*g/w**(2*kappa-1)-expected) == 0
    return {'contacts': derivatives, 'all_contacts_distinct_and_away_from_pole': True,
            'scalar_second_summand_has_exact_R_power_five': True,
            'scalar_orders_checked': [1, 3], 'first_cover_branch_points_at_least': 10,
            'first_cover_genus_bound_from_Riemann_Hurwitz': 4}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--manuscript', type=Path,
                        help='Manuscript to hash; defaults to the adjacent recovery copy.')
    args = parser.parse_args()
    here = Path(__file__).parent
    source = args.manuscript or here/'curves_and_abelian_families_20261117_v69.tex'
    result = {'status': 'PASS', 'sympy_version': s.__version__,
              'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'scope': 'Exact algebra only; geometric theorems are proved in the manuscript.',
              'twist_and_reductions': twist_and_reductions(),
              'contacts_and_infinity': contacts_and_infinity(),
              'balanced_boundary_checks': balanced_boundary_checks(),
              'general_contacts': general_contacts()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
