#!/usr/bin/env python3
"""Exact identities and local examples for adaptive native complement levels.

The symbolic identities are universal. The finite rational experiments verify
specified examples only; they do not establish prescribed-trace realization.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def scale(a, x):
    return a * x[0], a * x[1]


def mul(x, y):
    return x[0]*y[0] + 2*x[1]*y[1], x[0]*y[1] + x[1]*y[0]


def norm(x):
    return x[0]**2 - 2*x[1]**2


def valuation(x, p):
    x = F(x)
    if not x:
        return None
    a, b, result = abs(x.numerator), x.denominator, 0
    while a % p == 0:
        a //= p
        result += 1
    while b % p == 0:
        b //= p
        result -= 1
    return result


def residue(x, p):
    x = F(x)
    assert x.denominator % p
    return (x.numerator * pow(x.denominator, -1, p)) % p


def text_fraction(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else str(x)


def symbolic_checks():
    import sympy as s
    if s.__version__ != '1.14.0':
        raise ValueError('Use SymPy 1.14.0.')
    w, a, z, h, r, lam, k = s.symbols('w a z h r kappa k')
    N = a*a - 2*z*z
    V, J = 2*a/N, 1/N
    c = 1+w
    ws, Vs, Js = w/c**2, V/c, J/c**2
    Q = 1-Vs+Js
    d = (r+lam*w/r)**2 - 4*w/17
    identities = {
        'native_factor_rescaling': 1+ws*(c*h)**2-(1+w*h*h),
        'additional_native_factor': 1+ws*c*c-c,
        'unchanged_pole_input': 4*ws/Vs**2-4*w/V**2,
        'shifted_norm_denominator': Q-((c*a-1)**2-2*(c*z)**2)/(c*c*N),
        'trace_dependent_level_bound':
            2*(1+a*z)-(1+a+z)-(a*z+(1-a)*(1-z)),
        'varying_class_bare_point': (r+lam*w/r)**2-d-4*w/17,
        'class_kappa_2_over_17':
            d.subs(lam, s.Rational(2,17))-r*r-4*w*w/(289*r*r),
        'class_quadratic_discriminant':
            s.discriminant(s.expand(r*r*d), w)-16*r**4*(1-17*lam)/289,
        'normalized_class_lower_bound':
            1-4*ws/17-s.Rational(16,17)-(1-w)**2/(17*c*c),
        'normalized_class_fixed_point':
            1-(1-4*ws/17)-4*ws/17,
        'scaled_norm_one_trace_identity':
            (k*c*a-1)**2-2*(k*c*z)**2-1-k*c*c*N*(k-Vs),
    }
    m, y = s.symbols('m y')
    identities['norm_equation_conversion'] = (
        (17*m*d*y/V)**2-d*(17*m*m)*(17*m*m-4*w/V**2)
        + (289*m*m*d/V**2)*(m*m*V*V-d*y*y-4*w/17))
    for name, residual in identities.items():
        if s.cancel(residual) != 0:
            raise AssertionError(name)
    return sorted(identities)


def rational_checks():
    primes = (5,7,11,13,19,23,29,31,41,43,47,73)
    exponents = (-5,-3,-1,1,3,5)
    plans = (
        ((0,0,0),), ((1,0,0),), ((1,1,0),), ((2,1,-2),),
        ((1,0,-2),(1,1,0)), ((2,1,1),(1,-1,-2)),
        ((1,1,-3),(2,-1,-1),(1,0,2)),
        ((1,1,-1),(1,-1,-1)),
    )
    counts = {'native_cases': 0, 'bad_poles': 0, 'residue_cases': {},
              'varying_class_checks': 0, 'weight_unit_cases': 0,
              'nonzero_shifted_norm_cases': 0,
              'normalized_class_checks': 0}
    fingerprint = hashlib.sha256()
    for p in primes:
        local_plans = plans + tuple(((root,-1,-1),)
                                   for root in range(p) if root*root % p == 2)
        for n in exponents:
            for sign in (-1,1):
                w = sign*F(p)**n
                c = 1+w
                ws = w/(c*c)
                assert valuation(ws,p) == abs(n)
                for plan in local_plans:
                    W = (F(1),F(0))
                    for a,z,e in plan:
                        h = (F(a)*F(p)**e,F(z)*F(p)**e)
                        W = mul(W,add((F(1),F(0)),scale(w,mul(h,h))))
                    N = norm(W)
                    assert N
                    if not W[0]:
                        continue  # The native trace guard excludes this input.
                    V,J = 2*W[0]/N,1/N
                    b = 4*w/(V*V)
                    Ws = scale(c,W)
                    Vs,Js = 2*Ws[0]/norm(Ws),1/norm(Ws)
                    assert Vs == V/c and Js == J/(c*c)
                    assert b == 4*ws/(Vs*Vs)
                    assert valuation(Vs,p) >= 0 and valuation(Js,p) >= 0
                    key = (residue(Vs,p),residue(Js,p))
                    assert key in ((0,0),(1,0),(2,1))
                    label = str(key)
                    counts['residue_cases'][label] = counts['residue_cases'].get(label,0)+1
                    Q = 1-Vs+Js
                    assert Q == norm(add(Ws,(F(-1),F(0))))/norm(Ws)
                    if w > 0:
                        assert W[0] > 0 and N > 0
                        assert Ws[0] > 1 and norm(add(Ws,(F(-1),F(0)))) > 0
                        assert 0 < Q < 1
                    bad = valuation(b,p) < 0 and valuation(b,p) % 2
                    d0 = 1-4*ws/17
                    assert d0 >= F(16,17) and valuation(d0,p) == 0
                    if w > 0:
                        assert d0 < 1
                    counts['normalized_class_checks'] += 1
                    if Q:
                        counts['nonzero_shifted_norm_cases'] += 1
                    if bad:
                        counts['bad_poles'] += 1
                        assert key == (0,0) and Q and valuation(Q,p) == 0
                        m = 1/Q
                        level = 17*m*m
                        assert valuation(level,p) == 0
                        assert valuation(level*(level-b),p) % 2 == 1
                        assert valuation(d0*level*(level-b),p) % 2 == 1
                    for omega, order in ((w,n),(ws,abs(n))):
                        for rv in (-3,0,2):
                            R = F(p)**rv
                            for lam in (F(2,17),F(1),F(2)):
                                d = (R+lam*omega/R)**2-4*omega/17
                                assert d > 0
                                assert valuation(d,p) == 2*min(rv,order-rv)
                                if bad:
                                    assert valuation(d*level*(level-b),p) % 2 == 1
                                counts['varying_class_checks'] += 1
                    counts['native_cases'] += 1
                    fingerprint.update((str((p,n,sign,plan))+':'+text_fraction(b)+':'+text_fraction(Q)+'\n').encode())
        for pdepth in (1,2,3):
            w = F(p)**pdepth-1
            assert valuation(w,p) == 0
            assert valuation(w/(1+w)**2,p) == -2*pdepth
            counts['weight_unit_cases'] += 1
    counts['sample_sha256'] = fingerprint.hexdigest()
    return counts


def contact_example():
    # A rational product fixture, not an actual elliptic detector tuple.
    w = F(7,16)
    h = (F(-12,7),F(4,7))
    W = add((F(1),F(0)),scale(w,mul(h,h)))
    N = norm(W)
    V,J = 2*W[0]/N,1/N
    c = 1+w
    ws,Vs,Js = w/(c*c),V/c,J/(c*c)
    Q = 1-Vs+Js
    m = 1/Q
    b = 4*w/(V*V)
    assert W == (F(18,7),F(-6,7))
    assert V == 1 and J == F(7,36)
    assert Q == F(1897,4761) and m == F(4761,1897)
    assert b == F(7,4) and valuation(m,7) == -1
    return {'prime':7,'w':text_fraction(w),'b':text_fraction(b),
            'W':[text_fraction(x) for x in W],
            'V':text_fraction(V),'J':text_fraction(J),
            'normalized_w':text_fraction(ws),'normalized_V':text_fraction(Vs),
            'normalized_J':text_fraction(Js),'Q':text_fraction(Q),
            'm':text_fraction(m),'valuation_m':-1,
            'actual_elliptic_tuple':False,
            'scope':'Exact native-product example of a level pole at a positive odd contact; not a prepared elliptic realization.'}


def main(output):
    report = {
        'schema':'adaptive-native-complement-check/v50','status':'PASS',
        'symbolic_identities':symbolic_checks(),
        'finite_rational_checks':rational_checks(),
        'unbounded_level_contact_example':contact_example(),
        'new_retained_coordinates':0,
        'established_general_counts':[25,13],
        'conditional_realization_targets':[21,9],
        'actual_uniform_realization_proved':False,
        'scope':'Universal rational identities and finite exact local examples. '
                'The manuscript proves the valuation and whole-character guard theorems. '
                'This calculation supplies no actual uniform prescribed-trace realization, '
                'no proof of external arithmetic premises, and no new defining variable count.'}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','output':str(output),
                      'native_cases':report['finite_rational_checks']['native_cases'],
                      'actual_uniform_realization_proved':False}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    main(parser.parse_args().output)
