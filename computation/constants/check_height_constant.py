#!/usr/bin/env python3
"""Exact, independently enumerated primorial bound for the source constant."""
from pathlib import Path
from math import isqrt, prod
import hashlib
import json

ROOT = Path(__file__).resolve().parent
LIMIT = 76176


def sieve_primes(limit):
    flags = bytearray(b'\x01') * (limit + 1)
    flags[:2] = b'\x00\x00'
    for p in range(2, isqrt(limit) + 1):
        if flags[p]:
            flags[p*p:limit+1:p] = b'\x00' * ((limit-p*p)//p + 1)
    return [p for p in range(2, limit+1) if flags[p]]


def trial_primes(limit):
    def prime(n):
        if n < 2:
            return False
        if n % 2 == 0:
            return n == 2
        return all(n % d for d in range(3, isqrt(n)+1, 2))
    return [n for n in range(2, limit+1) if prime(n)]


def main():
    primes = sieve_primes(LIMIT)
    independent = trial_primes(LIMIT)
    assert primes == independent
    B = prod(primes)
    B2 = 1
    for p in independent:
        B2 *= p
    assert B == B2
    H = (1 << 110) * 210**1800 * B**19 + 128
    h = H.bit_length()
    assert len(primes) == 7499
    assert B.bit_length() == 109445
    assert h == 2093448
    assert (1 << (h-1)) < H < (1 << h)
    raw = H.to_bytes((h+7)//8, 'big')
    target = ROOT/'data'
    target.mkdir(exist_ok=True)
    (target/'height19.bin').write_bytes(raw)
    (target/'height19-primes.json').write_text(json.dumps(primes)+'\n')
    report = {
        'status':'PASS', 'prime_cutoff':LIMIT,
        'prime_count':len(primes),
        'independent_enumerations':['Eratosthenes sieve','trial division through the integer square root'],
        'primorial_bit_length':B.bit_length(),
        'height_constant':'2^110 * 210^1800 * (product of all primes <= 76176)^19 + 128',
        'height_constant_bit_length':h,
        'strict_lower_bound':'2^2093447',
        'strict_upper_bound':'2^2093448',
        'binary_encoding':'unsigned big endian',
        'height19_bin_bytes':len(raw),
        'height19_bin_sha256':hashlib.sha256(raw).hexdigest(),
        'most_significant_128_bits':str(H >> (h-128)),
        'scope':'Exact numerical sharpening of the stated source constant; the contact-height inequality using that constant remains an arithmetic input.',
        'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (target/'height19-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
