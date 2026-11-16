#!/usr/bin/env python3
"""Verify finite-class identities and an infinite prepared coefficient family."""
from pathlib import Path
from fractions import Fraction
from math import isqrt
import argparse
import hashlib
import json
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def valuation(value, prime):
    value = Fraction(value)
    if not value:
        raise ValueError('The valuation of zero is not used.')
    n, d = value.numerator, value.denominator
    answer = 0
    while n % prime == 0:
        n //= prime
        answer += 1
    while d % prime == 0:
        d //= prime
        answer -= 1
    return answer


def main(output):
    t, k, a, d, n, den, q = sp.symbols('t k a d n den q')
    checks = []

    def identity(name, expression):
        if sp.cancel(expression) != 0:
            raise ValueError(name)
        checks.append(name)

    identity('cleared finite quadratic root',
             q**2-d*a*den*(a*den-n)
             -den**2*((q/den)**2-d*a*(a-n/den)))
    u, v = sp.symbols('u v')
    rho = sp.sqrt(2)
    identity('rational-square character decomposition',
             (u+rho*v)**2-(u*u+2*v*v+2*u*v*rho))

    va, vd, vb, vm, vw = sp.symbols('va vd vb vm vw', integer=True)
    identity('negative odd local valuation parity',
             (2*va+2*vd-(2*vb+1))-(2*(va+vd-vb)-1))
    identity('whole-algebra guard parity',
             (1+2*vm-2*vw)-(1+2*(vm-vw)))

    collision = sp.Rational(17, 13)
    identity('coincident finite-branch radicands',
             17*17*(17-collision)-68*(68-collision))

    numerator = 34*(3272*t*t-409*t-136)
    denominator = 69*(17+409*t*t)
    qnumerator = 17*(17-544*t-409*t*t)
    s = numerator/denominator
    z = qnumerator/denominator
    b = s*s
    identity('conic parametrization', 17*s*s+409*z*z-289)
    identity('nonsquare complement class', 17*(17-b)-409*z*z)
    identity('upper real bound', sp.Rational(272, 69)-s
             -2*(17*272+409*17*t)/(69*(17+409*t*t)))
    if sp.cancel(sp.diff(b, t)) == 0:
        raise ValueError('The family must be nonconstant.')
    checks.append('nonconstant rational family')

    # These exact sign certificates hold for every real t>=10.
    sign_certificates = {}
    for name, polynomial, sign in (
            ('positive s numerator', numerator, 1),
            ('positive denominator', denominator, 1),
            ('nonzero q numerator', qnumerator, -1)):
        coefficients = sp.Poly(sign*polynomial.subs(t, 10+u), u).all_coeffs()
        if not all(c >= 0 for c in coefficients) or coefficients[-1] <= 0:
            raise ValueError(name)
        sign_certificates[name] = list(map(int, coefficients))
        checks.append(name)
    assert sp.Rational(272, 69)**2 < 17
    assert sp.isprime(409) and isqrt(409)**2 != 409
    checks.extend(['strict real upper bound below 17', 'nontrivial square class 409'])

    # Prove constant valuations on the entire integer progression, not a sample.
    modulus = 187272
    assert modulus == 2**3*3**4*17**2
    progression = []
    for prime, expected_num, expected_den in ((2, 2, 0), (3, 3, 2), (17, 1, 0)):
        data = {'prime': prime}
        for name, polynomial, expected in (
                ('numerator', numerator, expected_num),
                ('denominator', denominator, expected_den)):
            poly = sp.Poly(polynomial.subs(t, 10+modulus*k), k)
            constant = int(poly.nth(0))
            if valuation(constant, prime) != expected:
                raise ValueError('Wrong constant valuation.')
            nonconstant = [int(poly.nth(j)) for j in range(1, poly.degree()+1)]
            values = [valuation(c, prime) for c in nonconstant if c]
            if not all(value > expected for value in values):
                raise ValueError('Progression does not preserve valuation.')
            data[name] = {'constant_valuation': expected,
                          'nonconstant_coefficient_valuations': values}
        data['input_valuation'] = 2*(expected_num-expected_den)
        progression.append(data)
        checks.append('uniform progression valuation at '+str(prime))

    s0, q0, b0 = [sp.cancel(x.subs(t, 10)) for x in (s, z, b)]
    assert s0 == sp.Rational(1220124, 313697)
    assert q0 == -sp.Rational(87499, 313697)
    assert b0 == sp.Rational(1488702575376, 98405807809)
    assert isqrt(int(sp.denom(b0)))**2 == int(sp.denom(b0))
    checks.append('exact prepared fixture and square reduced denominator')

    source = ROOT/'papers/pole_parameters/guarded_complement_reduction_20261116_v45.tex'
    report = {
        'schema': 'finite-native-complement-classes/v46',
        'status': 'PASS', 'sympy': sp.__version__,
        'checks': checks, 'check_count': len(checks),
        'source': str(source.relative_to(ROOT)),
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'family': {'squareclass': 409, 'parameter': 't=10+187272*k, k>=0',
                   'fixture': {'s': str(s0), 'q': str(q0), 'b': str(b0)},
                   'sign_certificates': sign_certificates,
                   'uniform_valuation_certificates': progression},
        'conditional_counts': {'general': 21, 'conditional': 9},
        'actual_native_realization_proved': False,
        'scope': 'Exact algebra, parity identities, and a prepared coefficient family. '
                 'Finite-algebra soundness and the conditional implication are proved '
                 'in the manuscript. The family is not asserted to be native.'
    }
    encoded = json.dumps(report, indent=2)+'\n'
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(encoded)
    else:
        stored = HERE/'certificate.json'
        if stored.read_text() != encoded:
            raise ValueError('Committed certificate differs from reconstruction.')
    print(encoded)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    main(parser.parse_args().output)
