#!/usr/bin/env python3
"""Exact audit of the c-integrality obstruction; no complete-source claim."""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import json
from math import gcd
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent


def valuation(value, prime):
    value = Q(value)
    if not value:
        raise ValueError("valuation of zero is not used")
    numerator, denominator = abs(value.numerator), value.denominator
    answer = 0
    while numerator % prime == 0:
        numerator //= prime
        answer += 1
    while denominator % prime == 0:
        denominator //= prime
        answer -= 1
    return answer


def residue(value, modulus):
    value = Q(value)
    assert gcd(value.denominator, modulus) == 1
    return value.numerator * pow(value.denominator, -1, modulus) % modulus


def hensel_square(target, prime, digits, initial_root):
    modulus = prime**digits
    target_mod = residue(target, modulus)
    root = initial_root % prime
    assert (root * root - target_mod) % prime == 0
    assert root % prime != 0
    power = prime
    for _ in range(1, digits):
        error = (root * root - target_mod) // power
        correction = -error * pow(2 * root, -1, prime) % prime
        root += correction * power
        power *= prime
        assert (root * root - target_mod) % power == 0
    assert power == modulus
    return root


def norm_family(B):
    a, c, d, b, w, gamma = 5, Q(1, 5), Q(-7, 5), 2, 14, -2
    i, F, J = 250, 49, -1812 - 245 * B
    G, H, I = Q(-45594, 5), Q(-91188, 5), Q(4157625647, 25)
    assert d == b * w + (a - 2) * c + (4 * a - 5) * gamma
    assert d * d - (a * a - 1) * c * c == 1
    assert F * F - (a * a - 1) * i * i * c**4 == 1
    assert G == a + F * F * (c + 1 - a)
    assert H == c + F * F * (B - c) + c * F * J
    assert I * I - (G * G - 1) * H * H == 1
    assert H == 2 * G and I == 2 * G * G - 1
    assert c.denominator == 5 and i != 0
    assert c < B
    assert -J > 0
    assert H == c + (-F)**2 * (B - c) + c * (-F) * (-J)


def local_case(prime, a, digits=8):
    D = 4 * a - 5
    c = Q(2 * (a - 2), D)
    d = Q(2 * a * a - 4 * a + 3, D)
    assert d == (a - 2) * c + 1
    assert d * d - (a * a - 1) * c * c == 1
    k = -valuation(c, prime)
    assert k > 0
    i = prime**(2 * k + 1)
    J, B = 1, 3
    target_f = 1 + (a * a - 1) * i * i * c**4
    assert valuation(target_f - 1, prime) >= 2
    F = hensel_square(target_f, prime, digits, 1)
    G = a + F * F * (c + 1 - a)
    H = c + F * F * (B - c) + c * F * J
    assert valuation(G, prime) == valuation(H, prime) == -k
    scaled_G, scaled_H = prime**k * G, prime**k * H
    target_i = scaled_G**2 * scaled_H**2 - prime**(2 * k) * scaled_H**2 + prime**(4 * k)
    initial_i = residue(scaled_G * scaled_H, prime)
    root_i = hensel_square(target_i, prime, digits, initial_i)
    modulus = prime**digits
    assert residue(F * F - target_f, modulus) == 0
    assert residue(root_i * root_i - target_i, modulus) == 0
    assert root_i % prime != 0
    return {"prime": prime, "a": a, "c": str(c), "denominator_valuation": k,
            "precision_digits": digits, "F_residue": F, "scaled_I_residue": root_i}


def receipt():
    a, c, T, B, G = sp.symbols("a c T B G")
    D, delta = 4 * a - 5, a * a - 1
    first_residual = ((a - 2) * c + T)**2 - delta * c**2 - 1
    assert sp.expand(first_residual + D * c**2 - 2 * (a - 2) * T * c - (T**2 - 1)) == 0
    assert sp.expand(16 * delta - D * (4 * a + 5) - 9) == 0
    assert sp.expand((2 * G * G - 1)**2 - (G * G - 1) * (2 * G)**2 - 1) == 0
    c0 = 2 * (a - 2) / D
    d0 = (2 * a * a - 4 * a + 3) / D
    assert sp.cancel(d0 - (a - 2) * c0 - 1) == 0
    assert sp.cancel(d0**2 - delta * c0**2 - 1) == 0
    third_coordinate = sp.Rational(1, 5) + 49**2 * (B - sp.Rational(1, 5)) + sp.Rational(49, 5) * (-1812 - 245 * B)
    assert sp.expand(third_coordinate + sp.Rational(91188, 5)) == 0
    for B_value in range(3, 67, 2):
        norm_family(B_value)
    local = [local_case(prime, a_value) for prime, a_value in
             [(3, 8), (5, 5), (7, 3), (11, 4), (13, 11), (17, 14), (19, 6)]]
    return {
        "status": "PASS", "symbolic_identities": 6,
        "exact_rational_counterfamily_fixtures": 32,
        "local_hensel_fixtures": local,
        "full_source_counterexample_claim": False,
        "c_integer_predicate_removed": False,
        "variable_saving_claim": 0,
        "scope": "Exact counterfamily for the norm/linear/CRT subsystem and finite p-adic lifts; neither the full source nor rationality of the local Hensel roots is asserted.",
        "proof_sha256": hashlib.sha256((HERE / "README.md").read_bytes()).hexdigest(),
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args()
    result = receipt()
    path = HERE / "certificate.json"
    if args.write_certificate:
        path.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    else:
        assert json.loads(path.read_text()) == result
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
