#!/usr/bin/env python3
"""Exact automatic-conic obstructions, using Tunnell's necessary direction.

The noncongruence certificates use the coefficient of the original formal
q-product in Tunnell's introduction theorem (a). Euler's pentagonal identity
reduces the larger coefficient to a finite signed sum. Independent exhaustive
ternary counts check the same coefficients. No rank or BSD computation is used.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from math import gcd, isqrt
from pathlib import Path
import argparse
import json
import sympy as sp

HERE = Path(__file__).resolve().parent


def valuation(a, p):
    a = F(a)
    assert a
    def vp(n):
        n, v = abs(n), 0
        while n % p == 0:
            n //= p
            v += 1
        return v
    return vp(a.numerator)-vp(a.denominator)


def is_square(a):
    a = F(a)
    return a >= 0 and isqrt(a.numerator)**2 == a.numerator and \
        isqrt(a.denominator)**2 == a.denominator


def square_in_q2(a):
    v = valuation(a,2)
    if v % 2: return False
    u = F(a)/F(2)**v
    return u.numerator*pow(u.denominator,-1,8) % 8 == 1


def prepared(b):
    b = F(b)
    return 0 < b < 1 and isqrt(b.denominator)**2 == b.denominator and \
        square_in_q2(b) and valuation(b,2) >= 3


def direct_product_coefficients(limit):
    # Direct finite truncation of q Π(1-q^(8m))(1-q^(16m)) θ_2.
    coeff = [1]+[0]*limit
    for step in (8,16):
        for exponent in range(step,limit+1,step):
            for j in range(limit,exponent-1,-1):
                coeff[j] -= coeff[j-exponent]
    answer = [0]*(limit+1)
    for n in range(1,limit+1):
        for z in range(isqrt((n-1)//2)+1):
            answer[n] += (1 if z==0 else 2)*coeff[n-1-2*z*z]
    return answer


def pentagonal_terms(step, limit):
    answer = [(0,1)]
    k = 1
    while step*k*(3*k-1)//2 <= limit:
        for sign in (-1,1):
            exponent = step*k*(3*k+sign)//2
            if exponent <= limit:
                answer.append((exponent, -1 if k%2 else 1))
        k += 1
    return answer


def euler_coefficient(n):
    limit = n-1
    left, right = pentagonal_terms(8,limit), pentagonal_terms(16,limit)
    contributions = Counter()
    for a, sa in left:
        for b, sb in right:
            remainder = limit-a-b
            if remainder < 0 or remainder % 2: continue
            z = isqrt(remainder//2)
            if 2*z*z == remainder:
                contributions[sa*sb*(1 if z==0 else 2)] += 1
    return {'n':n, 'coefficient':sum(c*k for c,k in contributions.items()),
        'pentagonal_terms_8':len(left), 'pentagonal_terms_16':len(right),
        'nonzero_summands':sum(contributions.values()),
        'summand_counts':dict(sorted(contributions.items()))}


def ternary_counts(n):
    # Count all signed integer triples via nonnegative x,z and square y.
    # The even-z terms in the 8z² equation are precisely the 32z² equation.
    even = odd = 0
    for x in range(isqrt(n//2)+1):
        rest = n-2*x*x
        for z in range(isqrt(rest//8)+1):
            y2 = rest-8*z*z
            y = isqrt(y2)
            if y*y != y2: continue
            weight = (1 if x==0 else 2)*(1 if y==0 else 2)*(1 if z==0 else 2)
            if z%2: odd += weight
            else: even += weight
    difference = F(even-odd,2)
    assert difference.denominator == 1
    return {'n':n, 'count_8':even+odd, 'count_32':even,
            'count_32_minus_half_count_8':difference.numerator}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=HERE/'verification.json')
    args = parser.parse_args()
    z, delta, u, v, q, b, A = sp.symbols('z delta u v q b A')
    e_split = (49*delta**2-1)/(120*delta**3)
    R_split = sp.prod(delta**2-sp.Rational(1,a*a) for a in (3,5,8))/delta**6
    assert sp.factor(1-e_split**2-R_split)==0
    assert sp.factor(e_split-(7*delta-1)*(7*delta+1)/(120*delta**3))==0
    assert sp.factor(1-e_split-(3*delta-1)*(5*delta-1)*(8*delta+1)/(120*delta**3))==0
    assert sp.factor(1+e_split-(3*delta+1)*(5*delta+1)*(8*delta-1)/(120*delta**3))==0
    # Direct rational triangle: legs 2uv/q and (u²-v²)/q; when the pole
    # equations hold these become 2A/q and bq and have area bA.
    assert sp.expand((2*u*v)**2+(u*u-v*v)**2-(u*u+v*v)**2)==0

    small_e, small_b = F(9,41), F(348,349)**2
    small_r, small_p = F(3567,3490), F(3490,3567)
    small_A = small_e*(1-small_b)
    assert prepared(small_b) and valuation(small_b,2)==4
    assert small_b == (1-small_e*small_e)*small_r*small_r
    assert small_e*small_e+small_b*small_p*small_p==1
    assert small_A == 17*F(3,349)**2 and not is_square(small_A)
    small_t = (1-697*z*z)/(1+697*z*z)
    small_w = 2*z/(1+697*z*z)
    assert sp.factor(small_t**2+697*small_w**2-1)==0
    assert sp.factor(sp.Rational(9,41)*(1-small_t**2)-17*(3*small_w)**2)==0

    beta, theta, N = 969,457,15499155
    assert sp.factorint(beta)=={3:1,17:1,19:1}
    assert sp.isprime(theta) and gcd(beta,theta)==1
    assert N==beta*35*theta and all(v==1 for v in sp.factorint(N).values())
    ee = F(20,343)
    RR = 1-ee*ee
    tt, ww = F(38864,1235629), F(11759,1235629)
    bb, rr, pp = beta*tt*tt, 343*tt/11, 11/(343*tt)
    assert e_split.subs(delta,7)==sp.Rational(ee.numerator,ee.denominator)
    assert RR==beta*F(11,343)**2
    assert beta*tt*tt+theta*ww*ww==1
    assert prepared(bb) and valuation(bb,2)==8
    assert bb==RR*rr*rr and ee*ee+bb*pp*pp==1
    assert ee==35*F(2,49)**2
    assert bb*ee*(1-bb)==N*(F(2,49)*tt*ww)**2
    assert ee*(1-bb)==15995*(F(2,49)*ww)**2
    assert not is_square(ee*(1-bb))

    den = 1733*(969+457*z*z)
    T = (8721+73120*z-4113*z*z)/den
    W = (77520-17442*z-36560*z*z)/den
    assert sp.factor(beta*T*T+theta*W*W-1)==0
    assert T.subs(z,1)==sp.Rational(tt.numerator,tt.denominator)
    assert W.subs(z,1)==sp.Rational(ww.numerator,ww.denominator)
    assert sp.factor(beta*T*T*sp.Rational(20,343)*(1-beta*T*T)-
                     N*(2*T*W/49)**2)==0
    # For every 2-adic unit z, the numerator of T is 0 mod8 and its
    # denominator is 2 mod4, proving v2(T)>=2. No numerical sampling is
    # needed for this valuation claim: all four unit residues are exhausted.
    residues=[]
    for zz in (1,3,5,7):
        numerator = 8721+73120*zz-4113*zz*zz
        denominator = 1733*(969+457*zz*zz)
        assert numerator%8==0 and denominator%4==2
        residues.append({'z_mod8':zz,'T_numerator_mod8':0,'T_denominator_mod4':2})
    # Independently check several exact prepared members, including both
    # signs and nonintegral rational 2-adic units.
    members=[]
    for zz in (F(1),F(-1),F(3),F(1,3),F(7,9),F(19,101)):
        tz=F(T.subs(z,sp.Rational(zz.numerator,zz.denominator)))
        wz=F(W.subs(z,sp.Rational(zz.numerator,zz.denominator)))
        bz=beta*tz*tz
        assert prepared(bz)
        assert ee*(1-bz)==15995*(F(2,49)*wz)**2
        members.append({'z':str(zz),'b':str(bz),'v2_b':valuation(bz,2)})

    direct = direct_product_coefficients(257)
    for n in (1,3,5,7,9,17,41,73,121,169,257):
        assert euler_coefficient(n)['coefficient']==direct[n]
    certificates=[]
    for n, expected in ((17,-4),(N,-256)):
        a = euler_coefficient(n)
        counts = ternary_counts(n)
        assert a['coefficient']==expected==counts['count_32_minus_half_count_8']
        certificates.append({'formal_product':a,'independent_ternary_counts':counts})
    assert direct[17]==-4

    # Positive control at the same small fixed e: forcing a conic is not
    # intrinsically inconsistent, and this prepared b has a full witness.
    good_b = 1-small_e*small_e
    good_u, good_v, good_q = small_e, small_e*small_e, small_e
    assert prepared(good_b)
    assert small_e*small_e+good_b==1
    assert good_u*good_v==small_e*(1-good_b)
    assert good_u*good_u-good_v*good_v==good_b*good_q*good_q

    report={
        'status':'PASS',
        'scope':'automatic first conics fail on dense prepared multiplier families, including the split six-contact map at delta=7; no actual-detector counterexample asserted',
        'noncongruence_method':'Tunnell 1983 introduction Theorem(a), necessary direction only; coefficients of the original q-product computed exactly',
        'Tunnell_primary_source':'https://sites.math.rutgers.edu/~zeilberg/EM22/JT1983.pdf',
        'Tunnell_DOI':'10.1007/BF01389327',
        'symbolic_checks':['split contact identity','all rational zero fibers','rational triangle identity','small conic','split-map conic','square twist factor'],
        'small_counterexample':{'e':str(small_e),'b':str(small_b),'r':str(small_r),
            'p':str(small_p),'A':str(small_A),'v2_b':4,'noncongruent_class':17},
        'split_map_counterexample':{'delta':'7','e':str(ee),'R':str(RR),
            'beta':beta,'theta':theta,'t':str(tt),'w':str(ww),'b':str(bb),
            'r':str(rr),'p':str(pp),'v2_b':8,'noncongruent_class':N,
            'q_zero_excluded_by_A_squareclass':15995},
        'Tunnell_certificates':certificates,
        'direct_product_crosscheck_limit':257,
        'two_adic_unit_residues':residues,
        'exact_family_members':members,
        'positive_control':{'e':str(small_e),'b':str(good_b),'p':'1',
            'u':str(good_u),'v':str(good_v),'q':str(good_q)},
        'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','noncongruent_coefficients':{17:-4,N:-256},
        'dense_prepared_families':2,'certificate':str(args.output)},indent=2))


if __name__=='__main__':
    main()
