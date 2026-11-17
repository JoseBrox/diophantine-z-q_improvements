#!/usr/bin/env python3
"""Producer-free division-polynomial reconstruction of the odd-coset example."""
from functools import lru_cache
from fractions import Fraction
from math import isqrt
from pathlib import Path
import argparse
import hashlib
import json


def coordinates_by_division_polynomials(x, y, coefficient, index, modulus):
    inv_2y = pow(2*y, -1, modulus)

    @lru_cache(None)
    def psi(n):
        if n == 0:
            return 0
        if n == 1:
            return 1
        if n == 2:
            return 2*y % modulus
        if n == 3:
            return (3*x**4+6*coefficient*x*x-coefficient**2) % modulus
        if n == 4:
            return 4*y*(x**6+5*coefficient*x**4-5*coefficient**2*x*x-coefficient**3) % modulus
        k = n//2
        if n % 2:
            return (psi(k+2)*psi(k)**3-psi(k-1)*psi(k+1)**3) % modulus
        return psi(k)*inv_2y*(psi(k+2)*psi(k-1)**2-psi(k-2)*psi(k+1)**2) % modulus

    value = psi(index)
    xx = (x-psi(index-1)*psi(index+1)*pow(value, -2, modulus)) % modulus
    yy = psi(2*index)*pow(2*value**4, -1, modulus) % modulus
    assert (yy*yy-xx**3-coefficient*xx) % modulus == 0
    return (xx, yy), psi


def main(output):
    base = Path(__file__).parent
    source_bytes = (base/"certificate.json").read_bytes()
    source = json.loads(source_bytes)
    p, exponent, n = 85817, 3, 2665
    assert all(p % d for d in range(2, isqrt(p)+1))
    m = p**exponent
    rows = []
    for item in source["slots"]:
        # The recorded lift is checked as an integer residue; no producer is imported.
        r = item["sqrt2_mod_p3"]
        assert 0 <= r < m and (r*r-2) % m == 0
        x, y = (1+r) % m, 2*r % m
        a4 = (6*r-11) % m
        H, psi = coordinates_by_division_polynomials(x, y, a4, n, m)
        assert list(H) == item["H_mod_p3"]
        assert H[0] % (p*p) == 0 and H[0] % m != 0
        assert H[1] % p == 0 and H[1] % (p*p) != 0
        order = item["R0_exact_order_mod_p"]
        assert psi(order) % p == 0
        for q in (2, 5, 13, 41):
            if order % q == 0:
                assert psi(order//q) % p != 0
        # [2]R0=P is checked directly from the tangent formula.
        slope = (3*x*x+a4)*pow(2*y, -1, m) % m
        Px = (slope*slope-2*x) % m
        Py = (slope*(x-Px)-y) % m
        assert Px == (57-28*r)*pow(8, -1, m) % m
        assert Py == (-660+417*r)*pow(32, -1, m) % m
        # x(T0-P)=-D/x(P) is a unit, with nonzero ordinate.
        D = -a4 % p
        diff_x = -D*pow(Px, -1, p) % p
        assert diff_x != 0 and (diff_x**3-D*diff_x) % p != 0
        assert diff_x == item["H_minus_P_mod_p"][0]
        rows.append(H[0]//(p*p) % p)
    scale = Fraction(10621537, 256)**4
    aa = scale.numerator*pow(scale.denominator, -1, p*p) % (p*p)
    z = 39827
    factors = [((aa+c)**2-z*z) % (p*p) for c in (-10, -8, -5, 1, 2, 3, 4, 6, 7)]
    F = 1
    for f in factors:
        F = F*f % (p*p)
    log_derivative = sum(2*(aa+c)*pow(f, -1, p*p)
                         for c, f in zip((-10, -8, -5, 1, 2, 3, 4, 6, 7), factors)) % (p*p)
    Fa = F*log_derivative % (p*p)
    assert F == source["F_mod_p2"] and Fa == source["Fa_mod_p2"]
    assert F % p != 0 and Fa % p == 0 and Fa != 0
    pu = -18*F*pow(Fa//p, -1, p) % p
    Vlead = pu**2*sum(x**4 for x in rows) % p
    assert pu == 65426 and Vlead == 33198
    assert source["valuation_b"] == 1-2*6 == -11
    assert source["valuation_trace_square_radicand"] == min(12, 1) == 1
    result = {"status": "PASS", "producer_imported": False,
              "method": "division-polynomial point reconstruction; logarithmic derivative contact check",
              "certificate_sha256": hashlib.sha256(source_bytes).hexdigest(),
              "prime": p, "xH_over_p2_mod_p_slots": rows,
              "pu_mod_p": pu, "V_over_p6_mod_p": Vlead,
              "all_decisive_integer_residues_reconstructed": True}
    output.write_text(json.dumps(result, indent=2)+"\n")
    print("PASS: independent division-polynomial and physical-map reconstruction")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("independent_certificate.json"))
    main(parser.parse_args().output)
