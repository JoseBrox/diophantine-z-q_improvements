#!/usr/bin/env python3
"""Check the saved small pole counterexample without a PARI installation.

All rational identities, local preparations, finite-field point counts,
and squareclasses are recomputed.  The rank upper bound is read from the
separately pinned 2-descent certificate; this script does not recompute it.
"""
from fractions import Fraction as F
from hashlib import sha256
from math import gcd
from pathlib import Path
import json


def valuation(x, prime):
    assert x
    def integer_valuation(n):
        result = 0
        while n % prime == 0:
            n //= prime
            result += 1
        return result
    return integer_valuation(x.numerator)-integer_valuation(x.denominator)


def squarefree(n):
    sign = 1 if n > 0 else -1
    n = abs(n)
    prime = 2
    while prime*prime <= n:
        while n % (prime*prime) == 0:
            n //= prime*prime
        prime = 3 if prime == 2 else prime+2
    return sign*n


def main():
    folder = Path(__file__).resolve().parent
    witness = json.loads((folder/'small-fixed-tau17-obstruction.json').read_text())
    rank_path = folder/'fixed-tau17-obstruction.json'
    rank = json.loads(rank_path.read_text())
    assert witness['rank_source_certificate_sha256'] == sha256(rank_path.read_bytes()).hexdigest()
    u0, v0 = map(F, witness['base_point'])
    assert 17+3*u0*u0 == 2465*v0*v0
    t = F(witness['rational_parameter'])
    den = 3-2465*t*t
    assert den
    u = (-u0*(3+2465*t*t)+4930*v0*t)/den
    v = (v0*(3+2465*t*t)-6*u0*t)/den
    b = u*u
    assert (u,v,b) == tuple(F(witness[key]) for key in ('u','v','b'))
    assert 17+3*b == 2465*v*v
    assert 0 < b < F(1,10**80)
    assert witness['rational_square_root_b'] == str(u)
    vals = {str(p):valuation(b,p) for p in (2,3,17)}
    assert vals == witness['prepared_valuations'] == {'2':4,'3':2,'17':2}
    B = 17*b
    e = (17-b)/(17+3*b)
    ordinate = -4*B*17/(17**2+3*B)
    k = 17*u**3*(17-u*u)/(2465*v)
    assert (e,ordinate,k) == tuple(F(witness[key]) for key in ('e','p','scaling_k'))
    assert ordinate**2 == B*(1-e)*(1+3*e)
    assert k and B*B*e*(B-b*b) == 2465*k*k
    n = 2465
    px,py = witness['explicit_infinite_order_point']
    assert py*py == px*(px-n)*(px+3*n) and px == 51*39**2
    counts = {}
    for p in (7,11,13,19,23,31):
        assert 6*n % p
        squares = [0]*p
        for y in range(p):
            squares[y*y % p] += 1
        counts[str(p)] = 1+sum(squares[x*(x-n)*(x+3*n) % p] for x in range(p))
    assert counts == witness['good_prime_point_counts'] and gcd(*counts.values()) == 4
    classes = {1,-3,n,squarefree(-3*n)}
    classes |= {squarefree(51*c) for c in tuple(classes)}
    assert len(classes) == 8 and 17 not in classes
    assert sorted(classes) == witness['complete_x_squareclass_image'] == rank['complete_x_squareclass_image']
    assert rank['elliptic_parameter'] == n
    assert rank['unconditional_rank_upper_bound'] == 1
    assert rank['two_selmer_rank'] == 3
    report = {
        'status':'PASS',
        'scope':'Exact rational identities, preparation, good-reduction point counts and squareclasses. The rank upper bound is taken from the pinned descent certificate, not recomputed by this standard-library check.',
        'rank_recomputed':False,
        'rank_source_certificate_sha256':sha256(rank_path.read_bytes()).hexdigest(),
        'prepared_valuations':vals,
        'good_prime_point_counts':counts,
        'complete_x_squareclass_image':sorted(classes),
        'strict_bound':'0 < b < 10^-80',
    }
    output = folder/'small-fixed-tau17-algebra-verification.json'
    output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
