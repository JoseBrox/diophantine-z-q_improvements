#!/usr/bin/env python3
"""Exact arithmetic certificate for the explicit 229-variable quartic.

The numerical bounds and finite support checks complement the manuscript
proof. They do not certify its retained global arithmetic inputs.
"""
from fractions import Fraction as F
from math import isqrt, prod

S = {2, 3, 5, 7, 11, 13, 17, 37, 41, 2399}
theta = [F(0), F(-1, 2), F(-1), F(1, 2399), F(-32, 407)]
CN = 2**68 * 3**16 * 5**16 * 7**4
c0 = F(74712001, 1000000)


def log_unit_interval(x, terms=28):
    assert 1 <= x <= 2
    z = (x - 1) / (x + 1)
    z2 = z * z
    power = z
    total = F(0)
    for j in range(terms):
        total += 2 * power / (2 * j + 1)
        power *= z2
    tail = 2 * power / ((2 * terms + 1) * (1 - z2))
    return total, total + tail


LN2 = log_unit_interval(F(2))


def log_interval(x):
    x = F(x)
    assert x > 0
    k = x.numerator.bit_length() - x.denominator.bit_length()
    scale = F(2**k) if k >= 0 else F(1, 2**(-k))
    y = x / scale
    if y < 1:
        k -= 1
        y *= 2
    elif y >= 2:
        k += 1
        y /= 2
    lo, hi = log_unit_interval(y)
    if k >= 0:
        return lo + k * LN2[0], hi + k * LN2[1]
    return lo + k * LN2[1], hi + k * LN2[0]


def prime(p):
    return p >= 2 and all(p % d for d in range(2, isqrt(p) + 1))


small_primes = [p for p in range(2, 1001) if prime(p)]
assert len(small_primes) == 168


def support_in(n, gamma):
    n = abs(n)
    assert n
    used = set()
    for p in gamma:
        if n % p == 0:
            used.add(p)
            while n % p == 0:
                n //= p
    assert n == 1
    return used


def ceiling_binary(x):
    x = F(x)
    e = x.numerator.bit_length() - x.denominator.bit_length()
    while x >= 2**e:
        e += 1
    while x < 2**(e - 1):
        e -= 1
    return e


cases = [(F(3, 11), 15, {79, 89, 647, 3593})]

for center, target_N, extra in cases:
    gamma = S | extra
    assert all(prime(p) for p in gamma)
    contacts = theta + [center - t for t in theta]
    assert len(set(contacts)) == 10 and center / 2 not in contacts
    assert max(contacts) - min(contacts) < 7
    used = set()
    for t in contacts:
        used |= support_in(t.denominator, gamma)
        used |= support_in((t - center / 2).numerator, gamma)
        used |= support_in((t - center / 2).denominator, gamma)
    for i, t in enumerate(contacts):
        for u in contacts[i + 1 :]:
            used |= support_in((t - u).numerator, gamma)
            used |= support_in((t - u).denominator, gamma)
    assert used - S == extra
    J = prod(gamma)
    C = c0 * CN * J * prod(p + 1 for p in gamma)
    E_low = prod(F(p + 1, p) for p in small_primes if p not in gamma)
    H = max(3, abs(center.numerator) + abs(2 * center.numerator + center.denominator), 3 * center.denominator)
    assert C > 2425 + 120 * log_interval(H)[1]

    L = 9 * (2 * target_N - 1) // 4 + 1
    log149 = log_interval(149)
    log14 = log_interval(14)
    logJ = log_interval(J)
    logC = log_interval(C)
    logElow = log_interval(E_low)
    b_lo, b_hi = L * log149[0], L * log149[1]
    lam = F(2, 3) * (1 - F(1, 6006))
    alpha = F(1, 3) + F(1, 36036)
    shape_hi = logJ[1] + log14[1] / 6 + 2 * b_hi / 3
    margin_lo = lam * b_lo - log_interval(121)[1] - logC[1] - logElow[1] / 2 - alpha * log14[1] - log_interval(shape_hi)[1]
    assert margin_lo > 0

    # The previous N does not pass this precise sufficient comparison.
    old_L = 9 * (2 * (target_N - 1) - 1) // 4 + 1
    old_b_lo, old_b_hi = old_L * log149[0], old_L * log149[1]
    old_shape_lo = logJ[0] + log14[0] / 6 + 2 * old_b_lo / 3
    old_margin_hi = lam * old_b_hi - log_interval(121)[0] - logC[0] - logElow[0] / 2 - alpha * log14[0] - log_interval(old_shape_lo)[0]
    assert old_margin_hi < 0

    # Coarse bound used solely for the input/Lucas comparison.
    m = J.bit_length()
    e = 0
    while 1 + F(7 * m, 10) >= 22 * 2**e:
        e += 1
    K_exp = 150 + 2 * m + 2 * e
    assert log_interval(H)[1] < 2 ** (K_exp - 1) * 484
    input_const_hi = F(23, 22) * (K_exp + 18) * LN2[1]
    assert 149**L > 2**239 and 149**L > 600
    assert F(99, 100) * (5 * L - 1) > input_const_hi / 600 + F(6, 11)



# Direct checks for the displayed clean N=15 proof.
assert J == 30366775457346956958330 and J < 2**75
assert C < 2**300 and E_low < F(21,10) and H == 33
assert log_interval(149)[0] > 5 and log_interval(149)[1] < F(501,100)
assert log_interval(500)[1] < F(25,4)
assert LN2[1] < F(173287,250000)
assert log_interval(274)[1] < F(45,8)
assert log_interval(1001)[0] > 6
assert F(220*6005,6006) > F(219963,1000)
assert F(25,4)+300*F(173287,250000)+F(45,8) == F(1099097,5000)
assert F(53)+44*F(501,100) < 274
assert F(3,2)**2 > F(21,10)
assert F(5,2)**3 > 14 and 11**30 > 14*10**30
assert 121*F(3,2)*F(5,2)*F(11,10) < 500
assert K_exp == 304 and F(23,22)*(304+18)*LN2[1] < 240
assert F(99,100)*(5*66-1)>320
assert 149**7 > 22202*2**20  # scalar completeness for N>=3

# Scalar H4.2 constant and absence of a 149-contact.
BS=prod(S)
assert BS==1857890364330 and BS < 2**41
C2=c0*CN*BS*prod(p+1 for p in S)*41*F(7,10)
assert C2<2**237 and log_interval(BS)[0]>1
roots=[F(0),F(1),F(2401),F(-343,32)]
for i,x in enumerate(roots):
    for y in roots[i+1:]:
        support_in((x-y).numerator,{2,3,5,7})
        support_in((x-y).denominator,{2,3,5,7})
residues=[]
assert prime(149)
for x in roots:
    z=((x.numerator*pow(x.denominator,-1,149)-2504)*pow(51,-1,149))%149
    residues.append(z)
    assert pow(z,74,149)==148
assert residues==[59,97,109,108]
assert 102==2*3*17

# Constants for the complete torsion sum-height corollary.
assert 12*log_interval(96)[1]-12 < 43
assert 6+43+log_interval(864)[1]+log_interval(7)[1]/2 < 57
assert 40*log_interval(32)[1]+2285 < 2425
assert (2**231 < 149**32 < 2**232)

import argparse,json
from pathlib import Path
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path)
args=parser.parse_args()
report={
 'schema':'explicit229-arithmetic-certificate/v62','status':'PASS',
 'center':'3/11','midpoint':'3/22','exceptional_primes':sorted(gamma),
 'exceptional_product':str(J),'contact_height_constant_strict_power_two':300,
 'coarse_contact_constant_power_two':304,'scalar_height_constant_strict_power_two':238,
 'finite_euler_product_bound':'21/10','large_prime_exponent':'1/6006',
 'sufficient_N':15,'forced_scalar_exponent_L':66,'all_larger_N':True,
 'scalar_completeness_sufficient_N':3,'scalar_nonsquare_residues_149':residues,
 'half_integral_endpoint_squarefree_integer':102,
 'sum_height_bound':'B^2<40*h(Z)+2285',
 'three_argument_height_bound':'B^2<40*sum(h(t_j))+2425',
 'delta_lower_log_bound':'220*6005/6006',
 'delta_upper_log_bound':'1099097/5000',
 'fixed_coefficient_height':str(149**32),'fixed_coefficient_bits':232,
 'scope':'Exact finite identities and numerical inequalities; the manuscript supplies global arithmetic implications and completeness.',
 'arithmetic_foundations_independently_audited':False,
 'targets_21_and_9_proved':False
}
if args.output:
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
