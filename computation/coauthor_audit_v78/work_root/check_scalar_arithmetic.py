"""Independent integer certificates for the four-contact scalar and threshold.

No construction module or CAS is imported. Algebraic height and local arguments
are stated in the companion proof; this verifies their explicit constants.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from math import gcd, prod
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
P = 67
L = 143
T_BITS = 1727


def prime_support(n):
    n = abs(n)
    assert n
    out = set()
    d = 2
    while d*d <= n:
        if n%d == 0:
            out.add(d)
            while n%d == 0:
                n //= d
        d = 3 if d == 2 else d+2
    if n > 1:
        out.add(n)
    return out


def support(values):
    answer = set()
    for a in values:
        answer |= prime_support(a.numerator) | prime_support(a.denominator)
    return answer


def main():
    assert prime_support(P) == {P}
    Tmod = 1224**2 % P
    residues = []
    for x in range(P):
        beta = (1632*x*x+2477) % P
        a = beta*(beta-1) % P
        b = (beta-2401)*(32*beta+343) % P
        assert a*b*(b+Tmod*a) % P
        residues.append([x, beta, a, b, (b+Tmod*a)%P])
    assert 1632%P and Tmod and (32+Tmod)%P
    assert 1632 == 32*3*17 and 2477 >= 1632
    assert 2477%32 == 13
    for x in range(32):
        beta = 1632*x*x+2477
        a = beta*(beta-1)
        b = (beta-2401)*(32*beta+343)
        assert a%8 == b%8 == 4
        assert (P*(a//4)*(b//4))%8 == 1
    for p in (3,17):
        for x in range(p):
            beta = 1632*x*x+2477
            r = beta*(beta-1)*(beta-2401)*(32*beta+343)
            assert r%p and pow(P*r, (p-1)//2, p) == 1
    assert Q(33,144*P) < Q(1,167)
    # Degree four in beta. T <= F*P^L, uniformly for odd L>=3.
    f = 4*1224**2*P
    norm_a, norm_b = 2, 900064
    height_constant = max(102**2*f*norm_a*norm_b, (norm_b+f*norm_a)**2)
    assert height_constant < 2**128

    base = {2,3,5,7,11,13,17,37,41,2399}
    theta = [Q(0),Q(-1,2),Q(-1),Q(1,2399),Q(-32,407)]
    contacts = [[s+a for s in (4*j+2,4*j+4) for a in theta] for j in range(3)]
    poles = [values+[Q(-j-1)] for j,values in enumerate(contacts)]
    common = base | support(poles[0])
    for a,b,c in product(*poles):
        common |= prime_support(gcd((a-b).numerator,(a-c).numerator))
    assert common == base | {19,23,457,4799}
    scalar_contacts = [Q(0),Q(1),Q(2401),Q(-343,32)]
    gamma = common | support(a-b for a,b in combinations(scalar_contacts,2))
    assert gamma == common and P not in gamma
    # Also check the two unsquared-scale contact-and-pole sets at the forced prime.
    sets = [{(a.numerator*pow(a.denominator,-1,P))%P for a in row} for row in poles]
    assert not sets[0] & sets[1]
    cstar = Q(74712001,10**6)*2**68*3**16*5**16*7**4
    j = prod(gamma)
    scalar_bound = 2*cstar*j*j*prod(Q(p+1,p) for p in gamma)*j.bit_length()
    assert scalar_bound < 2**342
    comparison = []
    for index,values in enumerate(poles):
        bad = common | support(a-b for a,b in combinations(values,2))
        k = prod(base)**2
        e = prod(Q(p+1,p)**2 for p in base)
        for p in bad-base:
            collision = any((a-b).numerator%p == 0
                            for a in contacts[index][:5] for b in contacts[index][5:])
            power = 1+int(collision)
            k *= p**power
            e *= Q(p+1,p)**power
        assert k < 2**398 and cstar*k*e < 2**550
        comparison.append({"index":index, "exceptional":sorted(bad), "K":k})
    forced = P**(2*L+1)
    assert forced-1 >= 2**T_BITS
    assert forced >= 120*2**342
    # The coefficient 18, rather than 9, pays for the unsquared scales.
    assert 2**(T_BITS-3*551)*12**6 > 18**3*(2400+7*T_BITS)**6
    assert 200**2 < 2**16
    assert 200*(551+4+16) < 199*574
    assert sum(Q(7,10)**k/prod(range(1,k+1)) for k in range(5)) > 2
    result = {
        "status":"PASS", "producer_imported":False, "cas_used":False,
        "prime":P, "explicit_sufficient_odd_L":L,
        "forced_lower_bound_bits":T_BITS, "residues":residues,
        "scalar_exceptional":sorted(gamma), "height_constant":height_constant,
        "comparison_constants":comparison,
        "general25_threshold_effective":False,
        "scope":"Exact finite constants; the proof retains the stated arithmetic inputs."
    }
    (HERE/"scalar_arithmetic_certificate.json").write_text(json.dumps(result,indent=2)+"\n")
    print("PASS: all scalar residues, local square classes, degree-four height constants, and L=143 unsquared-scale inequalities.")


if __name__ == "__main__":
    main()
