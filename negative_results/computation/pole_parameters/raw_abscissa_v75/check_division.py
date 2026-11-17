#!/usr/bin/env python3
"""Third audit: division polynomials modulo p^3, with no group-law imports.

Formulas: A. Sutherland, MIT 18.783, Fall 2025, Lecture 5,
sections 5.5--5.6, https://math.mit.edu/classes/18.783/2025/LectureNotes5.pdf.
This checker evaluates the recurrences at the literal base point; it
does not use either the producer's projective law or the affine audit.
"""
from functools import lru_cache
from hashlib import sha256
from math import gcd, isqrt
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def division_multiple(n, x, y, aa, modulus, prime):
    assert (y*y-x*x*x-aa*x) % modulus == 0
    assert gcd(2*y, prime) == 1
    inv2y = pow(2*y, -1, modulus)

    @lru_cache(None)
    def psi(k):
        if k < 0:
            return -psi(-k) % modulus
        if k == 0:
            return 0
        if k == 1:
            return 1
        if k == 2:
            return 2*y % modulus
        if k == 3:
            return (3*x**4+6*aa*x*x-aa*aa) % modulus
        if k == 4:
            return 4*y*(x**6+5*aa*x**4-5*aa*aa*x*x-aa**3) % modulus
        h = k//2
        if k % 2:
            return (psi(h+2)*psi(h)**3-psi(h-1)*psi(h+1)**3) % modulus
        return (psi(h)*inv2y*(psi(h+2)*psi(h-1)**2
                              - psi(h-2)*psi(h+1)**2)) % modulus

    den = psi(n)
    assert gcd(den, prime) == 1
    xx = (x-psi(n-1)*psi(n+1)*pow(den, -2, modulus)) % modulus
    omega = ((psi(n+2)*psi(n-1)**2-psi(n-2)*psi(n+1)**2)
             * pow(4*y, -1, modulus)) % modulus
    yy = omega*pow(den, -3, modulus) % modulus
    assert (yy*yy-xx**3-aa*xx) % modulus == 0
    return xx, yy, psi.cache_info().currsize


def main():
    p = 76777
    assert all(p % d for d in range(2, isqrt(p)+1))
    modulus = p**3
    certificate = json.loads((HERE/'certificate.json').read_text())
    rows = []
    for rho2, expected_xunit, expected_yunit in (
            (3367298917, 64192, 57786), (2527408812, 61852, 63990)):
        assert (rho2*rho2-2) % (p*p) == 0
        correction = (-(rho2*rho2-2)//(p*p)*pow(2*rho2, -1, p)) % p
        rho = rho2+correction*p*p
        assert (rho*rho-2) % modulus == 0
        x = (57-28*rho)*pow(8, -1, modulus) % modulus
        y = (-660+417*rho)*pow(32, -1, modulus) % modulus
        aa = -(11-6*rho) % modulus
        x2, y2, _ = division_multiple(2, x, y, aa, modulus, p)
        slope = (3*x*x+aa)*pow(2*y, -1, modulus) % modulus
        assert x2 == (slope*slope-2*x) % modulus
        assert y2 == (slope*(x-x2)-y) % modulus
        xq, yq, count = division_multiple(10335, x, y, aa, modulus, p)
        assert xq % (p*p) == 0 and xq//(p*p) == expected_xunit
        assert yq % p == 0 and yq//p % p == expected_yunit
        recorded = next(row for row in certificate['point_valuations']
                        if row['sqrt2_mod_p2'] == rho2)
        assert [xq % (p*p), yq % (p*p)] == recorded['HminusP_affine_mod_p2']
        assert xq//(p*p) == recorded['x_over_p2_mod_p']
        rows.append(dict(sqrt2_mod_p3=rho, x_mod_p3=xq, y_mod_p3=yq,
                         x_over_p2_mod_p=expected_xunit,
                         y_over_p_mod_p=expected_yunit,
                         division_polynomials_evaluated=count))
    assert sum(row['sqrt2_mod_p3'] for row in rows) == modulus
    result = dict(status='PASS', method='division polynomials modulo p^3',
                  n=10335, p=p, modulus=modulus,
                  base_point_denominators_units=True,
                  division_polynomial_denominators_units=True,
                  independent_doubling_control=True,
                  curve_equation_verified_mod_p3=True,
                  literal_abscissa_valuations=[2, 2],
                  certificate_sha256=sha256((HERE/'certificate.json').read_bytes()).hexdigest(),
                  slots=rows)
    (HERE/'division_certificate.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
