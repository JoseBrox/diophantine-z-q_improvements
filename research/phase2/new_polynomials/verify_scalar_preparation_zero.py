#!/usr/bin/env python3
"""Independent fixed-arithmetic audit of the scalar normalization.

Uses exhaustive local-squareclass enumeration, not the source checker's
matrix-rank implementation. No construction or checker module is imported.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from math import prod
from pathlib import Path


def prime_factors(n):
    n = abs(n)
    out = set()
    q = 2
    while q * q <= n:
        if n % q == 0:
            out.add(q)
            while n % q == 0:
                n //= q
        q += 1
    if n > 1:
        out.add(n)
    return out


def local_class(q):
    result = []
    for p in (2, 3, 17):
        u = q
        v = 0
        while u % p == 0:
            u //= p
            v += 1
        result.append(v % 2)
        result.append(u % 8 if p == 2 else pow(u % p, (p - 1) // 2, p))
    return tuple(result)


def main():
    bad = (5, 19, 23, 349, 661, 5209)
    basis = (2, 3, 11, 17, 37, 67, 71)
    assert all(prime_factors(p) == {p} for p in bad + basis)
    assert set(bad).isdisjoint(basis)
    assert max(bad + basis) < 76176
    for p in basis:
        assert all((t * t + t + 23) % p for t in range(p))
    classes = {
        local_class(prod(p for p, flag in zip(basis, mask) if flag))
        for mask in product((0, 1), repeat=7)
    }
    assert len(classes) == 128
    contacts = (Fraction(0), Fraction(1), Fraction(2401),
                Fraction(-343, 32), Fraction(1, 2))
    values = [t * t + t + 23 for t in contacts]
    support = set().union(*(prime_factors(v.numerator) for v in values))
    assert support == set(bad)
    assert values == [Fraction(23), Fraction(25), Fraction(25 * 349 * 661),
                      Fraction(25 * 5209, 1024), Fraction(95, 4)]
    cmax = prod(bad + basis)
    assert cmax == 518513917206770054130
    assert 2 ** 16 * cmax * 204 ** 2 < 23 ** 24
    assert Fraction(1202 * 204 * 2, 2 ** 3) == 61302 < 2 ** 16
    assert 204 == 2 ** 2 * 3 * 17
    here = Path(__file__).resolve().parent
    receipt = {
        "status": "passed",
        "scope": "Fixed exact arithmetic only: contact evaluations and prime support, absence of quadratic roots at seven basis primes, exhaustive generation of all 128 local squareclasses, and the normalizer inequality. No external arithmetic theorem or emitted polynomial is certified.",
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_sha256": sha256((here / "scalar_preparation_zero.tex").read_bytes()).hexdigest(),
        "contact_values": [str(v) for v in values],
        "resultant_prime_support": sorted(support),
        "local_squareclasses_generated": len(classes),
        "maximum_abs_correction": cmax,
        "normalizer_inequality_left": 2 ** 16 * cmax * 204 ** 2,
        "normalizer_inequality_right": 23 ** 24,
    }
    target = here / "scalar-preparation-zero-independent-verification.json"
    target.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": "passed", "receipt": str(target)}))


if __name__ == "__main__":
    main()
