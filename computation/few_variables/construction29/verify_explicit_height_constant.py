#!/usr/bin/env python3
"""Independently evaluate the explicit H19 by trial-division enumeration.

No supplied prime table or sieve is used. This certifies the finite integer
constant, not the inherited theorem in which that constant occurs.
"""
from hashlib import sha256
import json
from math import prod
from pathlib import Path

HERE = Path(__file__).resolve().parent


def verify():
    limit=76176
    primes=[]
    for candidate in range(2,limit+1):
        is_prime=True
        for p in primes:
            if p*p>candidate: break
            if candidate%p==0:
                is_prime=False
                break
        if is_prime: primes.append(candidate)
    B=prod(primes)
    H=(1<<110)*210**1800*B**19+128
    H_bytes=H.to_bytes((H.bit_length()+7)//8,'big')
    assert len(primes)==7499 and primes[-1]==76163
    assert B.bit_length()==109445 and H.bit_length()==2093448
    assert sha256(H_bytes).hexdigest()=='4b4dab2ee796ed844df51b1d221c94bc857f7a65ce146c4c3ac805717c3a29b7'
    return {
        'status':'passed',
        'formula':'H19=2^110*210^1800*(product of primes p<=76176)^19+128',
        'prime_enumeration':'trial division by all earlier primes up to the square root; no sieve or supplied prime list',
        'prime_count':len(primes),'last_prime':primes[-1],
        'primorial_bit_length':B.bit_length(),
        'height_constant_bit_length':H.bit_length(),
        'height_constant_unsigned_big_endian_sha256':sha256(H_bytes).hexdigest(),
        'finite_cutoff_power_of_two_exponent':H.bit_length()+1,
        'scalar_test_order':48*(H.bit_length()+1),
        'scope':'Exact finite integer calculation only; the contact-height theorem remains an inherited arithmetic hypothesis.',
    }


if __name__=='__main__':
    report=verify()
    report['checker_sha256']=sha256(Path(__file__).read_bytes()).hexdigest()
    (HERE/'explicit-height-constant-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
