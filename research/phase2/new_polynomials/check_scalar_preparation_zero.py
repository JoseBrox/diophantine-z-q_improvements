#!/usr/bin/env python3
"""Exact finite checks for scalar_preparation_zero.tex.

This checks the fixed arithmetic constants and finite-field assertions.
It does not certify the source manuscript's external arithmetic inputs.
"""
from fractions import Fraction
from math import isqrt, prod
import json

BAD = [5, 19, 23, 349, 661, 5209]
BASIS = [2, 3, 11, 17, 37, 67, 71]


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def squareclass_vector(q):
    valuations = {}
    units = {}
    for p in (2,3,17):
        value=q
        e=0
        while value % p == 0:
            value //= p
            e += 1
        valuations[p]=e % 2
        units[p]=value
    two_bits={1:(0,0),3:(1,1),5:(0,1),7:(1,0)}[units[2] % 8]
    return [valuations[2],*two_bits,valuations[3],
            int(units[3] % 3 != 1),valuations[17],
            int(pow(units[17] % 17, 8, 17) != 1)]


def rank_mod_two(rows):
    basis={}
    for row in rows:
        v=sum(bit << i for i,bit in enumerate(row))
        for pivot in sorted(basis,reverse=True):
            if (v >> pivot) & 1:
                v ^= basis[pivot]
        if v:
            basis[v.bit_length()-1]=v
    return len(basis)


def main():
    vectors=[squareclass_vector(p) for p in BASIS]
    checks={
        'all_listed_numbers_prime': all(is_prime(p) for p in BAD+BASIS),
        'prime_sets_disjoint': not(set(BAD)&set(BASIS)),
        'exceptional_set_unchanged': max(BAD+BASIS) < 76176,
        'quadratic_has_no_root_at_basis_primes': all(
            all((x*x+x+23)%p for x in range(p)) for p in BASIS),
        'squareclass_rank_seven': rank_mod_two(vectors)==7,
        'table_exact': vectors==[
            [1,0,0,0,1,0,0], [0,1,1,1,0,0,1],
            [0,1,1,0,1,0,1], [0,0,0,0,1,1,0],
            [0,0,1,0,0,0,1], [0,1,1,0,0,0,0],
            [0,1,0,0,1,0,1]],
    }
    contacts=[Fraction(0),Fraction(1),Fraction(2401),
              Fraction(-343,32),Fraction(1,2)]
    expected=[Fraction(23),Fraction(25),Fraction(25*349*661),
              Fraction(25*5209,1024),Fraction(5*19,4)]
    checks['contact_resultants_exact']=[t*t+t+23 for t in contacts]==expected
    cmax=prod(BAD+BASIS)
    checks['correction_max_exact']=cmax==518513917206770054130
    checks['normalizer_real_bound']=2**16*cmax*204**2<23**24
    checks['uniform_contact_bound']=Fraction(1202*204*2,8)==61302<2**16
    checks['normalizer_small_prime_valuations']=204==2**2*3*17
    if not all(checks.values()):
        raise AssertionError(checks)
    print(json.dumps({'status':'PASS','scope':'Fixed exact arithmetic only; '
        'not a verification of external arithmetic hypotheses.',
        'checks':checks,'basis_vectors':dict(zip(BASIS,vectors)),
        'correction_count':2**14,'maximum_abs_correction':cmax,
        'normalizer':'204/23^12'},indent=2))


if __name__=='__main__':
    main()
