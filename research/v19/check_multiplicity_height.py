#!/usr/bin/env python3
"""Exact constants for the multiplicity contact-height theorem.

This verifies finite arithmetic and strict exponent comparisons.
It does not computationally prove the modular realization or height theorems.
"""
from fractions import Fraction
from hashlib import sha256
from math import isqrt, prod, factorial
from pathlib import Path
import argparse
import json


def trial_prime(n):
    if n < 2:
        return False
    return all(n % d for d in range(2, isqrt(n) + 1))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("multiplicity-height-certificate.json"))
    args = parser.parse_args()
    cutoff = 76176
    sieve = bytearray(b"\x01") * (cutoff + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, isqrt(cutoff) + 1):
        if sieve[p]:
            sieve[p*p::p] = b"\x00" * len(sieve[p*p::p])
    primes = [p for p in range(2, cutoff + 1) if sieve[p]]
    assert primes == [p for p in range(2, cutoff + 1) if trial_prime(p)]
    B = prod(primes)
    plus = prod(p + 1 for p in primes)
    C0 = 210**300
    assert B.bit_length() == 109445 and C0*C0 < B and B > 144
    assert C0*B*B > 912
    # B^2 E(B) is the integer B*product(p+1); log B < bit_length(B).
    upper = 67*C0*B*plus*B.bit_length()
    assert upper < 1 << 221231
    assert 7*upper < 1 << 221234
    taylor = sum((Fraction(5, 3)**k / factorial(k) for k in range(6)), Fraction(0))
    assert taylor > Fraction(36, 7)
    # If the character order is 2^a, r>=max(1,phi(2^a)/2).
    multiplicities = []
    for a in range(65):
        s = 2**a
        phi = 1 if a == 0 else 2**(a-1)
        minimum_r = max(1, (phi+1)//2)
        assert Fraction(s, minimum_r) <= 4
        multiplicities.append([s, minimum_r])
    exponent = Fraction(7, 3)
    local_order = 3
    assert exponent/local_order == Fraction(7, 9) < 1
    assert 5*exponent/(2*local_order) == Fraction(35, 18) < 2
    # Exact strict integer rounding in the K=A=5 local consequence.
    comparison_cases = scalar_cases = 0
    for nu in range(1, 202, 2):
        for mu in range(-200, 202, 2):
            if mu + nu <= 0:
                continue
            if mu <= nu:
                lower = Fraction(17*nu-7*mu, 8)
                least_integer = lower.numerator//lower.denominator + 1
                assert least_integer >= 3
                comparison_cases += 1
            else:
                lower = Fraction(17*mu-7*nu, 8)
                least_integer = lower.numerator//lower.denominator + 1
                assert least_integer >= 4
                scalar_cases += 1
    for mu in range(1, 202, 2):
        lower = Fraction(17*mu, 8)
        least_integer = lower.numerator//lower.denominator + 1
        assert least_integer >= 2*mu+1 and least_integer >= 3
    certificate = {
        "status": "PASS",
        "scope": "Finite numerical constants, multiplicity arithmetic and strict exponent comparisons; mathematical proofs and normalized arithmetic premises are separate.",
        "prime_cutoff": cutoff,
        "prime_count": len(primes),
        "prime_product_bit_length": B.bit_length(),
        "prime_product_sha256_big_endian": sha256(B.to_bytes((B.bit_length()+7)//8, "big")).hexdigest(),
        "level_constant": "210^300",
        "surface_multiplicity": "r=[E_f:Q]/2 >= phi(ord epsilon)/2; ord epsilon/r <= 4 for powers of two",
        "two_power_orders_checked": len(multiplicities),
        "height_bound": "h(a) <= 67*210^300*(B_*M)^2*E(B_*M)*log(B_*M)",
        "contact_constant": "C2=67*210^300*B_*^2*E(B_*)*log(B_*)",
        "constant_strict_log2_upper_bound": 221231,
        "pure_power_exponent": "7/3",
        "pure_power_constant_strict_log2_upper_bound": 221234,
        "exponential_taylor_lower_bound": str(taylor),
        "global_scalar_exponent_at_local_order_three": "7/9",
        "global_Lucas_exponent_at_local_order_three": "35/18",
        "K5_comparison_rounding_cases": comparison_cases,
        "K5_scalar_rounding_cases": scalar_cases,
        "local_source_implementation_status": "The local inequalities are verified; this certificate alone does not assert a new polynomial."
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(certificate, indent=2) + "\n")
    print(json.dumps({k: certificate[k] for k in (
        "status", "prime_count", "constant_strict_log2_upper_bound",
        "pure_power_constant_strict_log2_upper_bound",
        "K5_comparison_rounding_cases", "K5_scalar_rounding_cases")}))


if __name__ == "__main__":
    main()
