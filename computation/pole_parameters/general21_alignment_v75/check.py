#!/usr/bin/env python3
"""Exact identities for the conditional contact-alignment checkpoint."""
from pathlib import Path
from fractions import Fraction
import json
import sympy as sp

HERE = Path(__file__).resolve().parent
s, u, lam, rho, T = sp.symbols('s u lambda rho T')


def zero(expression):
    assert sp.cancel(expression) == 0


def main():
    aligned_lambda = 4/(rho*T**2)
    zero((1+rho*T**2)*aligned_lambda-aligned_lambda-4)
    delta0, delta1 = lam+1, lam+6
    physical_s = delta0/delta1
    theta = [sp.Rational(0),sp.Rational(-1,2),sp.Rational(-1),
             sp.Rational(1,2399),sp.Rational(-32,407)]
    contacts = [shift+t for shift in (2,4) for t in theta]
    assert len(set(contacts))==10 and all(t>0 for t in contacts)
    P = sp.prod(lam-t for t in contacts)
    R0, R1 = P/delta0**10, P/delta1**10
    zero(R1/R0-physical_s**10)
    zero(delta1**2*physical_s**10/delta0**2-physical_s**8)
    w0 = u/(1+u)**2
    w1 = s**10*u/(1+s**10*u)**2
    zero(w1/w0-(s**5*(1+u)/(1+s**10*u))**2)
    zero(s**-2*w1/w0-(s**4*(1+u)/(1+s**10*u))**2)
    critical = (1+s**2)/(s**4*(1+s**2+s**4))
    zero(critical-(1-s**4)/(s**4-s**10))
    zero(s**4*(1+critical)-1-s**10*critical)
    margin = ((1-s**2)*(2*s**6+4*s**4+6*s**2+3)
              /(3*s**4*(1+s**2+s**4)))
    zero(critical-sp.Rational(2,3)-margin)
    zero(1+s**10*u-s**4*(1+u)-(s**4-s**10)*(critical-u))
    assert Fraction(36,76249) < Fraction(2,3)
    report = {
        'schema':'general21-contact-alignment/v75',
        'status':'PASS',
        'hypotheses':['rho,T are nonzero rational numbers',
                      '0<rho<2/3',
                      'a=1+rho*T^2',
                      'lambda=4/(rho*T^2)',
                      'lambda exceeds every root of the stated contact polynomial'],
        'identities_checked':[
            'a*lambda=lambda+4',
            'R1=s^10*R0 and u1=s^10*u0 by identical contact numerators',
            'w1/w0=(s^5*(1+u0)/(1+s^10*u0))^2',
            '(delta1^2*u1)/(delta0^2*u0)=s^8',
            '(delta1^2*w1)/(delta0^2*w0)=(s^4*(1+u0)/(1+s^10*u0))^2',
            'unique positive equality threshold u*=(1+s^2)/(s^4*(1+s^2+s^4))',
            'u*-2/3=(1-s^2)*(2*s^6+4*s^4+6*s^2+3)/(3*s^4*(1+s^2+s^4))',
            '1+s^10*u-s^4*(1+u)=(s^4-s^10)*(u*-u)',
        ],
        'strict_inequality_argument': '0<s<1 gives u*>2/3, while 0<R0<1 gives 0<u0<rho<2/3.',
        'source_scalar_bound_comparison': '36/76249<2/3',
        'positive_distinct_contacts':[str(t) for t in contacts],
        'scope':'Coefficientwise detector collapse is excluded on this alignment and prepared domain. Actual square solutions, accidental product equalities and completeness are not decided.',
        'actual_elliptic_witness_claimed':False,
        'general21_completeness_claimed':False,
    }
    (HERE/'certificate.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: exact alignment identities and threshold factorization.')


if __name__=='__main__':
    main()
