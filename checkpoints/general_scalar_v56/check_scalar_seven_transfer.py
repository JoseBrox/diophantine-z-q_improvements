#!/usr/bin/env python3
"""Reproduce the consumed-prime certificate for the scalar-only pole transfer."""
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
from math import gcd, isqrt
import json

ell = 76249
assert all(ell % p for p in range(2, isqrt(ell)+1))
eta = 102
n = 116576341082536192
D = 5951086353
A = 1296233
Z0 = 12556178240
M = 189711668070091549022366223774716198062888712249407876629023195358725017888
assert A == 17*ell
assert eta == 2*3*17
assert 216 % 3 == 450459 % 3 == 0

def original_r(x, modulus=None):
    b = 216*x**4+450459
    if modulus:
        b %= modulus
    r = b*(b-1)*(b-2401)*(32*b+343)*(2*b-1)
    return r if modulus is None else r % modulus

def aligned_r(x, modulus=None):
    z = A*x*x+Z0
    b = 2*z*z-D*D
    if modulus:
        b %= modulus
    r = b*(b-n)*(b-2401*n)*(32*b+343*n)
    return r if modulus is None else r % modulus

assert aligned_r(0) == M

reports = []
for name, function, c in [
    ('original', original_r, 17),
    ('aligned', aligned_r, eta**2*M % ell),
]:
    rows = []
    for x in range(ell):
        r = function(x, ell)
        old_den = (1+c*r) % ell
        new_den = (1+7*c*r) % ell
        assert r != 0
        assert old_den != 0
        assert new_den != 0
        rows.append((x, r, old_den, new_den))
    text = ''.join(','.join(map(str, row))+'\n' for row in rows)
    reports.append({
        'source': name,
        'input_residues_checked': len(rows),
        'contact_residue_count': len({r[1] for r in rows}),
        'old_C_residue': c,
        'new_C_residue': 7*c % ell,
        'contact_zero_residues': 0,
        'old_denominator_zero_residues': 0,
        'new_denominator_zero_residues': 0,
        'ordered_row_sha256': sha256(text.encode()).hexdigest(),
        'constant_contact_residue': rows[0][1] if name == 'aligned' else None,
        'constant_new_denominator_residue': rows[0][3] if name == 'aligned' else None,
    })

def vp_integer(z, p):
    assert z
    z = abs(z)
    e = 0
    while z % p == 0:
        z //= p
        e += 1
    return e

def vp(q, p):
    return vp_integer(q.numerator,p)-vp_integer(q.denominator,p)

sample_reports = []
for name, function, expected_two in [
    ('original', original_r, 4), ('aligned', aligned_r, 12)
]:
    for L in (3, 5, 13):
        C = (17 if name == 'original' else eta**2*M)*(ell**((L+1)//2)+1)
        numerator_constant = eta**2*ell**L*(1 if name == 'original' else M)
        for x in range(-24,25):
            r = function(x)
            assert gcd(7*numerator_constant*r, 1+7*C*r) == 1
            old = Fraction(numerator_constant*r,(1+C*r)**2)
            new = Fraction(7*numerator_constant*r,(1+7*C*r)**2)
            assert new/old == 7*Fraction(1+C*r,1+7*C*r)**2
            assert 0 < new < old < Fraction(1,56)
            assert vp(new,2) == expected_two
            assert vp(new,7) >= 1
            assert vp(new,ell) == L
            assert isqrt(new.denominator)**2 == new.denominator
            # The ratio new/(7*old) is an exact rational square.
        sample_reports.append({'source':name,'L':L,'integer_inputs':49,
                               'two_adic_valuation':expected_two,
                               'seven_adic_valuation_at_least':1})

assert 3**2-2 == 7
assert Fraction(7*4,8**2) < 1
result = {
    'status':'PASS',
    'consumed_prime':ell,
    'scalar_change':'A_L*r/(1+C_L*r)^2 -> 7*A_L*r/(1+7*C_L*r)^2',
    'physical_weight_change':False,
    'intrinsic_pole_input':'d=b',
    'finite_certificates':reports,
    'integer_input_fixtures':sample_reports,
    'norm_multiplier':'N_Q(sqrt(2))/Q(3+sqrt(2)) = 7',
    'denominator_coprimality': {
        'contact_part':'gcd(r,1+7*C_L*r)=1',
        'original_coefficient_primes':[2,3,7,17,ell],
        'aligned_coefficient_support':'primes of 102*M divide C_L; 7 and ell are handled separately',
        'ell_verification':'exhaustive finite-residue certificate above',
        'integer_fixture_full_gcd':1,
    },
    'coordinate_count':25,
    'new_smaller_variable_bound':False,
    'scope':'Residue certificate is exhaustive; integer fixtures supplement the universal proof.'
}
Path(__file__).with_name('scalar_seven_transfer_certificate.json').write_text(
    json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
