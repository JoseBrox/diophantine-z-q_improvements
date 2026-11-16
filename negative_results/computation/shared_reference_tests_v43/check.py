#!/usr/bin/env python3
"""Exact local checks for the shared-reference detector obstructions.

The proof is Hensel-theoretic. The modular witnesses additionally check both
actual elliptic embeddings, both suggested baseline powers, and an actual
contact argument. No global rational source tuple is asserted.
"""
from pathlib import Path
from math import isqrt, prod
from hashlib import sha256
import argparse
import json
import sympy as sp

HERE = Path(__file__).resolve().parent
P = 76537
CONTACTS = (-5, -2, -1, 0, 2, 3, 4, 7)


def valuation(n, p=P):
    if n == 0:
        return None
    n = abs(n)
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def hensel(fun, derivative, seed, digits):
    assert fun(seed) % P == 0
    assert derivative(seed) % P
    x, current = seed % P, 1
    while current < digits:
        current = min(2 * current, digits)
        modulus = P ** current
        x = (x - fun(x) * pow(derivative(x), -1, modulus)) % modulus
        assert fun(x) % modulus == 0
    return x


def exact_divided_ratio(numerator, denominator, denominator_order, digits):
    factor = P ** denominator_order
    assert numerator % factor == denominator % factor == 0
    return (numerator // factor) * pow(denominator // factor, -1, P ** digits) % (P ** digits)


def check_local(embedding, baseline_power):
    digits, target = 60, 36
    modulus = P ** digits
    rho = hensel(lambda x: x*x-2, lambda x: 2*x, embedding, digits)
    i = hensel(lambda x: x*x+1, lambda x: 2*x, 8042, digits)
    D = (11-6*rho) % modulus
    a = (57-28*rho) * pow(8, -1, modulus) % modulus
    b = (-660+417*rho) * pow(32, -1, modulus) % modulus
    c = b * pow(a, -1, modulus) % modulus
    assert (b*b-a*a*a+D*a) % modulus == 0
    assert all(x % P for x in (D, a, b, c))

    # Q is formal with z_Q=p; H=Q+T0. U is formal with z_U=p^2.
    zQ, zU = P, P**2

    def formal_reciprocal(z):
        return hensel(lambda f: D*z*z*f*f+f-z*z,
                      lambda f: 2*D*z*z*f+1, 0, digits)

    fQ, fU = formal_reciprocal(zQ), formal_reciprocal(zU)
    hQ, hU = fQ // zQ, fU // zU
    assert valuation(fQ) == 2 and valuation(fU) == 4
    check_modulus = P**50
    assert (hQ*hQ-fQ+D*fQ**3) % check_modulus == 0
    assert (hU*hU-fU+D*fU**3) % check_modulus == 0

    xH, yH = -D*fQ, -D*hQ
    assert (yH*yH-xH**3+D*xH) % check_modulus == 0
    # Exact formula for v=ell^{-1} on the reference chart.
    v_modulus = P**59
    v = ((yH+b)*pow(xH-a, -1, v_modulus)+c) % v_modulus
    assert valuation(v) == 1
    # At H=Q+T0, S=1/zQ, hence L=-zU/zQ=-p exactly.
    L, beta = -P, 4
    C = L-beta
    assert valuation(C) == 0
    assert (hU*L*zQ+fU) % check_modulus == 0

    # sqrt(f_U)=zU*sqrt(f_U/zU^2), with the latter square root 1 mod p.
    unit_f = fU // (P**4)
    root_unit = hensel(lambda x: x*x-unit_f, lambda x: 2*x, 1, 56)
    root_f = zU*root_unit
    assert (root_f**2-fU) % check_modulus == 0
    w0 = (i*fU*root_f*v) % modulus
    assert valuation(w0) == 7
    assert (w0*w0+fU**3*v*v) % (P**55) == 0

    e3 = exact_divided_ratio(C*C*w0**3, fU**3, 12, target)
    last_power = baseline_power+3
    e_last = exact_divided_ratio(w0**last_power, fU**3, 12, target)
    assert valuation(e3) == 9
    assert valuation(e_last) == (16 if baseline_power == 1 else 30)
    fun = lambda y: 1-y*y+e3*y**3+e_last*y**last_power
    deriv = lambda y: -2*y+3*e3*y*y+last_power*e_last*y**(last_power-1)
    y = hensel(fun, deriv, 1, target)
    w = w0*y
    assert valuation(w) == 7

    # Multiply the original cleared factor by v^2 to avoid negative orders.
    # Its normalizing denominator has order v(f^3*v^2)=14.
    residual = v*v*w**last_power+C*C*v*v*w**3+w*w+fU**3*v*v
    assert residual % (P**50) == 0

    def contact_poly(t):
        return prod(t-a0 for a0 in CONTACTS)

    def contact_derivative(t):
        return sum(prod(t-a0 for j, a0 in enumerate(CONTACTS) if j != k)
                   for k in range(len(CONTACTS)))

    contact = hensel(lambda t: contact_poly(t)-w*(t-1)**6,
                     lambda t: contact_derivative(t)-6*w*(t-1)**5,
                     0, 43)
    assert valuation(contact) == 7
    assert (contact_poly(contact)-w*(contact-1)**6) % (P**43) == 0
    return {
        'sqrt_two_residue': embedding,
        'baseline_power': baseline_power,
        'reference_depth': 1,
        'numerator_depth': 2,
        'raw_ratio_order': 1,
        'comparison_order': 0,
        'contact_order': 7,
        'epsilon3_order': 9,
        'last_epsilon_order': valuation(e_last),
        'cleared_factor_verified_modulo': 'p^50',
        'contact_equation_verified_modulo': 'p^43',
        'reference_subgroup_constraint_imposed': False,
        'global_source_constraints_imposed': False,
    }


def check_squared_point(embedding):
    digits = 60
    modulus = P**digits
    rho = hensel(lambda x: x*x-2, lambda x: 2*x, embedding, digits)
    i = hensel(lambda x: x*x+1, lambda x: 2*x, 8042, digits)
    D = (11-6*rho) % modulus
    a = (57-28*rho)*pow(8, -1, modulus) % modulus
    b = (-660+417*rho)*pow(32, -1, modulus) % modulus
    c = b*pow(a, -1, modulus) % modulus
    beta, zQ, zU = 4, P, -4*P

    def formal_reciprocal(z):
        return hensel(lambda f: D*z*z*f*f+f-z*z,
                      lambda f: 2*D*z*z*f+1, 0, digits)

    fQ, fU = formal_reciprocal(zQ), formal_reciprocal(zU)
    hQ = fQ//P
    hU = (fU//P)*pow(-beta, -1, P**59) % (P**59)
    assert valuation(fQ) == valuation(fU) == 2
    assert (hU*hU-fU+D*fU**3) % (P**50) == 0
    assert (hU*beta*P+fU) % (P**50) == 0
    assert ((1-D*fU*fU)*beta*P+hU) % (P**50) == 0
    xH, yH = -D*fQ, -D*hQ
    assert (yH*yH-xH**3+D*xH) % (P**50) == 0
    v = ((yH+b)*pow(xH-a, -1, P**59)+c) % (P**59)
    assert valuation(v) == 1
    # q=i*ell/f_U, hence w=q^{-1}=f_U*v/i.
    w = (fU*v*pow(i, -1, modulus)) % modulus
    assert valuation(w) == 3
    assert (w*w+fU*fU*v*v) % (P**55) == 0

    def contact_poly(t):
        return prod(t-a0 for a0 in CONTACTS)

    def contact_derivative(t):
        return sum(prod(t-a0 for j, a0 in enumerate(CONTACTS) if j != k)
                   for k in range(len(CONTACTS)))

    contact = hensel(lambda t: contact_poly(t)-w*(t-1)**6,
                     lambda t: contact_derivative(t)-6*w*(t-1)**5,
                     0, 50)
    assert valuation(contact) == 3
    return {
        'sqrt_two_residue': embedding,
        'reference_depth': 1,
        'numerator_depth': 1,
        'target_beta': beta,
        'raw_ratio': beta,
        'comparison': 0,
        'contact_order': 3,
        'each_canceled_term_order': -5,
        'factor_value': 1,
        'cancellation_verified_modulo': 'p^55 after integral clearing',
        'contact_equation_verified_modulo': 'p^50',
        'global_source_constraints_imposed': False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=HERE/'verification.json')
    args = parser.parse_args()
    assert all(P%d for d in range(2, isqrt(P)+1))
    assert P > 76176 and P % 8 == 1
    assert 8042**2 % P == P-1
    t = sp.symbols('t')
    contact_weight = sp.prod(t-a0 for a0 in CONTACTS)/(t-1)**6
    derivative_at_zero = sp.diff(contact_weight, t).subs(t, 0)
    assert contact_weight.subs(t, 0) == 0 and derivative_at_zero == 1680

    i, r, ell, C, Y = sp.symbols('i r ell C Y', nonzero=True)
    f = r*r
    w0 = i*r**3/ell
    for baseline in (1, 3):
        power = baseline+3
        polynomial = (w0*Y)**power+C*C*(w0*Y)**3+ell*ell*(w0*Y)**2+f**3
        normalized = 1-Y*Y+(C*C*w0**3/f**3)*Y**3+(w0**power/f**3)*Y**power
        numerator = sp.fraction(sp.cancel(polynomial/f**3-normalized))[0]
        assert sp.rem(numerator, i*i+1, i) == 0

    q = i*ell/f
    numerator = sp.fraction(sp.cancel(q*ell**2+q**3*f**2))[0]
    assert sp.rem(numerator, i*i+1, i) == 0

    k, m = sp.symbols('k m', positive=True, integer=True)
    assert sp.expand(3*k+3*m+2*(m-k)) == k+5*m
    assert sp.expand(4*(k+3*m)-6*m) == 4*k+6*m
    assert sp.expand(6*(k+3*m)-6*m) == 6*k+12*m
    # Unit-chart weighted-square identity: J=q*ell^2 iff J*v=q*ell.
    q = sp.symbols('q', nonzero=True)
    assert sp.cancel((q*ell*ell)*(1/ell)-q*ell) == 0

    checks = [check_local(embedding, baseline)
              for embedding in (26935, 49602) for baseline in (1, 3)]
    squared_checks = [check_squared_point(embedding) for embedding in (26935, 49602)]
    report = {
        'status': 'PASS',
        'scope': 'local factor-level obstructions; no global defining-polynomial counterexample',
        'prime': P,
        'sqrt_minus_one_residue': 8042,
        'contact_derivative_at_zero': int(derivative_at_zero),
        'exact_symbolic_identity': 'P(w0 Y)/f^3 = 1-Y^2+epsilon3*Y^3+epsilon_last*Y^last',
        'hensel_reduction': '1-Y^2; derivative at Y=1 is -2 modulo p',
        'local_modular_checks': checks,
        'squared_point_local_checks': squared_checks,
        'not_imposed': ['global rational points', 'global cyclic indices',
                        'required doubled reference subgroup', 'both conjugate factors',
                        'other shifted detector', 'height relation', 'full pole constraints'],
        'verifier_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'local_checks': len(checks)+len(squared_checks),
                      'certificate': str(output)}, indent=2))


if __name__ == '__main__':
    main()
