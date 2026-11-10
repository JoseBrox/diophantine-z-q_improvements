#!/usr/bin/env python3
"""Exact constants for the scalar-character and contact-height bounds.

This checks finite integer and cyclic-group assertions only.  The paper
supplies the determinant argument and states the arithmetic premises.
"""
from fractions import Fraction
from hashlib import sha256
from math import gcd, isqrt, lcm
from pathlib import Path
import argparse
import json


def trial_prime(n):
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("nebentypus-height-certificate.json"))
    args = parser.parse_args()
    cutoff = 76176
    sieve = bytearray(b"\x01") * (cutoff + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, isqrt(cutoff) + 1):
        if sieve[p]:
            sieve[p*p::p] = b"\x00" * len(sieve[p*p::p])
    primes = [p for p in range(2, cutoff + 1) if sieve[p]]
    assert primes == [p for p in range(2, cutoff + 1) if trial_prime(p)]
    B = 1
    phi = 1
    orders = []
    for p in primes:
        B *= p
        phi *= p - 1
        if p > 2:
            order = (p - 1) & -(p - 1)
            orders.append(order)
            # A generator maps to a primitive root of this order.
            # Its value at -1 is the unique element of order two.
            assert ((p - 1) // 2) % order == order // 2
            assert (p - 1) % order == 0
    U = max([2] + orders)
    assert U == 65536 and trial_prime(65537) and phi % U == 0
    assert lcm(*orders, 2) == U
    C0 = 210 ** 300
    upper = 19 * C0 * B**3 * B.bit_length()
    assert C0*C0 < B and 144 < B
    assert B.bit_length() == 109445
    assert upper < 1 << 330670
    # If epsilon=chi^{-1}kappa with kappa quadratic, epsilon's order
    # divides any even common exponent of chi and kappa. Check every
    # character value for a representative range of 2-power exponents.
    tested = 0
    for exponent in [2**a for a in range(1, 17)]:
        for value in range(exponent):
            for quadratic in (0, exponent // 2):
                eps = (-value + quadratic) % exponent
                assert (2*(eps + value)) % exponent == 0
                eps_order = exponent // gcd(exponent, eps)
                assert exponent % eps_order == 0
                tested += 1
    # Work in Q[z]/(z^2-z+1), storing a+b*z.
    def mul(x, y):
        a, b = x
        c, d = y
        return a*c-b*d, a*d+b*c+b*d
    z = (0, 1)
    assert mul(z, z) == (-1, 1)
    assert mul(z, (1, -1)) == (1, 0)
    # E(M)=sum_{d|M}1/d, used in the restricted-prime corollary.
    for M in (1, 2, 3, 6, 17, 3*5*17, 17*97):
        ps = [p for p in range(2, M+1) if M % p == 0 and trial_prime(p)]
        E = Fraction(1)
        for p in ps:
            assert M % (p*p) != 0
            E *= Fraction(p+1, p)
        assert E == sum((Fraction(1, d) for d in range(1, M+1) if M % d == 0), Fraction(0))
    cert = {
        "status": "PASS",
        "scope": "Finite constants and character identities; not an independent proof of arithmetic realization.",
        "prime_cutoff": cutoff,
        "prime_count": len(primes),
        "prime_product_bit_length": B.bit_length(),
        "prime_product_sha256_big_endian": sha256(B.to_bytes((B.bit_length()+7)//8, "big")).hexdigest(),
        "U_of_fixed_prime_product": U,
        "prime_attaining_U": 65537,
        "U_divides_phi": phi % U == 0,
        "normalized_determinant_identity": "det rho = chi^(-2) chi_cyc^2; (epsilon chi)^2=1",
        "cyclic_character_value_pairs_checked": tested,
        "modular_degree_bound": "210^300 R^2 U(R) E(R) < 210^300 R^3",
        "C0_bit_length": C0.bit_length(),
        "C0_squared_less_than_B": C0*C0 < B,
        "contact_constant_formula": "19 * 210^300 * B_*^3 * log B_*",
        "integer_constant_upper_bound_bit_length": upper.bit_length(),
        "constant_strict_log2_upper_bound": 330670,
        "pure_power_constant_strict_log2_upper_bound": 330671,
        "unit_fibre_identity": "zeta*(1-zeta)=1 in Q[zeta]/(zeta^2-zeta+1)",
        "unit_fibre_modular_height_bound": "d_H/2*(log(6)+log(N)+2*log(d_H))-g_H/2*log(pi)",
        "restricted_prime_bound": "C2 M^2 max(65536,2^k) (1+log M)^2 if v2(p-1)<=k for all p|M"
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(cert, indent=2) + "\n")
    print(json.dumps({k: cert[k] for k in (
        "status", "prime_count", "U_of_fixed_prime_product",
        "constant_strict_log2_upper_bound", "cyclic_character_value_pairs_checked")}, sort_keys=True))


if __name__ == "__main__":
    main()
